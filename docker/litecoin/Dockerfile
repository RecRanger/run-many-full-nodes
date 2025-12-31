FROM debian:trixie-slim AS build

RUN apt-get update --yes \
  && apt-get install --yes --no-install-recommends \
    build-essential \
    ca-certificates \
    capnproto \
    ccache \
    clang-19 \
    cmake \
    git \
    libboost-dev \
    libcapnp-dev \
    libevent-dev \
    libsqlite3-dev \
    libzmq3-dev \
    pkg-config \
    python3 \
    systemtap-sdt-dev \
    build-essential libtool autotools-dev automake pkg-config bsdmainutils python3 libssl-dev \
    libevent-dev libboost-system-dev libboost-filesystem-dev libboost-test-dev libboost-thread-dev libfmt-dev
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV CRYPTO_COIN_PREFIX=/opt/litecoin
ARG COMMIT=master

WORKDIR /src

RUN git clone -b "$COMMIT" --single-branch --depth 1 "https://github.com/litecoin-project/litecoin.git" && \
    cd litecoin && \
    git fetch origin "$COMMIT" && \
    git checkout "$COMMIT" && \
    git clean -fdx

WORKDIR /src/litecoin

# https://github.com/litecoin-project/litecoin/blob/master/doc/build-unix.md
RUN ./autogen.sh
RUN ./configure --without-gui --without-miniupnpc
RUN make check

# Second stage
FROM debian:trixie-slim

ARG UID=101
ARG GID=101

ENV CRYPTO_COIN_DATA=/home/crypto_coin_user/.litecoin

RUN groupadd --gid ${GID} crypto_coin_user \
  && useradd --create-home --no-log-init -u ${UID} -g ${GID} crypto_coin_user \
  && apt-get update --yes \
  && apt-get install --yes --no-install-recommends \
    capnproto \
    gosu \
    libboost-dev \
    libevent-dev \
    libsqlite3-dev \
    libzmq3-dev \
    systemtap-sdt-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY --from=build /opt/litecoin /opt
ENV PATH=/opt/bin:$PATH

COPY docker-entrypoint.sh /entrypoint.sh

VOLUME ["/home/crypto_coin_user/.litecoin"]
EXPOSE 8332 8333 18332 18333 18443 18444 38333 38332

ENTRYPOINT ["/entrypoint.sh"]
RUN litecoind -version | grep "daemon version"
CMD ["litecoind"]
