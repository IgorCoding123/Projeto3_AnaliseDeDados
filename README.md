# Projeto 3: Análise de Comportamento de Usuário (E-commerce) 🧾📈

Fala pessoal! Esse aqui é o meu terceiro projeto focado em análise de dados. 

O objetivo principal aqui foi entender o **comportamento dos usuários** dentro de um e-commerce gigante (usei um dataset real do Kaggle com milhões de eventos). Eu queria descobrir onde as pessoas mais desistem de comprar e quais marcas estão mandando bem em vendas.

### 🧠 O que eu usei e aprendi:
*   **SQL (Direct Query):** Usei o DuckDB para rodar queries SQL direto em arquivos CSV gigantes (5GB+) sem precisar subir um banco de dados inteiro. Foi animal ver a velocidade disso.
*   **Funil de Conversão:** Analisei o caminho completo: *Visualizou -> Adicionou ao Carrinho -> Comprou*. 
*   **Python + Plotly:** Criei gráficos interativos para visualizar os gargalos e a receita por marca.
*   **Data Cleaning:** Lidei com anomalias reais, como compras que acontecem sem o evento de 'cart' ser registrado.

### 🔍 Os Desafios
Trabalhar com 5GB de dados no meu computador não foi fácil no começo, mas o DuckDB salvou o dia. Identifiquei que em Outubro de 2019, a **Apple** teve um desempenho absurdo comparado às outras marcas.

### 📁 Estrutura:
*   `sql/`: Onde guardei as queries que usei para as análises mais pesadas.
*   `src/`: Meus scripts Python para processar os dados e gerar os gráficos.
*   `README.md`: Este guia aqui.

---
**Nota:** Os dados originais são pesados demais pro GitHub, então se você baixar o projeto, vai precisar dos arquivos `.csv` originais (ou usar o meu gerador de dados sintéticos que deixei na pasta `src`).

Bora pra cima! 🚀
