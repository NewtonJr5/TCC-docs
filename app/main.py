import asyncio

from app.pipelines.reddit_pipeline import run_pipeline, run_continuous

from fastapi import FastAPI

from app.controller.controller import router as post_router

# async def main():
#     await run_continuous(
#         subreddit="python",
#         pages=3, 
#         interval=5
#     )


# if __name__ == "__main__":
#     asyncio.run(main())

app = FastAPI(
    title="Reddit Pipeline API"
)

app.include_router(
    post_router,
    prefix="/posts"
)