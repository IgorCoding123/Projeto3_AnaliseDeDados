-- 1. Funil de Conversão (Visit -> Cart -> Purchase)
-- Calcula quantos usuários únicos passaram por cada etapa
WITH funnel_counts AS (
    SELECT
        COUNT(DISTINCT user_id) FILTER (WHERE event_type = 'view') AS total_views,
        COUNT(DISTINCT user_id) FILTER (WHERE event_type = 'cart') AS total_carts,
        COUNT(DISTINCT user_id) FILTER (WHERE event_type = 'purchase') AS total_purchases
    FROM 'data/events.csv'
)
SELECT
    total_views AS "Viram Produtos",
    total_carts AS "Adicionaram ao Carrinho",
    total_purchases AS "Compraram",
    ROUND(total_carts * 100.0 / total_views, 2) || '%' AS "Taxa Visualização -> Carrinho",
    ROUND(total_purchases * 100.0 / total_carts, 2) || '%' AS "Taxa Carrinho -> Compra (Gargalo)",
    ROUND(total_purchases * 100.0 / total_views, 2) || '%' AS "Conversão Geral"
FROM funnel_counts;

-- 2. Onde os usuários desistem? (Drop-off por Categoria)
SELECT
    category_code,
    COUNT(DISTINCT user_id) FILTER (WHERE event_type = 'cart') AS cart_users,
    COUNT(DISTINCT user_id) FILTER (WHERE event_type = 'purchase') AS purchase_users,
    ROUND((1 - (COUNT(DISTINCT user_id) FILTER (WHERE event_type = 'purchase') * 1.0 / 
           NULLIF(COUNT(DISTINCT user_id) FILTER (WHERE event_type = 'cart'), 0))) * 100, 2) || '%' AS drop_off_rate
FROM 'data/events.csv'
GROUP BY category_code
ORDER BY drop_off_rate DESC;

-- 3. Tempo Médio até a Compra
-- Compara o primeiro 'view' da sessão com a primeira 'purchase' da mesma sessão
WITH session_times AS (
    SELECT
        user_session,
        MIN(event_time) FILTER (WHERE event_type = 'view') AS start_time,
        MIN(event_time) FILTER (WHERE event_type = 'purchase') AS purchase_time
    FROM 'data/events.csv'
    GROUP BY user_session
    HAVING purchase_time IS NOT NULL
)
SELECT
    AVG(purchase_time - start_time) AS tempo_medio_ate_compra
FROM session_times;

-- 4. Métricas de Produto (Ticket Médio e Receita por Marca)
SELECT
    brand,
    COUNT(*) FILTER (WHERE event_type = 'purchase') AS items_sold,
    SUM(price) FILTER (WHERE event_type = 'purchase') AS total_revenue,
    AVG(price) FILTER (WHERE event_type = 'purchase') AS avg_ticket
FROM 'data/events.csv'
GROUP BY brand
ORDER BY total_revenue DESC
LIMIT 10;
