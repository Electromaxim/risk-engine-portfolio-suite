import subprocess
import json
import os
from pathlib import Path
from lib_utils.logger import get_logger

logger = get_logger(__name__)

class ZoKratesProver:
    def __init__(self, circuit_dir: str = "zk/circuits"):
        self.circuit_dir = Path(circuit_dir)
        self.setup_done = {}
        
    def setup_circuit(self, circuit_name: str):
        """Compile circuit and generate trusted setup"""
        circuit_path = self.circuit_dir / f"{circuit_name}.zok"
        work_dir = self.circuit_dir / circuit_name
        
        # Create working directory
        work_dir.mkdir(exist_ok=True)
        
        # Execute ZoKrates commands
        commands = [
            f"zokrates compile -i {circuit_path} -o {work_dir}/out",
            f"zokrates setup -i {work_dir}/out -p {work_dir}/proving.key -v {work_dir}/verification.key",
        ]
        
        for cmd in commands:
            result = subprocess.run(cmd, shell=True, capture_output=True)
            if result.returncode != 0:
                logger.error(f"ZoKrates setup failed: {result.stderr.decode()}")
                raise RuntimeError("Circuit setup failed")
        
        self.setup_done[circuit_name] = True
        logger.info(f"Circuit {circuit_name} setup complete")
    
    def generate_proof(self, circuit_name: str, inputs: list) -> dict:
        """Generate ZK-SNARK proof for given inputs"""
        if not self.setup_done.get(circuit_name):
            self.setup_circuit(circuit_name)
            
        work_dir = self.circuit_dir / circuit_name
        inputs_file = work_dir / "inputs.json"
        
        # Save inputs to file
        with open(inputs_file, 'w') as f:
            json.dump(inputs, f)
        
        # Generate proof
        cmd = f"zokrates generate-proof -i {work_dir}/out -p {work_dir}/proving.key -j {work_dir}/proof.json -w {work_dir}/witness -s {work_dir}/abi.json < {inputs_file}"
        result = subprocess.run(cmd, shell=True, capture_output=True)
        
        if result.returncode != 0:
            logger.error(f"Proof generation failed: {result.stderr.decode()}")
            raise RuntimeError("Proof generation failed")
        
        # Load proof
        with open(work_dir / "proof.json") as f:
            return json.load(f)
    
    def verify_proof(self, circuit_name: str, proof: dict) -> bool:
        """Verify ZK-SNARK proof"""
        work_dir = self.circuit_dir / circuit_name
        proof_file = work_dir / "verify_proof.json"
        
        # Save proof to file
        with open(proof_file, 'w') as f:
            json.dump(proof, f)
        
        # Execute verification
        cmd = f"zokrates verify -j {proof_file} -v {work_dir}/verification.key"
        result = subprocess.run(cmd, shell=True, capture_output=True)
        
        return result.returncode == 0