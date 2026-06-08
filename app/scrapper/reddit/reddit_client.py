import asyncio
import random
from httpx import AsyncClient, HTTPStatusError, TimeoutException

# ---------------------------------------------------------------------------
# User-Agent pool – rotaciona a cada requisição para reduzir fingerprinting
# ---------------------------------------------------------------------------
_USER_AGENTS = [
    (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    ),
    (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/136.0.0.0 Safari/537.36"
    ),
    (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/135.0.0.0 Safari/537.36"
    ),
    (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) "
        "Gecko/20100101 Firefox/126.0"
    ),
    (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/17.4 Safari/605.1.15"
    ),
]

# ---------------------------------------------------------------------------
# Semáforo global – limita requisições simultâneas ao Reddit
# ---------------------------------------------------------------------------
REQUEST_SEMAPHORE = asyncio.Semaphore(3)

# ---------------------------------------------------------------------------
# Cliente base (sem User-Agent fixo – é injetado por request em posts.py)
# ---------------------------------------------------------------------------
_BASE_HEADERS = {
    "Accept": "application/json,text/html,*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.reddit.com/",
}

client = AsyncClient(
    headers=_BASE_HEADERS,
    follow_redirects=True,
    timeout=15.0,
)


def random_user_agent() -> str:
    """Retorna um User-Agent aleatório do pool."""
    return random.choice(_USER_AGENTS)


def random_delay(min_s: float = 1.0, max_s: float = 3.5) -> float:
    """Gera um delay aleatório (segundos) para simular comportamento humano."""
    return random.uniform(min_s, max_s)