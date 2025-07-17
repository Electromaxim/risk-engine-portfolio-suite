from services.risk-engine-core.models.heston_gpu import simulate_heston_gpu  

class ProductionDeltaHedger(DeltaHedger):  
    def _simulate_price(self, S0: float, dt: float) -> float:  
        """Production-grade simulation using GPU-accelerated Heston"""  
        paths, _ = simulate_heston_gpu(  
            S0=S0, v0=self.v0, r=self.r,  
            kappa=self.kappa, theta=self.theta,  
            sigma=self.sigma, rho=self.rho,  
            T=dt, N=5, n_paths=1  
        )  
        return paths[0][-1]  # Return final simulated price  

    def backtest(self, historical_data: pd.DataFrame) -> dict:  
        """Run historical backtest with real market vols"""  
        results = []  
        for date, row in historical_data.iterrows():  
            self.v0 = row["realized_vol"]  # Use historical volatility  
            results.append(self.hedge_portfolio(row["S0"], row["T"], row["sigma"]))  
        return pd.DataFrame(results)  