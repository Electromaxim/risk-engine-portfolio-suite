FROM intel/linux-sgx:latest

# Install financial verification libraries
RUN apt-get update && apt-get install -y \
    libssl-dev \
    libprotobuf-dev \
    build-essential

# Copy verification components
COPY services/compliance-security/sgx /app/sgx
WORKDIR /app/sgx/enclaves

# Build enclaves
RUN make SGX_MODE=HW SGX_PRERELEASE=1

CMD ["/bin/bash", "-c", "gramine-sgx ./exposure_verifier"]
EOF