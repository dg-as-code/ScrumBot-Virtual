from urllib import response
import ollama
from ollama._types import ResponseError
import requests

from api_userstory_gen import gerar_user_story_e_criterios

# Conectar ao Ollama (certifique-se de que ele está rodando)
client = ollama.Client()
MODELO_IA = "gemma3"
try:
    client.pull(MODELO_IA)
except Exception as e:
    print(f"Erro ao puxar o modelo '{MODELO_IA}': {e}")

contexto_scrum = [
    {"role": "system", "content": "Você é um Scrum Master experiente. Sua função é ajudar o time a seguir as boas práticas do Scrum. Responda de forma clara, objetiva e encorajadora. Você deve conduzir reuniões, dar feedback sobre user stories e sugerir melhorias no processo ágil. Mantenha-se no papel de Scrum Master e use a língua portuguesa. Não escreva código, apenas interaja como um facilitador do time."}
]

def enviar_prompt(prompt_usuario):
    """
    Envia um prompt para o modelo Ollama, mantendo o contexto da conversa.
    """
    contexto_scrum.append({"role": "user", "content": prompt_usuario})
    try:
        response = client.chat(
            model=MODELO_IA,
            messages=contexto_scrum,
            stream=True
        )
        resposta_completa = ""
        print("Scrum Master:", end=" ")
        for chunk in response:
            content = chunk['message']['content']
            print(content, end="", flush=True)
            resposta_completa += content
        print()
        contexto_scrum.append({"role": "assistant", "content": resposta_completa})
    except ResponseError as e:
        print(f"Erro ao interagir com o Ollama: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None
    return resposta_completa

def ler_backlog_da_api(url_api):
    """
    Lê os itens de backlog de uma API local usando o framework requests.
    """
    try:
        response = requests.get(url_api, timeout=10)
        response.raise_for_status()
        itens_backlog = response.json()
        backlog_formatado = ""
        for item in itens_backlog:
            backlog_formatado += f"- Título: {item.get('titulo', 'N/A')}\n  Descrição: {item.get('descricao', 'N/A')}\n\n"
        return backlog_formatado
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar com a API: {e}")
        return None
    except requests.exceptions.HTTPError as e: # type: ignore
        print(f"Erro HTTP: O servidor retornou um código de erro: {e}")
        return None
    except ValueError:
        print("Erro: A resposta da API não é um JSON válido.")
        return None
    except Exception as e:
        print(f"Erro inesperado ao ler o backlog: {e}")
        return None

def conduzir_daily_scrum():
    """
    Simula uma Daily Scrum, perguntando sobre progresso, plano e impedimentos.
    """
    print("\n--- INICIANDO DAILY SCRUM ---")
    print("Bom dia, pessoal! Vamos começar nossa Daily.")
    perguntas_daily = [
        "O que você fez ontem para ajudar o time a alcançar a meta da Sprint?",
        "O que você planeja fazer hoje?",
        "Existe algum impedimento que está te bloqueando?"
    ]
    for pergunta in perguntas_daily:
        prompt_ia = f"Ok. Próxima pergunta: {pergunta}"
        enviar_prompt(prompt_ia)
        resposta_usuario = input("Você: ").strip()
        prompt_para_ia = f"O membro do time disse: '{resposta_usuario}'. Dê um feedback breve e encorajador. O que você perguntaria a seguir?"
        enviar_prompt(prompt_para_ia)
    print("\n--- DAILY SCRUM CONCLUÍDA ---")
    enviar_prompt("A Daily Scrum de hoje está encerrada. Obrigado, time!")

def feedback_user_story():
    """
    Pede uma User Story e a IA dá feedback sobre clareza, aceitação e granularidade.
    """
    print("\n--- ANÁLISE DE USER STORY ---")
    print("Por favor, cole a User Story que você gostaria de revisar.")
    user_story = input("Você (User Story): ").strip()
    prompt_feedback = f"Analise a seguinte User Story e forneça um feedback sobre a clareza, os critérios de aceitação e a granularidade (se é grande ou pequena demais): '{user_story}'. Sugira melhorias."
    enviar_prompt(prompt_feedback)

def sugerir_melhorias_agil():
    """
    A IA sugere melhorias no processo ágil do time.
    """
    print("\n--- SUGESTÃO DE MELHORIAS ---")
    print("Scrum Master: Me conte sobre um problema ou um desafio que o time está enfrentando, e eu posso sugerir algumas melhorias no processo.")
    desafio = input("Você (Desafio): ").strip()
    prompt_melhoria = f"Com base no desafio '{desafio}' que o time está enfrentando, sugira 3 melhorias práticas para nosso processo ágil."
    enviar_prompt(prompt_melhoria)

def revisar_backlog():
    """
    Lê os itens de um backlog de uma API local e a IA 'revisa' automaticamente.
    """
    print("\n--- REVISÃO AUTOMÁTICA DE BACKLOG VIA API ---")
    print("Scrum Master: Lendo os itens do backlog da API local...")
    URL_BACKLOG = "http://127.0.0.1:5000/api/backlog"
    itens_backlog = ler_backlog_da_api(URL_BACKLOG)
    if not itens_backlog:
        print("Não foi possível realizar a revisão do backlog. Verifique se a API local está rodando.")
        return
    prompt_revisao = f"Analise a lista de itens de backlog a seguir e sugira quais estão prontos para a próxima Sprint e quais precisam de mais refinamento. Use critérios como clareza, tamanho e dependências. Aqui estão os itens: \n\n{itens_backlog}"
    enviar_prompt(prompt_revisao)

def gerar_user_story():
    print("\n--- GERAÇÃO DE USER STORY ---")
    print("Por favor, forneça uma breve descrição da funcionalidade desejada.")
    descricao = input("Você (Descrição da Funcionalidade): ").strip()
    print("Exemplo: 'Permitir que o usuário recupere a senha por e-mail.'")
    if not descricao:
        print("A descrição não pode ser vazia. Tente novamente.")
        return
    try:
        resultado = gerar_user_story_e_criterios(descricao)
    except Exception as e:
        print(f"Erro ao gerar User Story: {e}")
        return
    if resultado:
        user_story = resultado.get("user_story", "N/A")
        criterios = resultado.get("criterios_aceitacao", [])
        print("\nUser Story Gerada:")
        print(user_story)
        print("\nCritérios de Aceitação:")
        for criterio in criterios:
            print(f"- {criterio}")
    else:
        print("Não foi possível gerar a User Story. Verifique se o Ollama está rodando e o modelo 'gemma3' está disponível.")

def main():
    """
    Função principal que gerencia o fluxo do chatbot.
    """
    print("Olá! Eu sou seu Scrum Master virtual. Posso te ajudar com as seguintes tarefas:")
    print("1. Conduzir Daily Scrum")
    print("2. Dar feedback sobre uma User Story")
    print("3. Sugerir melhorias no processo ágil")
    print("4. Revisar automaticamente o Backlog (via API local)")
    print("5. Gerar uma User Story com Critérios de Aceitação")
    print("6. Sair")
    while True:
        print("\nO que você gostaria de fazer?")
        comando = input("Digite o número da opção (1-6): ").strip()
        if comando == '1':
            conduzir_daily_scrum()
        elif comando == '2':
            feedback_user_story()
        elif comando == '3':
            sugerir_melhorias_agil()
        elif comando == '4':
            revisar_backlog()
        elif comando == '5':
            gerar_user_story()
        elif comando == '6':
            print("Até a próxima! Lembre-se, estou aqui para ajudar o time a ter sucesso.")
            break
        else:
            print("Opção inválida. Por favor, escolha um número de 1 a 6.")

if __name__ == "__main__":
    main()

