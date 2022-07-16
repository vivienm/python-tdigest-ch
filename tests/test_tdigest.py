import math
import random

import pytest

from tdigest_ch import TDigest


class TestTDigest:
    def test_init(self):
        t = TDigest()
        assert not t
        assert len(t) == 0
        assert math.isnan(t.quantile(0.5))

        t = TDigest([1.0, 2.0, 3.0])
        assert t
        assert len(t) == 3
        assert t.quantile(0.5) == 2.0

        with pytest.raises(TypeError):
            TDigest(1)

    def test_bool(self):
        t = TDigest()
        assert not t

        t = TDigest([1.0, 2.0, 3.0])
        assert t

    def test_eq(self):
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
        t2 = "not a t-digest"
        assert t1 != t2

    def test_ior(self):
        t1 = TDigest([1.0, 2.0, 3.0])
        t2 = TDigest([3.0, 4.0, 5.0])
        t1 |= t2
        assert len(t1) == 6
        assert t1.quantile(0.0) == 1.0
        assert t1.quantile(1.0) == 5.0
        assert t1.quantile(0.5) == 3.0

        with pytest.raises(TypeError):
            t1 |= 1

    def test_len(self):
        t = TDigest()
        assert len(t) == 0

        t = TDigest([1.0, 2.0, 3.0])
        assert len(t) == 3

        t.add(4.0)
        assert len(t) == 4

        t.update([3.0, 4.0, 5.0])
        assert len(t) == 7

    def test_or(self):
        t1 = TDigest([1.0, 2.0, 3.0])
        t2 = TDigest([3.0, 4.0, 5.0])
        t3 = t1 | t2
        assert len(t3) == 6
        assert t3.quantile(0.0) == 1.0
        assert t3.quantile(1.0) == 5.0
        assert t3.quantile(0.5) == 3.0

        with pytest.raises(TypeError):
            t1 | 1

    def test_add(self):
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

    def test_clear(self):
        t = TDigest([1.0, 2.0, 3.0])
        t.clear()
        assert not t
        assert len(t) == 0
        assert math.isnan(t.quantile(0.5))

    def test_copy(self):
        t1 = TDigest([1.0, 2.0, 3.0])
        t2 = t1.copy()
        assert t1 == t2
        t1.add(4.0)
        assert t1 != t2
        assert len(t2) == 3

    def test_quantile(self):
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

    def test_quantile_extreme(self):
        t = TDigest()
        samples = [random.gauss(0.0, 1.0) for _ in range(10000)]
        t.update(samples)
        assert abs(t.quantile(1.0) - max(samples)) < 0.0001
        assert abs(t.quantile(0.0) - min(samples)) < 0.0001
        assert t.quantile(0.001) > min(samples)
        assert t.quantile(0.999) < max(samples)

    def test_quantile_uniform(self):
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

    def test_union(self):
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
            t1.union(1)

    def test_update(self):
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
            t1.update(1)
