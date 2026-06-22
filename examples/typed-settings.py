#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-core>=0.1.4,<0.2"]
# ///
"""Configure a KAOS module with typed settings — and keep secrets safe.

Every KAOS package configures itself through a typed `ModuleSettings` subclass
instead of scattered os.getenv calls. You get one predictable resolution order
(overrides > env vars > .env > defaults) and automatic secret redaction. This
example defines a module's settings, resolves a value from the environment, and
shows that a secret is redacted.

Fully offline and deterministic.

Run it:

    uv run examples/typed-settings.py
"""

from __future__ import annotations

import os

from pydantic import SecretStr

from kaos_core import ModuleSettings


class MyModuleSettings(ModuleSettings):
    """Settings for a hypothetical module, read from KAOS_MYMOD_* env vars."""

    model_config = {"env_prefix": "KAOS_MYMOD_"}

    max_items: int = 10
    api_key: SecretStr = SecretStr("")


def main() -> tuple[int, str]:
    # An operator sets this in the environment; the typed field picks it up.
    os.environ["KAOS_MYMOD_MAX_ITEMS"] = "42"
    os.environ["KAOS_MYMOD_API_KEY"] = "super-secret-token"

    settings = MyModuleSettings()

    print(f"max_items (from KAOS_MYMOD_MAX_ITEMS, overriding default 10): {settings.max_items}")
    # SecretStr redacts in repr/str/logs — you must call get_secret_value() to read it.
    print(f"api_key shown in logs/str: {settings.api_key}")
    print(f"api_key actual value (explicit): {settings.api_key.get_secret_value()}")
    return settings.max_items, str(settings.api_key)


if __name__ == "__main__":
    max_items, shown_key = main()
    assert max_items == 42, "env var should override the default"
    # The secret is redacted in its string form — never accidentally logged.
    assert "super-secret-token" not in shown_key, "secret leaked!"
    assert shown_key == "**********"
