import requests
import os

def download_data():
    # URL de um sample real do dataset "eCommerce Behavior Data from Multi-Category Store"
    url = "https://raw.githubusercontent.com/andypwyu/eCommerce-behavior/master/data/2019-Oct-sample.csv"
    
    # Backup: Caso o de cima falhe, tenta este (Online Retail Sample)
    fallback_url = "https://raw.githubusercontent.com/amankharwal/Website-data/master/ecommerce_data.csv"
    
    print(f"Tentando baixar dados reais de: {url}...")
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            print(f"Primeira URL falhou ({response.status_code}). Tentando fallback...")
            response = requests.get(fallback_url, timeout=15)
        
        response.raise_for_status()
        
        os.makedirs('data', exist_ok=True)
        
        with open('data/real_events.csv', 'wb') as f:
            f.write(response.content)
            
        print("✔ Sucesso! Arquivo salvo em: data/real_events.csv")
        
        # Mostrar o cabeçalho
        print("\nPrimeiras 5 linhas do arquivo real:")
        lines = response.text.splitlines()[:6]
        for line in lines:
            print(line)
            
    except Exception as e:
        print(f"Erro crítico ao baixar dados: {e}")

if __name__ == "__main__":
    download_data()
