# 🤖 MailSense: Sistema de Classificação e Automação de E-mails

Este projeto, chamado **MailSense**, é uma solução digital criada para automatizar a leitura, classificação e sugestão de respostas para e-mails. O objetivo é otimizar o tempo e a produtividade de equipes que lidam com um alto volume de mensagens diárias. A aplicação categoriza os e-mails como **Produtivos** ou **Improdutivos** e sugere respostas automáticas de acordo com o teor de cada mensagem.

## 🌟 Funcionalidades

- **Classificação de E-mails**: O sistema categoriza e-mails em duas classes principais:
    - **Produtivo**: E-mails que requerem uma ação ou resposta específica (ex: solicitações, dúvidas, problemas técnicos).
    - **Improdutivo**: E-mails que não demandam uma ação imediata (ex: agradecimentos, saudações, mensagens de spam).
- **Análise de Intenção**: Identifica a intenção do e-mail usando um modelo de *zero-shot classification*, com rótulos como `problema técnico`, `dúvida`, `solicitação`, `elogio` e `agradecimento`.
- **Geração de Respostas**: Sugere respostas automáticas e contextuais. [cite_start]O sistema combina templates pré-definidos com a API da OpenAI para gerar respostas mais dinâmicas e personalizadas, oferecendo um *fallback* caso a geração com a IA falhe.
- **Interface Web Simples**: Uma interface de usuário intuitiva que permite ao usuário inserir o conteúdo do e-mail diretamente e visualizar a classificação e a resposta sugerida instantaneamente.

---

## 🛠️ Tecnologias Utilizadas

Este projeto foi desenvolvido utilizando as seguintes ferramentas e bibliotecas:

### Backend
- **Python**: Linguagem de programação principal.
- **Flask**: Micro-framework web para a API.
- **Hugging Face Transformers**: Para o uso de modelos de IA como `facebook/bart-large-mnli`[cite: 3, 5].
- **PySentimiento**: Biblioteca para análise de sentimento em português, usada como um dos critérios de classificação.
- **OpenAI**: Para a geração dinâmica de respostas.
- **Numpy** e **Sympy**: Bibliotecas para cálculos e operações matemáticas.
- **Tqdm**: Para exibir barras de progresso.
- **Safetensors**: Usado para salvar e carregar tensores de forma segura e rápida[cite: 3, 4, 5].
- **Gunicorn**: Servidor de aplicação web Python, configurado para o deploy com o arquivo `Procfile`[cite: 2, 4].

### Hospedagem e Deploy
- **Hugging Face Spaces**: Plataforma de hospedagem para a aplicação, que facilita o deploy de projetos de IA. [cite_start]O arquivo `README.md` com metadados do Gradio sugere que o projeto foi configurado para ser executado nesta plataforma.
- **Render**: Plataforma de deploy alternativa, configurada no arquivo `render.yaml`.

---

# MailSense

Guia passo a passo para executar o projeto **MailSense** localmente.

---

## 📌 Pré-requisitos
Antes de começar, certifique-se de que possui instalado na sua máquina:
- Python 3.x
- pip

---

## 📥 1. Clonar o Repositório
Abra o terminal (Prompt de Comando, PowerShell, Git Bash, Terminal, etc.) e execute:

git clone <URL_DO_REPOSITORIO>  
cd MailSense

---

## ⚙️ 2. Configurar o Ambiente Virtual
É recomendado usar um ambiente virtual para isolar as dependências do projeto. Isso evita conflitos com outras bibliotecas do sistema.

Crie o ambiente virtual:

python -m venv venv

Ative o ambiente virtual:

- **Windows**:  
  venv\Scripts\activate  

- **macOS e Linux**:  
  source venv/bin/activate  

---

## 📦 3. Instalar as Dependências
Com o ambiente virtual ativado, instale as bibliotecas listadas no arquivo requirements.txt:

pip install -r requirements.txt

---

## 🔑 4. Configurar a Chave da API da OpenAI (Opcional)
Se desejar usar a funcionalidade de geração de respostas da OpenAI:

1. Abra o arquivo `app.py`.  
2. Localize a linha:  
   openai.api_key = "SUA_CHAVE_AQUI"  
3. Substitua `"SUA_CHAVE_AQUI"` pela sua chave de API real.  

---

## ▶️ 5. Executar o Servidor
Certifique-se de estar no diretório MailSense e com o ambiente virtual ativado.  
Inicie o servidor Flask com:

python app.py

Se tudo estiver correto, aparecerá no terminal:

 * Running on http://127.0.0.1:5000

---

## 🌐 6. Acessar a Aplicação
Abra o navegador e acesse:

http://127.0.0.1:5000

A interface da aplicação será carregada e você poderá usá-la normalmente.

## 📂 Versão Completa do Projeto (Arquivo ZIP)

Além da versão disponível no **GitHub** e hospedada no **Render**, também estou disponibilizando uma pasta **compactada (.zip)** contendo o projeto **completo para uso local**.

> ⚠️ **Importante:**  
> A versão que roda no Render foi ajustada com menos funcionalidades devido às limitações do plano gratuito.  
> Já o arquivo ZIP contém **todas as funcionalidades originais do MailSense**, conforme utilizado em ambiente local.

🔗 [Clique aqui para baixar a versão completa (Mega.nz)](https://mega.nz/file/bhhUVYSZ#nDevw4rwvDS6ann5tHEoKfXvEAoniQCda7foS-0k2Q8)



## Aviso de Direitos Autorais e Uso
