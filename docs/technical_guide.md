# Documentação Técnica - Sistema Multi-Agente para Criação e Validação de Questões

## Arquitetura do Sistema

O Sistema Multi-Agente para Criação e Validação de Questões é baseado em uma arquitetura modular que utiliza o padrão de design orientado a agentes. Cada agente é responsável por uma etapa específica do processo de criação e validação de questões educacionais.

### Visão Geral da Arquitetura

```
+----------------+     +----------------+     +----------------+     +----------------+     +----------------+
|                |     |                |     |                |     |                |     |                |
|     Agente     |     |     Agente     |     |     Agente     |     |     Agente     |     |     Agente     |
|   Gerenciador  | --> |  Conteudista   | --> |       RT       | --> |       DE       | --> |   Validador    |
|                |     |                |     |                |     |                |     |                |
+----------------+     +----------------+     +----------------+     +----------------+     +----------------+
        |                                                                                         |
        |                                                                                         |
        v                                                                                         v
+----------------+                                                                      +----------------+
|                |                                                                      |                |
|    Modelos     |                                                                      |   Documentos   |
|    de Dados    |                                                                      |     Finais     |
|                |                                                                      |                |
+----------------+                                                                      +----------------+
```

### Componentes Principais

1. **Agentes**: Módulos especializados que executam tarefas específicas no processo.
2. **Modelos de Dados**: Classes que representam as entidades do sistema.
3. **Utilitários**: Funções auxiliares para processamento de texto, manipulação de arquivos, etc.
4. **API REST**: Interface para interação com o sistema.
5. **Cliente de IA**: Módulo para comunicação com APIs de IA externas.

## Estrutura do Projeto

```
multi-agent-system/
├── app.py                  # Ponto de entrada da aplicação
├── config.py               # Configurações do sistema
├── requirements.txt        # Dependências do projeto
├── README.md               # Documentação do projeto
├── agents/                 # Módulos dos agentes
│   ├── __init__.py
│   ├── manager_agent.py    # Agente Gerenciador
│   ├── content_agent.py    # Agente Conteudista
│   ├── rt_agent.py         # Agente Revisor Técnico
│   ├── de_agent.py         # Agente Design Educacional
│   └── validator_agent.py  # Agente Validador
├── models/                 # Modelos de dados
│   ├── __init__.py
│   ├── question.py         # Modelo para questões
│   ├── report.py           # Modelo para relatórios
│   └── task.py             # Modelo para tarefas
├── utils/                  # Utilitários
│   ├── __init__.py
│   ├── ai_client.py        # Cliente para API de IA
│   ├── file_handler.py     # Manipulação de arquivos
│   └── text_processor.py   # Processamento de texto
├── templates/              # Templates para questões
│   ├── single_answer.json
│   ├── multiple_answer.json
│   └── assertion_reason.json
├── data/                   # Dados de entrada e saída
│   ├── input/              # Arquivos de entrada
│   └── output/             # Arquivos de saída
├── tests/                  # Testes automatizados
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_content_agent.py
│   ├── test_manager_agent.py
│   └── test_integration.py
└── docs/                   # Documentação
    ├── user_guide.md
    ├── technical_guide.md
    └── api_docs.md
```

## Fluxo de Dados

O fluxo de dados no sistema segue estas etapas:

1. O usuário fornece os objetivos de aprendizagem e a fundamentação teórica.
2. O Agente Gerenciador cria uma tarefa e a encaminha para o Agente Conteudista.
3. O Agente Conteudista elabora as questões e as retorna ao Agente Gerenciador.
4. O Agente Gerenciador encaminha as questões para o Agente RT.
5. O Agente RT valida tecnicamente as questões e as retorna ao Agente Gerenciador.
6. O Agente Gerenciador encaminha as questões para o Agente DE.
7. O Agente DE valida o design educacional das questões e as retorna ao Agente Gerenciador.
8. O Agente Gerenciador encaminha as questões para o Agente Validador.
9. O Agente Validador realiza a validação final e gera os documentos de saída.
10. O Agente Gerenciador entrega os documentos finais ao usuário.

## Modelos de Dados

### Task

Representa uma tarefa a ser processada pelo sistema.

**Atributos**:
- `id`: Identificador único da tarefa
- `creation_date`: Data de criação da tarefa
- `objectives`: Lista de objetivos de aprendizagem
- `theory_text`: Texto de fundamentação teórica
- `templates`: Dicionário com templates para os diferentes tipos de questão
- `stopwords`: Lista de palavras a serem evitadas
- `questions`: Lista de questões
- `reports`: Lista de relatórios
- `status`: Status da tarefa (created, in_progress, completed)
- `current_agent`: Agente atual

**Métodos**:
- `to_dict()`: Converte a tarefa para um dicionário
- `from_dict(data)`: Cria uma tarefa a partir de um dicionário
- `add_question(question)`: Adiciona uma questão à tarefa
- `add_report(report)`: Adiciona um relatório à tarefa
- `update_status(status, agent)`: Atualiza o status da tarefa
- `get_questions_for_objective(objective_id)`: Retorna as questões associadas a um objetivo
- `get_report_by_type(report_type)`: Retorna o relatório de um tipo específico

### Question

Representa uma questão educacional.

**Atributos**:
- `id`: Identificador único da questão
- `objective_id`: ID do objetivo de aprendizagem relacionado
- `type`: Tipo da questão (single_answer, multiple_answer, assertion_reason)
- `context`: Texto de contextualização da questão
- `statement`: Enunciado da questão
- `alternatives`: Lista de alternativas
- `feedback`: Dicionário com feedback para cada alternativa
- `metadata`: Metadados da questão
- `validation`: Dicionário com validações (rt, de, final)

**Métodos**:
- `to_dict()`: Converte a questão para um dicionário
- `from_dict(data)`: Cria uma questão a partir de um dicionário
- `update_metadata(modified_by)`: Atualiza os metadados da questão
- `add_validation(validation_type, status, comments, checklist)`: Adiciona uma validação à questão
- `to_markdown()`: Converte a questão para formato Markdown

### Report

Representa um relatório gerado durante o processo.

**Atributos**:
- `id`: Identificador único do relatório
- `type`: Tipo do relatório (development_report, validation_report)
- `creation_date`: Data de criação do relatório
- `agent`: Nome do agente que gerou o relatório
- `content`: Conteúdo do relatório

**Métodos**:
- `to_dict()`: Converte o relatório para um dicionário
- `from_dict(data)`: Cria um relatório a partir de um dicionário
- `to_markdown()`: Converte o relatório para formato Markdown

## Agentes

### ManagerAgent

Coordena o fluxo de trabalho entre os demais agentes.

**Métodos**:
- `initialize_task(objectives, theory_text)`: Inicializa uma nova tarefa
- `load_task(task_id)`: Carrega uma tarefa existente
- `assign_to_content_agent()`: Atribui a tarefa ao Agente Conteudista
- `assign_to_rt_agent()`: Atribui a tarefa ao Agente RT
- `assign_to_de_agent()`: Atribui a tarefa ao Agente DE
- `assign_to_validator_agent()`: Atribui a tarefa ao Agente Validador
- `get_task_status()`: Retorna o status atual da tarefa
- `get_final_results()`: Retorna os resultados finais da tarefa

### ContentAgent

Cria questões com base nos objetivos e fundamentação teórica.

**Métodos**:
- `create_questions(objectives, theory_text, templates, stopwords)`: Cria questões
- `create_single_answer_question(objective, theory_text, template, stopwords)`: Cria uma questão de resposta única
- `create_multiple_answer_question(objective, theory_text, template, stopwords)`: Cria uma questão de resposta múltipla
- `create_assertion_reason_question(objective, theory_text, template, stopwords)`: Cria uma questão de asserção-razão

### RTAgent

Valida a precisão técnica do conteúdo das questões.

**Métodos**:
- `validate_questions(questions, rt_checklist, stopwords)`: Valida tecnicamente as questões
- `validate_single_question(question, rt_checklist, stopwords)`: Valida tecnicamente uma única questão
- `search_external_information(topic)`: Simula uma pesquisa de informações externas
- `generate_validation_report(questions)`: Gera um relatório de validação técnica

### DEAgent

Valida a escrita e estrutura das questões.

**Métodos**:
- `validate_questions(questions, de_checklist, stopwords)`: Valida a escrita e estrutura das questões
- `validate_single_question(question, de_checklist, stopwords)`: Valida a escrita e estrutura de uma única questão
- `check_format_compliance(question)`: Verifica se a questão está em conformidade com o formato esperado
- `generate_validation_report(questions)`: Gera um relatório de validação de design educacional

### ValidatorAgent

Realiza a validação final das questões e gera os documentos de saída.

**Métodos**:
- `validate_questions(questions)`: Realiza a validação final das questões
- `perform_final_validation(question)`: Realiza a validação final de uma única questão
- `generate_development_report(questions)`: Gera um relatório de desenvolvimento do processo
- `generate_final_document(questions)`: Gera o documento final com as questões validadas

## Utilitários

### AIClient

Cliente para interagir com APIs de IA.

**Métodos**:
- `generate_text(prompt, max_tokens)`: Gera texto usando a API de IA
- `create_agent_prompt(agent_type, task_data)`: Cria um prompt para um agente específico

### FileHandler

Utilitários para manipulação de arquivos.

**Métodos**:
- `ensure_dir(directory)`: Garante que o diretório existe
- `read_json(file_path)`: Lê um arquivo JSON
- `write_json(data, file_path, backup)`: Escreve dados em um arquivo JSON
- `read_text(file_path)`: Lê um arquivo de texto
- `write_text(text, file_path, backup)`: Escreve texto em um arquivo
- `list_files(directory, pattern)`: Lista arquivos em um diretório
- `copy_file(source, destination)`: Copia um arquivo
- `save_task_data(task_id, data)`: Salva os dados de uma tarefa
- `load_task_data(task_id)`: Carrega os dados de uma tarefa
- `save_questions(task_id, questions)`: Salva as questões de uma tarefa
- `save_report(task_id, report_type, report_content)`: Salva um relatório
- `save_final_document(task_id, document_content)`: Salva o documento final

### TextProcessor

Utilitários para processamento de texto.

**Métodos**:
- `extract_json_from_text(text)`: Extrai um objeto JSON de um texto
- `extract_markdown_sections(text)`: Extrai seções de um texto em formato Markdown
- `check_restricted_words(text, stopwords)`: Verifica se o texto contém palavras restritivas
- `replace_restricted_words(text, stopwords, replacements)`: Substitui palavras restritivas no texto
- `extract_objectives(text)`: Extrai objetivos de aprendizagem de um texto
- `extract_questions_from_text(text)`: Extrai questões de um texto

## API REST

A API REST fornece endpoints para interagir com o sistema.

### Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | /health | Verifica se a aplicação está funcionando |
| POST | /task | Cria uma nova tarefa |
| GET | /task/{task_id} | Obtém o status de uma tarefa |
| POST | /task/{task_id}/content | Executa o Agente Conteudista |
| POST | /task/{task_id}/rt | Executa o Agente RT |
| POST | /task/{task_id}/de | Executa o Agente DE |
| POST | /task/{task_id}/validator | Executa o Agente Validador |
| POST | /task/{task_id}/run_all | Executa todos os agentes em sequência |
| GET | /task/{task_id}/results | Obtém os resultados finais de uma tarefa |
| POST | /upload | Faz upload de arquivos |

## Integração com APIs de IA

O sistema suporta integração com duas APIs de IA:

1. **DeepSeek**: API em nuvem que requer uma chave de API.
2. **Ollama**: API local que não requer chave de API, mas precisa ter o Ollama instalado.

### Configuração

A configuração da API de IA é feita através das seguintes variáveis de ambiente:

- `AI_PROVIDER`: Define o provedor de IA a ser utilizado (deepseek ou ollama)
- `DEEPSEEK_API_KEY`: Chave de API para o DeepSeek
- `OLLAMA_MODEL`: Modelo a ser utilizado pelo Ollama (padrão: deepseek-coder:6.7b)

### Formato das Requisições

**DeepSeek**:
```json
{
  "model": "deepseek-chat",
  "messages": [
    {"role": "user", "content": "prompt"}
  ],
  "max_tokens": 2000,
  "temperature": 0.7
}
```

**Ollama**:
```json
{
  "model": "deepseek-coder:6.7b",
  "prompt": "prompt",
  "stream": false,
  "options": {
    "num_predict": 2000,
    "temperature": 0.7
  }
}
```

## Testes

O sistema inclui testes automatizados para garantir seu correto funcionamento.

### Tipos de Testes

1. **Testes Unitários**: Testam componentes individuais do sistema.
2. **Testes de Integração**: Testam a interação entre diferentes componentes.
3. **Testes de API**: Testam os endpoints da API REST.

### Execução dos Testes

Para executar todos os testes:

```bash
python run_tests.py
```

Para executar um teste específico:

```bash
python -m unittest tests.test_content_agent
```

## Considerações de Segurança

1. **Autenticação**: O sistema não implementa autenticação por padrão. Em um ambiente de produção, é recomendável adicionar um mecanismo de autenticação.

2. **Validação de Entrada**: O sistema valida as entradas para evitar injeção de código ou outros ataques.

3. **Armazenamento de Dados**: Os dados são armazenados localmente. Em um ambiente de produção, é recomendável utilizar um banco de dados seguro.

4. **Chaves de API**: As chaves de API são armazenadas em variáveis de ambiente para evitar exposição.

## Limitações Conhecidas

1. **Desempenho**: O sistema pode ser lento para processar grandes volumes de questões devido às chamadas à API de IA.

2. **Dependência de APIs Externas**: O sistema depende de APIs externas para funcionar, o que pode causar problemas se essas APIs estiverem indisponíveis.

3. **Qualidade das Questões**: A qualidade das questões geradas depende da qualidade dos objetivos e da fundamentação teórica fornecidos.

## Extensões Futuras

1. **Interface Web**: Adicionar uma interface web para facilitar o uso do sistema.

2. **Mais Tipos de Questões**: Adicionar suporte a mais tipos de questões, como questões dissertativas ou de correspondência.

3. **Integração com LMS**: Integrar o sistema com sistemas de gestão de aprendizagem (LMS) como Moodle ou Canvas.

4. **Melhorias na IA**: Utilizar modelos de IA mais avançados para melhorar a qualidade das questões geradas.

5. **Banco de Dados**: Substituir o armazenamento em arquivos por um banco de dados para melhorar a escalabilidade e a segurança.

## Referências

1. [Flask Documentation](https://flask.palletsprojects.com/)
2. [DeepSeek API Documentation](https://platform.deepseek.com/docs)
3. [Ollama Documentation](https://ollama.ai/docs)
4. [Python Documentation](https://docs.python.org/3/)
5. [Markdown Guide](https://www.markdownguide.org/)

---

© 2025 Manus AI. Todos os direitos reservados.

