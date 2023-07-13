import psutil

print(psutil.cpu_times())
# scputimes(user=65531.796875, system=42440.76562500023, idle=1783904.3593749998, interrupt=5676.375, dpc=1846.609375)

# psutil.cpu_times_percent() 功能与之类似, 只不过返回的比例

psutil.pids()