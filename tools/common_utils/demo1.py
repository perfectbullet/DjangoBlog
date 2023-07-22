from typing import Optional

import psutil
from psutil import Process


def get_process_by_port(port) -> Optional[Process]:
    """
    按端口获取第一个匹配到的进程
    """
    for p in psutil.process_iter():
        for c in p.connections():
            if c.status == 'LISTEN' and c.laddr.port == port:
                return p
    return None

proc = get_process_by_port(5001)
print("PID", proc.pid, proc.name())
