import time


# seconds passed since epoch
seconds = time.time()
print("Seconds since epoch =", seconds)

local_time = time.ctime(seconds)

print(local_time)

GMT = time.gmtime(seconds)
print("GMT:", GMT)


time.sleep(5)