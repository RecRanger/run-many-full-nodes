"""Check the sync status of various cryptocurrencies by querying their CLI tools.

This is a companion to the BTCPay Server where each coin has a corresponding CLI script.
"""

# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "loguru",
# ]
# ///

import subprocess
import json
import datetime
import sys

from loguru import logger


COINS = [
    "feathercoin",
    "bitcoin",
    "bgold",
    "dash",
    "dogecoin",
    "litecoin",
    "monacoin",
    "viacoin",
]


def run_cli(cmd: list[str]) -> dict:
    """
    Run a command that outputs JSON and return the parsed dict.
    """
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Command failed: {' '.join(cmd)}", file=sys.stderr)
        logger.error(e.stderr.strip(), file=sys.stderr)
        raise

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        logger.error(f"❌ Invalid JSON from: {' '.join(cmd)}", file=sys.stderr)
        raise


def format_mediantime(ts: int | None) -> str:
    if ts is None:
        return "N/A"
    return datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc).isoformat()


def main():
    logger.info(datetime.datetime.now().isoformat())
    logger.info("")

    for coin in COINS:
        logger.info(f"==== {coin} ====")

        cmd = [f"{coin}-cli.sh", "getblockchaininfo"]
        info = run_cli(cmd)

        blocks = info.get("blocks")
        mediantime = info.get("mediantime")

        logger.info(f"blocks:      {blocks}")
        logger.info(f"mediantime:  {mediantime}")
        logger.info(f"date:        {format_mediantime(mediantime)}")
        logger.info("")

    logger.warning("No rule to scan monero yet.")
    logger.info("")
    logger.info(datetime.datetime.now().isoformat())


if __name__ == "__main__":
    main()
