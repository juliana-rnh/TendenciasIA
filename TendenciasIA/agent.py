import os
from google import genai
from tavily import TavilyClient

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "SUA_CHAVE_TAVILY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "SUA_CHAVE_GEMINI")
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "SEU_WEBHOOK_AQUI")

PROMPT_AGENTE = """
You are a cutting-edge AI Trend Scout specialized in Software Quality Assurance (QA) and Engineering Productivity.
Your objective is to filter the provided web search results to find emerging, trending, and next-generation AI tools.

CRITICAL INSTRUCTION: Do NOT include any tools that are listed in the "EXCLUDED_TOOLS_HISTORIC" section below. Focus strictly on newer trends or alternative platforms to ensure high-value novelty.

OUTPUT STRUCTURE:
Generate a highly scannable daily brief formatted exactly as follows in Portuguese:

### 🔎 [Nome da Ferramenta] - [Título Curto da Novidade]
- **Categoria:** [ex: QA Agêntico / Workspace Nativo de IA / Vibe-Coding]
- **O que há de novo:** [1-2 frases explicando o lançamento ou recurso]
- **Impacto em QA e Produtividade:** [Explicação direta de como acelera entregas ou elimina tarefas repetitivas]
- **Contexto da Fonte:** [Nome da Fonte/Plataforma] | [Link da Fonte]

[SEPARATOR]
Use the exact token '[TOOL_NAME]' followed by the name of the tool on a new line for each tool generated, so the system can parse it. Example:
[TOOL_NAME] Shiplight AI
"""

def buscar_tendencias_ia():
    tavily = TavilyClient(api_key=TAVILY_API_KEY)
    query = "new AI native QA tools autonomous testing agents cursor lovable bolt release news"
    response = tavily.search(query=query, search_depth="advanced", time_range="w", max_results=7)
    return response.get('results', [])

def processar_com_ia(resultados_busca, ferramentas_antigas):
    client = genai.Client(api_key=GEMINI_API_KEY)
    contexto_busca = "\n\n".join([f"Title: {r.get('title')}\nURL: {r.get('url')}\nContent: {r.get('content')}" for r in resultados_busca])
    
    exclusoes = "\n".join(ferramentas_antigas) if ferramentas_antigas else "Nenhuma ferramenta registrada ainda."
    prompt_completo = f"{PROMPT_AGENTE}\n\nEXCLUDED_TOOLS_HISTORIC:\n{exclusoes}\n\nResultados brutos:\n{contexto_busca}"
    
    response = client.models.generate_content(model='gemini-2.5-flash', contents=[prompt_completo])
    return getattr(response, 'text', str(response))

def atualizar_historico_e_limpar_output(resposta_ia):
    linhas = resposta_ia.split("\n")
    texto_limpo = []
    novas_ferramentas = []
    
    for linha in linhas:
        if linha.startswith("[TOOL_NAME]"):
            nome = linha.replace("[TOOL_NAME]", "").strip()
            if nome:
                novas_ferramentas.append(nome)
        elif "[SEPARATOR]" in linha:
            continue
        else:
            if not any(x in linha for x in ["[TOOL_NAME]", "[SEPARATOR]"]):
                texto_limpo.append(linha)
                
    if novas_ferramentas:
        with open("historico.txt", "a", encoding="utf-8") as f:
            for ferramenta in novas_ferramentas:
                f.write(f"{ferramenta}\n")
                
    return "\n".join(texto_limpo)

def enviar_para_discord(texto_formatado):
    import requests
    payload = {"content": "📢 **Boletim Diário: Tendências de IA** 🚀", "embeds": [{"description": texto_formatado, "color": 3447003}]}
    if "SEU_WEBHOOK" not in DISCORD_WEBHOOK_URL:
        requests.post(DISCORD_WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    ferramentas_antigas = []
    if os.path.exists("historico.txt"):
        with open("historico.txt", "r", encoding="utf-8") as f:
            ferramentas_antigas = [linha.strip() for lambda_line in f.readlines() if (linha := lambda_line.strip())]

    try:
        dados_da_web = buscar_tendencias_ia()
        resposta_bruta = processar_com_ia(dados_da_web, ferramentas_antigas)
        relatorio_final = atualizar_historico_e_limpar_output(resposta_bruta)
        enviar_para_discord(relatorio_final)
        print("🚀 Agente executado com sucesso!")
    except Exception as e:
        print(f"💥 Erro: {e}")
