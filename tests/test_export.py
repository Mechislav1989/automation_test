from domain.entities.product import Product
from infrastructure.csv_exporter import ProductCSVExporter


def test_csv_export(tmp_path, container):
    exporter = container.resolve(ProductCSVExporter)
    test_products = [Product(name="Test", price="$10")]
    
    file_path = tmp_path / "test.csv"
    exporter.export(test_products, file_path)
    
    with open(file_path) as f:
        content = f.read()
        assert "Test,$10" in content