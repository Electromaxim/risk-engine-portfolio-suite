import numpy as np
import pandas as pd
from services.ai-risk-copilot.log_parser.residual_forensics import ResidualForensics

def test_volatility_clustering_detection():
    # Create clustered volatility residuals
    np.random.seed(42)
    base_residuals = np.random.normal(size=500)
    clustered_vol = np.concatenate([np.random.normal(scale=0.5, size=250), 
                                   np.random.normal(scale=2.0, size=250)])
    test_data = pd.Series(base_residuals * clustered_vol)
    
    analyzer = ResidualForensics()
    results = analyzer.analyze(test_data)
    
    assert results["volatility_clustering"] > 0.4  # High persistence
    assert results["stationary"] is False
    assert sum(results["anomalies"]) > 40  # Expected anomalies