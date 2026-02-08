from fastapi import FastAPI
import requests
import csv
from datetime import datetime
import subprocess
import re
import platform
import os


def ping(host , ping_count):
    success_count = 0
    failure_count = 0
    timeout_count = 0
    latencies = []
    message = ""

    if platform.system() == "Windows":
        plat = "-n"
    elif platform.system() == "Linux":
        plat = "-c"
    else:
        plat = "-c"  # defensive coding

    for i in range(ping_count):  #Optimization Note: Can use threads instead of a synchronous loop , to be able to do the pings in parallel
        try:
            result = subprocess.run(["ping", plat, "1", host], capture_output=True, text=True) #Capturing CompletedProcess in result
            if "could not find host" in result.stdout.lower():
                message = f"Check for a typo, couldn't find the '{host}' on the internet"
                failure_count += 1
                break #stop pinging
            if "timed out" in result.stdout.lower():
                timeout_count += 1
                continue #skip
            if result.returncode != 0:
                message = 'Ping Failed'
                failure_count += 1
                break
            match = re.search(r"time=(\d+)ms", result.stdout)
            if match:
                latency_value = int(match.group(1))
                latencies.append(latency_value)
                success_count += 1
            else:
                failure_count += 1
        except Exception as e:
            message = f"Error pinging {host}: {e}"
            failure_count += 1
            break
    if latencies:
        average_latency = sum(latencies) / len(latencies)
    else:
        average_latency = None
    return{"host": host,
           "success": success_count,
           "failure": failure_count,
           "timeout": timeout_count,
           "avg_latency": average_latency,
           "message": message}
app = FastAPI(title="Guardian Health API")
bookmarks = []
@app.get("/")
def home():
    return {"message": "welcome"}


@app.post("/add")
def create_bookmark(name: str, url: str):
    new_site = {"name" : name.lower() , "url" : url , "status" : 0} #using .lower() for case sensitivity
    if new_site not in bookmarks:
        bookmarks.append(new_site)
    return bookmarks

@app.post("/del")
def delete_bookmark(name: str):
    global bookmarks
    bookmarks =[site for site in bookmarks if site["name"] != name.lower()]
    return bookmarks
@app.get("/check_all")
def check_all(ping_count: int = 1):
    all_results = []
    file_name = 'Network_Monitoring_logs.csv'
    file_exists = os.path.isfile(file_name)
    for site in bookmarks:
        host_to_ping = site["url"].replace("https://","").replace("http://","").split('/')[0]
        ping_result = ping(host_to_ping, ping_count)
        try:
            if ("https://") not in site["url"] and ("http://") not in site["url"]:
                site["url"] = "https://" + site["url"]
            req = requests.get(site["url"], timeout=5)
            site["status"] = req.status_code
        except:
            site["status"] = "Offline or 404"
        if "Check for a typo" in ping_result['message']:
            pass
        elif ping_result['success'] == 0 and site['status'] == 200: #If ping blocked but site works
            ping_result['message'] = "Host is UP (HTTP OK), but ICMP/Ping is blocked."
        elif site['status'] == "Offline or 404":   #If HTTP failed and we don't have a specific message yet
            if not ping_result['message']:  # Only set if message is empty
                ping_result['message'] = "Host appears to be DOWN."
        ping_result['total_attempted_pings'] = ping_result['success'] + ping_result['failure'] + ping_result['timeout']
        ping_result['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        all_results.append(ping_result)
    if all_results:
        with open(file_name, 'a', newline='') as csvfile:
            fieldnames = ['timestamp', 'host', 'total_attempted_pings', 'success', 'failure', 'timeout', 'avg_latency',
                          'message']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerows(all_results)
    return bookmarks