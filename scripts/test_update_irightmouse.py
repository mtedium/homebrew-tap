import unittest
from unittest.mock import patch
from update_irightmouse import FEED, main, parse_feed, parse_page, resolve_download


FEED_XML = b"""<rss xmlns:s="http://www.andymatuschak.org/xml-namespaces/sparkle">
<channel><item><s:version>2026110701</s:version>
<s:shortVersionString>2.5.1</s:shortVersionString>
<link>https://www.aodo365.com/irightmousepro.html</link></item></channel></rss>"""
CASK_URL = ('https://download.s21i.co99.net/file.dmg'
            '?f=iRightMousePro_2.5.1_2026110701.dmg')


class DownloadParsingTest(unittest.TestCase):
    def test_feed_without_download_link(self):
        self.assertEqual(parse_feed(FEED_XML), ('2.5.1', '2026110701'))

    def test_invalid_feed(self):
        for data in (b'<rss', b'<rss><channel/></rss>',
                     FEED_XML.replace(b'2026110701', b'unknown')):
            with self.subTest(data=data), self.assertRaises(ValueError):
                parse_feed(data)

    def test_current_build_checks_only_feed(self):
        with patch('update_irightmouse.CASK', **{'read_text.return_value': f'  url "{CASK_URL}"\n'}), \
             patch('update_irightmouse.fetch', return_value=FEED_XML) as fetch, \
             patch('update_irightmouse.subprocess.check_output') as curl, \
             patch('update_irightmouse.update_cask') as update:
            main()
        fetch.assert_called_once_with(FEED)
        curl.assert_not_called()
        update.assert_not_called()

    def test_website_build_must_match_feed(self):
        page = b'<a id="module3607FlBtn" href="https://a.u9c.cn/Example123">Download</a>'
        with patch('update_irightmouse.CASK', **{'read_text.return_value': f'  url "{CASK_URL}"\n'}), \
             patch('update_irightmouse.fetch', side_effect=[FEED_XML.replace(
                b'2026110701', b'2026110702'), page]), \
             patch('update_irightmouse.subprocess.check_output', return_value=CASK_URL), \
             patch('update_irightmouse.update_cask') as update:
            with self.assertRaisesRegex(ValueError, '与官方更新源不一致'):
                main()
        update.assert_not_called()

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
