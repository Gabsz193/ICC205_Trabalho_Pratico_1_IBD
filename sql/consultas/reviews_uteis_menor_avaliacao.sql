-- Consulta 1, parte 2
-- Dado um produto, 5 comentários mais úteis e com maior avaliação (prioridade para rating)
SELECT
    r.ID_REVIEW,
    r.ID_CUSTOMER,
    r.RATING,
    r.QTD_HELPFUL_VOTES,
    r.QTD_VOTES,
    r.DT_REVIEW
FROM Review r
INNER JOIN Product p ON p.ID_PRODUCT = r.ID_PRODUCT
WHERE p.ASIN = :asin_product
ORDER BY r.RATING ASC,
         r.QTD_HELPFUL_VOTES DESC,
         r.QTD_VOTES DESC
LIMIT 5;