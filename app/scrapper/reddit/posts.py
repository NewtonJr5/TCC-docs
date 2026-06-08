import asyncio
import logging

from .reddit_client import client, random_user_agent, random_delay, REQUEST_SEMAPHORE

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuração de retry
# ---------------------------------------------------------------------------
MAX_RETRIES = 4
BACKOFF_BASE = 2.0          # segundos – dobra a cada tentativa
RETRY_ON_STATUS = {429, 500, 502, 503, 504}


async def fetch_subreddit(subreddit: str, after: str | None = None) -> dict:
    """
    Busca uma página de posts de um subreddit.

    Proteções contra bloqueio do Reddit:
    - Rotação de User-Agent a cada chamada
    - Delay aleatório antes da requisição
    - Retry com backoff exponencial em erros transitórios
    - Semáforo global para controlar concorrência
    """
    url = f"https://www.reddit.com/r/{subreddit}.json"
    params = {"limit": 25}
    if after:
        params["after"] = after

    for attempt in range(1, MAX_RETRIES + 1):
        # Delay aleatório antes de cada tentativa (humano-like)
        delay = random_delay(
            min_s=1.0 * attempt,
            max_s=3.5 * attempt,
        )
        logger.debug("[%s] Aguardando %.1fs antes da tentativa %d/%d", subreddit, delay, attempt, MAX_RETRIES)
        await asyncio.sleep(delay)

        async with REQUEST_SEMAPHORE:
            try:
                response = await client.get(
                    url,
                    params=params,
                    headers={"User-Agent": random_user_agent()},
                )

                logger.debug("[%s] Status %d (tentativa %d)", subreddit, response.status_code, attempt)

                if response.status_code in RETRY_ON_STATUS:
                    backoff = BACKOFF_BASE ** attempt
                    logger.warning(
                        "[%s] HTTP %d – aguardando %.1fs antes de retentar (tentativa %d/%d)",
                        subreddit, response.status_code, backoff, attempt, MAX_RETRIES,
                    )
                    await asyncio.sleep(backoff)
                    continue

                response.raise_for_status()
                return response.json()

            except asyncio.TimeoutError:
                backoff = BACKOFF_BASE ** attempt
                logger.warning("[%s] Timeout – tentativa %d/%d, aguardando %.1fs", subreddit, attempt, MAX_RETRIES, backoff)
                await asyncio.sleep(backoff)

            except Exception as exc:
                logger.error("[%s] Erro inesperado na tentativa %d: %r", subreddit, attempt, exc)
                if attempt == MAX_RETRIES:
                    raise
                await asyncio.sleep(BACKOFF_BASE ** attempt)

    raise RuntimeError(f"fetch_subreddit falhou após {MAX_RETRIES} tentativas para r/{subreddit}")