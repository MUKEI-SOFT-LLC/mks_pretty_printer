import urllib.request 
from bs4 import BeautifulSoup, Tag, NavigableString

class GitHubCode :
    def __init__(self, url):
        if (not(url) or not(url.startswith('https://github.com/'))):
            raise BadUrlException('Bad url was requested.');
        self.github_url = url
        self.start_line = 1
        self.end_line = None
        self.ids = []
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
        urllib.request.HTTPError
        try: 
            req = urllib.request.Request(self.github_url)
            html = urllib.request.urlopen(req)
        except urllib.request.HTTPError as e:
            raise BadUrlException('Bad url was requested')
        soup = BeautifulSoup(html, "html5lib")
        all_lines = soup.find_all("td", attrs={"class": "blob-code-inner"})
        filtered = all_lines
        if (self.ids) :
            filtered = filter(lambda l: 0 < self.ids.count(l.get('id')), all_lines)
        self.codes = list(map(lambda l : GithubCodeLine(l), filtered))
        return self

    def lines(self): 
        return list(map(lambda l : l.line_as_string().replace('\\n', '\\\\n'), self.codes))


class GithubCodeLine:
    def __init__(self, line):
        self.line = line
        self.words = list(map(lambda w : GithubCodeElement(w), self.line.contents))

    def line_as_string(self) -> str:  
        return ''.join(list(map(lambda w: w.word, self.words)))

class GithubCodeElement:
    def __init__(self, word) :
        self.word = ''
        if (isinstance(word, Tag)) :
            self.word = word.get_text(strip=True)

        if (isinstance(word, NavigableString)) :
            self.word = word
            if ('\n' == self.word):
                self.word = ' '

class BadUrlException(Exception):
    pass