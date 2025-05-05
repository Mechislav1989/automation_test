import csv
from dataclasses import dataclass
import logging

from domain.entities.product import Product


@dataclass
class ProductCSVExporter:
    logger: logging.Logger
    
    def export(self, products: list[Product], filename: str="products.csv") -> None:
        headers = [
            "Product Name", 
            "Price",
        ]
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(headers)
                
                for product in products:
                    writer.writerow([
                        product.name,
                        product.price,
                    ])

            self.logger.info(f"Exported {len(products)} products to {filename}.")
        except Exception as e:
            self.logger.error(f"Failed to export products to CSV: {str(e)}")

