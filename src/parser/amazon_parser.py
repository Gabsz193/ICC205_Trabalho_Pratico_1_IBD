import os
import re
import uuid
from datetime import datetime
from typing import List
from tqdm import tqdm

from parser.category import Category
from parser.customer import Customer
from parser.group import Group
from parser.product import Product
from parser.product_category import ProductCategory
from parser.review import Review
from parser.similar_products import SimilarProducts


class AmazonParser:
    """
    Parser para dados do Amazon

    Esta classe tem como objetivo prover todos os métodos necessários para
    manipular os dados do Amazon.
    """

    file_lines: list[str]
    file_str: str
    caret_line: int = 0

    def __init__(self, input_filename: str):
        try:
            with open(input_filename, "r") as file:
                # Não demora muito, apesar do documento ter quase 1GB
                self.total_blocks = file.read().split("\n\n")
                self.total_blocks.pop(0)
                self.total_blocks.pop(-1)
        except FileNotFoundError:
            print("Arquivo não encontrado.")

    def get_count(self) -> int:
        # Pega a segunda linha do documento que possui a quantidade
        total = re.search(r'\d+', self.file_lines[1])

        return int(total.group())

    def get_data(self, start_line: int) -> tuple[list[str], int]:
        """
        Por enquanto, esta função está pegando uma linha do documento e
        verificando se está é o início de um produto via regex, presumindo
        que todos começam com 'ID: xxx'.

        Ela está retornando uma tupla com a lista de linhas do produto e a
        linha de termino. Consequentemente, para pegar o próximo, basta
        adicionar 1 ao valor da linha de termino.

        :param start_line: Linha de início de um produto (ID: xxx)
        :return: (lista de linhas do produto, linha de termino)
        """
        start_pattern = re.compile(r'^Id:\W*\d+$')

        current_line = start_line

        try:
            if not start_pattern.match(self.file_lines[start_line]):
                raise ValueError("Linha de início inválida")
        except IndexError:
            return [], -1

        while self.file_lines[current_line].strip() != "":
            current_line += 1

        # (Id:\s*(\d+)\n)(ASIN:\s*(\w+)\n)\s{2}(title:\s*(.+)\n)?\s{2}(group:\s*(\w+)\n)?\s{2}(salesrank:\s*(\d+)\n)?\s{2}(similar:\s*(\d+)\s*(.+)\n)\s{2}(categories:\s*\d+\n)?(\s{3}.+)?\s{2}(reviews:\s*total:\s*(\d+)\s*downloaded:\s*(\d+)\s*avg rating:\s*(\d+))\n(\s{3}.+)

        # (Id:\s*(\d+)\n)(ASIN:\s*(\w+)\n)(\s{2}(title:\s*(.+)\n)?\s{2}(group:\s*(\w+)\n)?\s{2}(salesrank:\s*(\d+)\n)?\s{2}(similar:\s*(\d+)\s*(.*)\n)\s{2}(categories:\s*\d+\n)?(\s{3}.+)?\s{2}(reviews:\s*total:\s*(\d+)\s*downloaded:\s*(\d+)\s*avg rating:\s*(\d+\.?\d*))\n(\s{3}.+))?

        return self.file_lines[start_line:current_line], current_line

    def new_parse_data(self, n: int = None, offset: int = 0) -> dict:

        super_mega_pattern = re.compile(
            r'(Id:\s*(\d+)\n)(ASIN:\s*(\w+)\n)(\s{2}(title:\s*(.+)\n)?\s{2}(group:\s*(\w+)\n)?\s{2}(salesrank:\s*(\d+)\n)?\s{2}(similar:\s*(\d+)\s*(.*)\n)\s{2}(categories:\s*\d+\n)?(\s{3}.+)?\s{2}(reviews:\s*total:\s*(\d+)\s*downloaded:\s*(\d+)\s*avg rating:\s*(\d+\.?\d*))\n(\s{3}.+))?',
            re.DOTALL)

        list_data = {
            'products': [],
            'groups': [],
            'categories': [],
            'reviews': [],
            'similar_products': [],
            'customers': [],
            'product_categories': [],
            'stop': -1,
        }

        # Verificar se offset é válido
        if offset < 0 or offset >= len(self.total_blocks):
            return list_data

        # Determinar os blocos a processar
        end_idx = len(self.total_blocks) if n is None else min(offset + n, len(self.total_blocks))
        blocks_to_process = self.total_blocks[offset:end_idx]

        for idx, block in enumerate(tqdm(blocks_to_process, desc="Fazendo parsing dos blocos", colour='green')):
            if match := super_mega_pattern.match(block):
                id_product = match.group(2)
                asin_product = match.group(4)
                title_product = match.group(7)
                group_product = match.group(9)
                salesrank_product = match.group(11)
                similar_products_asin = match.group(14)
                categories_product = match.group(16)
                total_product = match.group(18)
                downloaded_product = match.group(19)
                avg_rating_product = match.group(20)
                reviews_product = match.group(21)

                product = Product(
                    id_product=id_product,
                    asin=asin_product,
                    title=title_product,
                    id_group=group_product,
                    salesrank=salesrank_product,
                    total=total_product,
                    avg_rating=avg_rating_product,
                )

                group = Group(
                    id_group=group_product,
                    name=group_product,
                ) if group_product else None

                def get_cat_and_id(cat_line: str) -> tuple[str, str]:
                    cat_pattern = re.compile(r'^(.*)\[(.*)]$')
                    cat_name = cat_pattern.match(cat_line).group(1)
                    cat_id = cat_pattern.match(cat_line).group(2)
                    return cat_name, cat_id

                cat_lines = []

                if categories_product:
                    cat_lines = categories_product.split('\n')
                    cat_lines = list(map(lambda x: x.strip(), cat_lines))
                    cat_lines = list(filter(lambda x: x, cat_lines))

                product_categories = []
                categories = []

                for line in cat_lines:
                    cats = line.split('|')
                    cats = list(filter(lambda x: x, cats))
                    cats = list(map(get_cat_and_id, cats))

                    product_categories.append(ProductCategory(
                        id_product_category=uuid.uuid4().hex,
                        id_product=id_product,
                        id_category=cats[-1][1]
                    ))

                    cats.reverse()

                    for i in range(len(cats)):
                        categories.append(Category(
                            id_category=cats[i][1],
                            name=cats[i][0],
                            id_super_category=cats[i + 1][1] if i + 1 < len(cats) else None
                        ))

                unique_values = {}

                for cat in categories:
                    unique_values[cat.id_category] = cat

                categories = list(unique_values.values())

                if reviews_product:
                    reviews_product = reviews_product.split('\n')
                    reviews_product = list(filter(lambda x: x, reviews_product))
                    reviews_product = list(map(lambda x: x.strip(), reviews_product))
                else:
                    reviews_product = []

                reviews = []
                customers = []

                for review in reviews_product:
                    review_pattern = re.compile(
                        r'^(\d+-\d+-\d+)\s*cutomer:\s*(\w+)\s*rating:\s*(\d+)\s*votes:\s*(\d+)\s*helpful:\s*(\d+)$')
                    m = review_pattern.match(review)
                    review_date = datetime.strptime(m.group(1), "%Y-%m-%d")
                    customer_id = m.group(2)
                    rating = int(m.group(3))
                    votes = int(m.group(4))
                    helpful = int(m.group(5))

                    customers.append(Customer(id_customer=customer_id))

                    reviews.append(Review(
                        id_review=uuid.uuid4().hex,
                        id_product=id_product,
                        id_customer=customer_id,
                        dt_review=review_date,
                        rating=rating,
                        qtd_votes=votes,
                        qtd_helpful_votes=helpful,
                    ))

                similar_products = []

                if similar_products_asin:
                    similar_products_asin = similar_products_asin.split(' ')
                    similar_products_asin = list(filter(lambda x: x, similar_products_asin))
                else:
                    similar_products_asin = []

                i = 1
                for sim_prod in similar_products_asin:
                    similar_products.append(SimilarProducts(
                        id_product=id_product,
                        id_similar_product=sim_prod,
                        rank=i
                    ))
                    i+=1

                list_data['products'].append(product)
                list_data['groups'].append(group) if group else None
                list_data['categories'].extend(categories)
                list_data['reviews'].extend(reviews)
                list_data['similar_products'].extend(similar_products)
                list_data['customers'].extend(customers)
                list_data['product_categories'].extend(product_categories)
            else:
                print(block)
                raise Exception("Erro aqui")

        # Definir o índice onde parou
        list_data['stop'] = -1 if end_idx >= len(self.total_blocks) else end_idx

        return list_data

    @staticmethod
    def parse_data(lines: list[str]) -> Product:
        id_pattern = re.compile(r'^Id:\s*(\d+)$')
        asin_pattern = re.compile(r'^ASIN:\s*(\w+)$')
        title_pattern = re.compile(r'^ {2}title:\s*(.+)$')
        group_pattern = re.compile(r'^ {2}group:\s*(.+)$')
        sales_rank_pattern = re.compile(r'^ {2}salesrank:\s*(\d+)$')
        category_pattern = re.compile(r'^ {2}categories:\s*(.+)$')
        review_pattern = re.compile(r'^ {2}reviews:\s*(.+)$')
        similar_pattern = re.compile(r'^ {2}similar:\s*(.+)$')

        # Modelo de Product para setar as variáveis
        product = Product(
            id_product="",
            asin="",
        )

        current_line = 0

        while current_line < len(lines):
            line = lines[current_line]
            current_line += 1

            if match := id_pattern.match(line):
                product_id = match.group(1)
                product.id_product = product_id
                continue

            if match := asin_pattern.match(line):
                product_asin = match.group(1)
                product.asin = product_asin
                continue

            if match := title_pattern.match(line):
                product_title = match.group(1)
                product.title = product_title
                continue

            if match := group_pattern.match(line):
                product_group = match.group(1)
                product.group = Group(name=product_group)
                continue

            if match := sales_rank_pattern.match(line):
                product_sales_rank = match.group(1)
                product.salesrank = int(product_sales_rank)
                continue

            if match := category_pattern.match(line):
                product_category = match.group(1)
                # print(f"Product Category: {product_category}")
                # Precisar de ajuda com regex, eu uso esse site: https://regexr.com/
                # Mas talvez o jeito mais fácil seja fazer com IA.

                # Um for aqui para cada categoria, salvar dentro de produto.categories

                # Ponto importante a considerar:
                # Como pode ver, em product.categories, tem uma lista de categorias
                # em que cada categoria tem um categoria.super_category, que por sua
                # vez é uma categoria.

                # Acho q vai ficar melhor, ao invés de usar uma matriz, fazer uma lista
                # de árvores de categoria.

                n = int(product_category)
                product_categories = []

                while n > 0:
                    category_line = lines[current_line]
                    current_line += 1

                    categories = [x for x in category_line.strip().split('|') if x]
                    category_inner_pattern = re.compile(r'^(.*)\[(.*)]$')

                    # print("-"*30)
                    # print("Linha completa:", category_line.strip())
                    list_categories = []

                    for category in categories:
                        category_name = category_inner_pattern.match(category).group(1)
                        category_id = category_inner_pattern.match(category).group(2)
                        list_categories.append((category_id, category_name))

                    # print(list_categories) # Pega essa lista e faz uma árvore
                    temp = None
                    primeiro = None
                    for id_, name in list_categories[::-1]:
                        cat = Category(name=name, id_category=id_)
                        if primeiro is None:
                            primeiro = cat
                        if temp:
                            temp.super_category = cat
                        temp = cat

                    product_categories.append(primeiro)
                    # print("-"*30)

                    n -= 1
                product.categories = product_categories
                continue

            if match := review_pattern.match(line):

                # Aqui deve ser ok de fazer, quase a mesma lógica do de cima

                product_review = match.group(1)

                # print(f"Product Review: {product_review}")

                total_pattern = re.compile(r".*total:\s*(\d*)")
                downloaded_pattern = re.compile(r".*downloaded:\s*(\d*)")
                avg_rating_pattern = re.compile(r".*avg rating:\s*(\d*.?\d*)")

                total = int(total_pattern.match(product_review).group(1))
                downloaded = int(downloaded_pattern.match(product_review).group(1))
                avg_rating = float(avg_rating_pattern.match(product_review).group(1))

                product.total = total
                product.avg_rating = avg_rating

                # print(total)
                # print(downloaded)
                # print(avg_rating)

                review_line_pattern = re.compile(
                    r"^\s*(\d+-\d+-\d+)\s*cutomer:\s*(\w+)\s*rating:\s*(\d+)\s*votes:\s*(\d+)\s*helpful:\s*(\d+)$")

                for _ in range(downloaded):
                    review_line = lines[current_line]
                    current_line += 1
                    # print("-"*30)
                    # print(review_line)

                    m = review_line_pattern.match(review_line)

                    review_date = datetime.strptime(m.group(1), "%Y-%m-%d")
                    customer_id = m.group(2)
                    rating = int(m.group(3))
                    votes = int(m.group(4))
                    helpful = int(m.group(5))

                    review = Review(
                        customer=Customer(id_customer=customer_id),
                        dt_review=review_date,
                        rating=rating,
                        qtd_votes=votes,
                        qtd_helpful_votes=helpful,
                    )
                    # print("-"*30)

                    product.reviews.append(review)

                continue

            if match := similar_pattern.match(line):
                # Aqui é só fazer um split e colocar dentro de produto, tbm acho q é simples

                product_similar = match.group(1)
                # print(f"Product Similar: {product_similar}")

                list_similar = re.split(r"\s+", product_similar)
                list_similar.pop(0)

                # print(list_similar)

                product.similarProducts = list(map(
                    lambda x: SimilarProduct(id_similar_product=x),
                    list_similar,
                ))

                continue

        return product

    def parse_n_products(self, n: int = 5, start_from: int = 3, show_logs: bool = False) -> tuple[list[Product], int]:
        """
        Faz o parsing de N produtos do arquivo de dados da Amazon.

        Args:
            n (int, optional): Quantidade de produtos para fazer o parsing. Padrão é 5.
            start_from (int, optional): Quantidade de produtos para pular antes de começar o parsing. Padrão é 0.
            show_logs (bool, optional): Se True, exibe logs durante o processo de parsing. Padrão é False.
        Returns:
            list[Product]: Lista contendo os N produtos parseados do arquivo.
        """

        if start_from is None:
            start_from = 3

        def print_m(message: str):
            if show_logs:
                print(message)

        cur_line = start_from

        lines, end_line = self.get_data(cur_line)

        qtd_parsed = 1

        products = []

        for _ in range(n):
            if not lines:
                return products, -1

            product = self.parse_data(lines)
            products.append(product)
            print_m(f"Parsing nº {qtd_parsed}")
            qtd_parsed += 1
            print_m("-" * 30)
            cur_line = end_line + 1
            lines, end_line = self.get_data(cur_line)

        return products, cur_line