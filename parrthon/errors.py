from abc import ABC, abstractmethod

class ExitParrthon(Exception):
    pass

class ParrthonError(ABC):

    @abstractmethod
    def __repr__(self) -> str:
        ...

    @staticmethod
    def gen(msg: str) -> str:
        return f"Shiver me timbers: {msg}"

class InvalidVariableError(ParrthonError):
    def __init__(self, identifier: str):
        self.identifier = identifier

    def __repr__(self) -> str:
        return super().gen(f"Could not find ye variable `{self.identifier}`")

class UnknownFunctionError(ParrthonError):
    def __init__(self, identifier: str):
        self.identifier = identifier

    def __repr__(self) -> str:
        return super().gen(f"Could not find ye function `{self.identifier}`")