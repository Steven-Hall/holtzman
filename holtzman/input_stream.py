from typing_extensions import Protocol


class InputStream(Protocol):
    def read(self, number: int) -> str:
        pass
