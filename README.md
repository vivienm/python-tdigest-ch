# tdigest-ch

A Python library for estimating quantiles in a stream,
using [ClickHouse t-digest][ClickHouseRefTDigest] data structure.

The [t-digest][Dunning19] data structure is designed around computing
accurate quantile estimates from streaming data. Two t-digests can be merged,
making the data structure well suited for map-reduce settings.

[Documentation]

[ClickHouseRefTDigest]: https://clickhouse.com/docs/en/sql-reference/aggregate-functions/reference/quantiletdigest/
[Dunning19]: https://github.com/tdunning/t-digest/blob/main/docs/t-digest-paper/histo.pdf
[Documentation]: https://vivienm.github.io/python-tdigest-ch/docs/

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
