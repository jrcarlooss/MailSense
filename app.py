import os
from flask import Flask, render_template, request, jsonify
import re
import emoji
import openai

# ----------------------------------------------------
# 1. Inicializar o aplicativo Flask
# ----------------------------------------------------
app = Flask(__name__)

# ----------------------------------------------------
# 2. Configurações e listas
# ----------------------------------------------------
BLACKLIST_OFENSAS = ["burro", "idiota", "otário", "imbecil"]
BLACKLIST_SPAM = ["promoção imperdível", "ganhe dinheiro", "clique aqui", "oferta exclusiva"]
INTENCOES = ['problema técnico', 'reclamação', 'dúvida', 'solicitação', 'elogio', 'agradecimento', 'saudação', 'outros']
INTENCOES_IMPRODUTIVAS = ['elogio', 'agradecimento', 'saudação']

RESPOSTA_TEMPLATES = {
    'problema técnico': "Olá! Percebemos que você tem um problema técnico. Nossa equipe irá analisar e responder em breve.",
    'reclamação': "Obrigado pelo seu contato. Recebemos sua reclamação e vamos verificar imediatamente.",
    'dúvida': "Agradecemos sua mensagem! Entendemos que se trata de uma dúvida. Nossa equipe responderá em breve.",
    'solicitação': "Recebemos sua solicitação e nossa equipe está analisando. Retornaremos em breve.",
    'elogio': "Obrigado pelo seu elogio! Ficamos felizes em saber que você está satisfeito.",
    'agradecimento': "Agradecemos sua mensagem! Estamos à disposição para ajudar sempre que precisar.",
    'saudação': "Olá! Agradecemos por entrar em contato. Nossa equipe está à disposição.",
    'outros': "Não conseguimos identificar o assunto da sua mensagem. Por favor, forneça mais detalhes para ajudarmos melhor."
}

# ----------------------------------------------------
# 3. Funções auxiliares
# ----------------------------------------------------
def preprocessar_texto(texto):
    texto = re.sub(r'http\S+|www\S+|\S+@\S+', '', texto)
    texto = re.sub(r'[^\w\s.,?!áéíóúàèìòùãõâêîôûç]', '', texto, flags=re.UNICODE)
    return emoji.demojize(texto).lower().strip()

def contem_palavras_chave(texto, palavras_chave):
    return any(palavra in texto for palavra in palavras_chave)

# ----------------------------------------------------
# 4. Função para gerar resposta IA ou template
# ----------------------------------------------------
def gerar_resposta_ia_ou_template(texto_email, intencao_principal, intencoes_relevantes):
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    
    try:
        prompt = (
            f"O usuário enviou a seguinte mensagem: '{texto_email}'. "
            f"A intenção principal é: '{intencao_principal}'. "
            f"Gere uma resposta clara, educada e objetiva, ideal para um help desk. "
            f"A resposta deve ser em português."
        )

        from openai import ChatCompletion
        response = ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
        )
        resposta_ia = response['choices'][0]['message']['content'].strip()
        if resposta_ia:
            return resposta_ia
    except Exception as e:
        print(f"IA falhou, usando templates. Erro: {e}")

    # fallback com templates
    respostas = [RESPOSTA_TEMPLATES.get(intencao, RESPOSTA_TEMPLATES['outros'])
                 for intencao in intencoes_relevantes][:2]
    intencoes_produtivas = [i for i in intencoes_relevantes if i not in INTENCOES_IMPRODUTIVAS]
    if intencoes_produtivas:
        respostas = [RESPOSTA_TEMPLATES.get(i, RESPOSTA_TEMPLATES['outros']) for i in intencoes_produtivas][:2]
        if len(respostas) == 2:
            return f"{respostas[0]} Além disso, {respostas[1].lower()}"
        return respostas[0] if respostas else RESPOSTA_TEMPLATES['outros']
    intencao_principal = intencoes_relevantes[0] if intencoes_relevantes else 'outros'
    return RESPOSTA_TEMPLATES.get(intencao_principal, RESPOSTA_TEMPLATES['outros'])

# ----------------------------------------------------
# 5. Rotas
# ----------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/processar_email', methods=['POST'])
def processar_email():
    data = request.get_json()
    texto_email = data.get('email_text', '')
    if not texto_email:
        return jsonify({'error': 'Nenhum texto de e-mail fornecido.'}), 400

    try:
        texto_limpo = preprocessar_texto(texto_email)

        if len(texto_limpo.split()) < 5 or \
           contem_palavras_chave(texto_limpo, BLACKLIST_OFENSAS) or \
           contem_palavras_chave(texto_limpo, BLACKLIST_SPAM):
            return jsonify({'categoria': 'Improdutivo', 'resposta': RESPOSTA_TEMPLATES['agradecimento']})

        # Lazy load do modelo de sentimento apenas quando necessário
        from pysentimiento import create_analyzer
        sentiment_analyzer = create_analyzer(task="sentiment", lang="pt")
        sentimento = sentiment_analyzer.predict(texto_limpo).output

        if sentimento in ['POS', 'NEU']:
            categoria = 'Produtivo'
            # Lazy load zero-shot apenas se necessário
            from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
            intent_tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-mnli")
            intent_model = AutoModelForSequenceClassification.from_pretrained("facebook/bart-large-mnli")
            intent_classifier = pipeline("zero-shot-classification", model=intent_model, tokenizer=intent_tokenizer)
            
            resultado_intencao = intent_classifier(texto_limpo, candidate_labels=INTENCOES, multi_label=True)
            intencoes_relevantes = [label for label, score in zip(resultado_intencao['labels'], resultado_intencao['scores']) if score > 0.3][:2]
            intencao_principal = intencoes_relevantes[0] if intencoes_relevantes else 'outros'
            resposta_sugerida = gerar_resposta_ia_ou_template(texto_email, intencao_principal, intencoes_relevantes)
        else:
            categoria = 'Improdutivo'
            resposta_sugerida = RESPOSTA_TEMPLATES['agradecimento']

        return jsonify({'categoria': categoria, 'resposta': resposta_sugerida})

    except Exception as e:
        print(f"Erro ao processar o e-mail: {e}")
        return jsonify({'error': f'Ocorreu um erro: {e}'}), 500

# ----------------------------------------------------
# 6. Remover app.run() pois gunicorn vai rodar o app
# ----------------------------------------------------
