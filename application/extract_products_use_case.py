from dataclasses import dataclass
import logging

from application.base import UseCase
from infrastructure.browser_service import BrowserService
from infrastructure.csv_exporter import ProductCSVExporter


@dataclass
class ExtractProductsUseCase(UseCase[None]):
    _browser_service: BrowserService
    exporter: ProductCSVExporter

    @property
    def browser_service(self):
        return self._browser_service
    
    async def execute(self) -> None:
        products = await self.browser_service.extract_products()
        self.exporter.export(products)
