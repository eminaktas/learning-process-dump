# Read from a file with target string to END
with open("end_terminated_file.txt", 'rt') as f:
  lines = iter(lambda: f.readline().strip(), "END")
  reading = [int(line) for line in lines]

print(reading)


# Infinite loop
import datetime
from time import sleep
timestamps = iter(datetime.datetime.now, None)
# for or while is useable for iterators
# while True:
# for timestap in timestamps:
#   print(next(timestamps))
#   sleep(1)


# Realtime Data Iterator
from pathlib import Path
cwd = Path.cwd()
from shutil import disk_usage
def free_space():
  return disk_usage(cwd).free

free_space_reading = iter(free_space, None)
import time

for timestamp, free_bytes in zip(timestamps, free_space_reading):
  print(timestamp, free_bytes)
  time.sleep(1.0)
