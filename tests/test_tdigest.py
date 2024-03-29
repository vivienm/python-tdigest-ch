import math
import random

import pytest
from tdigest_ch import TDigest


class TestTDigest:
    def test_init(self) -> None:
        t = TDigest()
        assert not t
        assert len(t) == 0
        assert math.isnan(t.quantile(0.5))

        t = TDigest([1.0, 2.0, 3.0])
        assert t
        assert len(t) == 3
        assert t.quantile(0.5) == 2.0

        with pytest.raises(TypeError):
            TDigest(1)  # type: ignore

    def test_bool(self) -> None:
        t = TDigest()
        assert not t

        t = TDigest([1.0, 2.0, 3.0])
        assert t

    def test_eq(self) -> None:
        t1 = TDigest()
        t2 = TDigest()
        assert t1 == t2

        t1 = TDigest([1.0, 2.0, 3.0])
        t2 = TDigest([1.0, 2.0, 3.0])
        assert t1 == t2

        t1 = TDigest([1.0, 2.0, 3.0])
        t2 = TDigest([1.0, 2.0, 4.0])
        assert t1 != t2

        t1 = TDigest([1.0, 2.0, 3.0])
        t2 = "not a t-digest"  # type: ignore
        assert t1 != t2

    def test_ior(self) -> None:
        t1 = TDigest([1.0, 2.0, 3.0])
        t2 = TDigest([3.0, 4.0, 5.0])
        t1 |= t2
        assert len(t1) == 6
        assert t1.quantile(0.0) == 1.0
        assert t1.quantile(1.0) == 5.0
        assert t1.quantile(0.5) == 3.0

        with pytest.raises(TypeError):
            t1 |= 1  # type: ignore

    def test_len(self) -> None:
        t = TDigest()
        assert len(t) == 0

        t = TDigest([1.0, 2.0, 3.0])
        assert len(t) == 3

        t.add(4.0)
        assert len(t) == 4

        t.update([3.0, 4.0, 5.0])
        assert len(t) == 7

    def test_or(self) -> None:
        t1 = TDigest([1.0, 2.0, 3.0])
        t2 = TDigest([3.0, 4.0, 5.0])
        t3 = t1 | t2
        assert len(t3) == 6
        assert t3.quantile(0.0) == 1.0
        assert t3.quantile(1.0) == 5.0
        assert t3.quantile(0.5) == 3.0

        with pytest.raises(TypeError):
            t1 | 1  # type: ignore

    def test_add(self) -> None:
        t = TDigest()
        t.add(1.0)
        assert len(t) == 1
        assert t.quantile(0.0) == 1.0
        assert t.quantile(1.0) == 1.0
        assert t.quantile(0.5) == 1.0

        t.add(2.0)
        assert len(t) == 2
        assert t.quantile(0.0) == 1.0
        assert t.quantile(1.0) == 2.0
        assert t.quantile(0.5) == 1.0

        t.add(3.0)
        assert len(t) == 3
        assert t.quantile(0.0) == 1.0
        assert t.quantile(1.0) == 3.0
        assert t.quantile(0.5) == 2.0

        t.add(5.0, 4)
        assert len(t) == 7
        assert t.quantile(0.5) == 3.5

        with pytest.raises(TypeError):
            t.add("not a number")  # type: ignore

        with pytest.raises(TypeError):
            t.add(1.0, "not a number")  # type: ignore

        with pytest.raises(OverflowError):
            t.add(1.0, -1)

    def test_clear(self) -> None:
        t = TDigest([1.0, 2.0, 3.0])
        t.clear()
        assert not t
        assert len(t) == 0
        assert math.isnan(t.quantile(0.5))

    def test_copy(self) -> None:
        t1 = TDigest([1.0, 2.0, 3.0])
        t2 = t1.copy()
        assert t1 == t2
        t1.add(4.0)
        assert t1 != t2
        assert len(t2) == 3

    def test_from_json(self) -> None:
        t = TDigest.from_json(b"[[0.01,2048,2048],[[1.0,1],[2.0,1],[3.0,1]],3,3]")
        assert t.quantile(0.5) == 2.0

        t = TDigest.from_json("[[0.01,2048,2048],[[1.0,1],[2.0,1],[3.0,1]],3,3]")
        assert t.quantile(0.5) == 2.0

        with pytest.raises(TypeError):
            TDigest.from_json(1)  # type: ignore

        with pytest.raises(ValueError):
            TDigest.from_json(b"[[0.01,2048,2048],[[1.0,1],[2.0,1],[3.0,1]],3,3,1]")

    def test_quantile(self) -> None:
        t = TDigest()
        t.update([1, 2, 3])
        assert abs(t.quantile(0.5) - 2) < 0.0001

        t = TDigest()
        t.update([1, 2, 2, 2, 2, 2, 2, 2, 3])
        assert t.quantile(0.5) == 2.0

        t = TDigest()
        t.update([1, 1, 2, 2, 3, 4, 4, 4, 5, 5])
        assert t.quantile(0.3) == 2.0
        assert t.quantile(0.4) == 2.0

        with pytest.raises(TypeError):
            t.quantile("not a number")  # type: ignore

    def test_quantile_extreme(self) -> None:
        t = TDigest()
        samples = [random.gauss(0.0, 1.0) for _ in range(10000)]
        t.update(samples)
        assert abs(t.quantile(1.0) - max(samples)) < 0.0001
        assert abs(t.quantile(0.0) - min(samples)) < 0.0001
        assert t.quantile(0.001) > min(samples)
        assert t.quantile(0.999) < max(samples)

    def test_quantile_uniform(self) -> None:
        t = TDigest()
        samples = [random.random() for _ in range(50000)]
        t.update(samples)
        assert abs(t.quantile(0.50) - 0.5) < 0.01
        assert abs(t.quantile(0.10) - 0.1) < 0.01
        assert abs(t.quantile(0.90) - 0.9) < 0.01
        assert abs(t.quantile(0.01) - 0.01) < 0.005
        assert abs(t.quantile(0.99) - 0.99) < 0.005
        assert abs(t.quantile(0.001) - 0.001) < 0.001
        assert abs(t.quantile(0.999) - 0.999) < 0.001

    def test_to_json(self) -> None:
        t = TDigest([1.0, 2.0, 3.0])
        assert t.to_json() == b"[[0.01,2048,2048],[[1.0,1],[2.0,1],[3.0,1]],3,3]"

    def test_union(self) -> None:
        t1 = TDigest([1.0, 2.0, 3.0])
        t2 = TDigest([3.0, 4.0, 5.0])
        t3 = t1.union(t2)
        assert len(t3) == 6
        assert t3.quantile(0.0) == 1.0
        assert t3.quantile(1.0) == 5.0
        assert t3.quantile(0.5) == 3.0

        t4 = t1.union([3.0, 4.0, 5.0])
        assert len(t4) == 6
        assert t4.quantile(0.0) == 1.0
        assert t4.quantile(1.0) == 5.0
        assert t4.quantile(0.5) == 3.0

        with pytest.raises(TypeError):
            t1.union(1)  # type: ignore

        t5 = TDigest()
        t6 = t5.union()
        t6.update([1.0, 2.0, 3.0])
        assert len(t5) == 0
        assert len(t6) == 3

    def test_update(self) -> None:
        t1 = TDigest([1.0, 2.0, 3.0])
        t2 = TDigest([3.0, 4.0, 5.0])
        t1.update(t2)
        assert len(t1) == 6
        assert t1.quantile(0.0) == 1.0
        assert t1.quantile(1.0) == 5.0
        assert t1.quantile(0.5) == 3.0

        t1 = TDigest([1.0, 2.0, 3.0])
        t1.update([3.0, 4.0, 5.0])
        assert len(t1) == 6
        assert t1.quantile(0.0) == 1.0
        assert t1.quantile(1.0) == 5.0
        assert t1.quantile(0.5) == 3.0

        with pytest.raises(TypeError):
            t1.update(1)  # type: ignore
