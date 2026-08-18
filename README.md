# TendenciasIA

Uma aplicação que utiliza **Inteligência Artificial** para análise de tendências, integrando APIs de IA generativa (Google Genai) com busca web avançada (Tavily).

## 🚀 O que faz?

Analisa e identifica tendências usando modelos de IA, combinando dados em tempo real com processamento inteligente.

## 📋 Requisitos

- Python 3.8+
- Pip (gerenciador de pacotes Python)

## 🔧 Como executar

### 1. Clone o repositório
```bash
git clone https://github.com/juliana-rnh/TendenciasIA.git
cd TendenciasIA
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure suas chaves de API
Crie um arquivo `.env` na raiz do projeto com suas credenciais:
```
GOOGLE_GENAI_KEY=sua_chave_aqui
TAVILY_API_KEY=sua_chave_aqui
```

### 5. Execute a aplicação
```bash
python app.py
```

## 📦 Dependências principais

- **google-genai**: Acesso a modelos de IA do Google
- **tavily-python**: Busca web inteligente
- **requests**: Requisições HTTP

## 📝 Licença

Este projeto é de código privado.