import urllib.request
import threading
import time
import random
import sys

TIMEOUT = 2 # seconds
MAX_THREADS = 1000

START = time.time()
print(f"TIMEOUT={TIMEOUT}\nMAX_THREADS={MAX_THREADS}")

if len(sys.argv) > 1:
    if sys.argv[1].lower() == "all":
        PROXIES = -1
    else:
        PROXIES = int(sys.argv[1])
else:
    PROXIES = 10

IPPS = open("out.txt", "r").read().split("\n")
random.shuffle(IPPS)

IPPS = IPPS[:PROXIES]
PROXIES = len(IPPS)
print(f"Checking {len(IPPS)} proxies")
WORKING = []
threads = []
NOTWORKING = 0

def check(p):
    global WORKING, NOTWORKING, IP
    try:
        req = urllib.request.Request("http://www.httpbin.org/ip")
        req.set_proxy(p, "http")
        s = time.time()
        response = urllib.request.urlopen(req, timeout=TIMEOUT)
        if IP in response.read().decode():
            raise Exception('PROXY FORWARDS IP')
        WORKING.append([time.time() - s, p])
    except Exception:
        NOTWORKING += 1
        return
def checkpid(pid):
    global IPPS
    time.sleep(.1)
    check(IPPS[pid])
def checklist(pid, ll):
    for e in ll:
        check(e)


req = urllib.request.Request("https://api.ipify.org")
res = urllib.request.urlopen(req)
IP = res.read().decode()
print(f"Your IP: {IP}")
rr = PROXIES
if PROXIES > MAX_THREADS or PROXIES < 0:
    print(f"Starting {MAX_THREADS} threads... ")
    rr = PROXIES // MAX_THREADS
    for i in range(MAX_THREADS):
        ii = i*rr
        t = threading.Thread(target=checklist, args=(i, IPPS[ii:ii+rr], ))
        threads.append(t)
        t.start()
else:
    print(f"Starting {PROXIES} threads... ")
    for i in range(PROXIES):
        t = threading.Thread(target=checkpid, args=(i, ))
        threads.append(t)
        t.start()
for t in threads:
    t.join()

print(f"{PROXIES-NOTWORKING} proxies out of {PROXIES} were working ({((PROXIES-NOTWORKING)/PROXIES)*100}%)")
WORKING_SORTED = sorted(WORKING, key=lambda x: x[0])
open("working.txt", "w").write("\n".join([x[1] for x in WORKING_SORTED]) + "\n")
print(f"time: {time.time() - START}s")
input()

