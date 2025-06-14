# app.py (Backend completo)
from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import io
import random
import re
from datetime import datetime

app = Flask(__name__)

# Função para validar CNS (formato básico)
def validar_cns(cns):
    return re.match(r'^\d{15}$', cns) is not None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerar_cartao', methods=['POST'])
def gerar_cartao():
    # Receber dados do formulário
    nome = request.form['nome']
    data_nascimento = request.form['data_nascimento']
    sexo = request.form['sexo']
    cns = request.form['cns'].replace(' ', '')  # Remover espaços
    
    # Validar CNS
    if not validar_cns(cns):
        return render_template('erro.html', mensagem="CNS inválido! Deve conter 15 dígitos.")
    
    # Validar data de nascimento
    try:
        datetime.strptime(data_nascimento, '%Y-%m-%d')
    except ValueError:
        return render_template('erro.html', mensagem="Data de nascimento inválida!")
    
    # Criar cartão
    try:
        img = Image.new('RGB', (600, 400), color=(240, 248, 255))
        draw = ImageDraw.Draw(img)
        
        # Cores e fontes
        cor_fundo = (173, 216, 230)
        cor_texto = (0, 0, 139)
        fonte_titulo = ImageFont.truetype("arial.ttf", 28)
        fonte_dados = ImageFont.truetype("arial.ttf", 22)
        
        # Desenhar fundo
        draw.rectangle([(0, 0), (600, 100)], fill=cor_fundo)
        draw.rectangle([(0, 350), (600, 400)], fill=cor_fundo)
        
        # Textos
        draw.text((200, 40), "CARTÃO NACIONAL DE SAÚDE", fill=cor_texto, font=fonte_titulo)
        draw.text((50, 120), f"NOME: {nome}", fill='black', font=fonte_dados)
        draw.text((50, 170), f"NASCIMENTO: {data_nascimento}", fill='black', font=fonte_dados)
        draw.text((50, 220), f"SEXO: {sexo}", fill='black', font=fonte_dados)
        draw.text((50, 270), f"CNS: {cns}", fill='black', font=fonte_dados)
        draw.text((150, 365), "BRASIL - Ministério da Saúde", fill=cor_texto, font=fonte_dados)
        
        # Salvar imagem em memória
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
