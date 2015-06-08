#!/usr/bin/env python
#
# usage: $0 [-center] < in.utf-8 > out.svg

import sys

import svg, ghostmeat as font

har_style = { 'f' : "fill:#f7ee09;fill-opacity:1",
              's' : "fill:#f78a11;fill-opacity:1", }

def get_glyph(char):
    if char in font.glyphs:
        return font.glyphs[char]
    else:
        return font.glyph_missing

def get_kerning(c1, c2):
    if c1+c2 in font.kernpairs:
        return font.kernpairs[c1+c2]
    else:
        return 0

def get_char_id(c):
    return "glyph_u"+str(ord(c))

def get_char(c, relx, style, glyph_cache=[]):
    g = get_glyph(c)

    if c in glyph_cache:
        p = svg.use(get_char_id(c), "translate(%g 0)" % relx)
    else:
        glyph_cache.append(c)
        regions = filter(None, g['path'].split('Z'))
        styles = map(lambda x: style[x], g['colouring'])
        paths = "".join(svg.path(r+'Z', s) for (r, s) in zip(regions, styles))
        p = svg.group(svg.group(paths, "scale(1 -1)", id=get_char_id(c)), "translate(%g 0)" % relx)

    return (g['advance'], p)

def get_line(text, style, glyph_cache=[]):
    relx = 0
    chars = []
    last = ""
    for c in text:
        relx += get_kerning(last, c)
        (dx, char) = get_char(c, relx, style, glyph_cache)
        relx += dx
        chars.append(char)
        last = c

    return ("\n".join(chars), relx)

def get_multiline(text, style, center=False, glyph_cache=[]):
    rely = 0
    lines = map(lambda l: get_line(l, style, glyph_cache), text.split("\n"))
    maxwidth = max(map(lambda (_, w): w, lines))
    moved_lines = []

    for (line, width) in lines:
        if center:
            relx = (maxwidth-width)/2.
        else:
            relx = 0

        moved_lines.append(svg.group(line, "translate(%g %g)" % (relx, rely)))
        rely += font.units_per_em

    return ("\n".join(moved_lines), maxwidth, (len(lines)-1)*font.units_per_em)

def har_text_svg(text, font_size=72, margin=72, center=False,
                 style=har_style, glyph_cache=[], f=sys.stdout):

    scale = (font_size/float(font.units_per_em))
    top, right, bottom, left = margin+font.ascent*scale, margin, margin-font.descent*scale, margin

    (svg_text, w, h) = get_multiline(text, style, center)
    print >>f, svg.header(w*scale + left + right, h*scale + top + bottom)
    print >>f, svg.group(svg_text, "translate(%g %g) scale(%g)" % ( left, top, scale ) )
    print >>f, svg.footer()

if __name__ == '__main__':
    center = '-center' in sys.argv
    #text = u"".join(font.glyphs.keys())
    text = ''.join(sys.stdin.readlines()).decode('utf-8')
    if text[-1] == "\n":
        text = text[:-1]

    har_text_svg(text, center=center)

