from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Coroutine, ParamSpec
from playwright.async_api import ElementHandle, JSHandle


P = ParamSpec('P')


def handle_errors(log_message: str = 'Operation failed') -> Callable:
    def decorator(func: Callable[..., Coroutine[Any, Any, None]]) -> Callable:
        @wraps(func)
        async def wrapper(self, *args: P.args, **kwargs: P.kwargs) -> None:
            try:
                return await func(self, *args, **kwargs)
            except Exception as e:
                safe_args = [
                    f"Element<{await arg.get_attribute('data-test')}>" if isinstance(arg, (ElementHandle, JSHandle)) else arg 
                    for arg in args
                ]
                
                error_details = {
                    "operation": func.__name__,
                    "args": safe_args,
                    "kwargs": kwargs,
                    "error_type": type(e).__name__,
                    "error": str(e),
                }
                self.logger.error(f"{log_message}: {error_details}")
                await self._capture_error_evidence()
                raise BrowserOperationError(error_details) from e
        return wrapper
    return decorator


@dataclass
class BrowserOperationError(Exception):
    error_info: dict
    def __str__(self):
        return f"Browser operation failed with error: {self.error_info}"