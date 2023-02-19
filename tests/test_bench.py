import random
from typing import List

import pytest
from pytest_benchmark.fixture import BenchmarkFixture
from tdigest import TDigest as PyTDigest

from tdigest_ch import TDigest as RsTDigest


@pytest.fixture
def samples() -> List[float]:
    r = random.Random(42)
    return [r.gauss(0.0, 1.0) for _ in range(50000)]


@pytest.mark.benchmark(group="update")
def test_py_update(benchmark: BenchmarkFixture, samples: List[float]) -> None:
    t = PyTDigest()
    benchmark(t.batch_update, samples)
    assert -1.0 <= t.percentile(50) <= 1.0


@pytest.mark.benchmark(group="update")
def test_rs_update(benchmark: BenchmarkFixture, samples: List[float]) -> None:
    t = RsTDigest()
    benchmark(t.update, samples)
    assert -1.0 <= t.quantile(0.5) <= 1.0


@pytest.mark.benchmark(group="quantile")
def test_py_quantile(benchmark: BenchmarkFixture, samples: List[float]) -> None:
    t = PyTDigest()
    t.batch_update(samples)
    benchmark(t.percentile, 50)


@pytest.mark.benchmark(group="quantile")
def test_rs_quantile(benchmark: BenchmarkFixture, samples: List[float]) -> None:
    t = RsTDigest()
    t.update(samples)
    benchmark(t.quantile, 0.5)


@pytest.fixture(scope="session")
def full_tdigest() -> RsTDigest:
    return RsTDigest(random.gauss(0.0, 1.0) for _ in range(1_000_000))


@pytest.mark.benchmark(group="serialize")
def test_serialize(benchmark: BenchmarkFixture, full_tdigest: RsTDigest) -> None:
    benchmark(full_tdigest.to_json)


@pytest.mark.benchmark(group="deserialize")
def test_deserialize(benchmark: BenchmarkFixture, full_tdigest: RsTDigest) -> None:
    benchmark(RsTDigest.from_json, full_tdigest.to_json())
