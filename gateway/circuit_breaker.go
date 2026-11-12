package gateway

import (
	"crypto/sha256"
	"fmt"
	"sync"
	"time"
)

// CircuitBreakerTier represents the four degradation states
type CircuitBreakerTier int

const (
	TierOptimal CircuitBreakerTier = iota
	TierThrottled
	TierDowngraded
	TierEmergencyHalt
)

// RunwayEngine tracks real-time founder burn velocity
type RunwayEngine struct {
	mu           sync.RWMutex
	cashReserve  float64
	fixedDaily   float64
	windowSpends []float64
	tier         CircuitBreakerTier
}

func NewRunwayEngine(initialReserve, fixedDaily float64) *RunwayEngine {
	return &RunwayEngine{
		cashReserve:  initialReserve,
		fixedDaily:   fixedDaily,
		windowSpends: make([]float64, 0),
		tier:         TierOptimal,
	}
}

// EvaluateRequest enforces the hard solvency invariant: { Cash - cost >= 0 }
func (e *RunwayEngine) EvaluateRequest(service string, cost float64) (bool, string, string) {
	e.mu.Lock()
	defer e.mu.Unlock()

	if e.cashReserve < cost {
		return false, "TIER_3_HARD_HALT", "Insufficient liquid operating reserve"
	}

	e.cashReserve -= cost
	e.windowSpends = append(e.windowSpends, cost)

	// Produce cryptographic attestation
	proofData := fmt.Sprintf("%s:%.4f:%.4f:%d", service, cost, e.cashReserve, time.Now().UnixNano())
	hash := fmt.Sprintf("%x", sha256.Sum256([]byte(proofData)))

	return true, "TIER_0_OPTIMAL", hash
}
