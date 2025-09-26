-- Consulta 4
-- Listar os 10 produtos líderes de vendas em cada grupo

SELECT
    g.name       AS nome_grupo,
    ranked.id_product,
    ranked.title,
    ranked.salesrank,
    ranked.posicao
FROM (
    SELECT
        p.id_group,
        p.id_product,
        p.title,
        p.salesrank,
        ROW_NUMBER() OVER (
            PARTITION BY p.id_group
            ORDER BY p.salesrank ASC
        ) AS posicao
    FROM Product p
    WHERE p.salesrank IS NOT NULL
) AS ranked
JOIN GROUPS g ON g.id_group = ranked.id_group
WHERE ranked.posicao <= 10
ORDER BY g.name, ranked.posicao;