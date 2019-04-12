import asyncio
import subprocess
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Tuple, Optional, Sequence

__all__ = ['run', 'PIPE', 'DEVNULL']


async def _run_windows(cmd: Sequence, cwd=None, env=None, input=None, stdout=None, stderr=None,
                       timeout=None) -> Tuple[int, Optional[bytes], Optional[bytes]]:
    stdin = PIPE if input is not None else None

    def _task():
        proc = subprocess.Popen(cmd, cwd=cwd, env=env, stdin=stdin,
                                stdout=stdout, stderr=stderr)
        out, err = proc.communicate(input, timeout=timeout)
        if proc.poll() is None:
            proc.terminate()
        return proc.returncode, out, err
    loop: asyncio.BaseEventLoop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, _task)
    return result


async def _run(cmd: Sequence, cwd=None, env=None, input=None, stdout=None, stderr=None,
               timeout=None) -> Tuple[int, Optional[bytes], Optional[bytes]]:
    stdin = PIPE if input is not None else None
    proc = await asyncio.create_subprocess_exec(*cmd, cwd=cwd, env=env, stdin=stdin,
                                                stdout=stdout, stderr=stderr)
    if timeout is not None:
        try:
            out, err = await asyncio.wait_for(proc.communicate(input), timeout)
        except asyncio.TimeoutError:
            raise subprocess.TimeoutExpired(cmd, timeout, out, err)
    else:
        out, err = await proc.communicate(input)
    if proc.returncode is None:
        proc.terminate()
    return proc.returncode, out, err


if os.name == 'nt':
    run = _run_windows
    PIPE = subprocess.PIPE
    DEVNULL = subprocess.DEVNULL
else:
    run = _run
    PIPE = asyncio.subprocess.PIPE
    DEVNULL = asyncio.subprocess.DEVNULL
