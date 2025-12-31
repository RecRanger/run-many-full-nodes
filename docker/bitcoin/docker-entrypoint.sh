#!/bin/bash
set -e

if [ -n "${UID+x}" ] && [ "${UID}" != "0" ]; then
  usermod -u "$UID" crypto_coin_user
fi

if [ -n "${GID+x}" ] && [ "${GID}" != "0" ]; then
  groupmod -g "$GID" crypto_coin_user
fi

echo "$0: assuming uid:gid for crypto_coin_user:crypto_coin_user of $(id -u crypto_coin_user):$(id -g crypto_coin_user)"

if [ "$(echo "$1" | cut -c1)" = "-" ]; then
  echo "$0: assuming arguments for bitcoind"

  set -- bitcoind "$@"
fi

if [ "$(echo "$1" | cut -c1)" = "-" ] || [ "$1" = "bitcoind" ]; then
  mkdir -p "$CRYPTO_COIN_DATA"
  chmod 700 "$CRYPTO_COIN_DATA"
  # Fix permissions for home dir.
  chown -R crypto_coin_user:crypto_coin_user "$(getent passwd crypto_coin_user | cut -d: -f6)"
  # Fix permissions for bitcoin data dir.
  chown -R crypto_coin_user:crypto_coin_user "$CRYPTO_COIN_DATA"

  echo "$0: setting data directory to $CRYPTO_COIN_DATA"

  set -- "$@" -datadir="$CRYPTO_COIN_DATA"
fi

if [ "$1" = "bitcoind" ] || [ "$1" = "bitcoin-cli" ] || [ "$1" = "bitcoin-tx" ]; then
  echo
  exec gosu crypto_coin_user "$@"
fi

echo
exec "$@"
