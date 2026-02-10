## 🛡️ Guardian Health API

Guardian Health API is a resilient network monitoring service built with FastAPI. Unlike standard uptime tools, it uses a dual-layer verification system to distinguish between a service being truly down and a host simply hardening its security by blocking ICMP (Ping) traffic.

## 💥 Features:
✅Dual-Layer Monitoring: Verifies connectivity via ICMP (Ping) and Application-level availability via HTTP Status Codes

✅Persistent Resource Management: Dynamic RESTful endpoints (/add, /del, /check_all) to manage site bookmarks without restarting the service

✅Smart Error Diagnostics: A custom logic hierarchy that identifies DNS typos, firewall-blocked pings (e.g., Microsoft/AWS), and genuine service downtime

✅Automated CSV Logging: Generates historical performance data with ISO-standard timestamps, optimized for analysis in Excel or Google Sheets

✅Cross-Platform: Built-in detection to handle differing ping flags for Windows and Linux environments

## 📊 CSV Logging
-Results are saved to: Network_Monitoring_logs.csv

Each run appends new rows while keeping file intact

## 🖥️  Inputs - Outputs Example of usage

**Inputs:** 

1) Adding the names and the hosts that they want to ping: <img width="1297" height="608" alt="image" src="https://github.com/user-attachments/assets/20066a84-c903-48b0-aa99-552ee2901080" />

2) Pinging each of the hosts <img width="1296" height="337" alt="image" src="https://github.com/user-attachments/assets/b842dec8-a119-4613-a219-062eabbb91b4" /> (here for example 2 times)

**Outputs:**
1) In the web: <img width="1285" height="473" alt="image" src="https://github.com/user-attachments/assets/5ddbf53f-c892-4a8f-bd39-c17ee440aa0f" /> (status = 200 could be found and pinged)

3) In the csv: <img width="1067" height="144" alt="image" src="https://github.com/user-attachments/assets/68156399-59b9-4084-8fd2-3f527da62eeb" /> (appropriate message for the typos)

**Edge Cases (Hosts blocking the ICMP packets e.g Microsoft.com)**
1) In the web: <img width="1280" height="161" alt="image" src="https://github.com/user-attachments/assets/01b54fe5-c192-4b51-9d64-e5aec706b0a6" /> (Host is there since the status = 200)

2) In the csv: <img width="1051" height="161" alt="image" src="https://github.com/user-attachments/assets/c210078b-e2be-4791-9d83-7dcc69fe7522" /> (proper message that the host is there but blocking the pings - timeouts)

**Note:** Deleting works similar by putting the name in the field and deletes every host that name pinged in the web alongside with the name

## 🚨 Technical Challenges & Solutions
**1) The "Microsoft Ping" Paradox**

**Challenge😤:** Servers like microsoft.com often reported as "Offline" because they drop ICMP packets for security. 

**Solution💡**: I implemented an HTTP check. If a ping fails but the HTTP status returns 200 OK, the API identifies the host as active but "ICMP Blocked," preventing false-negative alerts.


**2) User Experience (UX) vs Data Precision**

**Challenge😤:** Users might enter URLs in many formats (google.com, http://google.com, https://google.com).

**Constraint🚨**: The requests library will crash if the protocol (http://) is missing, but the ping command will crash if the protocol is included.

**Solution💡**: Managed to strip the protocol for the ping check but ensured it's present for the HTTP check (Protocol Healing).

## 🛠️ System Requirements
  ### Operating Systems:

  Windows: (Fully tested)

  Linux: (Fully tested with -c ping flag support)

  ### Python Version:

  Python 3.7+ (Required for FastAPI and f-string support)

  ### External Libraries (Dependencies): You will need to install the following libraries to run the API:

  `fastapi`: The web framework used to build the API endpoints.

  `uvicorn`: The ASGI server used to run the FastAPI application.

  `requests`: Used for the application-layer (HTTP) health checks.


## 🚀 How to run
1) **Install dependencies:**

`pip install fastapi uvicorn requests`

2) **Run the API:**

`uvicorn main:app --reload`

3) **Interact with the API:**

Navigate to: `http://127.0.0.1:8000/docs`

## 🔧 Possible Improvements

1) **Parallel Execution (Threading or Asyncio)**
   
2) **Persistent Database Integration (SQL)**

3) **Frontend Dashboard** (e.g React)

## 👤 Author

**Nikolaos Vasilakopoulos**

**🌍 Portfolio:** (https://github.com/Independent3 , https://www.linkedin.com/in/nikolaos-vasilakopoulos-85714b3b0/)

**📧 Email:** nickvasilakopoulos@rocketmail.com
