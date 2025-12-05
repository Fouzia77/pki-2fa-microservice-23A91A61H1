#!/usr/bin/env python3
import datetime
import pathlib
import sys

# Make project root importable
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from app.totp_utils import generate_totp_code


def main():
    seed_path = pathlib.Path("/data/seed.txt")

    if not seed_path.exists():
        print("Seed file not found", file=sys.stderr)
        return

    hex_seed = seed_path.read_text().strip()

    try:
        code = generate_totp_code(hex_seed)
    except Exception as e:
        print(f"Error generating TOTP: {e}", file=sys.stderr)
        return

    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    print(f"{timestamp} - 2FA Code: {code}")


if __name__ == "__main__":
    main()