# 🥩 Automação de Catálogo Comercial (PDF para WhatsApp)

Este projeto é uma ferramenta de automação em Python desenvolvida para otimizar rotinas comerciais e de gestão de pedidos. O script extrai dados de um catálogo em PDF, aplica regras de negócio focadas em controle de estoque e precificação, e gera uma tabela limpa e formatada, pronta para envio rápido aos clientes via WhatsApp.

#Funcionalidades

* **Extração de Texto Estruturado:** Leitura linha a linha de PDFs com layout visual limpo (sem grades de tabela), utilizando fatiamento de strings.
* **Limpeza e Estruturação de Dados:** Tipagem e conversão de valores financeiros para cálculos matemáticos utilizando `pandas`.
* **Motor de Regras de Negócio:**
  * **Filtro de Estoque:** Descarta automaticamente produtos com 15 unidades ou menos.
  * **Exclusão de Categorias:** Ignora blocos inteiros do catálogo (ex: "Ultracongelados").
  * **Seleção de Melhor Preço:** Agrupa cortes de marcas variadas (Frangos, Suínos e Pescados) e mantém na lista final apenas a opção mais barata disponível.
  * **Padronização:** Tradução de siglas técnicas comerciais (ex: "S/N" substituído por "Sem noix").
* **Execução Ágil:** Acompanha um atalho `.bat` para execução local em apenas dois cliques, sem necessidade de navegar pelo terminal.

## 🛠️ Tecnologias Utilizadas

* **Python 3**
* **Pandas:** Para manipulação de DataFrames, filtragem condicional e remoção de duplicatas.
* **pdfplumber:** Para leitura e processamento robusto do texto do documento original.

## ⚙️ Como Utilizar no Dia a Dia

1. Clone o repositório em sua máquina local.
2. Instale as bibliotecas necessárias executando o comando: `pip install pandas pdfplumber`
3. Salve o catálogo atualizado do dia na pasta do projeto com o nome exato: `tabela_hoje.pdf`
4. Dê um duplo clique no arquivo `Gerar_tabela.bat`.
5. Copie o resultado gerado no terminal e envie aos clientes!
