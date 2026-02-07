from fastapi import FastAPI
import requests

app = FastAPI(title="Guardian Health API")
bookmarks = []
@app.get("/test-ping") #test pinging google to check how it works
def test_ping():
    response = requests.get("https://google.com")
    return response.status_code
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
def check_all():
    for site in bookmarks:
        url = site["url"]
        if ("http://") not in url and ("https://") not in url:
            url = "https://" + url
            site["url"] = url
        try:
            req = requests.get(site["url"])
            site["status"] = req.status_code
        except:
            site["status"] = "Offline or 404"
    return bookmarks