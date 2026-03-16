from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def gerar_ficha(funcionario, epi, data):

    nome_arquivo = f"ficha_{funcionario}.pdf"

    c = canvas.Canvas(nome_arquivo, pagesize=letter)

    c.setFont("Helvetica", 16)
    c.drawString(200, 750, "FICHA DE ENTREGA DE EPI")

    c.setFont("Helvetica", 12)

    c.drawString(100, 680, f"Funcionário: {funcionario}")
    c.drawString(100, 650, f"EPI entregue: {epi}")
    c.drawString(100, 620, f"Data da entrega: {data}")

    c.drawString(100, 560, "Declaro que recebi o EPI em perfeitas condições")
    c.drawString(100, 540, "e me comprometo a utilizá-lo corretamente.")

    c.drawString(100, 480, "Assinatura do funcionário:")

    c.line(100, 460, 400, 460)

    c.save()
    c.drawString(100, 200, "Assinatura do Funcionário:")

    c.drawImage(assinatura_path, 100, 120, width=200, height=60)
    
    return nome_arquivo
