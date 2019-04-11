import asyncio
import sys

if sys.platform == 'windows':
    asyncio.set_event_loop_policy(
        asyncio.WindowsProactorEventLoopPolicy())
