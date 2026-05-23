import os
import re
from flask import Flask, render_template, request
from PIL import Image
import pytesseract
from deep_translator import GoogleTranslator

app = Flask(__name__)

PASTA_UPLOAD = "static"

# Função auxiliar para pegar a lista de imagens salvas no histórico
def pegar_historico():
    if not os.path.exists(PASTA_UPLOAD):
        os.makedirs(PASTA_UPLOAD)
    # Pega apenas arquivos que sejam imagens (png, jpg, jpeg)
    arquivos = os.listdir(PASTA_UPLOAD)
    imagens = [arq for arq in arquivos if arq.lower().endswith(('.png', '.jpg', '.jpeg'))]
    return imagens

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        foto = request.files.get("arquivo_cardapio")
        
        if foto:
            nome_da_foto = foto.filename
            caminho_para_salvar = os.path.join(PASTA_UPLOAD, nome_da_foto)
            foto.save(caminho_para_salvar)
            
            imagem_aberta = Image.open(caminho_para_salvar)
            texto_extraido = pytesseract.image_to_string(imagem_aberta, lang="por+eng+rus")
            
            linhas_do_cardapio = texto_extraido.split("\n")
            cardapio_final = []
            
            for table_line in linhas_do_cardapio:
                linha_limpa = table_line.strip()
                
                if len(linha_limpa) < 2 or not any(c.isalnum() for c in linha_limpa):
                    continue
                
                eh_so_preco = re.match(r'^([\d.,\s]+(?:[a-zA-Zа-яА-ЯёЁ$€₽Рр]|руб|руб\.)?)$', linha_limpa)
                
                if eh_so_preco:
                    valor = eh_so_preco.group(0).strip()
                    cardapio_final.append({
                        "original": linha_limpa, 
                        "traduzido": f"<span style='background-color: #d35400; padding: 3px 8px; border-radius: 4px; color: white; font-size: 0.9em;'>💰 VALOR: {valor}</span>"
                    })
                else:
                    match_preco = re.search(r'([\d.,\s]+(?:[a-zA-Zа-яА-ЯёЁ$€₽Рр]|руб|руб\.)?)$', linha_limpa)
                    prato_original = linha_limpa
                    preco_detectado = ""
                    
                    if match_preco:
                        preco_detectado = match_preco.group(0).strip()
                        prato_original = linha_limpa[:match_preco.start()].strip()
                        prato_original = re.sub(r'[.\-_]{2,}', '', prato_original).strip()
                    
                    if prato_original:
                        try:
                            traducao_prato = GoogleTranslator(source='auto', target='pt').translate(prato_original)
                            if preco_detectado:
                                traducao_final = f"{traducao_prato} ➔ <span style='color: #ff9900;'>{preco_detectado}</span>"
                            else:
                                traducao_final = traducao_prato
                            cardapio_final.append({"original": linha_limpa, "traduzido": traducao_final})
                        except:
                            cardapio_final.append({"original": linha_limpa, "traduzido": linha_limpa})
            
            linhas_tabela = ""
            for item in cardapio_final:
                linhas_tabela += f"""
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #444; color: #aaa;">{item['original']}</td>
                    <td style="padding: 10px; border-bottom: 1px solid #444; color: #00ff00; font-weight: bold;">{item['traduzido']}</td>
                </tr>
                """
            
            return f"""
            <body style="background-color: #121212; color: white; font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 20px;">
                <h1>Menu Translator - Modo Estruturado 🍽️</h1>
                <p>Nomes traduzidos e valores avulsos organizados:</p>
                
                <table style="width: 100%; border-collapse: collapse; background-color: #1e1e1e; border-radius: 8px; overflow: hidden;">
                    <thead style="background-color: #333;">
                        <tr>
                            <th style="padding: 12px; text-align: left;">Cardápio Original</th>
                            <th style="padding: 12px; text-align: left;">Tradução / Preço Organizado</th>
                        </tr>
                    </thead>
                    <tbody>
                        {linhas_tabela}
                    </tbody>
                </table>
                
                <br><br>
                <a href="/" style="color: #3498db; text-decoration: none; font-weight: bold;">← Traduzir outro cardápio</a>
            </body>
            """
            
    # MÁGICA NOVA DO GET: Pegamos o histórico e mandamos para o HTML renderizar
    lista_historico = pegar_historico()
    return render_template("index.html", historico=lista_historico)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")