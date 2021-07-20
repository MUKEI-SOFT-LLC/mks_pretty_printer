var codeLines = '{% include "_code_content.html" %}';
var container = document.createElement('div');
container.innerHTML = codeLines;

var current = document.currentScript;
var target = current.nextElementSibling;
current.parentNode.insertBefore(container, target);

var script = document.createElement('script');
script.src = "https://cdn.jsdelivr.net/gh/google/code-prettify@master/loader/run_prettify.js?skin=desert";
current.parentNode.insertBefore(script, target);