from fastapi import WebSocket
import asyncio

class RiskStreamingEndpoint:
    @app.websocket("/ws/risk/{portfolio_id}")
    async def stream_risk_metrics(websocket: WebSocket, portfolio_id: int):
        await websocket.accept()
        while True:
            # Get real-time risk metrics
            metrics = risk_service.calculate_realtime_metrics(portfolio_id)
            
            # Send updates every second
            await websocket.send_json({
                "timestamp": datetime.utcnow().isoformat(),
                "var_99": metrics["var_99"],
                "liquidity_risk": metrics["liquidity_risk"],
                "concentration": metrics["top5_exposure"]
            })
            await asyncio.sleep(1)