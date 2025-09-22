import re

from schema import Product, Group


class AmazonParser:
    """
    Parser para dados do Amazon

    Esta classe tem como objetivo prover todos os métodos necessários para
    manipular os dados do Amazon.
    """

    file_lines: list[str]
    caret_line: int = 0

    def __init__(self, input_filename : str):
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

    def get_data(self, start_line : int) -> tuple[list[str], int]:
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

        if not start_pattern.match(self.file_lines[start_line]):
            raise ValueError("Linha de início inválida")

        while self.file_lines[current_line].strip() != "":
            current_line += 1

        return self.file_lines[start_line:current_line], current_line

    @staticmethod
    def parse_data(lines: list[str]):
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

        for line in lines:
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
                print(f"Product Group: {product.group}")
                continue

            if match := sales_rank_pattern.match(line):
                product_sales_rank = match.group(1)
                product.salesrank = product_sales_rank
                print(f"Product Sales Rank: {product_sales_rank}")
                continue

            if match := category_pattern.match(line):
                product_category = match.group(1)
                print(f"Product Category: {product_category}")
                continue

            if match := review_pattern.match(line):
                product_review = match.group(1)
                print(f"Product Review: {product_review}")
                continue

            if match := similar_pattern.match(line):
                product_similar = match.group(1)
                print(f"Product Similar: {product_similar}")
                continue

        print(product)
        print(lines)


parser = AmazonParser("data/amazon-meta.txt")

cur_line = 7

lines = parser.get_data(cur_line)[0]

parser.parse_data(lines)