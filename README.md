# tdigest-ch

A Python port of ClickHouse t-digest data structures, implemented in Rust.

## Usage

### Installation

Installing this package from sources requires [a recent version of Rust](https://www.rust-lang.org/tools/install).

```shell
pip install git+https://github.com/vivienm/python-tdigest-ch.git
```

### Example

```python
>>> from tdigest_ch import TDigest
>>> t = TDigest(range(1_000_001))
>>> round(t.quantile(0.99))
990000
```
