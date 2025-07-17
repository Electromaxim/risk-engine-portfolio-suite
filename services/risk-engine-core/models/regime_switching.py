import torch
import pyro
import pyro.distributions as dist
from pyro.infer import SVI, TraceEnum_ELBO
from pyro.optim import Adam
from lib_utils.logger import get_logger

logger = get_logger(__name__)

class RegimeSwitchingModel:
    def __init__(self, n_regimes: int = 3, n_steps: int = 252):
        self.n_regimes = n_regimes
        self.n_steps = n_steps
        self.transition_probs = None
        self.means = None
        self.volatilities = None

    def model(self, returns: torch.Tensor):
        # Priors for transition matrix
        with pyro.plate("regimes", self.n_regimes):
            transition = pyro.sample(
                "transition", 
                dist.Dirichlet(torch.ones(self.n_regimes) / self.n_regimes)
            mean = pyro.sample("mean", dist.Normal(0., 1.))
            vol = pyro.sample("vol", dist.HalfNormal(1.))
        
        # Initial state
        state = pyro.sample("state_0", dist.Categorical(torch.ones(self.n_regimes) / self.n_regimes))
        
        for t in pyro.markov(range(1, self.n_steps)):
            # Transition to next state
            state = pyro.sample(
                f"state_{t}", 
                dist.Categorical(transition[state]),
                infer={"enumerate": "parallel"}
            )
            # Emission model
            pyro.sample(
                f"obs_{t}", 
                dist.Normal(mean[state], vol[state]), 
                obs=returns[t]
            )

    def guide(self, returns: torch.Tensor):
        # Variational parameters
        trans_param = pyro.param(
            "trans_param", 
            torch.ones(self.n_regimes, self.n_regimes) / self.n_regimes,
            constraint=constraints.simplex)
        mean_param = pyro.param("mean_param", torch.zeros(self.n_regimes))
        vol_param = pyro.param("vol_param", torch.ones(self.n_regimes), constraint=constraints.positive)
        
        with pyro.plate("regimes", self.n_regimes):
            pyro.sample("transition", dist.Dirichlet(trans_param))
            pyro.sample("mean", dist.Delta(mean_param))
            pyro.sample("vol", dist.Delta(vol_param))
        
        # Initial state fixed as uniform
        pyro.sample("state_0", dist.Categorical(torch.ones(self.n_regimes) / self.n_regimes))

    def fit(self, returns: torch.Tensor, num_steps: int = 1000):
        """Fit model to return series using stochastic variational inference"""
        optim = Adam({"lr": 0.01})
        svi = SVI(self.model, self.guide, optim, loss=TraceEnum_ELBO(max_plate_nesting=1))
        
        pyro.clear_param_store()
        for step in range(num_steps):
            loss = svi.step(returns)
            if step % 100 == 0:
                logger.info(f"Step {step}: ELBO loss = {loss}")
        
        # Store learned parameters
        self.transition_probs = pyro.param("trans_param").detach().numpy()
        self.means = pyro.param("mean_param").detach().numpy()
        self.volatilities = pyro.param("vol_param").detach().numpy()
        logger.info("Regime switching model calibration complete")