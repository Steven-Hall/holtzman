from typing import Any, List

from .errors import MissingVariableError


class VariableContext:
    def __init__(self, variables: Any):
        self._contexts: List[Any] = [variables]

    def push_context(self, variables: Any) -> None:
        self._contexts.append(variables)

    def pop_context(self) -> Any:
        return self._contexts.pop()

    def __getitem__(self, key: str) -> Any:
        key_parts = key.split('.')

        for context in self._contexts:
            c = context
            for part in key_parts:
                if isinstance(c, dict):
                    if part in c:
                        c = c[part]
                    else:
                        raise MissingVariableError(key)
                else:
                    if hasattr(c, part):
                        c = getattr(c, part)
                    else:
                        raise MissingVariableError(key)

        return c
