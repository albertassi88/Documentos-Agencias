import json
from datetime import datetime, timedelta
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors

# =========================
# CONFIGURAÇÕES
# =========================


json_path = "arquivo.json"          # Caminho do JSON
imagem_path = "images/logo88.png"          # Caminho da imagem PNG
pdf_saida = "Declaração Artigo 299.pdf"      # Nome do PDF final
pdf_saida_anexo = "Declaração de Simples.pdf" # Nome do PDF final
imagem_rodape_path = "carimbos/88fm.png"

adicionar_assinatura = True  # ← CONTROLE CARIMBO


# ← CONTROLE DADOS DA RÁDIO

with open("json/radios.json", "r", encoding="utf-8") as f:
    radios = json.load(f)

radio_ativa = None

for radio in radios.values():
    if radio.get("ativa") == True:
        radio_ativa = radio
        break

if radio_ativa is None:
    raise ValueError("Nenhuma rádio ativa encontrada no radios.json")

# =========================
# REGISTRAR FONTES
# =========================

pdfmetrics.registerFont(TTFont("TimesNewRoman", "times.ttf"))
pdfmetrics.registerFont(TTFont("TimesNewRoman-Bold", "timesbd.ttf"))

# =========================
# LER JSON
# =========================

with open(json_path, "r", encoding="utf-8") as f:
    dados = json.load(f)

cliente = dados.get("cliente", "")
numero_pi = dados.get("numero_pi", "")

data_atual = datetime.now().strftime("%d/%m/%Y")

# =========================
# CRIAR PDF
# =========================

doc = SimpleDocTemplate(
    pdf_saida,
    pagesize=A4,
    rightMargin=72,
    leftMargin=72,
    topMargin=72,
    bottomMargin=72
)

# =========================
# ESTILOS PDF 1
# =========================

style_14 = ParagraphStyle(
    name="Times14",
    fontName="TimesNewRoman",
    fontSize=14,
    leading=18
)

style_14_bold = ParagraphStyle(
    name="Times14Bold",
    fontName="TimesNewRoman-Bold",
    fontSize=14,
    leading=18,
    alignment=1
)

style_12 = ParagraphStyle(
    name="Times11",
    fontName="TimesNewRoman",
    fontSize=11,
    leading=14,
    alignment=4
)

# =========================
# DADOS DA RÁDIO
# =========================

nome_radio = radio_ativa.get("nome_radio", "")
cnpj = radio_ativa.get("cnpj", "")
endereco = radio_ativa.get("endereco", "")

style_left = ParagraphStyle(
    name="left",
    fontName="TimesNewRoman",
    fontSize=11,
    leading=15,
)

elements = []

# =========================
# IMAGEM TOPO
# =========================

img_topo = Image(imagem_path, width=1.2 * inch, height=1.2 * inch)
elements.append(img_topo)
elements.append(Spacer(1, 40))

# =========================
# TEXTO
# =========================

elements.append(Paragraph(f"Volta Redonda/RJ, {data_atual}", style_14))
elements.append(Spacer(1, 40))

elements.append(Paragraph("ARTIGO 299 DO CÓDIGO PENAL BRASILEIRO.", style_14_bold))
elements.append(Spacer(1, 50))

elements.append(Paragraph(f"A {cliente}", style_14))
elements.append(Spacer(1, 25))

elements.append(Paragraph("A/C da Coordenação Geral de Processos de Pagamentos", style_14))
elements.append(Spacer(1, 40))

texto_declaracao = f"""
Declaramos, sob as penas do art. 299 do Código Penal Brasileiro, que esta empresa
RÁDIO ENERGIA LTDA-EPP, com sede Rua Moacyr de Paula Lobo, 104 – Vila Mury –
CEP 27283-350 – Volta Redonda - RJ, inscrita no CNPJ sob nº 31.232.747/0001-07,
prestou os serviços de publicidade objeto da PI nº {numero_pi},
mediante a(s) seguinte(s) veiculação(ões) descritas no comprovante em anexo.
"""

elements.append(Paragraph(texto_declaracao, style_12))
elements.append(Spacer(1, 60))

# =========================
# IMAGEM RODAPÉ (CONDICIONAL)
# =========================

if adicionar_assinatura:
    img_rodape = Image(imagem_rodape_path, width=4.8 * inch, height=2 * inch)
    elements.append(img_rodape)

# =========================
# GERAR PDF
# =========================

doc.build(elements)

# =========================
# PDF 2 - ANEXO IV
# =========================


doc2 = SimpleDocTemplate(
    pdf_saida_anexo,
    pagesize=A4,
    rightMargin=72,
    leftMargin=72,
    topMargin=50,
    bottomMargin=50
)

elements2 = []

# =========================
# ESTILOS PDF 2
# =========================

style_center = ParagraphStyle(
    name="center",
    fontName="TimesNewRoman",
    fontSize=11,
    leading=15,
    alignment=1
)

style_left = ParagraphStyle(
    name="left",
    fontName="TimesNewRoman",
    fontSize=11,
    leading=15,
)

style_justify = ParagraphStyle(
    name="justify",
    fontName="TimesNewRoman",
    fontSize=11,
    leading=16,
    alignment=4,
    firstLineIndent=25
)

style_right = ParagraphStyle(
    name="right",
    fontName="TimesNewRoman",
    fontSize=11,
    leading=15,
    alignment=2
)

style_left_indent = ParagraphStyle(
    name="Times12LeftIndent",
    fontName="TimesNewRoman",
    fontSize=11,
    leading=16,
    alignment=0,
    leftIndent=40  # espaço para a direita
)

# =========================
# LOGO
# =========================

logo = Image(imagem_path, width=60, height=60)
elements2.append(logo)

elements2.append(Spacer(1,1))

# =========================
# TÍTULO
# =========================

elements2.append(Paragraph("ANEXO IV", style_center))

elements2.append(Paragraph(
"DECLARAÇÃO A SER APRESENTADA PELA PESSOA JURÍDICA CONSTANTE DO INCISO XI DO ART. 4º",
style_center))

elements2.append(Paragraph(
"(Redação dada pela Instrução Normativa RFB nº 1.244, de 30 de janeiro de 2012) (Vide art. 3º da IN RFB nº 1.244/2012)",
style_center))

elements2.append(Spacer(1,1))

# =========================
# DESTINATÁRIO
# =========================

elements2.append(Paragraph("Ilmo. Sr.", style_left_indent))
elements2.append(Spacer(1,5))

elements2.append(Paragraph(cliente, style_left_indent))

elements2.append(Spacer(1,10))

# =========================
# TEXTO
# =========================

texto = f"""
Rádio Energia LTDA EPP, com sede na Rua Moacyr de Paula Lobo, 104, Vila Mury,
Volta Redonda/RJ, cep: 27.283-350 inscrita no CNPJ sob o nº 31.232.747/0001-07,
DECLARA a {cliente} para fins de não incidência na fonte do IRPJ, da Contribuição
Social sobre o Lucro Líquido (CSLL), da Contribuição para o Financiamento da
Seguridade Social (Cofins), e da Contribuição para o PIS/Pasep, a que se refere o
art. 64 da Lei nº 9.430, de 27 de dezembro de 1996, que é regularmente inscrita
no Regime Especial Unificado de Arrecadação de Tributos e Contribuições devidos
pelas Microempresas e Empresas de Pequeno Porte - Simples Nacional, de que trata
o art. 12 da Lei Complementar nº 123, de 14 de dezembro de 2006.
<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Para esse efeito, a declarante informa que:
<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;I - preenche os seguintes requisitos:
<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a) conserva em boa ordem, pelo prazo de 5 (cinco) anos, contado da data da
emissão, os documentos que comprovam a origem de suas receitas e a efetivação
de suas despesas, bem como a realização de quaisquer outros atos ou operações
que venham a modificar sua situação patrimonial; e
<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b) cumpre as obrigações acessórias a que está sujeita, em conformidade com a
legislação pertinente;
<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;II - o signatário é representante legal desta empresa, assumindo o compromisso
de informar à Secretaria da Receita Federal do Brasil e à pessoa jurídica
pagadora, imediatamente, eventual desenquadramento da presente situação e está
ciente de que a falsidade na prestação dessas informações, sem prejuízo do
disposto no art. 32 da Lei nº 9.430, de 1996, o sujeitará, com as demais pessoas
que para ela concorrem, às penalidades previstas na legislação criminal e
tributária, relativas à falsidade ideológica (art. 299 do Decreto-Lei nº 2.848,
de 7 de dezembro de 1940 - Código Penal) e ao crime contra a ordem tributária
(art. 1º da Lei nº 8.137, de 27 de dezembro de 1990).
"""

elements2.append(Paragraph(texto, style_justify))

elements2.append(Spacer(1,15))

# =========================
# DATA
# =========================

elements2.append(Paragraph(
    f"Volta Redonda/RJ, {data_atual}",
    style_right
))

# =========================
# CARIMBO / ASSINATURA
# =========================

if adicionar_assinatura:
    carimbo = Image(imagem_rodape_path,  width=4 * inch, height=1.5 * inch)
    elements2.append(carimbo)


# =========================
# GERAR PDF
# =========================

doc2.build(elements2)

# =========================
# GERAR PDF 3
# =========================

from datetime import timedelta
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape

pdf_relatorio = "Relatorio_Comprovante.pdf"

doc3 = SimpleDocTemplate(
    pdf_relatorio,
    pagesize=landscape(A4),  # ← PAPEL HORIZONTAL
    rightMargin=40,
    leftMargin=40,
    topMargin=40,
    bottomMargin=40
)

elements3 = []

# =========================
# LOGO
# =========================

logo = Image(imagem_path, width=80, height=80)

dados_radio = [
    [logo,
     Paragraph(f"<b>{nome_radio}</b><br/>CNPJ: {cnpj}<br/>{endereco}", style_left)
    ]
]

tabela_radio = Table(dados_radio, colWidths=[90, 400])

elements3.append(tabela_radio)

# =========================
# DATA CANTO DIREITO
# =========================

elements3.append(Paragraph(
    f"Volta Redonda/RJ {data_atual}",
    style_right
))


# =========================
# PERÍODO
# =========================

style_left3 = ParagraphStyle(
    name="left",
    fontName="TimesNewRoman",
    fontSize=9.5,
    leading=15,
)

datas_json = dados.get("datas", [])

periodo_inicio = ""
periodo_fim = ""

if datas_json:
    periodo_inicio = datas_json[0]["dia"]
    periodo_fim = datas_json[-1]["dia"]

elements3.append(Paragraph(
    f"Relatório de Comprovante - Período: {periodo_inicio} à {periodo_fim}",
    style_left
))

elements3.append(Spacer(1,4))

# =========================
# CLIENTE
# =========================

elements3.append(Paragraph(
    f"CLIENTE: {dados.get('cliente','')} / PRODUTO: {dados.get('material','')}",
    style_left3
))

elements3.append(Paragraph(
    f"PI: {dados.get('numero_pi','')} / FORMATO: {dados.get('formato','')} / PEÇA: {dados.get('peca','')}",
    style_left3
))

elements3.append(Paragraph(
    f"CAMPANHA: {dados.get('campanha','')} / TÍTULO: {dados.get('titulo','')}",
    style_left3
))


# =========================
# MONTAR TABELA
# =========================

tabela = [["Data", "Horários"]]


for dia_info in datas_json:

    dia = dia_info.get("dia")
    quantidade = dia_info.get("quantidade", 0)
    horarios = dia_info.get("horarios", [])

    horarios_final = horarios[:]

    # completar se faltar horário
    while len(horarios_final) < quantidade:

        ultimo = horarios_final[-1]

        h = datetime.strptime(ultimo,"%H:%M:%S")
        novo = h + timedelta(minutes=5)

        horarios_final.append(novo.strftime("%H:%M:%S"))

    # cortar se tiver mais
    horarios_final = horarios_final[:quantidade]

    inicio = datetime.strptime("09:30:00","%H:%M:%S")
    fim = datetime.strptime("17:00:00","%H:%M:%S")

    horarios_validos = []

    for h in horarios:
        hora = datetime.strptime(h,"%H:%M:%S")

        if inicio.time() <= hora.time() <= fim.time():
            horarios_validos.append(h)

    horarios_final = horarios_validos[:]

    if not horarios_final:
        horarios_final.append("09:30:00")

    while len(horarios_final) < quantidade:

        ultimo = datetime.strptime(horarios_final[-1],"%H:%M:%S")
        novo = ultimo + timedelta(minutes=5)

        if novo.time() > fim.time():
            novo = inicio

        horarios_final.append(novo.strftime("%H:%M:%S"))

    horarios_final = horarios_final[:quantidade]

    linha_horarios = "   ".join(horarios_final)

    tabela.append([dia, linha_horarios])

# =========================
# CRIAR TABELA
# =========================

t = Table(
    tabela,
    colWidths=[100, 650]  # espaço grande para horários
)

t.setStyle(TableStyle([
    ("GRID",(0,0),(-1,-1),0.3,colors.grey),
    ("BACKGROUND",(0,0),(-1,0),colors.lightgrey),

    ("FONTSIZE",(0,0),(-1,-1),9),
    ("TOPPADDING",(0,0),(-1,-1),1),
    ("BOTTOMPADDING",(0,0),(-1,-1),1),

    ("LEFTPADDING",(0,0),(-1,-1),2),
    ("RIGHTPADDING",(0,0),(-1,-1),2),
]))

elements3.append(t)
elements3.append(Spacer(1,5))
# =========================
# ASSINATURA
# =========================

if adicionar_assinatura:
    assinatura = Image(imagem_rodape_path, width=280, height=100)
    elements3.append(assinatura)

doc3.build(elements3)

print("Relatório de comprovante gerado com sucesso!")

print("PDF Declaração de Simples gerado com sucesso!")

print("PDF Declaração Artigo 299 gerado com sucesso!")
