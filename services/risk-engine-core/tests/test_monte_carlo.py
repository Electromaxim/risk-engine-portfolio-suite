def test_heston_volatility_clustering():
    simulator = MonteCarloSimulator(n_simulations=1000)
    paths = simulator.simulate(
        model='heston',
        S0=100, v0=0.04, r=0.01, 
        kappa=1.0, theta=0.04, sigma=0.2, rho=-0.7
    )
    
    # Check volatility persistence
    returns = np.diff(np.log(paths), axis=1)
    squared_returns = returns**2
    autocorr = np.corrcoef(squared_returns[:, :-1], squared_returns[:, 1:])[0, 1]
    assert autocorr > 0.3  # Expect volatility clustering