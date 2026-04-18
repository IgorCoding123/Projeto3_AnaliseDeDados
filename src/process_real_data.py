import pandas as pd
import numpy as np
import os

def process_data():
    print("--- Processando dados REAIS (UCI Online Retail) ---")
    
    # Carregar o arquivo Excel baixado
    try:
        df = pd.read_excel('data/real_data.xlsx', engine='openpyxl')
        print(f"Dataset carregado com {len(df)} linhas.")
    except Exception as e:
        print(f"Erro ao ler Excel: {e}")
        return

    # Limpar dados: Remover CustomerID nulos e Quantidade/Preço <= 0
    df = df.dropna(subset=['CustomerID'])
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
    
    # Criar eventos de Funil Sintéticos baseados nos dados REAIS
    # O dataset original só tem "Purchases". Vamos criar o comportamento prévio.
    
    events = []
    
    print("Simulando comportamento de navegação (View -> Cart -> Purchase)...")
    
    # Iterar por uma amostra (para performance)
    sample_df = df.sample(min(20000, len(df)), random_state=42)
    
    for _, row in sample_df.iterrows():
        user_id = int(row['CustomerID'])
        product_id = row['StockCode']
        price = row['UnitPrice']
        timestamp = row['InvoiceDate']
        session_id = f"sess_{user_id}_{timestamp.strftime('%Y%m%d')}"
        brand = "Unknown"
        category = "Retail"
        
        # 1. Todo mundo que comprou, visualizou (View)
        events.append([timestamp - pd.Timedelta(minutes=10), 'view', product_id, 1, category, brand, price, user_id, session_id])
        
        # 2. Todo mundo que comprou, adicionou ao carrinho (Cart)
        events.append([timestamp - pd.Timedelta(minutes=5), 'cart', product_id, 1, category, brand, price, user_id, session_id])
        
        # 3. A Compra Real
        events.append([timestamp, 'purchase', product_id, 1, category, brand, price, user_id, session_id])
        
    # Adicionar Drop-offs (Usuários que SÓ viram ou SÓ adicionaram ao carrinho)
    # Vamos adicionar 3000 sessions que desistiram
    print("Adicionando usuários que desistiram (Drop-offs)...")
    unique_users = df['CustomerID'].unique()
    
    for i in range(3000):
        uid = np.random.choice(unique_users)
        t = pd.Timestamp('2011-01-01') + pd.Timedelta(days=np.random.randint(0, 300))
        sid = f"abandon_{i}"
        
        # Só visualizou
        events.append([t, 'view', 'STOCK_X', 1, 'Retail', 'Brand_X', 10.0, uid, sid])
        
        # 50% chance de adicionar ao carrinho e desistir
        if np.random.random() < 0.5:
            events.append([t + pd.Timedelta(minutes=2), 'cart', 'STOCK_X', 1, 'Retail', 'Brand_X', 10.0, uid, sid])

    # Criar DataFrame final
    final_df = pd.DataFrame(events, columns=[
        'event_time', 'event_type', 'product_id', 'category_id', 
        'category_code', 'brand', 'price', 'user_id', 'user_session'
    ])
    
    final_df = final_df.sort_values('event_time')
    final_df.to_csv('data/events.csv', index=False)
    print(f"✔ Dataset REAIS + COMPORTAMENTAL gerado em data/events.csv ({len(final_df)} eventos).")

if __name__ == "__main__":
    process_data()
