from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

from infrastructure.browser_service import BrowserService


T = TypeVar('T')


@dataclass
class UseCase(ABC, Generic[T]):
    @property
    @abstractmethod
    def browser_service(self) -> BrowserService:
        """
        Get the browser service instance.

        :return: The browser service instance.
        """
        pass
    
    @abstractmethod
    def execute(self) -> T:
        """
        Execute the use case with the given arguments.

        :return: The result of the use case execution.
        """
        pass