# ICC205_Trabalho_Pratico_1_IBD

# Objetivo
Objetivo deste trabalho prático é projetar e implementar um banco de dados sobre produtos vendidos em uma loja de comércio eletrônico, incluindo avaliações e comentários de usuários sobre estes produtos.

# Requisitos Iniciais
- docker-compose
- python

# Como rodar
1. Preencha as variáveis de ambiente em `.env` como especificado em `.env.example`
2. Execute o comando:
   ```
   docker compose up
   ```
3. Crie e ative um ambiente virtual Python:
   ```
   python -m venv .venv
   source .venv/bin/activate  # ou .venv\Scripts\activate no Windows
   ```
4. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
5. Teste a conexão com o banco de dados:
   ```
   python src/check_connection.py
   ```