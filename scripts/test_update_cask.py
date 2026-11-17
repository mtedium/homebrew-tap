import plistlib
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from update_cask import update_cask


class PackageValidationTest(unittest.TestCase):
    def test_mismatched_zip_keeps_cask(self):
        with tempfile.TemporaryDirectory() as folder:
            cask = Path(folder) / 'app.rb'
            original = '  version "0.1"\n  sha256 "old"\n  url "old"\n'
            cask.write_text(original)

            def extract(args, **kwargs):
                if args[0] == 'curl':
                    Path(args[args.index('--output') + 1]).write_bytes(b'zip')
                    return
                info = Path(args[-1]) / 'App.app/Contents/Info.plist'
                info.parent.mkdir(parents=True)
                info.write_bytes(plistlib.dumps({'CFBundleIdentifier': 'wrong'}))

            with patch('update_cask.subprocess.run', side_effect=extract):
                with self.assertRaises(ValueError):
                    update_cask(cask, '1.0', 'https://example.com/app.zip',
                                'App.app', 'expected', archive='zip')
            self.assertEqual(cask.read_text(), original)

    def test_download_failure_stops_before_mounting(self):
        with tempfile.TemporaryDirectory() as folder:
            cask = Path(folder) / 'app.rb'
            original = '  version "0.1"\n  sha256 "old"\n  url "old"\n'
            cask.write_text(original)

            def timeout(args, *, check):
                self.assertTrue(check)
                self.assertEqual(args[0], 'curl')
                Path(args[args.index('--output') + 1]).write_bytes(b'partial')
                raise subprocess.CalledProcessError(28, args)

            with patch('update_cask.subprocess.run', side_effect=timeout) as run:
                with self.assertRaises(subprocess.CalledProcessError) as error:
                    update_cask(cask, '1.0', 'https://example.com/app.dmg',
                                'App.app', 'expected')
            self.assertEqual(error.exception.returncode, 28)
            self.assertEqual(run.call_count, 1)
            self.assertEqual(cask.read_text(), original)
