app/
│
├── main.py
│
├── core/
│   ├── config.py
│   └── logging.py
│
├── db/
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
│   ├── reddit/
│   │   ├── client.py
│   │   ├── posts.py
│   │   └── comments.py
│   │
│   ├── twitter/
│   └── youtube/
│
├── services/
│   ├── post_service.py
│   ├── embedding_service.py
│   └── pipeline_service.py
│
├── pipelines/
│   └── reddit_pipeline.py
│
├── schemas/
│   ├── post.py
│   └── comment.py
│
└── utils/
    ├── helpers.py
    └── constants.py