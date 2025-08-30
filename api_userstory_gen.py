from flask import Flask, request, jsonify
import re
import os
import requests
import json

from api_backlog import BACKLOG_USERS, BACKLOG_ITEMS

app = Flask(__name__)

# Lista em memória para armazenar User Stories
user_stories = []

USER_STORIES_FILE = "user_stories.json"

from typing import Optional

def gerar_user_story_e_criterios(descricao_funcionalidade: str) -> Optional[dict]:
    """
    Usa a IA local do Ollama para gerar uma User Story e seus Critérios de Aceitação.
    Aceita resposta tanto em texto quanto em JSON.
    """
    URL_GENERATE = "http://localhost:11434/api/generate"
    
    prompt = f"""
    Com base na seguinte descrição de funcionalidade, gere uma User Story no formato: "Como [persona], quero [funcionalidade], para [benefício]".
    Além disso, sugira 3 a 5 critérios de aceitação para esta User Story.

    Descrição: {descricao_funcionalidade}

    Siga o formato estritamente:
    User Story:
    Como [persona], quero [funcionalidade], para [benefício].

    Critérios de Aceitação:
    - Critério 1
    - Critério 2
    - Critério 3
    - Critério 4
    - Critério 5
    """

    data = {
        "model": "gemma3",
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(URL_GENERATE, headers=headers, data=json.dumps(data))
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("Erro: Ollama não está rodando ou não está acessível.")
        return None  

    resposta_json = response.json()

    # Verifica se a chave 'response' existe
    if 'response' not in resposta_json:
        print("Erro: A resposta do Ollama não tem a chave 'response'.")
        return None 

    conteudo_gerado = resposta_json['response']
    print("Sua user story e 5 critérios que você deve aderir:", conteudo_gerado)

    # Tenta fazer o parsing como JSON primeiro
    try:
        resultado = json.loads(conteudo_gerado)
        user_story = resultado.get("user_story", "N/A")
        criterios_aceitacao = resultado.get("critérios_de_aceitação", [])
        if user_story != "N/A" and criterios_aceitacao:
            return {
                "user_story": user_story,
                "criterios_aceitacao": criterios_aceitacao
            }
    except Exception:
        pass  # Não é JSON, tenta parsing por texto

    # Regex para encontrar User Story e Critérios em texto
    user_story_match = re.search(r'User Story:\s*(.*?)(?:\n|$)', conteudo_gerado, re.DOTALL)
    criterios_match = re.findall(r'-\s*(.*)', conteudo_gerado)

    if not user_story_match or not criterios_match:
        print("Erro: O formato da resposta não está correto.")
        return None 

    user_story = user_story_match.group(1).strip()
    criterios_aceitacao = [c.strip() for c in criterios_match]

    return {
        "user_story": user_story,
        "criterios_aceitacao": criterios_aceitacao
    }
    
######################################################################################################################################################

@app.route('/api/generate', methods=['POST'])
def gerar_historia():
    data = request.get_json()
    if not data or 'descricao' not in data:
        return jsonify({"error": "Parâmetro 'descricao' ausente"}), 400

    descricao = data['descricao']
    resultado = gerar_user_story_e_criterios(descricao)

    if resultado:
        user_stories.append(resultado)
        salvar_user_stories()
        return jsonify(resultado), 200
    else:
        return jsonify({"error": "Falha ao gerar User Story"}), 500

@app.route('/api/userstories', methods=['GET'])
def listar_user_stories():
    return jsonify(user_stories), 200

@app.route('/api/userstories/<int:indice>', methods=['DELETE'])
def remover_user_story(indice):
    if 0 <= indice < len(user_stories):
        removida = user_stories.pop(indice)
        salvar_user_stories()
        return jsonify({"removida": removida}), 200
    else:
        return jsonify({"error": "Índice inválido"}), 400

@app.route('/api/backlog', methods=['GET'])
def listar_backlog():
    return jsonify(BACKLOG_ITEMS), 200

def salvar_user_stories():
    with open(USER_STORIES_FILE, "w", encoding="utf-8") as f:
        json.dump(user_stories, f, ensure_ascii=False, indent=2)

def carregar_user_stories():
    global user_stories
    if os.path.exists(USER_STORIES_FILE):
        with open(USER_STORIES_FILE, "r", encoding="utf-8") as f:
            user_stories = json.load(f)

carregar_user_stories()

if __name__ == '__main__':
    app.run(debug=True)