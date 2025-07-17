import pytest
from services.scenario-library.engine.stress_engine import StressEngine

@pytest.fixture
def covid_scenario():
    return {
        "id": "covid_2020",
        "parameters": {
            "equity": -0.34,
            "credit": -0.28,
            "fx": {"USDCHF": 0.12}
        }
    }

def test_equity_shock(covid_scenario):
    portfolio = {
        "positions": [{"asset_id": "AAPL", "qty": 100, "price": 150, "currency": "USD", "asset_class": "equity"}],
        "base_currency": "CHF"
    }
    
    engine = StressEngine()
    shocked = engine.apply_scenario(portfolio, "covid_2020")
    
    # Verify 34% drop applied
    assert shocked["positions"][0]["price"] == pytest.approx(99.0)
    assert shocked["scenario_pnl"] == pytest.approx(-5100.0)  # 100 * (99 - 150)