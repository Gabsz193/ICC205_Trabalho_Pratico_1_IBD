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
from repositories.category_repository import CategoryRepository
from repositories.customer_repository import CustomerRepository
from repositories.groups_repository import GroupRepository
from repositories.product_category_repository import ProductCategoryRepository
from repositories.product_repository import ProductRepository
from repositories.review_repository import ReviewRepository
from repositories.similar_products_repository import SimilarProductsRepository

databaseConnection = DatabaseConnection(
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASS
)

group_repository = GroupRepository(connection=databaseConnection)
product_repository = ProductRepository(connection=databaseConnection)
category_repository = CategoryRepository(connection=databaseConnection)
customer_repository = CustomerRepository(connection=databaseConnection)
review_repository = ReviewRepository(connection=databaseConnection)
similar_products_repository = SimilarProductsRepository(connection=databaseConnection)
product_category_repository = ProductCategoryRepository(connection=databaseConnection)

def create_tables(script: str):
    try:
        with databaseConnection as conn:
            with conn.cursor() as cursor:
                cursor.execute(script)
        return 0
    except Exception as e:
        print(e)
        return -1


def insert_from_product(product: ProductParser):
    group_to_insert: Group = Group(
        id_group=product.group.name,
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
        id_group=product.group.name if product.group else None,
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

    return {
        'product': product_to_insert,
        'group': group_to_insert,
        'reviews': reviews_to_insert,
        'customers': customers_to_insert,
        'categories': categories_to_insert,
        'product_categories': product_categories_to_insert,
        'similar_products': similar_products_to_insert
    }


    # print(product_to_insert)
    # print(group_to_insert)
    # print(reviews_to_insert)
    # print(customers_to_insert)
    # print(categories_to_insert)
    # print(product_categories_to_insert)
    # print(similar_products_to_insert)


def parse_and_save(filename: str):
    parser = AmazonParser(filename)
    stop = 0
    batch_size = 10000

    grupo_existe = {}
    categoria_existe = {}

    save_similar_after = []

    while stop != -1:
        data = parser.new_parse_data(n=batch_size, offset=stop)
        stop = data['stop']

        produtos = data['products']
        groups = data['groups']

        new_groups = []
        new_categories = []


        for group in groups:
            if group.name not in grupo_existe:
                if not group_repository.find_by_id(group.id_group):
                    new_groups.append(group)
                    grupo_existe[group.name] = True
            else:
                continue

        groups = new_groups

        categories = data['categories']

        for categorie in categories:
            if categorie.id_category not in categoria_existe:
                if not category_repository.find_by_id(categorie.id_category):
                    new_categories.append(categorie)
                    categoria_existe[categorie.id_category] = True
            else:
                continue

        categories = new_categories

        customers = data['customers']
        product_categories = data['product_categories']
        reviews = data['reviews']
        similar_products = data['similar_products']
        save_similar_after.extend(similar_products)

        group_repository.save(groups)
        category_repository.save(categories)
        customer_repository.save(customers)
        product_repository.save(produtos)
        review_repository.save(reviews)
        product_category_repository.save(product_categories)

    news = []

    for similar in save_similar_after:
        if product_repository.find_by_asin(similar.id_similar_product):
            news.append(similar)

    similar_products_repository.save(news)




    # qtd_processed = 0
    # last_line = None
    #
    # for i in range(0, qtd_products, batch_size):
    #     products, last_line = amazon_parser.parse_n_products(batch_size, last_line)
    #     if last_line == -1:
    #         qtd_processed += len(products)
    #         break
    #     print("Linha a ser pega:", last_line)
    #     qtd_processed += len(products)
    #
    #     campos_a_inserir = []
    #     for product in products:
    #         campos_a_inserir.append(insert_from_product(product))
    #
    #     produtos = list(map(lambda x: x['product'], campos_a_inserir))
    #     groups = list(map(lambda x: x['group'], campos_a_inserir))
    #     categories = list(map(lambda x: x['categories'], campos_a_inserir))
    #     customers = list(map(lambda x: x['customers'], campos_a_inserir))
    #     product_categories = list(map(lambda x: x['product_categories'], campos_a_inserir))
    #     reviews = list(map(lambda x: x['reviews'], campos_a_inserir))
    #     similar_products = list(map(lambda x: x['similar_products'], campos_a_inserir))
    #
    #
    #     categories = list(chain.from_iterable(categories))
    #     customers = list(chain.from_iterable(customers))
    #     reviews = list(chain.from_iterable(reviews))
    #
    #     group_repository.save(groups)
    #     category_repository.save(categories)
    #     customer_repository.save(customers)
    #     product_repository.save(produtos)
    #     review_repository.save(reviews)
        # similar_products_repository.save(similar_products)

        # print("Quantidade de produtos processados:", qtd_processed, "...")

    # print("Quantidade total:", qtd_processed)


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
