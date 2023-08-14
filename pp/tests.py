from pp.models import BadUrlException, GitHubCode
from django.test import TestCase
from unittest.mock import patch, MagicMock

class GithubCodeTestCase(TestCase):
    def test_about_bad_url_on_constructor(self):
        self.assertRaises(BadUrlException, lambda: GitHubCode('https://www.google.com'))
    def test_about_code_range(self):
        gitHubCode = GitHubCode('https://github.com/not_requesable_source#L11-L22')
        self.assertEqual(gitHubCode.get_start_line(), 11)
        self.assertEqual(gitHubCode.get_end_line(), 22)
    def test_about_code_range_without_end(self):
        gitHubCode = GitHubCode('https://github.com/not_requesable_source#L11')
        self.assertEqual(gitHubCode.get_start_line(), 11)
        self.assertEqual(gitHubCode.get_end_line(), None)
    def test_about_code_range_without_start_and_end(self):
        gitHubCode = GitHubCode('https://github.com/not_requesable_source')
        self.assertEqual(gitHubCode.get_start_line(), 1)
        self.assertEqual(gitHubCode.get_end_line(), None)

    def test_about_code_selection(self):
        mock = MagicMock()
        mock.return_value = ["aaa", "bbb", "ccc", "ddd"]
        with patch('pp.models.GitHubCode._get_codes', mock):

            code = GitHubCode('https://github.com/not_requesable_source#L1').open()
            self.assertEqual(['aaa'], code.lines())

            code = GitHubCode('https://github.com/not_requesable_source#L4').open()
            self.assertEqual(['ddd'], code.lines())

            code = GitHubCode('https://github.com/not_requesable_source#L1-L2').open()
            self.assertEqual(['aaa', 'bbb'], code.lines())

            code = GitHubCode('https://github.com/not_requesable_source').open()
            self.assertEqual(['aaa', 'bbb', 'ccc', 'ddd'], code.lines())

            code = GitHubCode('https://github.com/not_requesable_source#L12-14').open()
            self.assertEqual([], code.lines())

            code = GitHubCode('https://github.com/not_requesable_source#L1-14').open()
            self.assertEqual(['aaa', 'bbb', 'ccc', 'ddd'], code.lines())

            code = GitHubCode('https://github.com/not_requesable_source#5').open()
            self.assertEqual([], code.lines())

