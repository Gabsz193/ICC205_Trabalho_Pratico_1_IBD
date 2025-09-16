import re

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


parser = AmazonParser("data/amazon-meta.txt")

actual_count = 0
cur_line = 3

while True:
    try:
        cur_line = parser.get_data(cur_line)[1] + 1
        print(f"Linha {actual_count} processada.")
        actual_count += 1
    except Exception:
        break

print(f"Quantidade total eh {parser.get_count()} mas documento tem realmente {actual_count}")