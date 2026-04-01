"""Tests for MCP server tools."""

from __future__ import annotations

import json

import pytest

pytest.importorskip("fastmcp")

from reprompt.storage.db import PromptDB


@pytest.fixture()
def mcp_db(tmp_path, monkeypatch):
    """Set up a test DB and point MCP tools at it."""
    monkeypatch.setenv("REPROMPT_DB_PATH", str(tmp_path / "test.db"))
    db = PromptDB(tmp_path / "test.db")
    db.insert_prompt(
        "fix the auth bug in the login handler",
        source="claude-code",
        timestamp="2026-03-10T10:00:00Z",
    )
    db.insert_prompt(
        "add unit tests for payment module", source="claude-code", timestamp="2026-03-10T11:00:00Z"
    )
    db.insert_prompt(
        "refactor the database connection pool",
        source="claude-code",
        timestamp="2026-03-10T12:00:00Z",
    )
    return db


# ─── search_prompts: keyword mode ─────────────────────────────────────────


def test_search_prompts_keyword_found(mcp_db):
    from reprompt.mcp import search_prompts

    result = search_prompts(query="auth")
    data = json.loads(result)
    assert len(data) == 1
    assert "auth" in data[0]["text"]


def test_search_prompts_keyword_not_found(mcp_db):
    from reprompt.mcp import search_prompts

    result = search_prompts(query="nonexistent_xyz")
    assert "No prompts" in result


def test_search_prompts_keyword_with_limit(mcp_db):
    from reprompt.mcp import search_prompts

    result = search_prompts(query="the", limit=2)
    data = json.loads(result)
    assert len(data) <= 2


# ─── search_prompts: pattern browse mode ──────────────────────────────────


def test_search_prompts_patterns_empty(mcp_db):
    from reprompt.mcp import search_prompts

    result = search_prompts()
    assert "No patterns yet" in result


def test_search_prompts_patterns_category_empty(mcp_db):
    from reprompt.mcp import search_prompts

    result = search_prompts(category="debug")
    assert "No patterns in category 'debug'" in result


def _insert_pattern(db, text, freq, cat, avg_len):
    """Helper to insert a pattern row into the test DB."""
    _sql = (
        "INSERT INTO prompt_patterns"
        " (pattern_text, frequency, category, avg_length, projects, examples)"
        " VALUES (?, ?, ?, ?, ?, ?)"
    )
    conn = db._conn()
    try:
        conn.execute(_sql, (text, freq, cat, avg_len, "[]", "[]"))
        conn.commit()
    finally:
        conn.close()


def test_search_prompts_patterns_with_data(mcp_db):
    """When patterns exist, returns them as JSON."""
    from reprompt.mcp import search_prompts

    _insert_pattern(mcp_db, "fix the bug", 5, "debug", 20)
    _insert_pattern(mcp_db, "add tests", 3, "test", 15)

    result = search_prompts()
    data = json.loads(result)
    assert len(data) == 2
    assert data[0]["pattern"] == "fix the bug"


def test_search_prompts_patterns_category_filter(mcp_db):
    """Category param filters patterns."""
    from reprompt.mcp import search_prompts

    _insert_pattern(mcp_db, "fix the bug", 5, "debug", 20)
    _insert_pattern(mcp_db, "add tests", 3, "test", 15)

    result = search_prompts(category="debug")
    data = json.loads(result)
    assert len(data) == 1
    assert data[0]["category"] == "debug"


def test_search_prompts_patterns_top_sort(mcp_db):
    """top=True sorts by frequency descending."""
    from reprompt.mcp import search_prompts

    _insert_pattern(mcp_db, "low freq", 1, "debug", 10)
    _insert_pattern(mcp_db, "high freq", 10, "implement", 25)

    result = search_prompts(top=True, limit=5)
    data = json.loads(result)
    assert len(data) == 2
    assert data[0]["frequency"] >= data[1]["frequency"]


# ─── Other tools ──────────────────────────────────────────────────────────


def test_scan_sessions_empty(tmp_path, monkeypatch):
    monkeypatch.setenv("REPROMPT_DB_PATH", str(tmp_path / "test.db"))
    from reprompt.mcp import scan_sessions

    result = json.loads(scan_sessions(source="claude-code"))
    # May find real sessions on dev machine; just verify structure
    assert "sessions_scanned" in result
    assert "new_stored" in result


def test_resource_status(mcp_db):
    from reprompt.mcp import resource_status

    result = json.loads(resource_status())
    assert "total_prompts" in result


def test_resource_library(mcp_db):
    from reprompt.mcp import resource_library

    result = json.loads(resource_library())
    assert isinstance(result, list)


def test_mcp_serve_cli(tmp_path, monkeypatch):
    """mcp-serve command exists and shows error without fastmcp if needed."""
    from typer.testing import CliRunner

    from reprompt.cli import app

    runner = CliRunner()
    result = runner.invoke(app, ["mcp-serve", "--help"])
    assert result.exit_code == 0
    assert "MCP" in result.output or "mcp" in result.output


def test_tool_count():
    """Verify the MCP server exposes exactly 9 tools."""
    import asyncio

    from reprompt.mcp import mcp as _mcp

    tools = asyncio.run(_mcp.list_tools())
    names = [t.name for t in tools]
    assert len(tools) == 9, f"Expected 9 tools, got {len(tools)}: {names}"


# ─── New tools (check, build, explain) ────────────────────────────────────


def test_check_prompt_quality():
    from reprompt.mcp import check_prompt_quality

    result = json.loads(check_prompt_quality("fix the auth bug in login.ts"))
    assert "total" in result
    assert "tier" in result
    assert "lint_issues" in result
    assert "rewritten" in result
    assert "suggestions" in result


def test_check_prompt_quality_with_model():
    from reprompt.mcp import check_prompt_quality

    result = json.loads(check_prompt_quality("fix the auth bug", model="claude"))
    assert "total" in result


def test_build_prompt_from_parts():
    from reprompt.mcp import build_prompt_from_parts

    result = json.loads(
        build_prompt_from_parts(
            task="fix the auth bug",
            files="src/auth.ts",
            error="TypeError: null",
            constraints="keep tests,no breaking changes",
        )
    )
    assert "prompt" in result
    assert "score" in result
    assert "tier" in result
    assert "src/auth.ts" in result["prompt"]
    assert "components_used" in result


def test_build_prompt_from_parts_minimal():
    from reprompt.mcp import build_prompt_from_parts

    result = json.loads(build_prompt_from_parts(task="fix the bug"))
    assert "prompt" in result
    assert result["score"] > 0


def test_explain_prompt_quality():
    from reprompt.mcp import explain_prompt_quality

    result = json.loads(explain_prompt_quality("fix the auth bug in login.ts"))
    assert "score" in result
    assert "tier" in result
    assert "summary" in result
    assert "strengths" in result
    assert "weaknesses" in result
    assert "tips" in result


def test_explain_prompt_quality_short():
    from reprompt.mcp import explain_prompt_quality

    result = json.loads(explain_prompt_quality("fix it"))
    assert result["score"] > 0
    assert len(result["summary"]) > 0
