import asyncio
import httpx
import os
import logging

logger = logging.getLogger(__name__)


async def self_ping_loop():
    """
    Keeps the HF Space alive by pinging its own /health/ping endpoint
    every 10 minutes. Starts after a 30-second grace period to let
    the server fully boot before the first ping.
    """
    await asyncio.sleep(30)

    app_url = os.getenv("APP_URL", "").rstrip("/")
    if not app_url:
        logger.warning("APP_URL not set — self-ping keep-alive disabled.")
        return

    logger.info(f"Self-ping keep-alive started → {app_url}/health/ping (every 10 min)")

    while True:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(f"{app_url}/health/ping")
                logger.info(f"Self-ping OK: {r.status_code}")
        except Exception as e:
            logger.warning(f"Self-ping failed: {e}")

        await asyncio.sleep(600)  # 10 minutes
