from collections.abc import Sequence
from typing import Any, Iterable, NoReturn, Optional, Union

from . import _rust  # type: ignore

_Elements = Union[Iterable[float], "TDigest"]


def _unsupported_operand_types(op: str, left: Any, right: Any) -> NoReturn:
    raise TypeError(
        f"unsupported operand type(s) for {op}:" f" {type(left)!r} and {type(right)}"
    )


class TDigest:
    """A t-digest data structure."""

    __slots__ = ["_inner"]

    _inner: _rust.TDigest

    def __init__(
        self,
        elems: Optional[_Elements] = None,
    ) -> None:
        if isinstance(elems, TDigest):
            self._inner = elems._inner.copy()
            return
        self._inner = _rust.TDigest()
        if elems is not None:
            self.update(elems)

    def __bool__(self) -> bool:
        return bool(self._inner)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TDigest) and self._inner.is_equal(other._inner)

    def __ior__(self, other: "TDigest") -> "TDigest":
        if not isinstance(other, TDigest):
            _unsupported_operand_types("|=", self, other)
        self._inner.update_digest(other._inner)
        return self

    def __len__(self) -> int:
        return len(self._inner)

    def __or__(self, other: "TDigest") -> "TDigest":
        if not isinstance(other, TDigest):
            _unsupported_operand_types("|", self, other)
        result = self.copy()
        result._inner.update_digest(other._inner)
        return result

    def add(self, value: float) -> None:
        """Add a value to the t-digest."""
        self._inner.add(value)

    def clear(self) -> None:
        """Clear the t-digest."""
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
        digest._inner = _rust.TDigest.from_json(json)
        return digest

    def quantile(self, q: float) -> float:
        """Return the qth quantile of the t-digest."""
        return self._inner.quantile(q)

    def to_json(self) -> bytes:
        """Return a JSON representation of the t-digest."""
        return self._inner.to_json()

    def update(self, *others: _Elements) -> None:
        """Update the t-digest, adding elements from all others."""
        if len(others) == 0:
            return
        for other in others:
            if isinstance(other, TDigest):
                self._inner.update_digest(other._inner)
            elif isinstance(other, Sequence):
                self._inner.update_sequence(other)
            else:
                self._inner.update_sequence(list(other))

    def union(self, *others: _Elements) -> "TDigest":
        """Return a new t-digest with elements from the t-digest and all others."""
        if len(others) == 0:
            return self
        result = self.copy()
        result.update(*others)
        return result