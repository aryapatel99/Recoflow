import argparse
import json
import os
import random
import time
from pathlib import Path

import httpx


DEFAULT_BASE_URL = "http://127.0.0.1:8000"


def load_scenario(path: str) -> list[dict]:
    scenario_path = Path(path)

    with scenario_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    return data["events"]


def send_event(
    client: httpx.Client,
    base_url: str,
    token: str,
    event: dict,
) -> None:

    payload = {
        "event_type": event["event_type"],
        "product_id": event.get("product_id"),
        "session_id": event.get(
            "session_id",
            f"sim-{random.randint(100000, 999999)}",
        ),
        "metadata": event.get(
            "metadata",
            {
                "source": "event_simulator",
            },
        ),
    }

    response = client.post(
        f"{base_url}/api/v1/events",
        json=payload,
        headers={
            "Authorization": f"Bearer {token}",
        },
        timeout=10,
    )

    response.raise_for_status()

    print(
        f"sent: {event['event_type']}"
        f" product={event.get('product_id')}"
        f" status={response.status_code}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="RecoFlow event simulator",
    )

    parser.add_argument(
        "--token",
        default=os.getenv("RECOFLOW_ACCESS_TOKEN"),
        help="JWT access token",
    )

    parser.add_argument(
        "--base-url",
        default=os.getenv(
            "RECOFLOW_API_URL",
            DEFAULT_BASE_URL,
        ),
    )

    parser.add_argument(
        "--scenario",
        default=str(
            Path(__file__).parent
            / "scenarios"
            / "basic_user_journey.json"
        ),
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=0.3,
    )

    args = parser.parse_args()

    if not args.token:
        raise SystemExit(
            "Missing token. Set RECOFLOW_ACCESS_TOKEN "
            "or pass --token."
        )

    events = load_scenario(args.scenario)

    with httpx.Client() as client:
        for event in events:
            send_event(
                client,
                args.base_url,
                args.token,
                event,
            )

            if args.delay > 0:
                time.sleep(args.delay)

    print(
        f"Simulation complete: {len(events)} events sent."
    )


if __name__ == "__main__":
    main()