from unittest.case import skip

from bs4.element import NavigableString, PageElement, Tag, TemplateString
from pp.models import BadUrlException, GitHubCode, GithubCodeElement, GithubCodeLine
from django.test import TestCase

# Create your tests here.
class GithubCodeTestCase(TestCase):
    def test_about_bad_url_on_constructor(self):
        self.assertRaises(BadUrlException, lambda: GitHubCode('https://www.google.com'))
    @skip('skip this test other than local machine.')        
    def test_about_bad_url_on_open(self):
        self.assertRaises(BadUrlException, lambda: GitHubCode('https://github.com/not_requesable_source').open())
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

class MockedLine :
    def __init__(self, contents):
        self.contents = contents

class GithubCodeLineTestCase(TestCase):
    def test_about_line_as_string(self):
        tag = Tag(name='span')
        tag.string = 'abcde'
        line = MockedLine([tag, NavigableString('aaa')])
        self.assertEqual(len(GithubCodeLine(line).words), 2)
        self.assertEqual(GithubCodeLine(line).line_as_string(), "abcdeaaa")

class DummyPageElement(PageElement):
    pass

class GithubCodeElementTestCase(TestCase):
    def test_about_tagged_element(self):
        tag = Tag(name='span')
        tag.string = 'abcde '
        self.assertEqual(GithubCodeElement(tag).word, 'abcde ')

    def test_about_navigable_string(self):
        self.assertEqual(GithubCodeElement(NavigableString('abcde')).word, 'abcde')

    def test_about_navigable_string_only_line_feed(self):
        self.assertEqual(GithubCodeElement(NavigableString('\n')).word, ' ')

    def test_about_unknown_target(self):
        self.assertEqual(GithubCodeElement(DummyPageElement()).word, '')

