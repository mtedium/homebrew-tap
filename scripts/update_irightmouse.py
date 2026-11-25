"""Check the official update feed and verify the DMG for a new build."""
from html.parser import HTMLParser
import re
import subprocess
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
from xml.etree import ElementTree
from update_cask import fetch, update_cask

HOME = 'https://www.aodo365.com/irightmousepro.html'
FEED = 'https://www.aodo365.com/iRightMouseUpdate.xml'
SPARKLE = '{http://www.andymatuschak.org/xml-namespaces/sparkle}'
CASK = Path(__file__).resolve().parents[1] / 'Casks/irightmouse-pro.rb'


class DownloadPageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.buttons = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and attrs.get('id') == 'module3607FlBtn':
            self.buttons.append(attrs.get('href') or '')


def parse_page(page):
    parser = DownloadPageParser()
    parser.feed(page)
    if len(parser.buttons) != 1:
        raise ValueError('下载元素 #module3607FlBtn 缺失或不唯一，请检查页面是否改版')
    href = parser.buttons[0]
    if not re.fullmatch(r'https://a\.u9c\.cn/[A-Za-z0-9]+', href):
        raise ValueError('官网下载按钮的短链格式发生变化，请人工确认')
    return href


def resolve_download(url):
    if not re.fullmatch(r'https://download\.s21i\.co99\.net/[^\s"\\#]+', url):
        raise ValueError('官网下载短链未返回预期的下载地址，请人工确认')
    parsed = urlsplit(url)
    names = parse_qs(parsed.query, keep_blank_values=True).get('f', [])
    name = names[0] if len(names) == 1 else ''
    match = re.fullmatch(r'iRightMousePro_?(\d+(?:\.\d+)+)_(\d+)\.dmg', name)
    if not parsed.path.endswith('.dmg') or not match:
        raise ValueError('官网下载文件名不符合预期，请人工确认')
    return match[1], url, match[2]


def parse_feed(data):
    try:
        items = ElementTree.fromstring(data).findall('./channel/item')
    except ElementTree.ParseError as error:
        raise ValueError('官方更新源返回了无效的 XML') from error
    if len(items) != 1:
        raise ValueError('官方更新源的发布条目缺失或不唯一，请人工确认')
    version = items[0].findtext(SPARKLE + 'shortVersionString', '').strip()
    build = items[0].findtext(SPARKLE + 'version', '').strip()
    if not re.fullmatch(r'[0-9]+(?:\.[0-9]+)+', version) or not re.fullmatch(r'[0-9]+', build):
        raise ValueError('官方更新源的版本或构建号格式发生变化，请人工确认')
    return version, build


def main():
    version, build = parse_feed(fetch(FEED))
    urls = re.findall(r'^  url "([^"]+)"$', CASK.read_text(), flags=re.M)
    if len(urls) != 1:
        raise ValueError('Cask 的下载地址缺失或不唯一')
    current_version, _, current_build = resolve_download(urls[0])
    if (version, build) == (current_version, current_build):
        print(f'已是官方更新源当前版本 {version}（构建 {build}）')
        return
    if int(build) <= int(current_build):
        raise ValueError('官方更新源的构建号未推进，请人工确认')

    short_url = parse_page(fetch(HOME).decode('utf-8'))
    # 先读取重定向目标，校验后再下载 DMG。
    redirect_url = subprocess.check_output([
        'curl', '-q', '--fail', '--silent', '--show-error', '--retry', '3',
        '--max-time', '30', '--output', '/dev/null', '--write-out', '%{redirect_url}', short_url,
    ], text=True)
    download_version, url, download_build = resolve_download(redirect_url)
    if (download_version, download_build) != (version, build):
        raise ValueError('官网下载文件名的版本或构建号与官方更新源不一致')
    update_cask(CASK, version, url, 'iRightMouse Pro.app', 'cn.better365.iRightMousePro', build)


if __name__ == '__main__':
    main()
