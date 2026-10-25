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
