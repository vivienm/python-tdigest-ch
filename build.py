from setuptools_rust import RustExtension

rust_extensions = [
    RustExtension(
        "tdigest_ch_rust",
        "src/tdigest_ch_rust/Cargo.toml",
    ),
]


def build(setup_kwargs):
    setup_kwargs.update(rust_extensions=rust_extensions)
