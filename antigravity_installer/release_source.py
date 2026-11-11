from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import re

DOWNLOAD_PAGE = "https://antigravity.google/download"
ALLOWED_HOSTS = ("storage.googleapis.com", "edgedl.me.gvt1.com")

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]
    def handle_starttag(self, tag, attrs):
        if tag.lower()=="a":
            href=dict(attrs).get("href")
            if href: self.links.append(href.replace("&amp;","&"))

def _get(url):
    req=Request(url,headers={"User-Agent":"Antigravity-Installer-Linux/1.1"})
    with urlopen(req,timeout=45) as response: return response.read()

def latest_downloads(products=None):
    parser=LinkParser(); parser.feed(_get(DOWNLOAD_PAGE).decode("utf-8","replace"))
    found={"app":[],"ide":[]}
    for href in parser.links:
        parsed=urlparse(href)
        if parsed.scheme!="https" or parsed.hostname not in ALLOWED_HOSTS or "linux-x64" not in href: continue
        if "Antigravity%20IDE.tar.gz" in href or "Antigravity IDE.tar.gz" in href: found["ide"].append(href)
        elif "Antigravity.tar.gz" in href: found["app"].append(href)
    requested=tuple(products or ("app","ide"))
    missing=[p for p in requested if not found[p]]
    if missing: raise RuntimeError("La página oficial de Google no ha proporcionado el paquete Linux x64 de: "+", ".join(missing))
    return {p:found[p][0] for p in requested}

def version_from_url(url):
    match=re.search(r"/(\d+\.\d+\.\d+)-\d+/linux-x64/",url)
    return match.group(1) if match else "unknown"

def download(url,destination,progress=None):
    parsed=urlparse(url)
    if parsed.scheme!="https" or parsed.hostname not in ALLOWED_HOSTS: raise ValueError("URL de descarga no autorizada.")
    req=Request(url,headers={"User-Agent":"Antigravity-Installer-Linux/1.1"})
    with urlopen(req,timeout=90) as response,open(destination,"wb") as out:
        total=int(response.headers.get("Content-Length","0") or 0); done=0
        while True:
            chunk=response.read(1024*1024)
            if not chunk: break
            out.write(chunk); done+=len(chunk)
            if progress: progress(done,total)
