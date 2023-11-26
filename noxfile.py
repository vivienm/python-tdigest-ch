import nox

nox.options.default_venv_backend = "none"


@nox.session()
def ruff(session: nox.Session) -> None:
    session.run("ruff", "check", ".")
    session.run("ruff", "format", "--check", ".")


@nox.session()
def mypy(session: nox.Session) -> None:
    session.run("mypy", ".")


@nox.session()
def pytest(session: nox.Session) -> None:
    session.run("pytest")


@nox.session()
def bench(session: nox.Session) -> None:
    session.run("pytest", "--benchmark-only")


@nox.session()
def sphinx(session: nox.Session) -> None:
    session.run("sphinx-build", "docs", "docs/_build/html")


@nox.session()
def audit(session: nox.Session) -> None:
    session.run("pip-audit", "--skip-editable")
