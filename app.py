import os
import re
import emoji
from flask import Flask, request, jsonify, render_template

# Variáveis globais para os modelos (inicialmente None)
sentiment_analyzer = None
intent_classifier = None

# Inicializa Flask
app = Flask(__name__)

# Listas de filtro
BLACKLIST_OFENSAS = ["burro", "idiota", "otário", "imbecil"]
BLACKLIST_SPAM = ["promoção imperdível", "ganhe dinheiro", "clique aqui", "oferta exclusiva"]
INTENCOES = ['problema técnico', 'reclamação', 'dúvida', 'solicitação', 'elogio', 'agradecimento', 'saudação', 'outros']
INTENCOES_IMPRODUTIVAS = ['elogio', 'agradecimento', 'saudação']

# Templates de respostas
RESPOSTA_TEMPLATES = {
    'problema técnico': "Olá! Percebemos que você tem um problema técnico. Nossa equipe irá analisar e responder em breve.",
    'reclamação': "Obrigado pelo seu contato. Recebemos sua reclamação e vamos verificar imediatamente.",
    'dúvida': "Agradecemos sua mensagem! Entendemos que se trata de uma dúvida. Nossa equipe responderá em breve.",
    'solicitação': "Recebemos sua solicitação e nossa equipe está analisando. Retornaremos em breve.",
    'elogio': "Obrigado pelo seu elogio! Ficamos felizes em saber que você está satisfeito.",
    'agradecimento': "Agradecemos sua mensagem! Estamos à disposição para ajudar sempre que precisar.",
    'saudação': "Olá! Agradecemos por entrar em contato. Nossa equipe está à disposição.",
    'outros': "Não conseguimos identificar o assunto da sua mensagem. Por favor, poderia nos dar mais detalhes sobre o que você precisa? Assim, poderemos te ajudar melhor."
}

# -----------------------
# Funções auxiliares
# -----------------------
def preprocessar_texto(texto):
    texto = re.sub(r'http\S+|www\S+|\S+@\S+', '', texto)
    texto = re.sub(r'[^\w\s.,?!áéíóúàèìòùãõâêîôûç]', '', texto, flags=re.UNICODE)
    texto = emoji.demojize(texto).lower().strip()
    return texto

def contem_palavras_chave(texto, palavras_chave):
    return any(palavra in texto for palavra in palavras_chave)

def carregar_modelos():
    """Carrega modelos de IA sob demanda"""
    global sentiment_analyzer, intent_classifier
    if sentiment_analyzer and intent_classifier:
        return

    from pysentimiento import create_analyzer
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

    sentiment_analyzer = create_analyzer(task="sentiment", lang="pt")
    tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-mnli")
    model = AutoModelForSequenceClassification.from_pretrained("facebook/bart-large-mnli")
    intent_classifier = pipeline("zero-shot-classification", model=model, tokenizer=tokenizer)

# -----------------------
# Rotas
# -----------------------
@app.route("/")
def home():
    return "Servidor ativo! ✅"

@app.route("/processar_email", methods=["POST"])
def processar_email():
    carregar_modelos()  # Carrega só quando necessário

    data = request.get_json()
    texto_email = data.get("email_text", "")

    if not texto_email:
        return jsonify({"error": "Nenhum texto de e-mail fornecido"}), 400

    texto_limpo = preprocessar_texto(texto_email)

    # Filtros rápidos
    if len(texto_limpo.split()) < 5 or \
       contem_palavras_chave(texto_limpo, BLACKLIST_OFENSAS) or \
       contem_palavras_chave(texto_limpo, BLACKLIST_SPAM):
        return jsonify({"categoria": "Improdutivo", "resposta": RESPOSTA_TEMPLATES["agradecimento"]})

    # Sentimento
    sentimento = sentiment_analyzer.predict(texto_limpo).output
    if sentimento in ["POS", "NEU"]:
        categoria = "Produtivo"
        resultado_intencao = intent_classifier(texto_limpo, candidate_labels=INTENCOES, multi_label=True)
        intencoes_relevantes = [
            label for label, score in zip(resultado_intencao["labels"], resultado_intencao["scores"]) if score > 0.3
        ][:2]
        intencao_principal = intencoes_relevantes[0] if intencoes_relevantes else "outros"
        resposta_sugerida = RESPOSTA_TEMPLATES.get(intencao_principal, RESPOSTA_TEMPLATES["outros"])
    else:
        categoria = "Improdutivo"
        resposta_sugerida = RESPOSTA_TEMPLATES["agradecimento"]

    return jsonify({"categoria": categoria, "resposta": resposta_sugerida})

# -----------------------
# NUNCA rodar app.run() no Render
# Gunicorn cuidará disso
# -----------------------
