from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import io
import re
from datetime import datetime
import os

app = Flask(__name__)

def validar_cns(cns):
    return re.match(r'^\d{15}$', cns) is not None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerar_cartao', methods=['POST'])
def gerar_cartao():
    nome = request.form['nome']
    data_nascimento = request.form['data_nascimento']
    sexo = request.form['sexo']
    cns = request.form['cns'].replace(' ', '')
    
    if not validar_cns(cns):
        return render_template('erro.html', mensagem="CNS inválido! Deve conter 15 dígitos.")
    
    try:
        datetime.strptime(data_nascimento, '%Y-%m-%d')
    except ValueError:
        return render_template('erro.html', mensagem="Data de nascimento inválida!")
    
    try:
        img = Image.new('RGB', (600, 400), color=(240, 248, 255))
        draw = ImageDraw.Draw(img)
        cor_fundo = (173, 216, 230)
        cor_texto = (0, 0, 139)
        
        # Desenhar fundo
        draw.rectangle([(0, 0), (600, 100)], fill=cor_fundo)
        draw.rectangle([(0, 350), (600, 400)], fill=cor_fundo)
        
        # Usar fonte padrão em vez de arial.ttf
        try:
            # Tentar carregar fonte padrão do sistema
            fonte_titulo = ImageFont.truetype("arial.ttf", 28)
            fonte_dados = ImageFont.truetype("arial.ttf", 22)
        except:
            # Se falhar, usar fonte básica
            fonte_titulo = ImageFont.load_default()
            fonte_dados = ImageFont.load_default()
            # Aumentar tamanho da fonte padrão
            fonte_titulo.size = 28
            fonte_dados.size = 22
        
        # Centralizar título
        titulo = "CARTÃO NACIONAL DE SAÚDE"
        titulo_largura = fonte_titulo.getlength(titulo)
        titulo_x = (600 - titulo_largura) / 2
        
        # Adicionar textos
        draw.text((titulo_x, 40), titulo, fill=cor_texto, font=fonte_titulo)
        draw.text((50, 120), f"NOME: {nome}", fill='black', font=fonte_dados)
        draw.text((50, 170), f"NASCIMENTO: {data_nascimento}", fill='black', font=fonte_dados)
        draw.text((50, 220), f"SEXO: {sexo}", fill='black', font=fonte_dados)
        draw.text((50, 270), f"CNS: {cns}", fill='black', font=fonte_dados)
        draw.text((150, 365), "BRASIL - Ministério da Saúde", fill=cor_texto, font=fonte_dados)
        
        # Salvar para download
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return send_file(
            img_byte_arr,
            mimetype='image/png',
            as_attachment=True,
            download_name=f'CNS_{nome.replace(" ", "_")}.png'
        )
    
    except Exception as e:
        return render_template('erro.html', mensagem=f"Erro ao gerar cartão: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
