from typing import Optional


def describe_service(path: str, fallback: Optional[str] = None) -> Optional[str]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return fallback
