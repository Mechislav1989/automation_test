from functools import lru_cache
import inspect
import logging

import punq

from application.checkout_use_case import CheckoutUseCase
from application.extract_products_use_case import ExtractProductsUseCase
from application.login_use_case import LoginUseCase
from application.base import UseCase
from infrastructure.browser_service import BrowserService, BrowserServiceState
from infrastructure.csv_exporter import ProductCSVExporter
from infrastructure.logger import configure_logger
from settings.configs.browser_config import BrowserConfig


@lru_cache(1)
def get_container() -> punq.Container:
    return _init_container()


def _init_container() -> punq.Container:
    container = punq.Container()

    def init_browser_config() -> BrowserConfig:
        return BrowserConfig(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            headless=True,
            stealth_mode=True,
        )

    container.register(logging.Logger, instance=configure_logger())

    container.register(
        BrowserService,
        scope=punq.Scope.singleton,
        factory=lambda: BrowserService(
            config=init_browser_config(),
            state=BrowserServiceState(),
            logger=container.resolve(logging.Logger),
        ),
    )
    container.register(LoginUseCase)

    container.register(
        ProductCSVExporter, 
        factory=lambda: ProductCSVExporter(logger=container.resolve(logging.Logger))
    )
    container.register(ExtractProductsUseCase)
    container.register(CheckoutUseCase)
    return container