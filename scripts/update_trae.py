"""Update Apple Silicon TRAE from its official release API."""
import json
import re
from pathlib import Path
from urllib.parse import urlsplit
from update_cask import fetch, update_cask

API = 'https://api.trae.ai/icube/api/v1/native/version/trae/latest'


def resolve_download(response):
    if not response.get('success'):
        raise ValueError('TRAE 更新接口返回失败')
    releases = [item for item in response['data']['manifest']['darwin']['versions']
                if item['region'] == 'va' and item['arch'] == 'apple']
    if len(releases) != 1:
        raise ValueError('TRAE Apple Silicon 发布信息缺失或不唯一')
    release = releases[0]
    url = urlsplit(release['url'])
    if (url.scheme != 'https' or url.hostname != 'lf-cdn.trae.ai'
            or not url.path.startswith('/obj/trae-ai-us/pkg/app/releases/stable/')
            or not url.path.endswith('/darwin/TRAE-darwin-arm64.dmg')
            or not re.fullmatch(r'\d+(?:\.\d+)+', release['version'])):
        raise ValueError('TRAE 下载来源或版本格式发生变化')
    return release['version'], release['url']


def main():
    version, url = resolve_download(json.loads(fetch(API)))
    update_cask(Path(__file__).resolve().parents[1] / 'Casks/trae.rb',
                version, url, 'Trae.app', 'com.trae.app')


if __name__ == '__main__':
    main()
