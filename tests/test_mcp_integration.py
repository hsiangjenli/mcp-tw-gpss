"""Integration checks that exercise the live GPSS MCP tools."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

import pytest

from mcp_tools.main import get_available_databases, search_patents


def _resolve_user_code() -> str | None:
    """Read the GPSS user code from environment or .env for integration tests."""

    env_value = os.getenv("USER_CODE")
    if env_value:
        return env_value.strip()

    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        return None

    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("USER_CODE="):
            return stripped.split("=", 1)[1].strip()

    return None


USER_CODE = _resolve_user_code()
if USER_CODE:
    os.environ["USER_CODE"] = USER_CODE


@pytest.mark.skipif(
    not USER_CODE, reason="USER_CODE not configured for integration test"
)
def test_available_databases_returns_entries():
    """Ensure the database listing endpoint responds with known regions."""

    result = asyncio.run(get_available_databases())

    assert result["success"] is True
    databases = result.get("databases")
    assert isinstance(databases, dict) and databases
    assert "TW" in databases


@pytest.mark.skipif(
    not USER_CODE, reason="USER_CODE not configured for integration test"
)
def test_search_patents_returns_payload():
    """Verify a live search provides request metadata and non-empty payload."""

    result = asyncio.run(
        search_patents(
            keywords="AI",
            max_results=5,
        )
    )

    assert result["success"] is True

    params = result.get("request_params")
    assert isinstance(params, dict)
    assert params.get("TI") == "AI"
    assert "userCode" not in params

    data_block = result.get("data")
    assert isinstance(data_block, dict)
    assert "raw" in data_block

    raw_payload = data_block["raw"]
    if isinstance(raw_payload, str):
        assert raw_payload.strip()
    else:
        assert isinstance(raw_payload, dict) and raw_payload

    parsed_payload = data_block.get("parsed")
    if parsed_payload is not None:
        assert isinstance(parsed_payload, dict)
        assert set(parsed_payload.keys()) >= {
            "total_count",
            "returned_count",
            "records",
        }
