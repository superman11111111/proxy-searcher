from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains 
from bs4 import BeautifulSoup

DELAY = 3
all_url = "https://checkerproxy.net/getAllProxy"
output = {}
roots = []
options = Options()
options.headless = True
#options.headless = False 

import os
driver = webdriver.Firefox(options=options, service_log_path=os.devnull)
driver.get(all_url)

ul = BeautifulSoup(driver.page_source, features="html.parser").select(".block > ul:nth-child(2)")
dates = [x.findAll(href=True)[0]["href"] for x in ul[0].findChildren("li")]
print(f"Found {len(dates)} sites")

for d in dates:
    dd = d.split("/")[-1]
    driver.get("https://checkerproxy.net" + d)
    try:
        import time
        time.sleep(.5)
        elem = WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".copy")))
        print(f"LOADED {dd}")
        roots.append((dd, BeautifulSoup(driver.page_source, features="html.parser")))
    except TimeoutException:
        print("Bad Internet, increase delay >3")
driver.close()

print("Parsing...")
for dd, root in roots:
    output[dd] = []
    tbody = root.select("#resultTable > tbody:nth-child(2)")[0]
    for tr in tbody.findAll("tr"):
        #print([x.findAll(text=True) for x in tr.findAll("td")[:3]])
        (ipp, loc, t) = [x.findAll(text=True)[0] for x in tr.findAll("td")[:3]]
        output[dd].append([ipp, loc, t])
print("\n".join([f"{len(v)} from {k}" for k, v in output.items()]))
print("Writing to disk")
open("all_info.txt", "w").write("\n\n".join([k + "\n" + "\n".join(["|".join(x) for x in v]) for k, v in output.items()]))
open("out.txt", "w").write("\n".join(["\n".join([i[0] for i in v]) for v in output.values()]))




