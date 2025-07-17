def dispatch_calibration_job(params: dict) -> str:
    """Route calibration to GPU/CPU based on complexity"""
    complexity = params["n_paths"] * params["n_steps"] / 1e9
    if complexity > 2.0 or config.USE_GPU:
        return run_heston_gpu.delay(params)  # Celery GPU task
    return run_heston_cpu.delay(params)