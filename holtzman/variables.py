from typing import Any, List

from .errors import MissingVariableError


class VariableContext:
    def __init__(self, variables: Any):
        self._contexts: List[Any] = [variables]

    def push_context(self, variables: Any) -> None:
        self._contexts.insert(0, variables)

    def pop_context(self) -> Any:
        return self._contexts.pop(0)

    def __repr__(self) -> str:
        return self._contexts.__str__()

    def find_var_in_context(self, context, key_parts):
        current_context = context
        for part in key_parts:
            if isinstance(current_context, dict) and (part in current_context):
                current_context = current_context[part]
            elif hasattr(current_context, part):
                current_context = getattr(current_context, part)
            else:
                return None
        return current_context

    def __getitem__(self, key: str) -> Any:
        key_parts: List[str] = key.split('.')

        for context in self._contexts:
            var = self.find_var_in_context(context, key_parts)
            if var is not None:
                return var

        raise MissingVariableError(key)
