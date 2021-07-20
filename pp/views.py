from django.http.response import HttpResponseBadRequest
from django.template.response import TemplateResponse
from pp.models import BadUrlException, GitHubCode

# Create your views here.
def pretty_print(request):

    try:
        gitHubCode = GitHubCode(request.GET.get('url')).open()
        lines = gitHubCode.lines()

        styles = open("./pp/templates/_style.html", 'r').read().replace('\n', '')
        return TemplateResponse(
            request,
            "_script.js",
            content_type="text/javascript; charset=utf8",
            context= {
                "lines": '\\n'.join(lines),
                "start": gitHubCode.start_line,
                "link": gitHubCode.github_url,
                "styles": styles
            })
    except BadUrlException:
        return HttpResponseBadRequest('Bad URL was requested.')
    
