# Estrutura do Projeto

Projeto de pipeline para coleta e consulta de dados de conteúdo digital.

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
│   ├── create_tables.py
│   └── recreate_tables.py
│
├── models/
│   ├── post.py
│   ├── canal.py
│   ├── categoria.py
│   └── plataforma.py
│
├── repositories/
│   ├── post_repository.py
│   ├── canal_repository.py
│   ├── categoria_repository.py
│   └── plataforma_repository.py
│
├── scrapper/
│   ├── extrator.py
│   └── youtube/
│       └── extrator_youtube.py
│
├── services/
│   ├── post_service.py
│   └── youtube_service.py
│
├── pipelines/
│   └── ...
│
└── utils/
```

## Descrição dos diretórios

| Diretório | Descrição |
|-----------|-----------|
| **database/** | Responsável pela conexão com o banco de dados, definição da base dos modelos e criação das tabelas. |
| **models/** | Contém os modelos de dados (ORM), responsáveis pelo mapeamento entre as tabelas do banco de dados e os objetos da aplicação. |
| **repositories/** | Implementa a camada de acesso aos dados, concentrando operações de consulta, inserção, atualização e remoção. |
| **scrapper/** | Responsável pela coleta de dados das plataformas monitoradas. Cada plataforma possui uma implementação independente. |
| **services/** | Contém a lógica de negócio da aplicação, realizando o processamento dos dados obtidos pelos scrappers e coordenando as operações do sistema. |
| **pipelines/** | Implementa os fluxos de coleta e processamento de dados. |
| **main.py** | Ponto de entrada da aplicação, responsável por iniciar a API FastAPI. |

# Como executar o projeto

## Pré-requisitos

Antes de iniciar, certifique-se de ter instalado:

- Python 3.10 ou superior
- PostgreSQL
- Git

# 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd pipeline_reddit
```

# 2. Subir os containers Docker

Certifique-se de que o Docker Desktop esteja em execução e, na raiz do projeto, execute:

```bash
docker compose up -d
```

Para verificar se os containers estão em execução:

```bash
docker ps
```

Para visualizar os logs (opcional):

```bash
docker compose logs -f
```

# 3. Criar o ambiente virtual

## Windows

```bash
python -m venv .venv
```

## Linux/macOS

```bash
python3 -m venv .venv
```

# 4. Ativar o ambiente virtual

## Windows (PowerShell)

```bash
.venv\Scripts\Activate.ps1
```

## Windows (CMD)

```bash
.venv\Scripts\activate.bat
```

## Linux/macOS

```bash
source .venv/bin/activate
```

Após a ativação, o terminal deverá exibir:

```text
(.venv)
```

# 5. Instalar as dependências

```bash
pip install -r requirements.txt
```

# 6. Configurar as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as informações necessárias.

Exemplo:

```env
DATABASE_URL=postgresql+asyncpg://usuario:senha@localhost:5432/nome_do_banco

API_KEY_YOUTUBE=sua_chave
```

Caso contrário, execute o script SQL de criação das tabelas.

# 8. Executar a aplicação

```bash
python -m uvicorn app.main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

# 9. Acessar a documentação

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

# Encerrando a aplicação

Para interromper a API:

```text
CTRL + C
```

Para parar os containers Docker:

```bash
docker compose down
```

Se desejar remover também os volumes (apagando os dados persistidos do banco):

```bash
docker compose down -v
```