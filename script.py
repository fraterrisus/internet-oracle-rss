from bs4 import BeautifulSoup
from datetime import datetime, timezone
from dateutil import parser
import re
import requests
from xml.etree import ElementTree as ET

base_url = "https://internetoracle.org/ftp"

def parse_digest(body):
    lines = body.split("\n")
    phase = 0
    item = {'description': []}
    for line in lines:
        if phase == 0:
            if re.match(r"^===", line):
                item['description'].append(line)
                phase = 1
            continue
        if phase == 1:
            if re.match(r"^---", line):
                break
            if re.match(r"^Title: ", line):
                item['title'] = line[7:]
            if re.match(r"^Date: ", line):
                item['pubDate'] = parser.parse(line[5:])
            item['description'].append(line)
            continue

    item['description'] = "\n".join(item['description'])
    return item

def get_digests():
    urls = []
    files = []
    digests = []

    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.select('a[href]')
    for link in links:
        if re.match(r"^\d\d/", link['href']):
            urls.append(f"{base_url}/{link['href']}")

    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.select('a[href]')
        for link in links:
            if re.match(r"^\d\d\d\d$", link['href']):
                files.append(link['href'])

    files.sort()
    files.reverse()
    for i in range(25):
        digest_index = files[i]
        response = requests.get(f"{base_url}/{digest_index[0:2]}/{digest_index}")
        digest = parse_digest(response.text)
        digest['link'] = f"https://internetoracle.org/digest.cgi?N={digest_index}"
        digest['guid'] = f"https://internetoracle.org/digest.cgi?N={digest_index}"
        digests.append(digest)

    return digests

def get_bestofs():
    files = []
    bestofs = []

    response = requests.get(base_url + "/best/")
    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.select('a[href]')
    for link in links:
        if re.match(r"^\d\d\d\d-\d\d\d\d$", link['href']):
            files.append(link['href'])

    files.sort()
    files.reverse()
    for i in range(2):
        bestof_index = files[i]
        response = requests.get(f"{base_url}/best/{bestof_index}")
        digest = parse_digest(response.text)
        digest['link'] = f"https://internetoracle.org/bestof.cgi?N={bestof_index}"
        digest['guid'] = f"https://internetoracle.org/bestof.cgi?N={bestof_index}"
        bestofs.append(digest)

    return bestofs

def write_rss(stories: list[dict]) -> ET.ElementTree:
    rfc822 = "%a, %d %b %Y %H:%M:%S %z"
    timestamp = datetime.now(timezone.utc).strftime(rfc822)

    root = ET.Element('rss', {"xmlns:atom": "http://www.w3.org/2005/Atom", "version": "2.0"})
    channel = ET.SubElement(root, 'channel')

    channel_children = {
        'title': 'Internet Oracle Digests',
        'link': 'https://internetoracle.org/',
        'description': 'The latest oracularity digests, including best-of digests.',
        'language': 'en-US',
        'pubDate': timestamp,
        'lastBuildDate': timestamp,
        'generator': 'internet-oracle-rss.py',
    }
    for tag in channel_children:
        child = ET.SubElement(channel, tag)
        child.text = channel_children[tag]

    ET.SubElement(channel, 'atom:link', {
        'href': 'https://stuff.hitchhikerprod.com/internet-oracle.rss',
        'rel': 'self',
        'type': 'application/rss+xml',
    })

    for story in stories:
        item = ET.SubElement(channel, 'item')
        for tag in story:
            child = ET.SubElement(item, tag)
            if tag == 'description':
                pass
            elif tag == 'pubDate':
                child.text = story[tag].strftime(rfc822)
            else:
                child.text = story[tag]

    return ET.ElementTree(root)

if __name__ == '__main__':
    stories = []
    stories.extend(get_digests())
    stories.extend(get_bestofs())
    stories.sort(key=lambda x : x['pubDate'].timestamp())
    stories.reverse()
    doc = write_rss(stories[0:20])
    doc.write("internet-oracle.rss", encoding="utf-8", )
