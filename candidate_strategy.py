"""Estrategia Optimizada - Fase 2.1 (Upgrades Mensuales y Corrección de Diccionario)"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

from interfaces import (
    BaseDispatcherStrategy,
    CarrierService,
    CarrierSnapshot,
    DeliveryAttemptResult,
    DispatchContext,
    FleetUpgradeDecision,
    MonthlyPlanningContext,
    Shipment,
)

class CandidateStrategy(BaseDispatcherStrategy):
    """Estrategia avanzada con Batching, Upgrades y Control de Retención."""

    def __init__(self, carrier_service: CarrierService) -> None:
        super().__init__(carrier_service)
        self.clusters: Dict[Tuple[str, str, int, Tuple[str, ...]], List[Shipment]] = defaultdict(list)

    def on_shipments_available(self, now: datetime, shipments: Tuple[Shipment, ...]) -> None:
        for s in shipments:
            key = (s.delivery_cluster_id, s.zone, s.attempt_number, tuple(sorted(s.required_capabilities)))
            self.clusters[key].append(s)

    def _get_compatible_carriers(self, carriers: Tuple[CarrierSnapshot, ...], zone: str, req_caps: Tuple[str, ...]) -> List[CarrierSnapshot]:
        compatibles = []
        for c in carriers:
            if c.available_units > 0 and c.operates_now and zone in c.allowed_zones:
                if all(req in c.capabilities for req in req_caps):
                    compatibles.append(c)
        
        def carrier_cost(c: CarrierSnapshot) -> int:
            surcharge = next((zp.surcharge_cents for zp in c.zone_prices if zp.zone == zone), 0)
            return c.base_fee_cents + surcharge
            
        compatibles.sort(key=carrier_cost)
        return compatibles

    def on_dispatch_tick(self, context: DispatchContext) -> None:
        new_clusters = defaultdict(list) # CORRECCIÓN DEL ERROR AQUÍ

        for key, shipments in self.clusters.items():
            if not shipments:
                continue

            cluster_id, zone, attempt_number, req_caps = key
            
            ready = []
            not_ready = []
            for s in shipments:
                if context.now >= s.ready_at:
                    ready.append(s)
                else:
                    not_ready.append(s)

            if not ready:
                new_clusters[key] = not_ready
                continue

            ready.sort(key=lambda s: (s.ready_at, s.sla_deadline))

            while ready:
                oldest = ready[0]
                wait_minutes = (context.now - oldest.ready_at).total_seconds() / 60.0
                
                # REGLAS DE EMERGENCIA
                must_dispatch = wait_minutes >= 30  # Riesgo de retención (límite 45)
                urgent_sla = (oldest.sla_deadline - context.now).total_seconds() / 3600.0 <= 6  # Faltan <= 6 horas

                current_carriers = self.carrier_service.snapshot()
                compatible_carriers = self._get_compatible_carriers(current_carriers, zone, req_caps)
                
                dispatched_in_this_loop = False

                for carrier in compatible_carriers:
                    cap = carrier.batch_capacity
                    is_full_batch = len(ready) >= cap
                    
                    # Para ahorrar contingencia: evitamos transportistas caros si no es emergencia
                    is_expensive = carrier.base_fee_cents > 1000
                    
                    if must_dispatch or urgent_sla or (is_full_batch and not is_expensive):
                        batch = ready[:cap]
                        batch_ids = tuple(s.shipment_id for s in batch)

                        receipt = self.carrier_service.dispatch_batch(carrier.carrier_id, batch_ids)
                        
                        if receipt.accepted:
                            ready = ready[cap:]
                            dispatched_in_this_loop = True
                            break
                        else:
                            # CONTROL DE ZOMBIS
                            if receipt.rejection_reason in {"TERMINAL_SHIPMENT", "UNKNOWN_SHIPMENT", "SHIPMENT_NOT_READY"}:
                                ready.pop(0)
                                dispatched_in_this_loop = True
                                break

                if not dispatched_in_this_loop:
                    break

            not_ready.extend(ready)
            if not_ready:
                new_clusters[key] = not_ready

        self.clusters = new_clusters

    def on_delivery_succeeded(self, result: DeliveryAttemptResult) -> None:
        pass

    def on_delivery_failed(self, result: DeliveryAttemptResult) -> None:
        if not result.terminal:
            s = result.shipment
            key = (s.delivery_cluster_id, s.zone, s.attempt_number, tuple(sorted(s.required_capabilities)))
            self.clusters[key].append(s)

    def on_monthly_planning(self, context: MonthlyPlanningContext) -> Tuple[FleetUpgradeDecision, ...]:
        """Contrata mejoras (vehículos, velocidad y capacidad) para los 3 transportistas más baratos."""
        decisions = []
        if context.upgrades_enabled:
            cheap_carriers = sorted(context.carriers, key=lambda c: c.base_fee_cents)
            
            for c in cheap_carriers[:3]:
                if "EXTRA_UNIT" in c.supported_upgrades:
                    decisions.append(FleetUpgradeDecision(c.carrier_id, "EXTRA_UNIT", 3))
                if "EXPANDED_CAPACITY" in c.supported_upgrades:
                    decisions.append(FleetUpgradeDecision(c.carrier_id, "EXPANDED_CAPACITY", 1))
                if "SPEED_SHIFT" in c.supported_upgrades:
                    decisions.append(FleetUpgradeDecision(c.carrier_id, "SPEED_SHIFT", 1))
                    
        return tuple(decisions)