import urllib.request
import threading
import time
import random

PROXIES = 10

IPPS = open("out.txt", "r").read().split("\n")
random.shuffle(IPPS)
IPPS = IPPS[:PROXIES]
WORKING = []
NOTWORKING = 0
def checker(pid):
    global IPPS, WORKING, NOTWORKING
    print(f"Thread {pid}: {IPPS[pid]}")
    for ipp in IPPS[pid]:
        try:
            req = urllib.request.Request("http://www.httpbin.org/ip")
            req.set_proxy(ipp, "http")
            s = time.time()
            response = urllib.request.urlopen(req)
            tt = time.time() - s

            # print(response.read().decode('utf8'))
            WORKING.append([tt, ipp])
        except Exception:
            NOTWORKING += 1


threads = []
for i in range(PROXIES):
    t = threading.Thread(target=checker, args=(i, ))
    threads.append(t)
    t.start()
for t in threads:
    t.join()

IPPS_N = len(IPPS)
print(f"{PROXIES-NOTWORKING} proxies out of {IPPS_N} were working ({(NOTWORKING/IPPS_N)*100}%)")
WORKING_SORTED = sorted(WORKING, key=lambda x: x[0])
open("working.txt", "w").write("\n".join([x[1] for x in WORKING_SORTED]))
input()

