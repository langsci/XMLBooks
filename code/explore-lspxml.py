#!/usr/bin/env python3

# ------------------------------------------------------------
# Copyright: (c) Language Science Press 2015.
# Contact: mathias.schenner@langsci-press.org
# License: Creative Commons Attribution 4.0 Licence (CC BY).
#
# This is demo code for the LangSci linguistic example database
# available at https://github.com/langsci/lsp-xml
# ------------------------------------------------------------

import json
import os
import re
import sys
import xml.dom.minidom as dom
from itertools import chain


class Example:
    """
    A simple representation of a linguistic example sentence.
    """

    def __init__(self, xmlex, default_lang=None, reference=None):
        """
        Build an example instance from its lsp-xml representation.

        :param xmlex: an <example> element from an lsp-xml file.
        :param default_lang: optional default language.
        :param reference: optional reference string.
        """
        self.language = Example._extract_language(xmlex, default_lang)
        self.words = Example._extract_words(xmlex)
        self.lines = Example._extract_lines(xmlex)
        self.reference = reference

    def __str__(self):
        """
        Return reference, language, gloss lines and free lines.
        """
        ref = ["reference: {}".format(self.reference)] if self.reference else []
        lang = ["language: {}".format(self.language)] if self.language else []
        glosses = ("{}: {}".format(k," ".join(v)) for k,v in self.words.items())
        lines = ("{}: {}".format(k,v) for k,v in self.lines.items())
        return "\n".join(chain(ref, lang, glosses, lines))

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

    def to_simple_tuple(self):
        """
        Return a simplified tuple representation of the form:
        (source, translation, language, reference).
        """
        src = Example._sanitize_src(" ".join(self.get_words("src"))
                                    if self.has_glosses
                                    else self.get_line("source"))
        trans = Example._sanitize_trans(self.get_line("translation"))
        lang = self.language
        ref = self.reference
        tup = (src, trans, lang, ref)
        # only return tuple if all elements are populated
        if all(tup):
            return tup

    @staticmethod
    def _extract_language(xmlex, default_lang):
        lang = (xmlex.firstChild.firstChild.data
                if (xmlex.hasChildNodes() and
                    xmlex.firstChild.tagName == "language")
                else None)
        if not lang:
            lang = (Example._extract_language(
                      Example._get_sup_example(xmlex), default_lang)
                    if Example._has_sup_example(xmlex)
                    else default_lang)
        return lang

    @staticmethod
    def _extract_words(xmlex):
        # build a { linetype : [string] } dict
        xwords = xmlex.getElementsByTagName("word")
        words = map(lambda d: list(d.items()),
                    (Example._extract_word(w) for w in xwords))
        return {k:v for k,v in
                map(lambda x: (x[0][0], list(
                    map(lambda y: y[1], x))), (zip(*words)))}

    @staticmethod
    def _extract_word(xmlwd):
        morpheme_sep = "-"
        xmorphemes = xmlwd.getElementsByTagName("morpheme")
        all_blocks = (m.getElementsByTagName("block") for m in xmorphemes)
        morphemes = (((b.getAttribute("type"),
                      (b.firstChild.data if b.hasChildNodes() else ""))
                      for b in blocks) for blocks in all_blocks)
        return {k:v for k,v in
                map(lambda x: (x[0][0], morpheme_sep.join(
                    map(lambda y: y[1], x))), (zip(*morphemes)))}

    @staticmethod
    def _extract_lines(xmlex):
        # build a { linetype : string } dict
        tags = ["source", "translation"]
        return {tag: (Example._extract_line(xmlex, tag).firstChild.data
                      if Example._extract_line(xmlex, tag).hasChildNodes()
                      else "")
                for tag in tags
                if Example._extract_line(xmlex, tag)}

    @staticmethod
    def _extract_line(xmlex, tag):
        maybe_line = xmlex.getElementsByTagName(tag)
        if len(maybe_line) > 0:
            return maybe_line[0]

    @staticmethod
    def _has_sup_example(xmlex):
        # Return whether the example has a parent example.
        return bool(Example._get_sup_example(xmlex))

    @staticmethod
    def _get_sup_example(xmlex):
        # Return the parent example of an example element
        # (or None if there is no containing example).
        nextnode = xmlex.parentNode
        if nextnode.nodeType != dom.Node.DOCUMENT_NODE:
            nextnode = nextnode.parentNode
            if nextnode.nodeType != dom.Node.DOCUMENT_NODE:
                assert nextnode.tagName == "examples"
                return nextnode.previousSibling

    @staticmethod
    def _sanitize_src(src):
        """
        Trim source string, dropping square brackets around constituents
        and grammatical category labels.
        """
        # fail if example contains ungrammatical parts or alternatives
        if any(map(lambda x: x in src, ["*", "/", "(", ")"])):
            return None
        # remove constituent brackets
        while True:
            repl = re.sub(r"\[(.*?)\]\w*", r"\1", src)
            if src != repl:
                src = repl
            else:
                return repl

    @staticmethod
    def _sanitize_trans(trans):
        """
        Trim translation string down to a minimum, dropping embedded
        metadata like corpus references or citations.
        """
        # heuristic: extract first string between typographic quotes
        # that is terminated by a period or followed by whitespace.
        xs = re.findall(r"(?:‘(.*?\.)’)|(?:‘(.*?[^.])’(?:\s|$))", trans)
        return "".join(xs[0]) if xs else None


# -------------------- global functions

def read_examples(xmlfile):
    """
    Build a list of Example objects from an lsp-xml document.
    """
    # some metadata: default language and reference
    default_language = {"berghall.xml": "Mauwake",
                        "schackow.xml": "Yakkha",
                        "wilbur.xml": "Pite Saami"}
    reference = {"berghall.xml": "Liisa Berghäll",
                 "cangemi.xml": "Francesco Cangemi",
                 "dahl.xml": "Östen Dahl",
                 "handschuh.xml": "Corinna Handschuh",
                 "klamer.xml": "Marian Klamer",
                 "schackow.xml": "Diana Schackow",
                 "wilbur.xml": "Joshua Wilbur"}
    # parse examples
    doc = dom.parse(xmlfile)
    key = os.path.basename(xmlfile)
    lang = default_language.get(key)
    ref = reference.get(key)
    examples = filter(lambda e: not(e.is_empty()),
                      map(lambda ex: Example(ex, lang, ref),
                          doc.getElementsByTagName("example")))
    return list(examples)

def convert_to_tuples(examples):
    """
    Convert a list of Example objects to tuples of the form:
    (source, translation, language, reference).
    """
    convert1 = lambda e: e.to_simple_tuple()
    return list(filter(bool, map(convert1, examples)))

def convert_to_json(examples):
    """
    Convert a list of Example objects to a JSON list
    where each element has the following form:
    [source, translation, language, reference].
    """
    return json.dumps(convert_to_tuples(examples),
                      indent=2,
                      ensure_ascii=False)

def convert_to_html_table(example):
    """
    Return string representation of an HTML table for an Example object.

    This function illustrates how to extract information from Example
    objects. Notice that we are explicitly selecting the 'src', 'imt'
    and 'translation' lines. If an Example does not have such lines,
    the corresponding table lines will be empty.
    """
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


# -------------------- main

def print_count(xmlfile):
    # print number of glossed and unglossed examples
    (glossed, unglossed) = count_examples(xmlfile)
    print("{}:\n{} glossed examples\n{} unglossed examples".format(
            xmlfile, glossed, unglossed))

def print_html(examples, exnr):
    # print single example as html table
    maxnr = len(examples) - 1
    if exnr > maxnr or exnr < 0:
        sys.exit("Error: No such example."
                 + " Choose a number in [0,{}]".format(maxnr))
    else:
        print(convert_to_html_table(examples[exnr]))

def main():
    # with one argument: print simple statistics
    if len(sys.argv) == 2:
        print_count(sys.argv[1])

    # with two arguments: convert to json or html
    elif len(sys.argv) == 3:
        xmlfile = sys.argv[1]
        examples = read_examples(xmlfile)

        # if second argument is "json",
        # print all examples in a simplified json format
        if sys.argv[2] == "json":
            print(convert_to_json(examples))

        # if second argument is an example number,
        # convert that example to an html table
        else:
            try:
                exnr = int(sys.argv[2])
            except ValueError:
                sys.exit("Error: Provide a number as second argument"
                         + " to select an example.")
            print_html(examples, exnr)

    else:
        sys.exit("Usage: provide an lsp-xml file as argument")

if __name__ == "__main__":
    main()
