from pyro.infer import SVI, TraceEnum_ELBO  
from pyro.optim import ClippedAdam  
import horovod.torch as hvd  

class DistributedRegimeModel(RegimeSwitchingModel):  
    def fit_distributed(self, returns: torch.Tensor, num_epochs: int = 100):  
        # Initialize Horovod  
        hvd.init()  
        torch.cuda.set_device(hvd.local_rank())  
        
        # Shard data across workers  
        shard = returns.chunk(hvd.size(), dim=0)[hvd.rank()]  
        
        # Configure optimizer  
        optimizer = ClippedAdam({"lr": 0.01 * hvd.size()})  
        optimizer = hvd.DistributedOptimizer(optimizer)  
        
        # Training loop  
        for epoch in range(num_epochs):  
            epoch_loss = 0.0  
            loss = self.svi.step(shard)  
            epoch_loss += hvd.allreduce(loss).item()  
            
            if hvd.rank() == 0 and epoch % 10 == 0:  
                print(f"Epoch {epoch}: Loss = {epoch_loss/hvd.size()}")  
        
        # Sync parameters  
        params = pyro.get_param_store()  
        for name in params:  
            tensor = hvd.allreduce(params[name])  
            params[name] = tensor / hvd.size()  