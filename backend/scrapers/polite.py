import time
import urllib.robotparser as rp
from urllib.parse import urlparse

import httpx

UA = "HoodieFinderStudentProject/0.1"
DELAY_SECONDS = 5
_last_hit, _robots = {}, {}


def allowed(url):
    p = urlparse(url)
    host = f"{p.scheme}://{p.netloc}"
    if host not in _robots:
        r = rp.RobotFileParser(host + "/robots.txt")
        r.read()
        _robots[host] = r
    return _robots[host].can_fetch(UA, url)


def get(url):
    if not allowed(url):
        raise PermissionError(f"robots.txt says no: {url}")
    host = urlparse(url).netloc
    wait = DELAY_SECONDS - (time.time() - _last_hit.get(host, 0))
    if wait > 0:
        time.sleep(wait)
    _last_hit[host] = time.time()
    resp = httpx.get(url, headers={"User-Agent": UA}, timeout=20, follow_redirects=True)
    if resp.status_code in (403, 429, 430):
        raise RuntimeError(f"Blocked or rate-limited by {host} ({resp.status_code}) - stopping")
    resp.raise_for_status()
    return resp