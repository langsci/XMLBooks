#!/usr/bin/env python3

# ------------------------------------------------------------
# Copyright: (c) Language Science Press 2015.
# Contact: mathias.schenner@langsci-press.org
# License: Creative Commons Attribution 4.0 Licence (CC BY).
#
# This is demo code for the LangSci linguistic example database
# available at https://github.com/langsci/lsp-xml
# ------------------------------------------------------------

import sys
from xml.dom.minidom import parse
from itertools import chain


class Example:
    """
    A simple representation of a linguistic example sentence.
    """

    def __init__(self, xmlex):
        """
        Build an example instance from its lsp-xml representation.

        :param xmlex: an <example> element from an lsp-xml file.
        """
        self.language = self._extract_language(xmlex)
        self.words = self._extract_words(xmlex)
        self.lines = self._extract_lines(xmlex)

    def __str__(self):
        """
        Return language (if known) as well as all glossed and unglossed lines.
        """
        language = ["language: {}".format(self.language)] if self.language else []
        glosses = ("{}: {}".format(k," ".join(v)) for k,v in self.words.items())
        lines = ("{}: {}".format(k,v) for k,v in self.lines.items())
        return "\n".join(chain(language, glosses, lines))

    def has_glosses(self):
        """
        Return whether the example contains gloss lines.
        """
        return bool(self.words)

    def has_lines(self):
        """
        Return whether the example contains non-empty free lines.
        """
        return any(self.lines.values())

    def is_empty(self):
        """
        Return whether the example contains no lines.
        """
        return not(self.has_glosses() or self.has_lines())

    def get_words(self, key):
        """
        Return a list of words for the provided type of gloss line.

        :param key: a gloss line type, e.g. 'src' or 'imt'.
        """
        return self.words.get(key, [])

    def get_line(self, key):
        """
        Return a string representation for the provided type of free line.

        :param key: a non-glossed line type, e.g. 'source' or 'translation'.
        """
        return self.lines.get(key, "")

    def _extract_language(self, xmlex):
        lang = xmlex.getElementsByTagName("language")
        if len(lang) > 0:
            return lang[0].firstChild.data
        else:
            return None

    def _extract_words(self, xmlex):
        # build a { linetype : [string] } dict
        xwords = xmlex.getElementsByTagName("word")
        words = map(lambda d: list(d.items()),
                    (self._extract_word(w) for w in xwords))
        return {k:v for k,v in
                map(lambda x: (x[0][0], list(
                    map(lambda y: y[1], x))), (zip(*words)))}

    def _extract_word(self, xmlwd):
        morpheme_sep = "-"
        xmorphemes = xmlwd.getElementsByTagName("morpheme")
        all_blocks = (m.getElementsByTagName("block") for m in xmorphemes)
        morphemes = (((b.getAttribute("type"),
                      (b.firstChild.data if b.hasChildNodes() else ""))
                      for b in blocks) for blocks in all_blocks)
        return {k:v for k,v in
                map(lambda x: (x[0][0], morpheme_sep.join(
                    map(lambda y: y[1], x))), (zip(*morphemes)))}

    def _extract_lines(self, xmlex):
        # build a { linetype : string } dict
        tags = ["source", "translation"]
        return {tag: (self._extract_line(xmlex, tag).firstChild.data
                      if self._extract_line(xmlex, tag).hasChildNodes()
                      else "")
                for tag in tags
                if self._extract_line(xmlex, tag)}

    def _extract_line(self, xmlex, tag):
        maybe_line = xmlex.getElementsByTagName(tag)
        if len(maybe_line) > 0:
            return maybe_line[0]
        else:
            return None


# -------------------- global functions

def read_examples(xmlfile):
    """
    Build a list of Example objects from an lsp-xml document.
    """
    doc = parse(xmlfile)
    examples = [Example(e) for e in doc.getElementsByTagName("example")]
    return examples

def convert_to_html_table(example):
    """
    Return string representation of an HTML table for an Example object.

    This function illustrates how to extract information from Example
    objects. Notice that we are explicitly selecting the 'src', 'imt'
    and 'translation' lines. If an Example does not have such lines,
    the corresponding table lines will be empty.
    """
    if example.is_empty():
        return "Sorry, this example is empty."
    src = example.get_words("src")
    imt = example.get_words("imt")
    trans = example.get_line("translation")
    table = lambda rows: "<table>\n{}\n</table>".format("\n".join(rows))
    tline = lambda cells: "<tr><td>{}</td></tr>".format("</td><td>".join(cells))
    mline = lambda line: '<tr><td colspan="{}">{}</tr>'.format(len(src), line)
    return table([tline(src), tline(imt), mline(trans)])

def count_examples(xmlfile):
    """
    Return the number of glossed and unglossed examples in an lsp-xml file.
    """
    examples = read_examples(xmlfile)
    gloss = lambda e: (e.has_glosses(), not(e.has_glosses()) and e.has_lines())
    (glossed, unglossed) = map(sum,(zip(*map(gloss, examples))))
    return (glossed, unglossed)

if __name__ == "__main__":

    if len(sys.argv) == 2:
        xmlfile = sys.argv[1]
        (glossed, unglossed) = count_examples(xmlfile)
        print("{}:\n{} glossed examples\n{} unglossed examples".format(
                xmlfile, glossed, unglossed))

    elif len(sys.argv) == 3:
        xmlfile = sys.argv[1]
        exnr = int(sys.argv[2])
        examples = read_examples(xmlfile)
        maxnr = len(examples) - 1
        if exnr > maxnr or exnr < 0:
            sys.exit("No such example. Choose a number in [0,{}]".format(maxnr))
        else:
            print("Converting example {} from {} to HTML:".format(exnr, xmlfile))
            print(convert_to_html_table(examples[exnr]))

    else:
        sys.exit("Usage: provide an lsp-xml file as argument")
