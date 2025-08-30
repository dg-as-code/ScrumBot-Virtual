from flask import Flask, jsonify

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Dados de exemplo que a API irá retornar
# Isso simula a resposta de um serviço de gerenciamento de projetos
BACKLOG_ITEMS = [
    {
        "id": 1,
        "titulo": "Implementar login de usuário",
        "descricao": "Permitir que usuários se autentiquem com email e senha."
    },
    {
        "id": 2,
        "titulo": "Adicionar filtro de backlog",
        "descricao": "Criar uma funcionalidade de busca para filtrar itens por palavra-chave."
    },
    {
        "id": 3,
        "titulo": "Otimizar o carregamento de imagens",
        "descricao": "Reduzir o tamanho das imagens para melhorar a performance da página."
    },
    {
        "id": 4,
        "titulo": "Corrigir bug no formulário de contato",
        "descricao": "A validação de email não está funcionando corretamente."
    }
]
BACKLOG_USERS = [
    {
        "id": 1,
        "user_story": "Como usuário, quero fazer login com meu email e senha para acessar minha conta.",
        "criterios_aceitacao": [
            "O sistema deve validar o email e a senha.",
            "O usuário deve ser redirecionado para a página inicial após o login.",
            "Deve haver uma mensagem de erro para credenciais inválidas."
        ]
    },
    {
        "id": 2,
        "user_story": "Como administrador, quero filtrar itens do backlog por palavra-chave para encontrar tarefas rapidamente.",
        "criterios_aceitacao": [
            "O filtro deve ser aplicado em tempo real enquanto o usuário digita.",
            "Deve ser possível combinar múltiplas palavras-chave.",
            "Os resultados devem ser atualizados dinamicamente."
        ]
    }
]

# Define a rota para a API de backlog
# A URL completa será http://127.0.0.1:5000/api/backlog
@app.route('/api/backlog', methods=['GET'])
def get_backlog():
    """Retorna os itens de backlog como uma resposta JSON."""
    return jsonify(BACKLOG_ITEMS)

if __name__ == '__main__':
    # Roda o servidor Flask.
    # debug=True permite que o servidor recarregue automaticamente ao salvar o arquivo.
    app.run(debug=True)