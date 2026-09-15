import pdfplumber
import pandas as pd

caminho_pdf = "tabela_hoje.pdf"

dados_extraidos = []
categoria_atual = "DESCONHECIDA"

categorias_conhecidas = [
    "FRANGOS", "SUÍNOS", "SALGADOS", "RESFRIADOS", "CONGELADOS", 
    "CORDEIRO", "BATATAS", "FRIOS E", "LATICÍNIOS", "ULTRACONGELADOS", 
    "PESCADOS", "EMBUTIDOS"
]

# Leitura por Linhas

with pdfplumber.open(caminho_pdf) as pdf:
    for pagina in pdf.pages:
        linhas_texto = pagina.extract_text().split('\n')
        
        for linha in linhas_texto:
            linha_limpa = linha.strip().upper()
            
            # Rastreador de Categoria
            for cat in categorias_conhecidas:
                if cat in linha_limpa:
                    categoria_atual = cat
            
            if linha_limpa and linha_limpa[0].isdigit() and " R$ " in linha_limpa:
                try:
                   
                    esquerda, direita = linha_limpa.split(" R$ ")
                    
                    
                    partes_esquerda = esquerda.split(" ", 1)
                    codigo = partes_esquerda[0]
                    produto_marca = partes_esquerda[1] # Nome e marca ficaram juntos, o que é ótimo
                    
                  
                    partes_direita = direita.split()
                    preco = partes_direita[0]
                    estoque = partes_direita[-2] # Pega o penúltimo item da linha (o estoque)
                    
                    dados_extraidos.append({
                        "CODIGO": codigo,
                        "PRODUTO": produto_marca,
                        "PRECO": preco,
                        "ESTOQUE": estoque,
                        "CATEGORIA": categoria_atual
                    })
                except Exception as e:
                    continue 


df = pd.DataFrame(dados_extraidos)

df['ESTOQUE'] = pd.to_numeric(df['ESTOQUE'], errors='coerce')
df = df.dropna(subset=['ESTOQUE'])
df['ESTOQUE'] = df['ESTOQUE'].astype(int)

df['PRECO_NUM'] = df['PRECO'].str.replace('.', '', regex=False) 
df['PRECO_NUM'] = df['PRECO_NUM'].str.replace(',', '.', regex=False) 
df['PRECO_NUM'] = pd.to_numeric(df['PRECO_NUM'], errors='coerce')

df['PRODUTO'] = df['PRODUTO'].str.replace("S/N", "SEM NOIX", case=False)
df['PRODUTO'] = df['PRODUTO'].str.replace("S/C", "SEM CORDÃO", case=False)


df = df[df['ESTOQUE'] > 15]

df = df[df['CATEGORIA'] != 'ULTRACONGELADOS']

categorias_alvo = ["FRANGOS", "SUÍNOS", "PESCADOS"]
df['PRODUTO_BASE'] = df['PRODUTO'].apply(lambda x: " ".join(str(x).split()[:3]))

df_alvos = df[df['CATEGORIA'].isin(categorias_alvo)]
df_outros = df[~df['CATEGORIA'].isin(categorias_alvo)]

df_alvos = df_alvos.sort_values(by='PRECO_NUM', ascending=True)
df_alvos = df_alvos.drop_duplicates(subset=['CATEGORIA', 'PRODUTO_BASE'], keep='first')

df_final = pd.concat([df_outros, df_alvos])
df_final = df_final.sort_values(by=['CATEGORIA', 'PRODUTO'])

texto_whatsapp = "🥩 *TABELA DE CORTES ATUALIZADA* 🥩\n"
categoria_print = ""

for index, linha in df_final.iterrows():
    if linha['CATEGORIA'] != categoria_print:
        categoria_print = linha['CATEGORIA']
        texto_whatsapp += f"\n📦 *{categoria_print}*\n"

    produto = str(linha['PRODUTO']).title()
    preco = str(linha['PRECO']).strip()
    estoque = linha['ESTOQUE']
    
    texto_whatsapp += f"🔸 {produto}: R$ {preco} (Est: {estoque})\n"

print(texto_whatsapp)