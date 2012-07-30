# Script from http://www.w3.org/QA/2008/04/unescape-html-entities-python.html
import re
import htmlentitydefs


def unescape(text):
    """Removes HTML or XML character references
      and entities from a text string.
      keep &amp;, &gt;, &lt; in the source code.
    from Fredrik Lundh
    http://effbot.org/zone/re-sub.htm#unescape-html
    """
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                #print "erreur de valeur"
                pass
        else:
            # named entity
            try:
                if text[1:-1] == "amp":
                    text = "&amp;amp;"
                elif text[1:-1] == "gt":
                    text = "&amp;gt;"
                elif text[1:-1] == "lt":
                    text = "&amp;lt;"
                else:
                    #print text[1:-1]
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                #print "keyerror"
                pass
        return text  # leave as is
    return re.sub("&#?\w+;", fixup, text)
