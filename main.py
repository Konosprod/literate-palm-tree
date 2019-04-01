from bs4 import BeautifulSoup
import urllib3.request
import certifi
import sys
import os
import uuid

def download_file(http, url, dir=""):
    r = http.request('GET', url, preload_content=False)
    filename = r.headers
    if not filename["Content-Disposition"]:
        filename = uuid.uuid4()
    else:
        filename = filename["Content-Disposition"].replace("attachment; filename=", "")

    path = os.path.join(dir, filename)

    with open(path, 'wb') as out:
        while True:
            data = r.read(1024)
            if not data:
                break
            out.write(data)

    r.release_conn()

dir = sys.argv[2]
http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())
next_page  = sys.argv[1]

while next_page is not None:
    source = BeautifulSoup(http.request("GET", next_page).data, "html.parser")

    links = source.find_all("a", {"title":"Télécharger en EPUB"})
    next_page = source.find("a", {"rel":"next"})

    if not next_page:
        next_page = None
    else:
        next_page = "http://fr.feedbooks.com"+ next_page["href"]

    for link in links:
            url = link["href"]
            download_file(http, url, dir)



