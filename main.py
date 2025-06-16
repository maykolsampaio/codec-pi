from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
import os 
import requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = 'CODEC-PI'
CORS(app)
# ========================
# Função para envio de e-mail
# ========================
def enviar_email(nome, email, mensagem):
    remetente = os.getenv("EMAIL_REMETENTE")
    senha = os.getenv("EMAIL_SENHA")
    destinatario = os.getenv("EMAIL_DESTINATARIO")

    corpo = f"Nome: {nome}\nEmail: {email}\nMensagem: {mensagem}"

    msg = MIMEText(corpo)
    msg["Subject"] = "Mensagem do Formulário de Contato"
    msg["From"] = remetente
    msg["To"] = destinatario

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(remetente, senha)
            smtp.send_message(msg)
        print("Email enviado com sucesso!")
    except Exception as e:
        print("Erro ao enviar email:", e)

# ========================
# Função para envio via WhatsApp (CallMeBot)
# ========================
def enviar_whatsapp(mensagem):
    numero = os.getenv("WHATSAPP_NUMERO")
    apikey = os.getenv("WHATSAPP_APIKEY")

    url = "https://api.callmebot.com/whatsapp.php"
    params = {
        "phone": numero,
        "text": mensagem,
        "apikey": apikey
    }

    try:
        response = requests.get(url, params=params)
        print("WhatsApp:", response.text)
    except Exception as e:
        print("Erro ao enviar WhatsApp:", e)

# ========================
# Rota principal
# ========================
@app.route("/")
def index():
    return render_template("index.html")

# ========================
# Rota envia mensagem
# ========================
@app.route('/enviar_mensagem', methods=['POST'])
def enviar_mensagem():
    try:
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form.get('telefone', '')
        mensagem = request.form['mensagem']

        texto = f"Nova mensagem de contato:\nNome: {nome}\nEmail: {email}\nTelefone: {telefone}\nMensagem: {mensagem}"

        enviar_email(nome, email, mensagem)
        enviar_whatsapp(texto)

        return jsonify({"mensagem": "Mensagem enviada com sucesso!", "categoria": "success"})
    except Exception as e:
        print("Erro geral:", e)
        return jsonify({"mensagem": "Erro ao enviar mensagem. Por favor, tente novamente.", "categoria": "error"})


def main():
    app.run(port=int(os.environ.get("PORT", 80)))


if __name__ == "__main__":
    main()
