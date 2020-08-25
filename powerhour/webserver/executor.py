import asyncio
from concurrent.futures import ThreadPoolExecutor


def init_worker_thread(*args):
    """
    Initialize a new event loop for each thread in the executor
    """
    asyncio.set_event_loop(asyncio.new_event_loop())


executor = ThreadPoolExecutor(initializer=init_worker_thread)
