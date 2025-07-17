import dask
from dask.distributed import Client
from metrics.var import calculate_var
from lib_data.calendar import is_trading_day

def run_risk_calculation(portfolio_ids: list[int]):
    """Orchestrate parallel VaR calculations using Dask"""
    with Client(n_workers=8, threads_per_worker=1) as client:
        futures = []
        for pid in portfolio_ids:
            # Lazy computation graph
            future = client.submit(
                calculate_var, 
                portfolio=load_portfolio(pid), 
                confidence=0.99,
                n_sim=50000
            )
            futures.append(future)
        
        # Gather results with timeout
        results = client.gather(futures, timeout=300)
        return dict(zip(portfolio_ids, results))

def daily_risk_job():
    """Scheduled job for end-of-day risk metrics"""
    if not is_trading_day():
        return
    
    portfolios = get_active_portfolios()
    risk_metrics = run_risk_calculation([p.id for p in portfolios])
    save_to_database(risk_metrics)