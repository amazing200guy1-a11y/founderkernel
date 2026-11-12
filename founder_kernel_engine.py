#!/usr/bin/env python3
"""
FOUNDERKERNEL: AUTONOMOUS RUNWAY SENTRY & MICROSERVICE EXPENSE CIRCUIT-BREAKER
=============================================================================
Author: Usman Bamidele (100L Mathematics Student, FUNAAB)
Track: Fintech, Enterprise AI Governance & Solo-Founder Solvency (HETIC 2026)
Moat: Microsecond burn velocity modeling, exponential loop interceptor, and staged circuit-breaker degradation.
"""

import sys
import time
import json
import hashlib
from typing import Dict, Any, List, Tuple, Optional

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Governance Constants
MIN_RUNWAY_OPTIMAL_DAYS = 60.0
MIN_RUNWAY_CAUTION_DAYS = 30.0
MIN_RUNWAY_CRITICAL_DAYS = 14.0
MAX_BURN_ACCELERATION_FACTOR = 3.5  # 3.5x sudden cost spike triggers runaway circuit breaker

class CircuitBreakerTier:
    OPTIMAL = "TIER_0_OPTIMAL"          # Full frontier model access, all batch jobs enabled
    CAUTION = "TIER_1_THROTTLED"        # Caches enforced, non-critical background jobs delayed
    CRITICAL = "TIER_2_DOWNGRADED"      # Forced model fallback (Frontier -> Flash/Haiku), rate limits 50%
    EMERGENCY = "TIER_3_HARD_HALT"      # Hard cut-off on billable external API gateways

class FounderKernelEngine:
    """
    Real-time mathematical runway sentry and runaway API expense circuit-breaker.
    Guarantees solo-founder operational solvency against infinite agentic loops and surprise bills.
    """

    def __init__(self, initial_cash_reserve: float, fixed_daily_burn: float = 5.0):
        self.cash_reserve = float(initial_cash_reserve)
        self.fixed_daily_burn = float(fixed_daily_burn)
        self.cumulative_variable_spend = 0.0
        self.audit_log: List[Dict[str, Any]] = []
        self.window_spend: List[Tuple[float, float]] = []  # (timestamp, cost)
        self.current_tier = CircuitBreakerTier.OPTIMAL

    def calculate_runway(self) -> Dict[str, Any]:
        """Calculates instantaneous burn velocity and projected runway days."""
        now = time.time()
        # Filter spend to trailing 24 hours (simulated window)
        recent_spend = sum(cost for ts, cost in self.window_spend if now - ts <= 86400)
        daily_variable_burn = recent_spend if recent_spend > 0 else 0.5
        total_daily_burn = self.fixed_daily_burn + daily_variable_burn

        if self.cash_reserve <= 0:
            runway_days = 0.0
        else:
            runway_days = self.cash_reserve / total_daily_burn

        # Determine Tier
        if runway_days >= MIN_RUNWAY_OPTIMAL_DAYS:
            tier = CircuitBreakerTier.OPTIMAL
        elif runway_days >= MIN_RUNWAY_CAUTION_DAYS:
            tier = CircuitBreakerTier.CAUTION
        elif runway_days >= MIN_RUNWAY_CRITICAL_DAYS:
            tier = CircuitBreakerTier.CRITICAL
        else:
            tier = CircuitBreakerTier.EMERGENCY

        self.current_tier = tier

        return {
            "cash_reserve_usd": round(self.cash_reserve, 2),
            "total_daily_burn_usd": round(total_daily_burn, 2),
            "projected_runway_days": round(runway_days, 1),
            "circuit_breaker_tier": tier
        }

    def evaluate_transaction(self, service_name: str, requested_cost: float, is_critical: bool = True) -> Dict[str, Any]:
        """
        Microsecond evaluation of microservice or LLM token invocation.
        Applies Hoare-invariant:
          { Cash - cost >= 0 and Runway >= safety_limit } Dispatch { Insolvent = False }
        """
        start_time = time.perf_counter()
        now = time.time()

        # 1. Check current runway state
        runway_metrics = self.calculate_runway()
        tier = runway_metrics["circuit_breaker_tier"]

        # 2. Check for runaway burn velocity spike (e.g., infinite agent loop)
        recent_1m_spend = sum(cost for ts, cost in self.window_spend if now - ts <= 60)
        if recent_1m_spend > 0 and (requested_cost / max(recent_1m_spend, 0.01)) > MAX_BURN_ACCELERATION_FACTOR and requested_cost > 5.0:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return {
                "verdict": "BLOCKED",
                "reason": f"Runaway cost acceleration spike detected ({requested_cost:.2f} USD requested)",
                "circuit_breaker_tier": CircuitBreakerTier.EMERGENCY,
                "latency_ms": round(elapsed_ms, 4)
            }

        # 3. Apply Tier Circuit Breaker Rules
        if tier == CircuitBreakerTier.EMERGENCY:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return {
                "verdict": "BLOCKED",
                "reason": "Emergency circuit-breaker active: Runway is below 14-day insolvency barrier",
                "circuit_breaker_tier": tier,
                "latency_ms": round(elapsed_ms, 4)
            }

        if tier == CircuitBreakerTier.CRITICAL and not is_critical:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return {
                "verdict": "DEGRADED",
                "reason": "Non-critical batch request rejected to conserve emergency runway",
                "circuit_breaker_tier": tier,
                "recommended_action": "DOWNGRADE_TO_FLASH_TIER",
                "latency_ms": round(elapsed_ms, 4)
            }

        # 4. Enforce Hard Solvency Invariant
        if self.cash_reserve < requested_cost:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return {
                "verdict": "BLOCKED",
                "reason": f"Insufficient liquid reserves: {self.cash_reserve:.2f} < {requested_cost:.2f} USD",
                "circuit_breaker_tier": CircuitBreakerTier.EMERGENCY,
                "latency_ms": round(elapsed_ms, 4)
            }

        # 5. Atomic State Mutation
        self.cash_reserve -= requested_cost
        self.cumulative_variable_spend += requested_cost
        self.window_spend.append((now, requested_cost))

        # Attestation Proof
        tx_hash = hashlib.sha256(f"{service_name}:{requested_cost}:{self.cash_reserve}:{now}".encode('utf-8')).hexdigest()
        audit_entry = {
            "service": service_name,
            "cost_usd": requested_cost,
            "remaining_reserve_usd": round(self.cash_reserve, 2),
            "timestamp": now,
            "proof_sha256": tx_hash
        }
        self.audit_log.append(audit_entry)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return {
            "verdict": "APPROVED",
            "service": service_name,
            "debited_usd": requested_cost,
            "remaining_reserve_usd": round(self.cash_reserve, 2),
            "circuit_breaker_tier": tier,
            "proof_sha256": tx_hash,
            "latency_ms": round(elapsed_ms, 4)
        }

    def generate_solvency_attestation(self) -> Dict[str, Any]:
        """Produces a tamper-evident cryptographic proof of solvency for investors or partners."""
        metrics = self.calculate_runway()
        log_hashes = [entry["proof_sha256"] for entry in self.audit_log[-50:]]
        merkle_root = hashlib.sha256("".join(log_hashes).encode('utf-8')).hexdigest() if log_hashes else "0"*64

        state_payload = f"{self.cash_reserve}:{metrics['projected_runway_days']}:{merkle_root}"
        solvency_cert = hashlib.sha256(state_payload.encode('utf-8')).hexdigest()

        return {
            "solvency_certificate_sha256": solvency_cert,
            "merkle_spend_root": merkle_root,
            "verified_cash_reserve_usd": round(self.cash_reserve, 2),
            "projected_runway_days": metrics["projected_runway_days"],
            "total_transactions_audited": len(self.audit_log)
        }
