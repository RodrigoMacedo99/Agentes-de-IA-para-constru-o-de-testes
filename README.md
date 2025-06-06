# Sistema Multi-Agente para Criação e Validação de Questões

Um sistema baseado em múltiplos agentes especializados para automatizar o processo de criação, revisão e validação de questões educacionais.

## Visão Geral

O Sistema Multi-Agente para Criação e Validação de Questões utiliza uma abordagem baseada em múltiplos agentes especializados para criar questões educacionais de alta qualidade. O sistema é composto por cinco agentes:

1. **Agente Gerenciador**: Coordena o fluxo de trabalho entre os demais agentes.
2. **Agente Conteudista**: Cria questões com base nos objetivos e fundamentação teórica.
3. **Agente Revisor Técnico (RT)**: Valida a precisão técnica do conteúdo das questões.
4. **Agente Design Educacional (DE)**: Valida a escrita e estrutura das questões.
5. **Agente Validador**: Realiza a validação final das questões e gera os documentos de saída.

## Características

- Criação automatizada de questões educacionais
- Validação técnica e pedagógica das questões
- Suporte a múltiplos tipos de questões (resposta única, resposta múltipla, asserção-razão)
- Integração com APIs de IA (DeepSeek, Ollama)
- API REST para interação programática
- Geração de relatórios e documentos finais

## Requisitos

- Python 3.8 ou superior
- Dependências listadas em `requirements.txt`
- Acesso à internet (para APIs de IA)

## Instalação Rápida

```bash
# Clonar o repositório
git clone https://github.com/seu-usuario/multi-agent-system.git
cd multi-agent-system

# Instalar as dependências
pip install -r requirements.txt

# Configurar as variáveis de ambiente
export DEEPSEEK_API_KEY="sua-chave-api"  # Opcional
export AI_PROVIDER="deepseek"  # ou "ollama" para execução local

# Iniciar o servidor
python app.py
```

Para instruções detalhadas, consulte o [Guia de Instalação](docs/installation_guide.md).

## Uso Básico

### Iniciar o Servidor

```bash
python app.py
```

O servidor será iniciado em `http://0.0.0.0:5000`.

### Criar uma Nova Tarefa

```bash
curl -X POST http://localhost:5000/task \
  -H "Content-Type: application/json" \
  -d '{
    "objectives": "Obj.1: Identificar critérios de qualidade e relevância dos dados.",
    "theory_text": "A qualidade dos dados é fundamental para o sucesso de projetos de ciência de dados."
  }'
```

### Executar o Fluxo Completo

```bash
curl -X POST http://localhost:5000/task/12345678/run_all
```

Para instruções detalhadas, consulte o [Guia do Usuário](docs/user_guide.md).

## Documentação

- [Guia do Usuário](docs/user_guide.md)
- [Guia Técnico](docs/technical_guide.md)
- [Documentação da API](docs/api_docs.md)
- [Guia de Instalação](docs/installation_guide.md)

## Estrutura do Projeto

```
multi-agent-system/
├── app.py                  # Ponto de entrada da aplicação
├── config.py               # Configurações do sistema
├── requirements.txt        # Dependências do projeto
├── README.md               # Documentação do projeto
├── agents/                 # Módulos dos agentes
├── models/                 # Modelos de dados
├── utils/                  # Utilitários
├── templates/              # Templates para questões
├── data/                   # Dados de entrada e saída
├── tests/                  # Testes automatizados
└── docs/                   # Documentação
```

## Contribuição

Contribuições são bem-vindas! Por favor, siga estas etapas:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das suas alterações (`git commit -am 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.



