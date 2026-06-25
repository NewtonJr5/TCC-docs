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