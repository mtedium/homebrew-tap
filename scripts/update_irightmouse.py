"""Resolve the official download button, verify the DMG, then update the Cask."""
import hashlib
from html.parser import HTMLParser
import json
import plistlib
import re
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import urlencode, urlsplit

HOME = 'https://www.aodo365.com/irightmousepro.html'
CASK = Path(__file__).resolve().parents[1] / 'Casks/irightmouse-pro.rb'


def fetch(url, data=None):
    args = ['curl', '--fail', '--location', '--compressed', '--silent',
            '--show-error', '--retry', '3', '--max-time', '180', url]
    if data is not None:
        args += ['--data', urlencode(data)]
    return subprocess.check_output(args)


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
    with tempfile.TemporaryDirectory() as folder:
        folder = Path(folder)
        dmg = folder / 'download.dmg'
        dmg.write_bytes(fetch(url))
        digest = hashlib.sha256(dmg.read_bytes()).hexdigest()
        current = CASK.read_text()
        updated = current
        for key, value in [('version', version), ('sha256', digest), ('url', url)]:
            updated, count = re.subn(r'^  ' + key + r' ".*"$',
                                     lambda _: f'  {key} "{value}"', updated, count=1, flags=re.M)
            if count != 1:
                raise ValueError(f'Cask 缺少 {key}')
        if updated == current:
            print(f'已是官网当前版本 {version}，安装包未变化')
            return
        mount = folder / 'volume'
        subprocess.run(['hdiutil', 'attach', '-readonly', '-nobrowse', '-mountpoint', str(mount), str(dmg)], check=True)
        try:
            info = plistlib.loads((mount / 'iRightMouse Pro.app/Contents/Info.plist').read_bytes())
            if (info.get('CFBundleIdentifier') != 'cn.better365.iRightMousePro'
                    or info.get('CFBundleShortVersionString') != version
                    or str(info.get('CFBundleVersion')) != build):
                raise ValueError('DMG 中应用标识、版本或构建号不匹配')
        finally:
            subprocess.run(['hdiutil', 'detach', str(mount)], check=True)
        candidate = folder / 'candidate.rb'
        candidate.write_text(updated)
        subprocess.run(['ruby', '-c', str(candidate)], check=True)
        CASK.write_text(updated)
        print(f'已更新为 {version}，构建号 {build}，SHA256 {digest}')


if __name__ == '__main__':
    main()
