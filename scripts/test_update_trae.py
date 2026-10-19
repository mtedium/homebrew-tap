import unittest
from update_trae import resolve_download


class TraeReleaseTest(unittest.TestCase):
    def test_uses_api_version_and_exact_url(self):
        url = 'https://lf-cdn.trae.ai/obj/trae-ai-us/pkg/app/releases/stable/2.3.99999/darwin/TRAE-darwin-arm64.dmg'
        item = {'region': 'va', 'arch': 'apple', 'version': '3.7.0', 'url': url}
        response = {'success': True, 'data': {'manifest': {'darwin': {'versions': [item]}}}}
        self.assertEqual(resolve_download(response), ('3.7.0', url))
        for key, value in [('region', 'cn'), ('arch', 'intel'),
                           ('url', 'https://other.example/app.dmg'), ('version', 'bad')]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                resolve_download({'success': True, 'data': {'manifest': {
                    'darwin': {'versions': [{**item, key: value}]}}}})
        with self.assertRaises(ValueError):
            resolve_download({'success': False})


if __name__ == '__main__':
    unittest.main()
