-- Consulta 7
-- Listar os 10 clientes que mais fizeram comentários por grupo
SELECT
    ranked.id_group,
    g.name         AS nome_grupo,
    ranked.id_customer,
    ranked.total_reviews,
    ranked.posicao
FROM (
    SELECT
        p.id_group,
        r.id_customer,
        COUNT(*) AS total_reviews,
        ROW_NUMBER() OVER (
            PARTITION BY p.id_group
            ORDER BY COUNT(*) DESC
        ) AS posicao
    FROM Review r
    JOIN Product p ON p.id_product = r.id_product
    GROUP BY p.id_group, r.id_customer
) AS ranked
JOIN GROUPS g ON g.id_group = ranked.id_group
WHERE ranked.posicao <= 10
ORDER BY ranked.id_group, ranked.posicao;