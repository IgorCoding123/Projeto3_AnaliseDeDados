import duckdb
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os

def run_analysis():
    DATA_PATH = 'archive/2019-Oct.csv'
    
    print(f"--- 1. Carregando dados REAIS ({DATA_PATH}) ---")
    print("Isso pode levar alguns segundos devido ao tamanho do arquivo (5GB+)...")
    
    # Connect to DuckDB
    con = duckdb.connect(database=':memory:')
    
    funnel_query = f"""
    WITH funnel_counts AS (
        SELECT
            COUNT(DISTINCT user_id) FILTER (WHERE event_type = 'view') AS views,
            COUNT(DISTINCT user_id) FILTER (WHERE event_type = 'cart') AS carts,
            COUNT(DISTINCT user_id) FILTER (WHERE event_type = 'purchase') AS purchases
        FROM '{DATA_PATH}'
    )
    SELECT * FROM funnel_counts;
    """
    funnel_data = con.execute(funnel_query).df()
    
    # Plotly Funnel
    stages = ["Visualizou Produto", "Adicionou ao Carrinho", "Finalizou Compra"]
    values = [funnel_data['views'][0], funnel_data['carts'][0], funnel_data['purchases'][0]]
    
    fig = go.Figure(go.Funnel(
        y = stages,
        x = values,
        textinfo = "value+percent initial",
        marker = {"color": ["#636EFA", "#EF553B", "#00CC96"]}
    ))
    
    fig.update_layout(title_text="Funil de Comportamento do Usuário", template="plotly_dark")
    fig.write_html("funil_conversao.html")
    print("[OK] Grafico de Funil gerado: funil_conversao.html")

    print("\n--- 2. Identificando Gargalos ---")
    # Drop-off rate calculation
    drop_off_cart = 100 - (funnel_data['purchases'][0] / funnel_data['carts'][0] * 100)
    print(f"ALERTA DE GARGALO: {drop_off_cart:.2f}% dos usuarios que adicionam ao carrinho NAO finalizam a compra.")

    print("\n--- 3. Análise por Marca (Top 5 Receita) ---")
    brand_query = f"""
    SELECT
        brand,
        SUM(price) AS receita
    FROM '{DATA_PATH}'
    WHERE event_type = 'purchase'
    GROUP BY brand
    ORDER BY receita DESC
    LIMIT 5;
    """
    brand_df = con.execute(brand_query).df()
    print(brand_df)

    # Performance por Categoria
    cat_query = f"""
    SELECT
        category_code,
        COUNT(*) FILTER (WHERE event_type = 'view') as views,
        COUNT(*) FILTER (WHERE event_type = 'purchase') as sales,
        (sales * 100.0 / views) as conv_rate
    FROM '{DATA_PATH}'
    WHERE category_code IS NOT NULL
    GROUP BY category_code
    ORDER BY conv_rate DESC
    LIMIT 15;
    """
    cat_df = con.execute(cat_query).df()
    
    fig_cat = px.bar(cat_df, x='category_code', y='conv_rate', 
                     title="Taxa de Conversão por Categoria",
                     labels={'conv_rate': 'Taxa de Conversão (%)'},
                     template="plotly_dark",
                     color='conv_rate',
                     color_continuous_scale='Viridis')
    fig_cat.write_html("conversao_categoria.html")
    print("[OK] Grafico de Categorias gerado: conversao_categoria.html")

if __name__ == "__main__":
    if not os.path.exists('data/events.csv'):
        print("Erro: data/events.csv não encontrado. Execute src/generate_data.py primeiro.")
    else:
        run_analysis()
