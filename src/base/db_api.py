from collections.abc import Sequence, Mapping
from typing import Any, Protocol



class Cursor(Protocol):
    description: Sequence[Any] | None
    rowcount: int
    arraysize: int

    def close(self) -> None:
        ...

    def execute(self, operation: Any, *args, **kwargs) -> None:
        ...

    def executemany(
        self,
        operation: Any,
        seq_of_parameters: Sequence[Any] | Mapping[Any, Any],
        *args,
        **kwargs
    ) -> None:
        ...

    def fetchone(self) -> Sequence[Any] | None:
        ...

    def fetchmany(self, size: int = 0) -> Sequence[Sequence[Any]]:
        ...

    def fetchall(self, size: int = 0) -> Sequence[Sequence[Any]]:
        ...

    def setinputsizes(self, sizes: Sequence[Any]) -> None:
        ...

    def setoutputsize(self, size: Any, column: int | None = None) -> None:
        ...

class Connection(Protocol):
    def close(self) -> None:
        ...

    def commit(self) -> None:
        ...

    def cursor(self, *args, **kwargs) -> Cursor:
        ...