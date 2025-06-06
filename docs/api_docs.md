# Documentação da API - Sistema Multi-Agente para Criação e Validação de Questões

## Visão Geral

A API REST do Sistema Multi-Agente para Criação e Validação de Questões permite interagir com o sistema de forma programática. Esta documentação descreve os endpoints disponíveis, os formatos de requisição e resposta, e exemplos de uso.

## Base URL

```
http://localhost:5000
```

## Autenticação

A API não implementa autenticação por padrão. Em um ambiente de produção, é recomendável adicionar um mecanismo de autenticação.

## Formatos de Resposta

Todas as respostas são retornadas no formato JSON.

## Códigos de Status HTTP

| Código | Descrição |
|--------|-----------|
| 200 | Sucesso |
| 400 | Requisição inválida |
| 404 | Recurso não encontrado |
| 500 | Erro interno do servidor |

## Endpoints

### Verificação de Saúde

#### GET /health

Verifica se a aplicação está funcionando.

**Exemplo de Requisição**:
```bash
curl http://localhost:5000/health
```

**Exemplo de Resposta**:
```json
{
  "status": "ok"
}
```

### Gerenciamento de Tarefas

#### POST /task

Cria uma nova tarefa.

**Parâmetros**:

| Nome | Tipo | Descrição |
|------|------|-----------|
| objectives | string | Objetivos de aprendizagem |
| theory_text | string | Texto de fundamentação teórica |

**Exemplo de Requisição**:
```bash
curl -X POST http://localhost:5000/task \
  -H "Content-Type: application/json" \
  -d '{
    "objectives": "Obj.1: Identificar critérios de qualidade e relevância dos dados.",
    "theory_text": "A qualidade dos dados é fundamental para o sucesso de projetos de ciência de dados."
  }'
```

**Exemplo de Resposta**:
```json
{
  "task_id": "12345678",
  "message": "Tarefa criada com sucesso"
}
```

#### GET /task/{task_id}

Obtém o status de uma tarefa.

**Parâmetros**:

| Nome | Tipo | Descrição |
|------|------|-----------|
| task_id | string | ID da tarefa |

**Exemplo de Requisição**:
```bash
curl http://localhost:5000/task/12345678
```

**Exemplo de Resposta**:
```json
{
  "task_id": "12345678",
  "status": "in_progress",
  "current_agent": "content_agent",
  "questions_count": 1,
  "reports_count": 0
}
```

### Execução de Agentes

#### POST /task/{task_id}/content

Executa o Agente Conteudista.

**Parâmetros**:

| Nome | Tipo | Descrição |
|------|------|-----------|
| task_id | string | ID da tarefa |

**Exemplo de Requisição**:
```bash
curl -X POST http://localhost:5000/task/12345678/content
```

**Exemplo de Resposta**:
```json
{
  "task_id": "12345678",
  "message": "Criadas 1 questões"
}
```

#### POST /task/{task_id}/rt

Executa o Agente Revisor Técnico.

**Parâmetros**:

| Nome | Tipo | Descrição |
|------|------|-----------|
| task_id | string | ID da tarefa |

**Exemplo de Requisição**:
```bash
curl -X POST http://localhost:5000/task/12345678/rt
```

**Exemplo de Resposta**:
```json
{
  "task_id": "12345678",
  "message": "Revisadas 1 questões"
}
```

#### POST /task/{task_id}/de

Executa o Agente Design Educacional.

**Parâmetros**:

| Nome | Tipo | Descrição |
|------|------|-----------|
| task_id | string | ID da tarefa |

**Exemplo de Requisição**:
```bash
curl -X POST http://localhost:5000/task/12345678/de
```

**Exemplo de Resposta**:
```json
{
  "task_id": "12345678",
  "message": "Revisadas 1 questões"
}
```

#### POST /task/{task_id}/validator

Executa o Agente Validador.

**Parâmetros**:

| Nome | Tipo | Descrição |
|------|------|-----------|
| task_id | string | ID da tarefa |

**Exemplo de Requisição**:
```bash
curl -X POST http://localhost:5000/task/12345678/validator
```

**Exemplo de Resposta**:
```json
{
  "task_id": "12345678",
  "message": "Validação concluída. Arquivos salvos: /path/to/questions.json, /path/to/report.md, /path/to/document.md"
}
```

#### POST /task/{task_id}/run_all

Executa todos os agentes em sequência.

**Parâmetros**:

| Nome | Tipo | Descrição |
|------|------|-----------|
| task_id | string | ID da tarefa |

**Exemplo de Requisição**:
```bash
curl -X POST http://localhost:5000/task/12345678/run_all
```

**Exemplo de Resposta**:
```json
{
  "task_id": "12345678",
  "status": "completed",
  "message": "Todos os agentes executados com sucesso",
  "results_path": {
    "questions": "/path/to/questions_12345678.json",
    "report": "/path/to/development_12345678.md",
    "document": "/path/to/final_document_12345678.md"
  }
}
```

### Resultados

#### GET /task/{task_id}/results

Obtém os resultados finais de uma tarefa.

**Parâmetros**:

| Nome | Tipo | Descrição |
|------|------|-----------|
| task_id | string | ID da tarefa |

**Exemplo de Requisição**:
```bash
curl http://localhost:5000/task/12345678/results
```

**Exemplo de Resposta**:
```json
{
  "task_id": "12345678",
  "status": "completed",
  "questions": {
    "questions": [
      {
        "id": "abcd1234",
        "objective_id": "Obj.1",
        "type": "single_answer",
        "context": "A qualidade dos dados é fundamental para o sucesso de projetos de ciência de dados.",
        "statement": "Qual critério é mais importante para garantir resultados confiáveis?",
        "alternatives": [
          {"id": "a", "text": "A completude dos dados", "correct": true},
          {"id": "b", "text": "O tamanho do conjunto de dados", "correct": false},
          {"id": "c", "text": "A fonte dos dados", "correct": false},
          {"id": "d", "text": "O formato de armazenamento", "correct": false},
          {"id": "e", "text": "A idade dos dados", "correct": false}
        ],
        "feedback": {
          "a": "Correta. A completude dos dados é fundamental.",
          "b": "Incorreta. A qualidade é mais importante que a quantidade.",
          "c": "Incorreta. A fonte não é o critério mais relevante.",
          "d": "Incorreta. O formato tem pouca relação com a qualidade.",
          "e": "Incorreta. A idade depende do contexto da análise."
        },
        "validation": {
          "rt": {
            "status": "approved",
            "comments": "O conteúdo está tecnicamente correto.",
            "checklist": {
              "item1": {"result": "sim", "observation": "As questões abordam os conteúdos tratados"}
            }
          },
          "de": {
            "status": "approved",
            "comments": "A questão está bem estruturada.",
            "checklist": {
              "item1": {"result": "sim", "observation": "O texto-base está claro"}
            }
          },
          "final": {
            "status": "approved",
            "comments": "A questão passou por todas as etapas de validação com sucesso."
          }
        }
      }
    ]
  },
  "report": "# Relatório de Desenvolvimento\n\n## Resumo\n\nEste relatório descreve o processo de desenvolvimento e validação de questões educacionais...",
  "document": "# Questões Validadas\n\n## Objetivo 1\n\n### Questão 1 (Resposta Única)\n\n**Contextualização:**\nA qualidade dos dados é fundamental para o sucesso de projetos de ciência de dados..."
}
```

### Upload de Arquivos

#### POST /upload

Faz upload de arquivos.

**Parâmetros**:

| Nome | Tipo | Descrição |
|------|------|-----------|
| file | file | Arquivo a ser enviado |

**Exemplo de Requisição**:
```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@/path/to/local/file.txt"
```

**Exemplo de Resposta**:
```json
{
  "message": "Arquivo file.txt enviado com sucesso",
  "path": "/path/to/file.txt"
}
```

## Modelos de Dados

### Task

```json
{
  "id": "12345678",
  "creation_date": "2023-01-01T00:00:00",
  "objectives": ["Obj.1: Identificar critérios de qualidade e relevância dos dados."],
  "theory_text": "A qualidade dos dados é fundamental para o sucesso de projetos de ciência de dados.",
  "templates": {
    "single_answer": "...",
    "multiple_answer": "...",
    "assertion_reason": "..."
  },
  "stopwords": ["limita-se", "apenas", "somente"],
  "questions": [...],
  "reports": [...],
  "status": "in_progress",
  "current_agent": "content_agent"
}
```

### Question

```json
{
  "id": "abcd1234",
  "objective_id": "Obj.1",
  "type": "single_answer",
  "context": "A qualidade dos dados é fundamental para o sucesso de projetos de ciência de dados.",
  "statement": "Qual critério é mais importante para garantir resultados confiáveis?",
  "alternatives": [
    {"id": "a", "text": "A completude dos dados", "correct": true},
    {"id": "b", "text": "O tamanho do conjunto de dados", "correct": false},
    {"id": "c", "text": "A fonte dos dados", "correct": false},
    {"id": "d", "text": "O formato de armazenamento", "correct": false},
    {"id": "e", "text": "A idade dos dados", "correct": false}
  ],
  "feedback": {
    "a": "Correta. A completude dos dados é fundamental.",
    "b": "Incorreta. A qualidade é mais importante que a quantidade.",
    "c": "Incorreta. A fonte não é o critério mais relevante.",
    "d": "Incorreta. O formato tem pouca relação com a qualidade.",
    "e": "Incorreta. A idade depende do contexto da análise."
  },
  "metadata": {
    "created_by": "content_agent",
    "last_modified_by": "validator_agent",
    "creation_date": "2023-01-01T00:00:00",
    "last_modified": "2023-01-01T01:00:00"
  },
  "validation": {
    "rt": {
      "status": "approved",
      "comments": "O conteúdo está tecnicamente correto.",
      "checklist": {
        "item1": {"result": "sim", "observation": "As questões abordam os conteúdos tratados"}
      }
    },
    "de": {
      "status": "approved",
      "comments": "A questão está bem estruturada.",
      "checklist": {
        "item1": {"result": "sim", "observation": "O texto-base está claro"}
      }
    },
    "final": {
      "status": "approved",
      "comments": "A questão passou por todas as etapas de validação com sucesso."
    }
  }
}
```

### Report

```json
{
  "id": "efgh5678",
  "type": "development_report",
  "creation_date": "2023-01-01T01:00:00",
  "agent": "validator_agent",
  "content": {
    "summary": "Este relatório descreve o processo de desenvolvimento e validação de questões educacionais.",
    "steps": [
      {
        "agent": "content_agent",
        "description": "O Agente Conteudista foi responsável pela criação inicial das questões.",
        "observations": "As questões criadas seguiram o template fornecido."
      },
      {
        "agent": "rt_agent",
        "description": "O Agente RT validou a precisão técnica do conteúdo das questões.",
        "observations": "Todas as questões foram aprovadas pelo RT."
      },
      {
        "agent": "de_agent",
        "description": "O Agente DE validou a estrutura e qualidade pedagógica das questões.",
        "observations": "As questões foram aprovadas pelo DE."
      }
    ],
    "recommendations": [
      "Incluir exemplos específicos de questões bem elaboradas para cada tipo.",
      "Fornecer diretrizes mais detalhadas sobre como elaborar feedbacks construtivos.",
      "Incluir orientações sobre como adaptar as questões para diferentes níveis de dificuldade."
    ]
  }
}
```

## Tratamento de Erros

### Formato de Erro

```json
{
  "error": "Mensagem de erro"
}
```

### Exemplos de Erros

#### Requisição Inválida

```json
{
  "error": "Objetivos e fundamentação teórica são obrigatórios"
}
```

#### Recurso Não Encontrado

```json
{
  "error": "Tarefa 12345678 não encontrada"
}
```

#### Erro Interno do Servidor

```json
{
  "error": "Erro ao criar questões"
}
```

## Limitações da API

1. **Rate Limiting**: A API não implementa rate limiting por padrão. Em um ambiente de produção, é recomendável adicionar um mecanismo de rate limiting.

2. **Tamanho das Requisições**: O tamanho máximo das requisições é limitado pelo servidor web. Requisições muito grandes podem ser rejeitadas.

3. **Tempo de Resposta**: As operações que envolvem chamadas à API de IA podem levar algum tempo para serem concluídas.

## Exemplos de Uso

### Fluxo Completo

```bash
# 1. Criar uma tarefa
curl -X POST http://localhost:5000/task \
  -H "Content-Type: application/json" \
  -d '{
    "objectives": "Obj.1: Identificar critérios de qualidade e relevância dos dados.",
    "theory_text": "A qualidade dos dados é fundamental para o sucesso de projetos de ciência de dados."
  }'

# Resposta: {"task_id": "12345678", "message": "Tarefa criada com sucesso"}

# 2. Executar todos os agentes em sequência
curl -X POST http://localhost:5000/task/12345678/run_all

# Resposta: {"task_id": "12345678", "status": "completed", "message": "Todos os agentes executados com sucesso", ...}

# 3. Obter os resultados finais
curl http://localhost:5000/task/12345678/results

# Resposta: {"task_id": "12345678", "status": "completed", "questions": {...}, "report": "...", "document": "..."}
```

### Execução Passo a Passo

```bash
# 1. Criar uma tarefa
curl -X POST http://localhost:5000/task \
  -H "Content-Type: application/json" \
  -d '{
    "objectives": "Obj.1: Identificar critérios de qualidade e relevância dos dados.",
    "theory_text": "A qualidade dos dados é fundamental para o sucesso de projetos de ciência de dados."
  }'

# Resposta: {"task_id": "12345678", "message": "Tarefa criada com sucesso"}

# 2. Executar o Agente Conteudista
curl -X POST http://localhost:5000/task/12345678/content

# Resposta: {"task_id": "12345678", "message": "Criadas 1 questões"}

# 3. Executar o Agente RT
curl -X POST http://localhost:5000/task/12345678/rt

# Resposta: {"task_id": "12345678", "message": "Revisadas 1 questões"}

# 4. Executar o Agente DE
curl -X POST http://localhost:5000/task/12345678/de

# Resposta: {"task_id": "12345678", "message": "Revisadas 1 questões"}

# 5. Executar o Agente Validador
curl -X POST http://localhost:5000/task/12345678/validator

# Resposta: {"task_id": "12345678", "message": "Validação concluída. Arquivos salvos: ..."}

# 6. Obter os resultados finais
curl http://localhost:5000/task/12345678/results

# Resposta: {"task_id": "12345678", "status": "completed", "questions": {...}, "report": "...", "document": "..."}
```

## Suporte

Para obter suporte ou relatar problemas com a API, entre em contato com a equipe de desenvolvimento ou abra uma issue no repositório do projeto.

---

© 2025 Manus AI. Todos os direitos reservados.

