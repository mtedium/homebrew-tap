import copy
import unittest
from update_removemacai import resolve_download


class RemoveMacAIReleaseTest(unittest.TestCase):
    def test_stable_gui_asset(self):
        url = 'https://github.com/omlahore/RemoveMacAI/releases/download/v1.2.0/RemoveMacAI.zip'
        response = {'tag_name': 'v1.2.0', 'draft': False, 'prerelease': False,
                    'assets': [{'name': 'RemoveMacAI.zip', 'browser_download_url': url}]}
        self.assertEqual(resolve_download(response), ('1.2.0', url))
        for key, value in [('draft', True), ('prerelease', True), ('tag_name', 'v1.2.0-beta.1'),
                           ('assets', []), ('assets', response['assets'] * 2)]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                resolve_download({**response, key: value})
        for key, value in [('name', 'removemacai.tar.gz'),
                           ('browser_download_url', 'https://other.example/RemoveMacAI.zip')]:
            changed = copy.deepcopy(response)
            changed['assets'][0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                resolve_download(changed)

    def test_actions_token_authenticates_only_release_api(self):
        import json
        import subprocess
        from unittest.mock import patch
        from update_removemacai import main

        release = {'tag_name': 'v1.1.4', 'assets': [{
            'name': 'RemoveMacAI.zip',
            'browser_download_url': 'https://github.com/omlahore/RemoveMacAI/releases/download/v1.1.4/RemoveMacAI.zip'}]}

        def github_request(args, **kwargs):
            # 模拟匿名额度耗尽；凭据须经 stdin 传入，异常不得带出 token。
            self.assertNotIn('test-token', ' '.join(args))
            if kwargs.get('input') != b'Authorization: Bearer test-token\n':
                raise subprocess.CalledProcessError(56, args, stderr=b'403 rate limit exceeded')
            return json.dumps(release).encode()

        with patch.dict('os.environ', {'GITHUB_TOKEN': 'test-token'}), \
                patch('update_cask.subprocess.check_output', side_effect=github_request), \
                patch('update_removemacai.update_cask') as update:
            main()
        self.assertEqual(update.call_args.kwargs, {'build': '1.1.4', 'archive': 'zip'})
