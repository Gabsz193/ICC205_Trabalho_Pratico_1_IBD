from db.connection import DatabaseConnection
from models.product import Product
from repositories.product_repository import ProductRepository

productRepository = ProductRepository(connection=DatabaseConnection())

product = productRepository.save(product=Product(
    id_product="123",
    asin="123213",
    title="Teste",
    salesrank=123,
    total=123,
    id_group="123",
    avg_rating=5.0
))

print(product)
