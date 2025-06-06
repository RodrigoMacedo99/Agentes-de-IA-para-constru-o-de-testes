# Guia de Instalação - Sistema Multi-Agente para Criação e Validação de Questões

Este guia fornece instruções detalhadas para instalar e configurar o Sistema Multi-Agente para Criação e Validação de Questões.

## Requisitos do Sistema

### Requisitos de Hardware

- CPU: 2 núcleos ou mais
- RAM: 4GB ou mais
- Espaço em disco: 1GB ou mais

### Requisitos de Software

- Sistema operacional: Linux, macOS ou Windows
- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)
- Git (opcional, para clonar o repositório)

## Instalação

### 1. Obter o Código-Fonte

Existem duas maneiras de obter o código-fonte do sistema:

#### Opção 1: Clonar o Repositório Git

```bash
git clone https://github.com/seu-usuario/multi-agent-system.git
cd multi-agent-system
```

#### Opção 2: Baixar o Arquivo ZIP

1. Baixe o arquivo ZIP do repositório
2. Extraia o arquivo ZIP
3. Navegue até o diretório extraído

```bash
unzip multi-agent-system.zip
cd multi-agent-system
```

### 2. Criar um Ambiente Virtual (Recomendado)

É recomendável criar um ambiente virtual para isolar as dependências do projeto.

#### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar as Variáveis de Ambiente

#### Linux/macOS

```bash
export DEEPSEEK_API_KEY="sua-chave-api"  # Opcional
export AI_PROVIDER="deepseek"  # ou "ollama" para execução local
export DEBUG="True"  # Para ambiente de desenvolvimento
```

#### Windows

```bash
set DEEPSEEK_API_KEY=sua-chave-api
set AI_PROVIDER=deepseek
set DEBUG=True
```

Alternativamente, você pode criar um arquivo `.env` na raiz do projeto:

```
DEEPSEEK_API_KEY=sua-chave-api
AI_PROVIDER=deepseek
DEBUG=True
```

### 5. Configurar o Ollama (Opcional)

Se você optar por usar o Ollama como provedor de IA, siga estas etapas:

1. Instale o Ollama seguindo as instruções em [ollama.ai](https://ollama.ai)
2. Baixe o modelo DeepSeek:

```bash
ollama pull deepseek-coder:6.7b
```

3. Configure o sistema para usar o Ollama:

```bash
export AI_PROVIDER="ollama"
export OLLAMA_MODEL="deepseek-coder:6.7b"
```

### 6. Verificar a Instalação

Para verificar se a instalação foi bem-sucedida, execute os testes:

```bash
python run_tests.py
```

## Configuração

### Estrutura de Diretórios

Certifique-se de que a estrutura de diretórios esteja correta:

```
multi-agent-system/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── agents/
├── models/
├── utils/
├── templates/
├── data/
│   ├── input/
│   └── output/
├── tests/
└── docs/
```

### Configuração do Servidor

Por padrão, o servidor é configurado para executar em `0.0.0.0:5000`. Para alterar esta configuração, edite o arquivo `config.py` ou defina as variáveis de ambiente:

```bash
export HOST="127.0.0.1"
export PORT="8080"
```

### Configuração de Logging

Os logs são armazenados em `logs/app.log`. Para alterar o nível de logging, edite o arquivo `config.py` ou defina a variável de ambiente:

```bash
export LOG_LEVEL="DEBUG"  # ou "INFO", "WARNING", "ERROR", "CRITICAL"
```

## Inicialização

### Iniciar o Servidor

```bash
python app.py
```

O servidor será iniciado e estará disponível no endereço configurado (por padrão, `http://0.0.0.0:5000`).

### Verificar o Status do Servidor

Para verificar se o servidor está funcionando corretamente, acesse o endpoint de verificação de saúde:

```bash
curl http://localhost:5000/health
```

A resposta deve ser:

```json
{
  "status": "ok"
}
```

## Solução de Problemas

### Problemas Comuns

#### 1. Erro ao Instalar Dependências

**Problema**: Erro ao instalar as dependências listadas em `requirements.txt`.

**Solução**:
- Verifique se você está usando uma versão compatível do Python (3.8 ou superior)
- Atualize o pip: `pip install --upgrade pip`
- Instale as dependências uma a uma para identificar qual está causando o problema

#### 2. Erro de Conexão com a API de IA

**Problema**: Erro ao conectar-se à API de IA.

**Solução**:
- Verifique se a chave de API está configurada corretamente
- Verifique se há conectividade com a internet
- Se estiver usando o Ollama, verifique se o serviço está em execução

#### 3. Erro ao Iniciar o Servidor

**Problema**: Erro ao iniciar o servidor.

**Solução**:
- Verifique se a porta configurada está disponível
- Verifique se você tem permissão para vincular à porta configurada
- Verifique os logs para obter mais informações sobre o erro

### Logs

Os logs do sistema são armazenados em `logs/app.log`. Consulte-os para obter informações detalhadas sobre erros ou problemas.

## Atualização

Para atualizar o sistema para uma nova versão:

1. Faça backup dos seus dados:

```bash
cp -r data/output data/output_backup
```

2. Atualize o código-fonte:

```bash
git pull  # Se você clonou o repositório
```

Ou baixe e extraia a nova versão.

3. Atualize as dependências:

```bash
pip install -r requirements.txt
```

4. Execute os testes para verificar se tudo está funcionando corretamente:

```bash
python run_tests.py
```

## Desinstalação

Para desinstalar o sistema:

1. Pare o servidor (se estiver em execução)
2. Remova o diretório do projeto:

```bash
rm -rf multi-agent-system
```

3. Remova o ambiente virtual (se tiver criado um):

```bash
rm -rf venv
```

## Próximos Passos

Após a instalação e configuração, consulte o [Guia do Usuário](user_guide.md) para aprender a usar o sistema.

---

© 2025 Manus AI. Todos os direitos reservados.

