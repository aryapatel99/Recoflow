import subprocess
import sys


def run_command(command: list[str]) -> None:
    print(f"Running: {' '.join(command)}")

    result = subprocess.run(
        command,
        check=False,
    )

    if result.returncode != 0:
        raise SystemExit(
            f"Command failed with exit code {result.returncode}"
        )


def main() -> None:
    run_command(
        [
            sys.executable,
            "-m",
            "alembic",
            "upgrade",
            "head",
        ]
    )

    print()
    print("RecoFlow database schema is up to date.")


if __name__ == "__main__":
    main()