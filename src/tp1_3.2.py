import uuid

from db.connection import DatabaseConnection
from args import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS, INPUT
from models.category import Category as ModelCategory
from models.customer import Customer as ModelCustomer
from models.group import Group
from models.product import Product
from models.product_category import ProductCategory
from models.review import Review as ModelReview
from models.similar_products import SimilarProducts
from parser.amazon_parser import AmazonParser
from parser.schema import Product as ProductParser, Category


def create_tables(script: str):
    try:
        with DatabaseConnection(
                DB_HOST,
                DB_PORT,
                DB_NAME,
                DB_USER,
                DB_PASS
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(script)
        return 0
    except Exception as e:
        print(e)
        return -1


def insert_from_product(product: ProductParser):
    group_id: str = uuid.uuid4().hex
    group_to_insert: Group = Group(
        id_group=group_id,
        name=product.group.name,
    ) if product.group else None
    reviews_to_insert: list[ModelReview] = []
    customers_to_insert: list[ModelCustomer] = []
    categories_to_insert: list[ModelCategory] = []
    product_categories_to_insert: list[ProductCategory] = []
    similar_products_to_insert: list[SimilarProducts] = []

    product_to_insert: Product = Product(
        id_product=product.id_product,
        asin=product.asin,
        title=product.title,
        id_group=group_id if product.group else None,
        salesrank=product.salesrank,
        total=product.total,
        avg_rating=product.avg_rating,
    )

    i = 1

    for similar_product in product.similarProducts:
        similar_products_to_insert.append(SimilarProducts(
            id_product=product.id_product,
            id_similar_product=similar_product.id_similar_product,
            rank=i
        ))
        i += 1

    for review in product.reviews:
        review_id = uuid.uuid4().hex

        customers_to_insert.append(ModelCustomer(
            id_customer=review.customer.id_customer,
        ))

        reviews_to_insert.append(ModelReview(
            id_review=review_id,
            id_product=product.id_product,
            id_customer=review.customer.id_customer,
            dt_review=review.dt_review,
            rating=review.rating,
            qtd_votes=review.qtd_votes,
            qtd_helpful_votes=review.qtd_helpful_votes,
        ))

    for category in product.categories:
        current_category: Category = category

        product_category_id: str = uuid.uuid4().hex

        product_categories_to_insert.append(ProductCategory(
            id_product_category=product_category_id,
            id_product=product.id_product,
            id_category=current_category.id_category,
        ))

        while current_category.super_category is not None:
            categories_to_insert.append(ModelCategory(
                id_category=current_category.id_category,
                name=current_category.name,
                id_super_category=current_category.super_category.id_category,
            ))

            current_category = current_category.super_category

        categories_to_insert.append(ModelCategory(
            id_category=current_category.id_category,
            name=category.name,
            id_super_category=None
        ))

    print("Processou")

    # print(product_to_insert)
    # print(group_to_insert)
    # print(reviews_to_insert)
    # print(customers_to_insert)
    # print(categories_to_insert)
    # print(product_categories_to_insert)
    # print(similar_products_to_insert)


def parse_and_save(filename: str):
    amazon_parser = AmazonParser(filename)

    qtd_products = amazon_parser.get_count()
    # qtd_products = 15000
    batch_size = 5000

    qtd_processed = 0
    last_line = None

    for i in range(0, qtd_products, batch_size):
        products, last_line = amazon_parser.parse_n_products(batch_size, last_line)
        if last_line == -1:
            qtd_processed += len(products)
            break
        print("Linha a ser pega:", last_line)
        qtd_processed += len(products)
        for product in products:
            insert_from_product(product)
        print("Quantidade de produtos processados:", qtd_processed, "...")

    print("Quantidade total:", qtd_processed)


def main():
    try:
        with open('sql/schema.sql', 'r') as f:
            script = f.read()
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return -1

    if create_tables(script) == -1:
        return -1

    parse_and_save(INPUT)

    return 0


if __name__ == '__main__':
    exit_code = main()
    exit(exit_code)
