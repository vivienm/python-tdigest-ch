import os
from pathlib import Path
from tempfile import TemporaryDirectory

import nox

nox.options.default_venv_backend = "venv"
nox.options.reuse_existing_virtualenvs = True

os.environ.update({"PDM_IGNORE_SAVED_PYTHON": "1"})


@nox.session()
def black(session: nox.Session) -> None:
    session.run(
        "pdm",
        "sync",
        "--clean",
        "-G",
        "black",
        "--no-default",
        "--no-editable",
        "--no-self",
        external=True,
    )
    session.run("black", "--check", ".")


@nox.session()
def isort(session: nox.Session) -> None:
    session.run(
        "pdm",
        "sync",
        "--clean",
        "-G",
        "isort",
        "--no-default",
        "--no-editable",
        "--no-self",
        external=True,
    )
    session.run("isort", "--check", ".")


@nox.session()
def flake8(session: nox.Session) -> None:
    session.run(
        "pdm",
        "sync",
        "--clean",
        "-G",
        "flake8",
        "--no-default",
        "--no-editable",
        "--no-self",
        external=True,
    )
    session.run("flake8")


@nox.session()
def mypy(session: nox.Session) -> None:
    session.run(
        "pdm",
        "sync",
        "--clean",
        "-G",
        "mypy",
        "--no-editable",
        "--no-self",
        external=True,
    )
    session.run("mypy", ".")


@nox.session(python=["3.7", "3.8", "3.9", "3.10"])
def pytest(session: nox.Session) -> None:
    session.run(
        "pdm",
        "sync",
        "--clean",
        "-G",
        "pytest",
        "--no-editable",
        external=True,
    )
    session.run("pytest", "--benchmark-skip")


@nox.session()
def bench(session: nox.Session) -> None:
    session.run(
        "pdm",
        "sync",
        "--clean",
        "-G",
        "pytest",
        external=True,
    )
    session.run("pytest", "--benchmark-only")


@nox.session()
def safety(session: nox.Session) -> None:
    session.run(
        "pdm",
        "sync",
        "--clean",
        "-G",
        "safety",
        "--no-default",
        "--no-editable",
        "--no-self",
        external=True,
    )
    with TemporaryDirectory(prefix="nox_") as tmpdir:
        requirements = Path(tmpdir) / "requirements.txt"
        session.run(
            "pdm",
            "export",
            "-dG",
            ":all",
            "--without-hashes",
            "-o",
            str(requirements),
            silent=True,
            external=True,
        )
        session.run(
            "safety",
            "check",
            "-r",
            str(requirements),
        )
