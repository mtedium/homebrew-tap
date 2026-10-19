import unittest
from update_irightmouse import parse_page, resolve_download


class DownloadParsingTest(unittest.TestCase):
    def test_download_element(self):
        page = """<a href='/other'>下载专业版</a>
        <a HREF='javascript:fileDownload({&quot;jumpIde&quot;:&quot;Y29ycmVjdA==&quot;})'
           ID="module3607FlBtn">立即获取</a>"""
        self.assertEqual(parse_page(page), 'Y29ycmVjdA==')

    def test_changed_element_fails(self):
        button = '<a id="module3607FlBtn" href="/download">下载</a>'
        for page in ['', button, button * 2]:
            with self.subTest(page=page), self.assertRaises(ValueError):
                parse_page(page)

    def test_download_response(self):
        # 模拟接口返回的地址；生产代码原样使用，不拼接文件 ID。
        url = '//download.s21i.co99.net/new-file.dmg?f=release.dmg&v=123'
        response = {'success': True, 'file': {
            'name': 'iRightMousePro2.6.0_2026101901.dmg',
            'allowDownload': True, 'downloadUrl': url}}
        self.assertEqual(resolve_download(response),
                         ('2.6.0', 'https:' + url, '2026101901'))
        for key, value in [('name', 'OtherApp.dmg'), ('allowDownload', False),
                           ('downloadUrl', 'https://other.example/app.dmg')]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                resolve_download({'success': True, 'file': {**response['file'], key: value}})
        with self.assertRaises(ValueError):
            resolve_download({'success': False})


if __name__ == '__main__':
    unittest.main()
