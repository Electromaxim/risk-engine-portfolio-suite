import pycuda.autoinit
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
import numpy as np

with open("cuda/heston_kernel.cu", "r") as f:
    kernel_code = f.read()
mod = SourceModule(kernel_code)
heston_kernel = mod.get_function("heston_simulate")

def simulate_heston_gpu(S0, v0, r, kappa, theta, sigma, rho, T, N, n_paths):
    # Allocate device memory
    d_paths = cuda.mem_alloc(n_paths*(N+1)*4)
    d_vols = cuda.mem_alloc(n_paths*(N+1)*4)
    
    # Configure grid/block
    block_size = 256
    grid_size = (n_paths + block_size - 1) // block_size
    
    # Execute kernel
    heston_kernel(
        d_paths, d_vols, 
        np.float32(S0), np.float32(v0), np.float32(r),
        np.float32(kappa), np.float32(theta), np.float32(sigma), np.float32(rho),
        np.float32(T), np.int32(N), np.int32(n_paths),
        block=(block_size,1,1), grid=(grid_size,1)
    )
    
    # Copy results to host
    paths = np.empty(n_paths*(N+1), dtype=np.float32)
    vols = np.empty(n_paths*(N+1), dtype=np.float32)
    cuda.memcpy_dtoh(paths, d_paths)
    cuda.memcpy_dtoh(vols, d_vols)
    
    return paths.reshape(n_paths, N+1), vols.reshape(n_paths, N+1)