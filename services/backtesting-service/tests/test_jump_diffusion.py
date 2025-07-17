def test_jump_detection():
    calibrator = JumpModelCalibrator()
    # Create dataset with jumps
    prices = np.random.lognormal(mean=0, sigma=0.2, size=1000)
    prices[500:502] *= 0.7  # Simulate 30% drop
    
    params = calibrator.calibrate(prices)
    assert params["jump_lambda"] > 0.05  # Should detect jumps
    assert params["jump_mu"] < -0.25