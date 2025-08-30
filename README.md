# ScrumBot-Virtual

##  ChatBot - Scrum Master com IA

### Descrição

O projeto consiste em uma API de chatbot que simula a interação de um Scrum master liderando uma daily. 
ele analisa user storys de reuniões passadas e oferece sugestões de melhoria para as sprints do projeto.
ele é feito em pyhton com os frameworks Flask para gerenciamento de servidores, ollama para uma analise 
de uma inteligencia artificial e requests para para realizar integração entre os frameworks.

##### Ele pode:

   * Liderar dailys
   * Gerar user stories
   * Revisar user stories
   * Passar feedbacks para o time
   * Sugerir melhorias para a sprint
        
---

### Requisitos

  * Python v3.13 ou superior
  * Ollama instalado no seu computador (Windows/Mac/Linux)
  * Modelo **gemma3** baixado no Ollama (~3GB)

---

### Iniciar Ambiente Virtual; 

        cd .venv\ 

        cd Scripts

        dir 

        .\Activate.ps1

### Instalar dependencias;

        pip install Flask

        pip install ollama

        pip install requests

### Utilazar dois terminal;

##### primeiro terminal uso para rodar servidor flask;

            python api_backlog.py

##### segundo terminal uso para rodar chatbot;

            python scrum-master-bot.py

### Estrutura 

    \Atv Eng. Soft.
    |-\.venv
    |-api_backlog.py
    |-scrum-master-bot.py
    |_README.txt




