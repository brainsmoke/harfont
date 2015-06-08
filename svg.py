
def header(width, height):
    return """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:xlink="http://www.w3.org/1999/xlink"
   width="""+"\""+str(width)+"\""+"""
   height="""+"\""+str(height)+"\""+"""
   id="harfont"
   >"""

def background(width, height, style):
    return "<rect width=\""+str(width)+"\" height=\""+str(height)+"\"" + \
           " style=\""+style+"\" />"

def footer():
    return "</svg>"

def group(code, transform=None, id=None):
    if id:
        ident = ' id="'+id+'"'
    else:
        ident = ''

    if transform:
        trans = ' transform="'+transform+'"'
    else:
        trans = ''

    return "<g"+ident+trans+">"+code+"</g>\n"

def path(path, style):
    return '<path d="'+path+'" style="'+style+'"/>'

def use(id, transform=None):
    if transform:
        trans = ' transform="'+transform+'"'
    else:
        trans = ''

    return '<use xlink:href="#'+id+'" '+trans+'/>'

