"""Resolve the official download button, verify the DMG, then update the Cask."""
from html.parser import HTMLParser
import json
import re
from pathlib import Path
from urllib.parse import urlsplit
from update_cask import fetch, update_cask

HOME = 'https://www.aodo365.com/irightmousepro.html'
CASK = Path(__file__).resolve().parents[1] / 'Casks/irightmouse-pro.rb'


class DownloadPageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.buttons = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and attrs.get('id') == 'module3607FlBtn':
            self.buttons.append(attrs.get('href', ''))


def parse_page(page):
    parser = DownloadPageParser()
    parser.feed(page)
    if len(parser.buttons) != 1:
        raise ValueError('下载元素 #module3607FlBtn 缺失或不唯一，请检查页面是否改版')
    href = parser.buttons[0]
    match = re.search(r'"jumpIde"\s*:\s*"([A-Za-z0-9+/=]+)"', href)
    if 'fileDownload' not in href or not match:
        raise ValueError('官网下载元素缺少文件下载参数')
    return match[1]


def resolve_download(response):
    if not response.get('success'):
        raise ValueError('官网下载接口返回失败')
    info = response['file']
    match = re.fullmatch(r'iRightMousePro(\d+(?:\.\d+)+)_(\d+)\.dmg', info['name'])
    if not match or not info.get('allowDownload'):
        raise ValueError('下载文件名不符合预期，或不允许下载')
    url = info['downloadUrl']
    if url.startswith('//'):
        url = 'https:' + url
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or parsed.hostname != 'download.s21i.co99.net':
        raise ValueError('官网下载地址域名发生变化，请人工确认')
    return match[1], url, match[2]


def main():
    ide = parse_page(fetch(HOME).decode('utf-8'))
    response = json.loads(fetch('https://www.aodo365.com/rajax/site_h.jsp?cmd=getWafNotCk_getFilePath',
                                {'ide': ide, 'url': '/irightmousepro.html'}))
    version, url, build = resolve_download(response)
    update_cask(CASK, version, url, 'iRightMouse Pro.app', 'cn.better365.iRightMousePro', build)


if __name__ == '__main__':
    main()
