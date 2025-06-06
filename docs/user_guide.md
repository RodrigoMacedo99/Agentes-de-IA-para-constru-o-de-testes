# Guia do Usuário - Sistema Multi-Agente para Criação e Validação de Questões

## Introdução

O Sistema Multi-Agente para Criação e Validação de Questões é uma ferramenta projetada para automatizar o processo de criação, revisão e validação de questões educacionais. Utilizando uma abordagem baseada em múltiplos agentes especializados, o sistema garante que as questões criadas sejam de alta qualidade, tecnicamente precisas e pedagogicamente adequadas.

Este guia fornece instruções detalhadas sobre como utilizar o sistema, desde a instalação até a obtenção dos resultados finais.

## Visão Geral do Sistema

O sistema é composto por cinco agentes especializados:

1. **Agente Gerenciador**: Coordena o fluxo de trabalho entre os demais agentes.
2. **Agente Conteudista**: Cria questões com base nos objetivos e fundamentação teórica.
3. **Agente Revisor Técnico (RT)**: Valida a precisão técnica do conteúdo das questões.
4. **Agente Design Educacional (DE)**: Valida a escrita e estrutura das questões.
5. **Agente Validador**: Realiza a validação final das questões e gera os documentos de saída.

## Requisitos do Sistema

- Python 3.8 ou superior
- Dependências listadas em `requirements.txt`
- Acesso à internet (para APIs de IA)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/multi-agent-system.git
cd multi-agent-system
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
```bash
export DEEPSEEK_API_KEY="sua-chave-api"  # Opcional
export AI_PROVIDER="deepseek"  # ou "ollama" para execução local
export DEBUG="True"  # Para ambiente de desenvolvimento
```

## Configuração

### Configuração da API de IA

O sistema suporta duas opções de API de IA:

1. **DeepSeek**: API em nuvem (requer chave de API)
2. **Ollama**: Execução local de modelos de IA (não requer chave de API, mas precisa ter o Ollama instalado)

Para configurar a API de IA, defina a variável de ambiente `AI_PROVIDER` como `deepseek` ou `ollama`.

Se estiver usando o DeepSeek, defina também a variável de ambiente `DEEPSEEK_API_KEY` com sua chave de API.

### Arquivos de Configuração

Os principais arquivos de configuração são:

- `config.py`: Configurações gerais do sistema
- `templates/`: Templates para os diferentes tipos de questão
- `data/stopwords.txt`: Lista de palavras a serem evitadas nas questões

## Uso Básico

### Iniciar o Servidor

```bash
python app.py
```

O servidor será iniciado em `http://0.0.0.0:5000`.

### Criar uma Nova Tarefa

Para criar uma nova tarefa, envie uma requisição POST para `/task` com os seguintes dados:

```json
{
  "objectives": "Obj.1: Identificar critérios de qualidade e relevância dos dados, como completude, consistência e ausência de vieses.",
  "theory_text": "A qualidade dos dados é fundamental para o sucesso de projetos de ciência de dados e análise. Dados de alta qualidade são caracterizados por sua precisão, completude, consistência e relevância para o problema em questão."
}
```

Exemplo usando curl:

```bash
curl -X POST http://localhost:5000/task \
  -H "Content-Type: application/json" \
  -d '{"objectives": "Obj.1: Identificar critérios de qualidade e relevância dos dados.", "theory_text": "A qualidade dos dados é fundamental para o sucesso de projetos de ciência de dados."}'
```

A resposta será algo como:

```json
{
  "task_id": "12345678",
  "message": "Tarefa criada com sucesso"
}
```

### Executar o Fluxo Completo

Para executar todos os agentes em sequência, envie uma requisição POST para `/task/{task_id}/run_all`:

```bash
curl -X POST http://localhost:5000/task/12345678/run_all
```

A resposta será algo como:

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

### Executar Agentes Individualmente

Se preferir, você pode executar cada agente individualmente:

1. **Agente Conteudista**:
```bash
curl -X POST http://localhost:5000/task/12345678/content
```

2. **Agente RT**:
```bash
curl -X POST http://localhost:5000/task/12345678/rt
```

3. **Agente DE**:
```bash
curl -X POST http://localhost:5000/task/12345678/de
```

4. **Agente Validador**:
```bash
curl -X POST http://localhost:5000/task/12345678/validator
```

### Obter o Status da Tarefa

Para verificar o status atual da tarefa:

```bash
curl http://localhost:5000/task/12345678
```

A resposta será algo como:

```json
{
  "task_id": "12345678",
  "status": "in_progress",
  "current_agent": "content_agent",
  "questions_count": 1,
  "reports_count": 0
}
```

### Obter os Resultados Finais

Para obter os resultados finais da tarefa:

```bash
curl http://localhost:5000/task/12345678/results
```

A resposta incluirá as questões validadas, o relatório de desenvolvimento e o documento final.

## Tipos de Questões Suportados

O sistema suporta três tipos de questões:

1. **Resposta Única**: Questões com uma única alternativa correta.
2. **Resposta Múltipla**: Questões com múltiplas afirmativas, onde o aluno deve identificar quais são verdadeiras.
3. **Asserção-Razão**: Questões com duas asserções relacionadas por uma relação de causa e efeito.

## Formatos de Saída

Os resultados são disponibilizados em três formatos:

1. **JSON**: Contém todas as questões validadas com seus metadados.
2. **Markdown (Relatório)**: Relatório de desenvolvimento explicando o processo.
3. **Markdown (Documento Final)**: Documento final com todas as questões validadas, formatado para fácil leitura.

## Solução de Problemas

### Problemas Comuns

1. **Erro de Autenticação da API**:
   - Verifique se a variável de ambiente `DEEPSEEK_API_KEY` está configurada corretamente.

2. **Erro ao Criar Questões**:
   - Verifique se os objetivos e a fundamentação teórica são suficientemente detalhados.
   - Verifique se há conectividade com a internet.

3. **Questões Rejeitadas na Validação**:
   - Verifique os logs para identificar os motivos da rejeição.
   - Ajuste os objetivos ou a fundamentação teórica para fornecer mais contexto.

### Logs

Os logs do sistema são armazenados em `logs/app.log`. Consulte-os para obter informações detalhadas sobre erros ou problemas.

## Exemplos

### Exemplo 1: Criação de Questão de Resposta Única

**Objetivo**:
```
Obj.1: Identificar critérios de qualidade e relevância dos dados, como completude, consistência e ausência de vieses.
```

**Fundamentação Teórica**:
```
A qualidade dos dados é fundamental para o sucesso de projetos de ciência de dados e análise. Dados de alta qualidade são caracterizados por sua precisão, completude, consistência e relevância para o problema em questão.
```

**Questão Gerada**:
```
Contextualização:
A qualidade dos dados é fundamental para o sucesso de projetos de ciência de dados e análise. Dados de alta qualidade são caracterizados por sua precisão, completude, consistência e relevância para o problema em questão.

Enunciado:
Ao avaliar a qualidade de um conjunto de dados para um projeto de análise, qual dos seguintes critérios é mais importante para garantir resultados confiáveis?

Alternativas:
a) A completude dos dados, garantindo que não existam valores ausentes que possam comprometer a análise
b) O tamanho do conjunto de dados, priorizando sempre a maior quantidade possível de registros
c) A fonte dos dados, dando preferência para dados coletados internamente pela organização
d) O formato de armazenamento dos dados, priorizando formatos proprietários mais seguros
e) A idade dos dados, utilizando principalmente dados históricos para análises preditivas

Feedback:
a) Correta. A completude dos dados é um critério fundamental de qualidade, pois valores ausentes podem distorcer análises e levar a conclusões incorretas. Dados completos permitem análises mais precisas e confiáveis.
b) Incorreta. Embora o tamanho do conjunto de dados seja relevante, a qualidade é mais importante que a quantidade. Um conjunto de dados grande, mas com problemas de qualidade, pode levar a resultados menos confiáveis que um conjunto menor e de alta qualidade.
c) Incorreta. A fonte dos dados é importante, mas não é o critério mais relevante para a qualidade. Dados externos podem ser tão ou mais valiosos que dados internos, dependendo do contexto e da confiabilidade da fonte.
d) Incorreta. O formato de armazenamento tem pouca relação com a qualidade intrínseca dos dados. Formatos abertos podem ser tão seguros e úteis quanto formatos proprietários, e a escolha depende mais das necessidades de processamento.
e) Incorreta. A idade dos dados deve ser avaliada conforme o contexto da análise. Dados recentes podem ser mais relevantes para muitas análises, enquanto dados históricos são essenciais para análises de tendências ou sazonalidade.
```

## Suporte

Para obter suporte ou relatar problemas, entre em contato com a equipe de desenvolvimento ou abra uma issue no repositório do projeto.

## Próximos Passos

- Implementação de interface web para facilitar o uso do sistema
- Suporte a mais tipos de questões
- Integração com sistemas de gestão de aprendizagem (LMS)

---

© 2025 Manus AI. Todos os direitos reservados.

