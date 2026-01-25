"""Check the sync status of various cryptocurrencies by querying their CLI tools.

This is a companion to the BTCPay Server where each coin has a corresponding CLI script.
"""

import subprocess
import json
import datetime
import sys


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
        print(f"❌ Command failed: {' '.join(cmd)}", file=sys.stderr)
        print(e.stderr.strip(), file=sys.stderr)
        raise

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON from: {' '.join(cmd)}", file=sys.stderr)
        raise


def format_mediantime(ts: int | None) -> str:
    if ts is None:
        return "N/A"
    return datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc).isoformat()


def main():
    print(datetime.datetime.now().isoformat())
    print()

    for coin in COINS:
        print(f"==== {coin} ====")

        cmd = [f"{coin}-cli.sh", "getblockchaininfo"]
        info = run_cli(cmd)

        blocks = info.get("blocks")
        mediantime = info.get("mediantime")

        print(f"blocks:      {blocks}")
        print(f"mediantime:  {mediantime}")
        print(f"date:        {format_mediantime(mediantime)}")
        print()

    print("Don't have a rule to scan monero yet.")
    print()
    print(datetime.datetime.now().isoformat())


if __name__ == "__main__":
    main()
