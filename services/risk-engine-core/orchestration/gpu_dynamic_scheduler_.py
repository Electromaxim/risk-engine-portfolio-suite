# services/risk-engine-core/orchestration/gpu_dynamic_scheduler.py
from prometheus_client import Counter

# Add new metrics
GPU_FAILURE_METRIC = Counter('gpu_failures_total', 'Count of GPU processing failures')
VOLATILITY_BREAKER = Gauge('volatility_breaker', 'Circuit breaker status')

class DynamicGPUOrchestrator:
    def allocate_resources(self) -> dict:
        """Enhanced with circuit breaker and fallback"""
        if VOLATILITY_BREAKER.get() == 1:
            return {"fallback_mode": 100}  # CPU fallback
        
        try:
            if self.volatility_index > 45:
                allocation = {"scenario_analysis": 90, "intraday_var": 10}
            elif self.volatility_index > 30:
                allocation = {"scenario_analysis": 80, "intraday_var": 20}
            elif time.strftime("%H:%M") > "15:30":
                allocation = {"scenario_analysis": 70, "intraday_var": 30}
            else:
                allocation = {"scenario_analysis": 40, "intraday_var": 60}
                
            # Auto-scaling based on queue depth
            queue_depth = self._get_calculation_queue()
            if queue_depth > 1000:
                allocation = {k: v * 1.5 for k, v in allocation.items()}
                
            return allocation
        except Exception as e:
            GPU_FAILURE_METRIC.inc()
            VOLATILITY_BREAKER.set(1)  # Trigger circuit breaker
            return self._fallback_allocation()
    
    def _fallback_allocation(self) -> dict:
        """CPU fallback when GPU fails"""
        return {
            "cpu_scenario_analysis": 60,
            "cpu_intraday_var": 40
        }