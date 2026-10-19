"""Download and verify an official DMG before changing its Cask."""
import hashlib
import plistlib
import re
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import urlencode


def fetch(url, data=None):
    args = ['curl', '--fail', '--location', '--compressed', '--silent',
            '--show-error', '--retry', '3', '--max-time', '180', url]
    if data is not None:
        args += ['--data', urlencode(data)]
    return subprocess.check_output(args)


def update_cask(cask, version, url, app, bundle_id, build=None):
    with tempfile.TemporaryDirectory() as folder:
        folder = Path(folder)
        dmg = folder / 'download.dmg'
        dmg.write_bytes(fetch(url))
        digest = hashlib.sha256(dmg.read_bytes()).hexdigest()
        current = cask.read_text()
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
            info = plistlib.loads((mount / app / 'Contents/Info.plist').read_bytes())
            if (info.get('CFBundleIdentifier') != bundle_id
                    or info.get('CFBundleShortVersionString') != version
                    or (build is not None and str(info.get('CFBundleVersion')) != build)):
                raise ValueError('DMG 中应用标识、版本或构建号不匹配')
        finally:
            subprocess.run(['hdiutil', 'detach', str(mount)], check=True)
        candidate = folder / 'candidate.rb'
        candidate.write_text(updated)
        subprocess.run(['ruby', '-c', str(candidate)], check=True)
        cask.write_text(updated)
        print(f'{cask.stem} 已更新为 {version}，SHA256 {digest}')

