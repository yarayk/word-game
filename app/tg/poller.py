import asyncio
import logging
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.web.app import Application

logger = logging.getLogger(__name__)


class Poller:
    def __init__(self, app: "Application"):
        self.app = app
        self._task: Optional[asyncio.Task] = None
        self._offset: int = 0

    async def start(self) -> None:
        await self.app.store.tg_client.start()
        self._task = asyncio.create_task(self._poll())
        logger.info("Poller started")

    async def stop(self) -> None:
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        await self.app.store.tg_client.stop()
        logger.info("Poller stopped")

    async def _poll(self) -> None:
        while True:
            try:
                updates = await self.app.store.tg_client.get_updates(
                    offset=self._offset,
                    timeout=30,
                )
                for update in updates:
                    self._offset = update.update_id + 1
                    await self._handle_update(update)
            except asyncio.CancelledError:
                raise
            except Exception as e:
                logger.exception("Polling error: %s", e)
                await asyncio.sleep(1)

    async def _handle_update(self, update) -> None:
        from app.tg.handlers import handle_update
        await handle_update(update, self.app)