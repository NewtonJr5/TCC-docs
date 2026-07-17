# Estrutura do Projeto

```text
app/
│
├── main.py
│
├── controller/
│   └── controller.py
│
├── database/
│   ├── connection.py
│   ├── base.py
│   └── create_tables.py
│
├── models/
│   ├── post.py
│   ├── comment.py
│   ├── canal.py
│   ├── categoria.py
│   └── plataforma.py
│
├── repositories/
│   ├── post_repository.py
│   ├── comment_repository.py
│   └── ...
│
├── scrapers/
│
├── services/
│   └──  post_service.py
│
├── pipelines/
│   └── reddit_pipeline.py
│
└── utils/
```

## Descrição dos diretórios

| Diretório | Descrição |
|-----------|-----------|
| **core/** | Configurações gerais da aplicação, como variáveis de ambiente, configurações e sistema de logs. |
| **db/** | Responsável pela conexão com o banco de dados, definição da base dos modelos e criação das tabelas. |
| **models/** | Contém os modelos de dados (ORM), responsáveis pelo mapeamento entre as tabelas do banco de dados e os objetos da aplicação. |
| **repositories/** | Implementa a camada de acesso aos dados, concentrando operações de consulta, inserção, atualização e remoção. |
| **scrapers/** | Responsável pela coleta de dados das plataformas monitoradas. Cada plataforma possui uma implementação independente. |
| **services/** | Contém a lógica de negócio da aplicação, realizando o processamento dos dados obtidos pelos scrapers e coordenando as operações do sistema. |
| **pipelines/** | Implementa os fluxos completos de coleta e processamento de dados para cada plataforma. |
| **schemas/** | Define os esquemas de validação e serialização dos dados utilizados pela API. |
| **utils/** | Armazena funções auxiliares, constantes e utilitários compartilhados entre os módulos do sistema. |
| **main.py** | Ponto de entrada da aplicação, responsável por inicializar a API e registrar as configurações necessárias. |

# Como executar o projeto

## Pré-requisitos

Antes de iniciar, certifique-se de ter instalado:

- Python 3.10 ou superior
- PostgreSQL
- Git

## 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd pipeline_reddit
```

## 2. Criar o ambiente virtual

### Windows

```bash
python -m venv .venv
```

### Linux/macOS

```bash
python3 -m venv .venv
```

## 3. Ativar o ambiente virtual

### Windows (PowerShell)

```bash
.venv\Scripts\Activate.ps1
```

### Windows (CMD)

```bash
.venv\Scripts\activate.bat
```

### Linux/macOS

```bash
source .venv/bin/activate
```

Após a ativação, o terminal deverá exibir:

```text
(.venv)
```

## 4. Instalar as dependências

```bash
pip install -r requirements.txt
```

## 5. Configurar as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as informações necessárias.

Exemplo:

```env
DATABASE_URL=postgresql+asyncpg://usuario:senha@localhost:5432/nome_do_banco

YOUTUBE_API_KEY=sua_chave
```

## 6. Criar o banco de dados

Crie um banco PostgreSQL e configure a variável `DATABASE_URL` para apontar para ele.

Caso o projeto utilize migrações com Alembic:

```bash
alembic upgrade head
```

Caso contrário, execute o script SQL de criação das tabelas.

## 7. Executar a aplicação

```bash
python -m uvicorn app.main:app --reload
```

A API ficará disponível em:

```
http://127.0.0.1:8000
```

## 8. Acessar a documentação

Swagger UI:

```
http://127.0.0.1:8000/docs
```

ReDoc:

```
http://127.0.0.1:8000/redoc
```

## Encerrando a aplicação

Para interromper o servidor, pressione:

```text
CTRL + C
```