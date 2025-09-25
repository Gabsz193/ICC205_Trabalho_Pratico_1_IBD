import re
from datetime import datetime

from parser.schema import Product, Group, Category, Review, Customer, SimilarProduct


class AmazonParser:
    """
    Parser para dados do Amazon

    Esta classe tem como objetivo prover todos os métodos necessários para
    manipular os dados do Amazon.
    """

    file_lines: list[str]
    caret_line: int = 0

    def __init__(self, input_filename: str):
        try:
            with open(input_filename, "r") as file:
                # Não demora muito, apesar do documento ter quase 1GB

                self.file_lines = file.readlines()
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

        return self.file_lines[start_line:current_line], current_line

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