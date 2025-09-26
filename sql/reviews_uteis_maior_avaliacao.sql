-- Consulta 1, parte 1
-- Dado um produto, 5 comentários mais úteis e com maior avaliação (prioridade para rating)
SELECT
    r.ID_REVIEW,
    r.ID_CUSTOMER,
    r.RATING,
    r.QTD_HELPFUL_VOTES,
    r.QTD_VOTES,
    r.DT_REVIEW
FROM Review r
WHERE r.ID_PRODUCT = :id_produto
ORDER BY r.RATING DESC,
         r.QTD_HELPFUL_VOTES DESC,
         r.QTD_VOTES DESC
LIMIT 5;