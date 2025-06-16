from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
import requests

app = Flask(__name__)

# ========================
# Função para envio de e-mail
# ========================
def enviar_email(nome, email, mensagem):
    remetente = "maykolsampaio@ifpi.edu.br"
    senha = "ddinysayjdwmeeej"  # Use senha de app (não a senha normal do Gmail)
    destinatario = "maykolsampaio@gmail.com"

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
    numero = "5586988065306"
    apikey = "SUA_API_KEY_DO_CALLMEBOT"

    url = f"https://api.callmebot.com/whatsapp.php"
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
@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        mensagem = request.form['mensagem']

        texto = f"Nova mensagem de contato:\nNome: {nome}\nEmail: {email}\nMensagem: {mensagem}"

        # Envia email
        enviar_email(nome, email, mensagem)

        # Envia WhatsApp
        enviar_whatsapp(texto)

        return "Mensagem enviada com sucesso!"

    return render_template("formulario.html")





EMAIL_DESTINO = "maykolsampaio@ifpi.edu.br"
SENHA_EMAIL = "ddinysayjdwmeeej"
WHATSAPP_NUMERO = "5586988965306"
WHATSAPP_APIKEY = (
    "000000"  # Gere no site: https://www.callmebot.com/blog/free-api-whatsapp-messages/
)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # Porta para TLS


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/enviar', methods=['POST'])
def enviar():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        mensagem = request.form.get('mensagem')

        if not all([email, mensagem]):
            flash("Todos os campos são obrigatórios.", "error")
            return redirect(url_for('index'))

        success, message = send_email_gmail(email, mensagem)

        if success:
            flash(message, "success")
        else:
            flash(message, "error")
        
        return redirect(url_for('index'))


def send_email_gmail(EMAIL_DESTINO, mensagem):
    data = request.get_json()
    nome = data.get("nome")
    email = data.get("email")
    telefone = data.get("telefone", "")
    mensagem = data.get("mensagem")

    texto = f"""Nova mensagem do site:

Nome: {nome}
Email: {email}
Telefone: {telefone}
Mensagem: {mensagem}
"""

    # Enviar por e-mail (SMTP simples)
    try:
        if not EMAIL_DESTINO or not SENHA_EMAIL:
            app.logger.error(
                "Credenciais do Gmail não configuradas nas variáveis de ambiente."
            )
        return (
            False,
            "Erro de configuração do servidor: credenciais de e-mail ausentes.",
        )
        msg = MIMEText(texto)
        msg["Subject"] = "Dúvida de" + nome + "sobre o CODEC-PI. Telefone: " + telefone
        msg["From"] = email  # Trocar por seu e-mail remetente
        msg["To"] = EMAIL_DESTINO

        app.logger.info(
            f"Tentando enviar e-mail para {EMAIL_DESTINO} de {GMAIL_USERNAME}"
        )

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()  # Identificar-se para o servidor
            server.starttls()  # Iniciar criptografia TLS
            server.ehlo()  # Re-identificar-se após TLS
            server.login(EMAIL_DESTINO, SENHA_EMAIL)
            server.sendmail(GMAIL_USERNAME, [EMAIL_DESTINO], msg.as_string())
            app.logger.info(f"E-mail enviado com sucesso para {EMAIL_DESTINO}")
            return True, "E-mail enviado com sucesso!"
    except smtplib.SMTPAuthenticationError:
        app.logger.error(
            "Erro de autenticação SMTP. Verifique o username e a senha de app."
        )
        return (
            False,
            "Erro de autenticação. Verifique suas credenciais de e-mail (especialmente a senha de app).",
        )
    except smtplib.SMTPServerDisconnected:
        app.logger.error("Servidor SMTP desconectado. Tente novamente mais tarde.")
        return False, "O servidor de e-mail desconectou. Tente novamente mais tarde."
    except smtplib.SMTPException as e:
        app.logger.error(f"Erro SMTP: {e}")
        return False, f"Ocorreu um erro ao enviar o e-mail: {e}"
    except Exception as e:
        app.logger.error(f"Erro inesperado ao enviar e-mail: {e}")
        return False, f"Ocorreu um erro inesperado: {e}"

    # Enviar por WhatsApp
    try:
        message = (
            f"{nome} enviou uma mensagem: {mensagem} - Email: {email} - Tel: {telefone}"
        )
        requests.get(
            "https://api.callmebot.com/whatsapp.php",
            params={
                "phone": WHATSAPP_NUMERO,
                "text": message,
                "apikey": WHATSAPP_APIKEY,
            },
        )
    except Exception as e:
        print("Erro ao enviar WhatsApp:", e)

    return jsonify({"status": "sucesso"})




