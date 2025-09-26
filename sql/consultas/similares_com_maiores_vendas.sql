-- Consulta 2
-- Dado um produto, listar similares com maior salesrank que ele
SELECT
    sp.ID_SIMILAR_PRODUCT,
    p_sim.ID_PRODUCT      AS ID_PRODUTO_SIMILAR,
    p_sim.TITLE           AS TITULO_SIMILAR,
    p_sim.SALESRANK       AS SALESRANK_SIMILAR,
    p_base.SALESRANK      AS SALESRANK_BASE
FROM Product p_base
JOIN Similar_Products sp
       ON sp.ID_PRODUCT = p_base.ASIN
JOIN Product p_sim
       ON p_sim.ASIN = sp.ID_SIMILAR_PRODUCT
WHERE p_base.ASIN = :asin_product
  AND p_sim.SALESRANK < p_base.SALESRANK
ORDER BY p_sim.SALESRANK ASC;