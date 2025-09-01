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

## 💻 Como Executar o Projeto Localmente

Para rodar o projeto na sua máquina, siga os passos abaixo:

### Pré-requisitos
- **Python 3.x** e **pip** instalados.

### 1. Clonar o Repositório
```bash
git clone [https://github.com/jrcarlooss/MailSense.git](https://github.com/jrcarlooss/MailSense.git)
cd MailSense

## Aviso de Direitos Autorais e Uso
