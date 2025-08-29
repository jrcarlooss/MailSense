import os
from flask import Flask, render_template, request, jsonify
import re
import emoji
import openai
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from pysentimiento import create_analyzer

# ----------------------------------------------------
# 1. Inicializar o aplicativo Flask
# ----------------------------------------------------
app = Flask(__name__)

# ----------------------------------------------------
# 2. Variáveis globais (modelos só serão carregados quando necessários)
# ----------------------------------------------------
sentiment_analyzer = None
intent_classifier = None

# ----------------------------------------------------
# 3. Função para carregar modelos sob demanda
# ----------------------------------------------------
def carregar_modelos():
    global sentiment_analyzer, intent_classifier
    if sentiment_analyzer is None or intent_classifier is None:
        print("🔄 Carregando modelos de IA...")
        sentiment_analyzer = create_analyzer(task="sentiment", lang="pt")

        intent_tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-mnli")
        intent_model = AutoModelForSequenceClassification.from_pretrained("facebook/bart-large-mnli")
        intent_classifier = pipeline("zero-shot-classification", model=intent_model, tokenizer=intent_tokenizer)
        print("✅ Modelos carregados com sucesso!")

# ----------------------------------------------------
# 4. Funções auxiliares
# ----------------------------------------------------
def preprocessar_texto(texto):
    texto = re.sub(r'http\S+|www\S+|\S+@\S+', '', texto)
    texto = re.sub(r'[^\w\s.,?!áéíóúàèìòùãõâêîôûç]', '', texto, flags=re.UNICODE)
    texto = emoji.demojize(texto).lower().strip()
    return texto

# ----------------------------------------------------
# 5. Rotas
# ----------------------------------------------------
@app.route("/")
def home():
    return "Servidor Flask está rodando no Render 🚀"

@app.route("/ping")
def ping():
    return jsonify({"status": "ok", "mensagem": "Servidor ativo!"})

@app.route("/processar_email", methods=['POST'])
def processar_email():
    try:
        carregar_modelos()  # modelos só são carregados quando essa rota é chamada
    except Exception as e:
        return jsonify({"error": f"Falha ao carregar modelos: {e}"}), 500

    data = request.get_json()
    texto_email = data.get("email_text", "")
    if not texto_email:
        return jsonify({"error": "Nenhum texto de e-mail fornecido."}), 400

    # Aqui você insere sua lógica de processamento...
    texto_limpo = preprocessar_texto(texto_email)
    return jsonify({"texto_limpo": texto_limpo, "mensagem": "Processado com sucesso!"})

# ----------------------------------------------------
# 6. Executar localmente (Render ignora isso)
# ----------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)


# ----------------------------------------------------
# 7. Executar Servidor
# ----------------------------------------------------
#if __name__ == '__main__':
#    port = int(os.environ.get("PORT", 5000))
#    app.run(host='0.0.0.0', port=port, debug=False)
