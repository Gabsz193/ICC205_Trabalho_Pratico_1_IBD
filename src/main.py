from datetime import datetime
from db.connection import DatabaseConnection
from models.group import Group
from models.product import Product
from models.category import Category
from models.customer import Customer
from models.review import Review
from models.similar_products import SimilarProducts
from repositories.groups_repository import GroupRepository
from repositories.product_repository import ProductRepository
from repositories.category_repository import CategoryRepository
from repositories.customer_repository import CustomerRepository
from repositories.review_repository import ReviewRepository
from repositories.similar_products_repository import SimilarProductsRepository

# ==========================
# Teste GroupRepository
# ==========================
groupRepository = GroupRepository(connection=DatabaseConnection())

group = groupRepository.save(group=Group(
    id_group="123",
    name="Grupo Teste"
))
print("Group salvo:", group)

group_found = groupRepository.find_by_id("123")
print("Group encontrado:", group_found)

groups = groupRepository.find_all()
print("Todos os groups:", groups)

#deleted_group = groupRepository.delete("123")
#print("Group deletado:", deleted_group)


# ==========================
# Teste ProductRepository
# ==========================
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
print("Product salvo:", product)

product = productRepository.save(product=Product(
    id_product="456",
    asin="250805",
    title="Teste2",
    salesrank=456,
    total=456,
    id_group="123",
    avg_rating=4.0
))
print("Product salvo:", product)


# ==========================
# Teste CategoryRepository
# ==========================
categoryRepository = CategoryRepository(connection=DatabaseConnection())

category = categoryRepository.save(category=Category(
    id_category="001",
    name="Categoria Teste",
    id_super_category=None
))
print("Category salva:", category)

category_found = categoryRepository.find_by_id("001")
print("Category encontrada:", category_found)

categories = categoryRepository.find_all()
print("Todas as categories:", categories)

#deleted_category = categoryRepository.delete("001")
#print("Category deletada:", deleted_category)


# ==========================
# Teste CustomerRepository
# ==========================
customerRepository = CustomerRepository(connection=DatabaseConnection())

customer = customerRepository.save(customer=Customer(
    id_customer="C001"
))
print("Customer salvo:", customer)

customer_found = customerRepository.find_by_id("C001")
print("Customer encontrado:", customer_found)

customers = customerRepository.find_all()
print("Todos os customers:", customers)

#deleted_customer = customerRepository.delete("C001")
#print("Customer deletado:", deleted_customer)


# ==========================
# Teste ReviewRepository
# ==========================
reviewRepository = ReviewRepository(connection=DatabaseConnection())

review = reviewRepository.save(review=Review(
    id_review="R001",
    id_product="123",
    id_customer="C001",
    dt_review=datetime.now(),
    rating=5,
    qtd_votes=10,
    qtd_helpful_votes=8
))
print("Review salva:", review)

review_found = reviewRepository.find_by_id("R001")
print("Review encontrada:", review_found)

reviews = reviewRepository.find_all()
print("Todas as reviews:", reviews)

deleted_review = reviewRepository.delete("R001")
print("Review deletada:", deleted_review)


# ==========================
# Teste SimilarProductsRepository
# ==========================
similarRepository = SimilarProductsRepository(connection=DatabaseConnection())

similar = similarRepository.save(similar=SimilarProducts(
    id_product="123",
    id_similar_product="456",
    rank=1
))
print("SimilarProduct salvo:", similar)

similar_found = similarRepository.find_by_id("123", "456")
print("SimilarProduct encontrado:", similar_found)

similars = similarRepository.find_all()
print("Todos os SimilarProducts:", similars)

deleted_similar = similarRepository.delete("123", "456")
print("SimilarProduct deletado:", deleted_similar)