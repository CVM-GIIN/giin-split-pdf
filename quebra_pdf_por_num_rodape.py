import os
import re

from PyPDF2 import PdfReader, PdfWriter

pasta_le = "C:/Users/milcent/cvm.gov.br/SPS - General/Demandas GIIN/GPS-2/Americanas/Docs/RJ"
arquivo_orig = "0803087-20.2023.8.19.0001 (parte 2).pdf"
caminho_le = os.path.join(pasta_le, arquivo_orig)

pasta_grava = os.path.join(pasta_le, "Parte 2")
if not os.path.exists(pasta_grava):
    os.mkdir(pasta_grava)

prefixo_grava = "".join(arquivo_orig.split(".")[:-1])

# Padrão Regex do rodapé de docs do processo (Ex: 'Num. 42643258 - Pág. 14')
num_rodape = re.compile(r"Num. \d{8} \- Pág. \d*")

reader = PdfReader(caminho_le)
writer = PdfWriter()

pags_geral = 1
doc = "índice"
for page in reader.pages:
    text = page.extract_text()
    # Procura pelo padrão no texto
    rod = re.search(num_rodape, text)
    # Se houver o padrão, extrai o número do doc; se não, é o índice
    doc_1 = re.search(r"\d{8}", rod[0])[0] if rod is not None else "índice"
    # Caso mude o número 
    if doc_1 != doc:
        print(f"Início de novo Documento {doc_1} na página {pags_geral}")
        # Grava o que já está acumulado no writer
        with open(
            os.path.join(
                pasta_grava, f"{prefixo_grava}_doc_{doc}.pdf"),
                "wb") as arquivo_doc:
            writer.write(arquivo_doc)
        # Atribui o número à variável de checagem e instancia um novo writer
        doc = doc_1
        writer = PdfWriter()
        writer.add_page(page)
    else:
        writer.add_page(page)
    pags_geral += 1
# Grava o último documento após o fim do loop
with open(os.path.join(
            pasta_grava, f"{prefixo_grava}_doc_{doc}.pdf")
            ,"wb") as arquivo_doc:
    writer.write(arquivo_doc)
