FROM zokrates/zokrates:0.8.1

# Install financial circuit libraries
RUN git clone https://github.com/finma-zokrates-libs \
    && cp -r finma-zokrates-libs/src/* /home/zokrates \
    && rm -rf finma-zokrates-libs

WORKDIR /app
COPY services/compliance-security/zkp/circuits ./circuits

CMD ["sleep", "infinity"]