-- Consulta 3
-- Dado um produto, mostrar a evolução diária das médias de rating
SELECT
    r.DT_REVIEW::date        AS dia,
    AVG(r.RATING)            AS media_avaliacao,
    COUNT(*)                 AS total_reviews
FROM Review r
INNER JOIN Product p ON p.ID_PRODUCT = r.ID_PRODUCT
WHERE p.ASIN = :asin_product
GROUP BY r.DT_REVIEW::date
ORDER BY dia;