set shell := ["bash", "-uc"]

ci: cargo-fmt cargo-clippy cargo-audit ruff mypy pytest sphinx pip-audit typos

[group('rust')]
cargo-fmt:
  cargo fmt --check

[group('rust')]
cargo-clippy:
  cargo clippy --all-targets

# https://github.com/rustsec/rustsec/issues/1241
[group('rust')]
cargo-audit:
  cargo audit --file <(grep -v 'git+https://github.com/vivienm/' Cargo.lock)

[group('python')]
ruff:
  uv run ruff check

[group('python')]
ruff-format:
  uv run ruff format --check

[group('python')]
mypy:
  uv run mypy .

[group('python')]
pytest *args="":
  uv run pytest {{args}}

[group('python')]
pytest-benchmark:
  uv run pytest --benchmark-only

[group('python')]
sphinx:
  uv run sphinx-build docs docs/_build/html

[group('python')]
pip-audit:
  uv run pip-audit --strict --require-hashes --disable-pip --requirement <(uv pip compile --no-header --no-annotate --generate-hashes --universal <(uv pip list --format=freeze --exclude-editable))

typos:
  typos
