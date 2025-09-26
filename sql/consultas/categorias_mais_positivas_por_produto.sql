-- Consulta 6
-- Listar as 5 categorias com maior média de rating (somente das avaliações úteis e positivas)
-- foi definido avaliação útil e positiva como rating>=4 e helpful>=1
SELECT
    c.ID_CATEGORY,
    c.NAME AS nome_categoria,
    AVG(r.RATING) AS media_avaliacoes_uteis_positivas,
    COUNT(*) AS total_reviews_uteis_positivas
FROM Category c
JOIN Product_Category pc
      ON pc.ID_CATEGORY = c.ID_CATEGORY
JOIN Review r
      ON r.ID_PRODUCT = pc.ID_PRODUCT
WHERE r.RATING >= 4
  AND r.QTD_HELPFUL_VOTES >= 1
GROUP BY c.ID_CATEGORY, c.NAME
ORDER BY media_avaliacoes_uteis_positivas DESC
LIMIT 5;