"""CLI-level tests for `cb describe-node`, especially the optional --path arg.

The underlying ``describe_node()`` function is tested in test_intake_helpers.py;
these tests use Typer's ``CliRunner`` to verify the CLI surface, including
the warning when ``--path`` points at a vault whose profile does not activate
the requested node type.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest
from typer.testing import CliRunner

from company_brain.cli import app
from company_brain.scaffold import scaffold


runner = CliRunner()


@pytest.fixture
def meddev_vault(tmp_path: Path) -> Path:
    result = scaffold(
        tmp_path / "meddev",
        "medical-device",
        today=date(2026, 5, 21),
        init_git=False,
    )
    return result.vault_path


@pytest.fixture
def default_vault(tmp_path: Path) -> Path:
    result = scaffold(
        tmp_path / "default",
        "default",
        today=date(2026, 5, 21),
        init_git=False,
    )
    return result.vault_path


# ---------------------------------------------------------------------------
# Without --path (legacy behavior)
# ---------------------------------------------------------------------------


def test_describe_node_without_path_prints_json() -> None:
    result = runner.invoke(app, ["describe-node", "pillar"])
    assert result.exit_code == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["name"] == "pillar"
    assert result.stderr == ""


def test_describe_node_unknown_type_exits_2() -> None:
    result = runner.invoke(app, ["describe-node", "not-a-real-type"])
    assert result.exit_code == 2
    assert "not-a-real-type" in result.stderr


# ---------------------------------------------------------------------------
# With --path: type is active in the vault's profile
# ---------------------------------------------------------------------------


def test_describe_node_with_path_active_type_no_warning(meddev_vault: Path) -> None:
    """`source` is always active. --path against any vault should succeed silently."""

    result = runner.invoke(app, ["describe-node", "source", "--path", str(meddev_vault)])
    assert result.exit_code == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["name"] == "source"
    assert "warning" not in result.stderr.lower()


def test_describe_node_with_path_meddev_only_type_active_no_warning(
    meddev_vault: Path,
) -> None:
    """`indication-for-use` is active in medical-device. No warning expected."""

    result = runner.invoke(
        app,
        ["describe-node", "indication-for-use", "--path", str(meddev_vault)],
    )
    assert result.exit_code == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["name"] == "indication-for-use"
    assert "warning" not in result.stderr.lower()


# ---------------------------------------------------------------------------
# With --path: type is NOT active in the vault's profile
# ---------------------------------------------------------------------------


def test_describe_node_with_path_meddev_type_in_default_vault_warns(
    default_vault: Path,
) -> None:
    """`indication-for-use` is not active in the default profile. Warn but succeed."""

    result = runner.invoke(
        app,
        ["describe-node", "indication-for-use", "--path", str(default_vault)],
    )
    assert result.exit_code == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["name"] == "indication-for-use"
    assert "warning" in result.stderr.lower()
    assert "not active" in result.stderr
    assert "default" in result.stderr


# ---------------------------------------------------------------------------
# With --path: vault has no PROFILE.md
# ---------------------------------------------------------------------------


def test_describe_node_with_path_to_non_vault_warns_but_succeeds(
    tmp_path: Path,
) -> None:
    """A path that isn't a vault produces a stderr warning, exit 0, JSON still printed."""

    not_a_vault = tmp_path / "empty"
    not_a_vault.mkdir()

    result = runner.invoke(app, ["describe-node", "pillar", "--path", str(not_a_vault)])
    assert result.exit_code == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["name"] == "pillar"
    assert "warning" in result.stderr.lower()
    assert "could not be read" in result.stderr


# ---------------------------------------------------------------------------
# --path with -P short flag
# ---------------------------------------------------------------------------


def test_describe_node_short_flag_P_works(meddev_vault: Path) -> None:
    result = runner.invoke(app, ["describe-node", "pillar", "-P", str(meddev_vault)])
    assert result.exit_code == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["name"] == "pillar"
