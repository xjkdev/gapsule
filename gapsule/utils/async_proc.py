import subprocess
import asyncio

from tornado.iostream import PipeIOStream


async def async_communicate(proc: subprocess.Popen, input=None, timeout=None):
    awaiting_list = []
    future_out = None
    future_err = None
    if proc.stdin is not None:
        if input is None:
            proc.stdin.close()
        else:
            async_in = PipeIOStream(proc.stdin.fileno())
            future_in = async_in.write(input)
            future_in.add_done_callback(lambda future: async_in.close())
            awaiting_list.append(future_in)
    if proc.stdout is not None:
        async_out = PipeIOStream(proc.stdout.fileno())
        future_out = async_out.read_until_close()
        awaiting_list.append(future_out)
    if proc.stderr is not None:
        async_err = PipeIOStream(proc.stderr.fileno())
        future_err = async_err.read_until_close()
        awaiting_list.append(future_err)

    _done, pending = await asyncio.wait(awaiting_list, timeout=timeout)

    if len(pending) > 0:
        proc.kill()
        raise subprocess.TimeoutExpired(proc.cmd, timeout)
    out = future_out.result() if future_out is not None else None
    err = future_err.result() if future_err is not None else None
    return out, err
