# Copyright @Myth 2024
# see: https://myth.cx/p/hugo-auto-submit-baidu/

import sys, os
import requests
import lxml.etree

from urllib.parse import urlparse, urlunparse
from concurrent.futures import ThreadPoolExecutor


def insert_path_segment(url, segment):
    parsed_url = urlparse(url)
    new_path = f"/{segment}{parsed_url.path}"
    new_url = urlunparse(parsed_url._replace(path=new_path))
    return new_url


def purge_url(url):
    headers = {"User-Agent": "curl/7.12.1"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        print(f"success: {url}, got {res.text}")
    except Exception as e:
        print(f"failed, got exception: {e}", file=sys.stderr)


def get_urls(sitemap_path: str):
    urls = []
    if sitemap_path.endswith("xml"):
        tree = lxml.etree.parse(sitemap_path)
        namespaces = {
            "sitemapindex": "http://www.sitemaps.org/schemas/sitemap/0.9",
        }
        for url in tree.xpath("//sitemapindex:loc/text()", namespaces=namespaces):
            urls.append(url)
    else:
        with open(sitemap_path) as fd:
            urls.extend(
                i for i in (i.strip() for i in fd.readlines()) if not i.startswith("#")
            )
    return urls


def handle_urls(urls: list[str], segment):
    new_urls = []
    for url in urls:
        new_urls.append(insert_path_segment(url, segment))
    return new_urls


if __name__ == "__main__":
    urls = get_urls(sys.argv[1])
    urls = handle_urls(urls, sys.argv[2])
    print(urls)
    with ThreadPoolExecutor() as executor:
        list(executor.map(purge_url, urls))
