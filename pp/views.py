from mks_pretty_printer.settings import BASE_DIR
from django.http.response import HttpResponseBadRequest
from django.template.response import TemplateResponse
from pp.models import BadUrlException, GitHubCode
import os

# Create your views here.
def pretty_print(request):

    try:
        gitHubCode = GitHubCode(request.GET.get('url')).open()
        lines = gitHubCode.lines()
        styleHtmlFile = os.path.join(os.path.dirname(__file__), 'templates', '_style.html')
        styles = open(styleHtmlFile, 'r').read().replace('\n', '')
        return TemplateResponse(
            request,
            "_script.js",
            content_type="text/javascript; charset=utf8",
            context= {
                "lines": ''.join(list(map(lambda l : f'{l}\\n', lines))),
                "start": gitHubCode.start_line,
                "link": gitHubCode.github_url,
                "styles": styles
            })
    except BadUrlException:
        return HttpResponseBadRequest('Bad URL was requested.')
    
