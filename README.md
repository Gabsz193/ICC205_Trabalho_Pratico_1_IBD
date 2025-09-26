# ICC205_Trabalho_Pratico_1_IBD

# Objetivo
Objetivo deste trabalho prático é projetar e implementar um banco de dados sobre produtos vendidos em uma loja de comércio eletrônico, incluindo avaliações e comentários de usuários sobre estes produtos. 

# Requisitos Iniciais
- docker-compose
- python

# Como rodar
1. Preencha as variáveis de ambiente em `.env` como especificado em `.env.example`.
2. Primeiramente, coloque o `amazon-meta.txt` na pasta `/data` Execute o comando:
   ```
   docker compose up -d
   ```
3. Para ver o comando --help da aplicação, execute
   ```
   docker compose run app
    ```
4. Para crias as tabelas e povoar o banco de dados, primeiramente:
    ```
    docker compose run --rm app python src/tp1_3.2.py --input /data/amazon-meta.txt
   ```
5. Para gerar as tabelas do dashboard, execute o comando:
    ```
   docker compose run --rm app python src/tp1_3.3.py --output out
   ```