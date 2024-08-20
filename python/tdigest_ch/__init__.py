from typing import Any, Iterable, NoReturn, Optional, Union

from ._lowlevel import TDigest as _TDigest

TDigestible = Union[Iterable[float], "TDigest"]


def _unsupported_operand_types(op: str, left: Any, right: Any) -> NoReturn:
    raise TypeError(
        f"unsupported operand type(s) for {op}: {type(left)!r} and {type(right)!r}"
    )


class TDigest:
    """T-digest data structure for approximating the quantiles of a distribution.

    Examples:
        >>> digest = TDigest();
        >>> # Add some elements.
        >>> digest.add(1.0);
        >>> digest.add(2.0);
        >>> digest.add(3.0);
        >>> # Get the median of the distribution.
        >>> digest.quantile(0.5);
        2.0
    """

    __slots__ = ["_inner"]

    _inner: _TDigest

    def __init__(
        self,
        elems: Optional[TDigestible] = None,
    ) -> None:
        if isinstance(elems, TDigest):
            self._inner = elems._inner.copy()
            return
        self._inner = _TDigest()
        if elems is not None:
            self.update(elems)

    def __bool__(self) -> bool:
        return bool(self._inner)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TDigest) and self._inner.is_equal(other._inner)

    def __ior__(self, other: "TDigest") -> "TDigest":
        """Update the t-digest, adding elements from the other.

        Examples:
            >>> digest_1 = TDigest([1.0, 2.0, 3.0])
            >>> digest_2 = TDigest([4.0, 5.0])
            >>> digest_1 |= digest_2
            >>> len(digest_1)
            5
        """
        if not isinstance(other, TDigest):
            _unsupported_operand_types("|=", self, other)
        self._inner.update_digest(other._inner)
        return self

    def __len__(self) -> int:
        """Return the number of elements in the t-digest.

        Examples:
            >>> digest = TDigest([1.0, 2.0, 3.0])
            >>> len(digest)
            3
            >>> digest.add(3.0, count=2)
            >>> len(digest)
            5
        """
        return len(self._inner)

    def __or__(self, other: "TDigest") -> "TDigest":
        """Return a new t-digest with elements from the t-digest and the other.

        Examples:
            >>> digest_1 = TDigest([1.0, 2.0, 3.0])
            >>> digest_2 = TDigest([4.0, 5.0])
            >>> digest = digest_1 | digest_2
            >>> len(digest)
            5
            >>> digest.quantile(0.5)
            3.0
        """
        if not isinstance(other, TDigest):
            _unsupported_operand_types("|", self, other)
        result = self.copy()
        result._inner.update_digest(other._inner)
        return result

    def add(self, value: float, count: int = 1) -> None:
        """Add a value to the t-digest.

        Examples:
            >>> digest = TDigest()
            >>> digest.add(1.0)
            >>> digest.add(2.0)
            >>> len(digest)
            2
        """
        if count == 1:
            self._inner.add(value)
        else:
            self._inner.add_many(value, count)

    def clear(self) -> None:
        """Clear the t-digest, removing all values.

        Examples:
            >>> digest = TDigest()
            >>> digest.add(1.0)
            >>> digest.clear()
            >>> len(digest)
            0
        """
        self._inner.clear()

    def copy(self) -> "TDigest":
        """Return a copy of the t-digest."""
        return TDigest(self)

    @staticmethod
    def from_json(json: Union[str, bytes]) -> "TDigest":
        """Return a t-digest from a JSON representation."""
        if isinstance(json, str):
            json = json.encode()
        digest = TDigest.__new__(TDigest)
        digest._inner = _TDigest.from_json(json)
        return digest

    def quantile(self, level: float) -> float:
        """Return the estimated quantile of the t-digest.

        Examples:
            >>> digest = TDigest([1.0, 2.0, 3.0, 4.0, 5.0])
            >>> digest.quantile(0.5)
            3.0
        """
        return self._inner.quantile(level)  # type: ignore

    def to_json(self) -> bytes:
        """Return a JSON representation of the t-digest."""
        return self._inner.to_json()  # type: ignore

    def union(self, *others: TDigestible) -> "TDigest":
        """Return a new t-digest with elements from the t-digest and all others.

        Examples:
            >>> digest_1 = TDigest([1.0, 2.0, 3.0])
            >>> digest_2 = TDigest([4.0, 5.0])
            >>> digest = digest_1.union(digest_2)
            >>> len(digest)
            5
            >>> digest.quantile(0.5)
            3.0
        """
        result = self.copy()
        result.update(*others)
        return result

    def update(self, *others: TDigestible) -> None:
        """Update the t-digest, adding elements from all others.

        Examples:
            >>> digest = TDigest([1.0, 2.0, 3.0])
            >>> digest.update([4.0, 5.0])
            >>> len(digest)
            5
            >>> digest.quantile(0.5)
            3.0
        """
        for other in others:
            if isinstance(other, TDigest):
                self._inner.update_digest(other._inner)
            elif isinstance(other, (list, tuple)):
                self._inner.update_vec(other)
            else:
                self._inner.update_vec(list(other))
