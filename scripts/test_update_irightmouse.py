import unittest
from update_irightmouse import parse_page, resolve_download


class DownloadParsingTest(unittest.TestCase):
    def test_download_element(self):
        page = """<a href='/other'>下载专业版</a>
        <a HREF='https://a.u9c.cn/Example123'
           ID="module3607FlBtn"><span>下载专业版</span></a>"""
        self.assertEqual(parse_page(page), 'https://a.u9c.cn/Example123')

    def test_changed_element_fails(self):
        button = '<a id="module3607FlBtn" href="https://a.u9c.cn/Example123">下载</a>'
        for page in ['', button.replace('a.u9c.cn', 'other.example'), button * 2,
                     '<a id="module3607FlBtn" href>下载</a>']:
            with self.subTest(page=page), self.assertRaises(ValueError):
                parse_page(page)

    def test_download_redirect(self):
        for version, build, separator in [('2.6.0', '2026101901', ''),
                                          ('2.5.1', '2026110701', '_')]:
            url = ('https://download.s21i.co99.net/new-file.dmg'
                   f'?f=iRightMousePro{separator}{version}_{build}.dmg&v=123')
            with self.subTest(url=url):
                self.assertEqual(resolve_download(url), (version, url, build))

    def test_invalid_redirect(self):
        download = 'https://download.s21i.co99.net/file.dmg'
        query = '?f=iRightMousePro_2.5.1_2026110701.dmg&v=123'
        for url in ['', download, download + '?f=OtherApp.dmg',
                    download + query + '&f=OtherApp.dmg',
                    download.replace('file.dmg', 'file.zip') + query,
                    download.replace('download.s21i.co99.net', 'other.example') + query]:
            with self.subTest(url=url), self.assertRaises(ValueError):
                resolve_download(url)


if __name__ == '__main__':
    unittest.main()
