"""
Real-Time Risk Streaming Endpoint
Provides live risk metrics via WebSocket with 100ms latency
"""
import asyncio
from fastapi import WebSocket
from lib_risk.metrics import calculate_intraday_risk
from redis import Redis

class RiskStreamManager:
    def __init__(self):
        self.active_connections = {}
        self.redis = Redis(host='risk-cache')
        
    async def connect(self, websocket: WebSocket, portfolio_id: int):
        await websocket.accept()
        self.active_connections[portfolio_id] = websocket
        asyncio.create_task(self._stream_metrics(websocket, portfolio_id))
        
    async def _stream_metrics(self, websocket: WebSocket, portfolio_id: int):
        """Push risk metrics every 100ms until connection closes"""
        while True:
            try:
                # Get latest portfolio snapshot
                portfolio = self.redis.get(f'portfolio:{portfolio_id}')
                if not portfolio:
                    await asyncio.sleep(0.1)
                    continue
                    
                # Calculate live risk metrics
                metrics = calculate_intraday_risk(portfolio)
                
                # Send via WebSocket
                await websocket.send_json({
                    "timestamp": datetime.utcnow().isoformat(),
                    "var_99": metrics["var_99"],
                    "expected_shortfall": metrics["es_99"],
                    "liquidity_horizon": metrics["liquidity_risk"],
                    "max_drawdown": metrics["max_dd"]
                })
                await asyncio.sleep(0.1)  # 10 updates/sec
                
            except Exception as e:
                logger.error(f"Stream error: {e}")
                break

# FastAPI Endpoint
@app.websocket("/live-risk/{portfolio_id}")
async def risk_stream(websocket: WebSocket, portfolio_id: int):
    manager = RiskStreamManager()
    await manager.connect(websocket, portfolio_id)