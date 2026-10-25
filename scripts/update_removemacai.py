"""Update the GUI app from official stable GitHub releases."""
import json
import re
from pathlib import Path
from update_cask import fetch, update_cask

API = 'https://api.github.com/repos/omlahore/RemoveMacAI/releases/latest'


def resolve_download(response):
    tag = response.get('tag_name', '')
    if (response.get('draft') or response.get('prerelease')
            or not re.fullmatch(r'v\d+(?:\.\d+)+', tag)):
        raise ValueError('RemoveMacAI 稳定版信息不符合预期')
    assets = [a for a in response.get('assets', []) if a.get('name') == 'RemoveMacAI.zip']
    expected = f'https://github.com/omlahore/RemoveMacAI/releases/download/{tag}/RemoveMacAI.zip'
    if len(assets) != 1 or assets[0].get('browser_download_url') != expected:
        raise ValueError('RemoveMacAI 图形版下载来源或文件名发生变化')
    return tag[1:], assets[0]['browser_download_url']


def main():
    version, url = resolve_download(json.loads(fetch(API)))
    update_cask(Path(__file__).resolve().parents[1] / 'Casks/removemacai.rb',
                version, url, 'RemoveMacAI.app', 'io.github.omlahore.removemacai.app',
                build=version, archive='zip')


if __name__ == '__main__':
    main()
