from bs4 import BeautifulSoup, Tag, NavigableString
from selenium import webdriver

DEFAULT_OPTION = webdriver.ChromeOptions()
DEFAULT_OPTION.add_argument('--headless')
DEFAULT_OPTION.add_argument('--no-sandbox')

class GitHubCode :
    def __init__(self, url):
        if (not(url) or not(url.startswith('https://github.com/'))):
            raise BadUrlException('Bad url was requested.');
        self.github_url = url
        self.start_line = 1
        self.end_line = None
        self.ids = []
        self.codes = []
        fragments = self.github_url.split('#')
        if (2 == len(fragments)):
            range_array = fragments[1].split('-')
            if (2 == len(range_array)):
                self.start_line = int(range_array[0].replace('L', ''))
                self.end_line = int(range_array[1].replace('L', ''))
                self.ids = list(map(lambda x : self.formatAsId(x) ,range(self.start_line, self.end_line + 1)))
            elif (1 == len(range_array)):
                self.start_line = int(range_array[0].replace('L', ''))
                self.ids = [self.formatAsId(self.start_line)]

    def formatAsId(self, num) -> str : return 'LC{}'.format(num)

    def get_start_line(self) -> int :
        return self.start_line

    def get_end_line(self) -> int :
        return self.end_line

    def open(self) :
        all_lines = self._get_codes()
        if (1 == self.start_line and -1 == self.github_url.find('#') and not self.end_line ):
            # all lines.
            self.codes = all_lines
        elif(not self.end_line and self.start_line <= len(all_lines)):
            # specific line only.
            self.codes.append(all_lines[self.start_line - 1])
        else:
            # lines selected range. ex "1-5"
            self.codes = all_lines[self.start_line - 1:self.end_line]
        return self

    def lines(self): 
        return list(map(lambda l: l.replace('\\n', '\\\\n') ,self.codes))
    
    # declare for mock testing...
    def _get_codes(self):
        browser = webdriver.Chrome(options=DEFAULT_OPTION)
        browser.get(self.github_url)
        html = browser.page_source
        soup = BeautifulSoup(html, "html5lib")
        return soup.find(id = 'read-only-cursor-text-area').get_text().split('\n')

class BadUrlException(Exception):
    pass