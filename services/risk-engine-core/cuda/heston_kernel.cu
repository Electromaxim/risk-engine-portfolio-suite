__global__ void heston_simulate(
    float *d_paths, 
    float *d_vols, 
    float S0, float v0, float r, 
    float kappa, float theta, float sigma, float rho, 
    float T, int N, int n_paths
) {
    half h_S0 = __float2half(S0);
    half h_v0 = __float2half(v0);
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= n_paths) return;

    curandState state;
    curand_init(clock64(), idx, 0, &state);
    
    float S = S0;
    float v = v0;
    d_paths[idx * (N+1)] = S0;
    d_vols[idx * (N+1)] = v0;
    
    for (int i=1; i<=N; i++) {
        float dt = T/N;
        float z1 = curand_normal(&state);
        float z2 = rho * z1 + sqrtf(1 - rho*rho) * curand_normal(&state);
        
        // Volatility process
        v = fmaxf(v + kappa*(theta - v)*dt + sigma*sqrtf(v*dt)*z1, 0.001f);
        
        // Price process
        S = S * expf((r - 0.5*v)*dt + sqrtf(v*dt)*z2);
        
        d_paths[idx*(N+1)+i] = S;
        d_vols[idx*(N+1)+i] = v;
    }
}