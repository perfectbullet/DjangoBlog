import shlex
import asyncio

async def run(cmd, arg):
    proc = await asyncio.create_subprocess_exec(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout}')
    if stderr:
        print(f'[stderr]\n{stderr}')

if __name__ == '__main__':
    jar_path = './nginxWebUI-3.6.1.jar'
    start_str = 'java -jar ' + jar_path

    cmd = shlex.split(start_str)
    asyncio.run(run('java', ['-jar', jar_path]))
