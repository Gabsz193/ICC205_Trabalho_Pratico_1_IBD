-- Consulta 5
-- Listar os 10 produtos com a maior média de rating (somente as úteis e positivas)
-- foi definido avaliação útil e positiva como rating>=4 e helpful>=1
SELECT
    p.ID_PRODUCT,
    p.TITLE,
    AVG(r.RATING) AS media_avaliacao_uteis_positivas,
    COUNT(*) AS total_reviews_uteis_positivas
FROM Product p
JOIN Review r
      ON r.ID_PRODUCT = p.ID_PRODUCT
WHERE r.RATING >= 4
  AND r.QTD_HELPFUL_VOTES >= 1
GROUP BY p.ID_PRODUCT, p.TITLE
ORDER BY media_avaliacao_uteis_positivas DESC
LIMIT 10;