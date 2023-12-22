import re
from django.utils.html import escape

def replace(line):
    x = line.group(0)
    if x[-1] in '*/]':
        f = x[-1]

        return '\\' + x[:-1] + '\\' + f
    return '\\' + x.strip() + '\\' + re.findall(r'(\s|\n|$)', x)[0]

def process_chords_text(text):
    """Replace all chords in text with html span.chord tags"""
    text = escape(text)
    result = ""
    for line in text.split("\n"):

        if len(line.split()) < 3 or len(re.findall(r"([A-H][#b]?[dimMaj7sus4b0-9\+]*)(\s|$|\/|\*)", line)) > 1:
            line = re.sub(r"([A-H][#b]?[dimMaj7sus4b0-9\+]*)(\s|$|\/|\*)", replace, line)

        line = re.sub(r"\\+([A-H][#b]?[dimMaj7sus4b0-9\+]*)\\+", r'<span class="chord">\1</span>', line)

        result += line + '\n'
    return result
