# LSP-XML User Guide

## Introduction

This guide provides a concise introduction to linguistic example
sentences and their XML representation in the
[lsp-xml](https://github.com/langsci/lsp-xml) repository.

## About the data

This repository contains a set of linguistic example sentences
that were extracted from open access books published with
[Language Science Press](http://langsci-press.org/).
The files are named after the main author or editor of the book from
which the examples were extracted. In particular:

- `cangemi.xml`: examples from
  [Prosodic detail in Neapolitan Italian](http://langsci-press.org/catalog/book/16)
  by Francesco Cangemi.

- `handschuh.xml`: examples from
  [A typology of marked-S languages](http://langsci-press.org/catalog/book/18)
  by Corinna Handschuh.

- `klamer.xml`: examples from
  [The Alor-Pantar languages: History and typology](http://langsci-press.org/catalog/book/22)
  edited by Marian Klamer.

- `wilbur.xml`: examples from
  [A grammar of Pite Saami](http://langsci-press.org/catalog/book/17)
  by Joshua Wilbur.

All data in this directory is published under the
[Creative Commons Attribution 4.0 Licence](http://creativecommons.org/licenses/by/4.0/)
(CC BY 4.0).

## What are linguistic example sentences?

Let's start with a simple example:

(1) This is an English sentence.

Of course, linguists often talk about languages other than English.
Here is an example sentence from another language:

(2) Qau a ta ewar mis.

If everybody understood every language equally well, this would be
fine. But for most readers, (2) will not make any sense. We would like
to know, for example, what language the example is from, what each
word means and what the sentence as a whole means, i.e. how we would
express that sentence in English. (In the following and in the actual
data files, we will use English as a meta language to communicate
about object languages potentially other than English.)

There is a format commonly used by linguists to express this information
in a compact way, called
[interlinear glossed text](https://en.wikipedia.org/wiki/Interlinear_gloss)
or *IGT* for short.
The example in (2) looks as follows in this format:

<table class="lingex" id="ex3">
<tbody>
<tr class="meta">
  <td class="exnr">(3)</td>
  <td colspan="5" class="lang">Teiwa</td>
<tr class="src">
  <td></td>
  <td>Qau</td>
  <td>a</td>
  <td>ta</td>
  <td>ewar</td>
  <td>mis.</td>
</tr>
<tr class="imt">
  <td></td>
  <td>good</td>
  <td>3<span style="font-variant: small-caps;">sg</span></td>
  <td><span style="font-variant: small-caps;">top</span></td>
  <td>return</td>
  <td>sit</td>
</tr>
<tr class="trans">
  <td></td>
  <td colspan="5">‘So she sits down again.’</td>
</tr>
</tbody>
</table>

If you want to learn more about interlinear glossed text,
we recommend to have a look at the
[Leipzig Glossing Rules](http://www.eva.mpg.de/lingua/resources/glossing-rules.php)
that codify a standard set of conventions used by linguists worldwide.

## What does an example sentence look like in our XML format?

[Language Science Press](http://langsci-press.org/) publishes
linguistic books that potentially contain many such examples, both
glossed and unglossed.  This repository provides example sentences
from these books in a structured XML format. But what do example
sentences look like in this XML format?

Every example sentence corresponds to an `<example>` element.
These are structured as follows:

```xml
<example>
  <language>
    <!-- name of the language the example sentence is from -->
  </language>
  <reference>
    <!-- bibliographic reference to the source of the sentence,
         e.g. a grammar for that language or a linguistic article -->
  </reference>
  <label>
    <!-- an internal name of the example for cross-references -->
  </label>
  <alignedwords>
    <!-- translations for (every part of) every word, as discussed below -->
  </alignedwords>
  <translation>
    <!-- a translation of the whole sentence -->
  </translation>
</example>
```

For most purposes, you may ignore the `<reference>` and `<label>`
elements, but `<language>` and `<translation>` might be interesting.

Example (3) would look as follows in this format:

```xml
<example>
  <language>Teiwa</language>
  <reference>Klamer2010grammar</reference>
  <label>bkm:Ref336875300</label>
  <alignedwords>
    <!-- see below -->
  </alignedwords>
  <translation>‘So she sits down again.’</translation>
</example>
```

So far we have omitted details about how the word-level translations
are represented. Here is how they would look like for example (3):

```xml
<alignedwords>
  <word>
    <morpheme>
      <block type="src">Qau</block>
      <block type="imt">good</block>
    </morpheme>
  </word>
  <word>
    <morpheme>
      <block type="src">a</block>
      <block type="imt">3sg</block>
    </morpheme>
  </word>
  <!-- ... more words -->
</alignedwords>
```

The `<alignedwords>` element contains a list of words, and each word
is represented in its original form (in a `<block>` element of type
`src`, for *source language*) paired with its translation (in a
`<block>` element of type `imt`, for *interlinear morpheme translation*).
There are some abbreviations that are commonly found in
`imt` blocks, e.g. `3` means *third person*, and `sg` means
*singular*. Many of these abbreviations are listed in the appendix of
the [Leipzig Glossing Rules](http://www.eva.mpg.de/lingua/resources/glossing-rules.php).
Our XML format supports several other types of blocks, but `src` and
`imt` are the two most common ones.
(If you want to know the fine details, have a look at the
[schema](https://github.com/langsci/lsp-xml/blob/master/schemas/LinguisticExamples.rnc).)

But why are these words wrapped in another `<morpheme>` layer? This is
because words may consist of several parts (called *morphemes* in
linguistics) that each have meanings on their own. For example, the
English word *cats* consists of the morpheme *cat* and the plural
marker *s*.

Here is an example of a multi-morpheme word taken from the actual
data:

```xml
<alignedwords>
  <!-- ... -->
  <word>
    <morpheme>
      <block type="src">ge</block>
      <block type="imt">3sg.alien</block>
    </morpheme>
    <morpheme>
      <block type="src">topi</block>
      <block type="imt">hat</block>
    </morpheme>
  </word>
  <!-- ... -->
</alignedwords>
```

Since the data are extracted from actual linguistic books, written by
different authors who are following slightly different conventions,
not every example looks exactly the same. First, not every example has
explicit metadata, thus the `<language>`, `<reference>` and `<label>`
elements may be missing. Second, there are both glossed and unglossed
example sentences. An unglossed example sentence has a simpler
structure and looks as follows:

```xml
<example>
  <alignedwords>
    <!-- this element is empty in unglossed sentences -->
  </alignedwords>
  <source>
    <!-- a sentence in the original language -->
  </source>
  <translation>
    <!-- an (optional) translation of that sentence -->
  </translation>
</example>
```

Here is a minimal example, taken from the actual data:

```xml
<example>
  <alignedwords>
  </alignedwords>
  <source>As for Milena, she drinks it unsweetened;
    as for the others, I couldn’t tell.</source>
</example>
```

There is one final complication:
Linguistic example sentences may also have subexamples.
That's why we cannot simply put all `<example>` sentences
under the root element. Instead, we use a container
element for example sentences that may contain
additional subexamples. This looks as follows:

```xml
<exampleitem>
  <example>
    <!-- a single example sentence can go here -->
  </example>
  <examples>
    <!-- a list of subexamples (example items) can go here -->
  </examples>
</exampleitem>
```

Notice that subexamples are wrapped in an `<examples>` element
which is also the root element of the XML format we are using.
In this way, subexamples may contain subexamples themselves.

We hope that you now have a pretty good idea of how the XML files are
structured. For the official details, have a look at our RELAX NG
[schema](https://github.com/langsci/lsp-xml/blob/master/schemas/LinguisticExamples.rnc)
or the [files themselves](https://github.com/langsci/lsp-xml/tree/master/data).

## Getting started: How to extract some data using using Python

Let's say, we want to find out how many examples from each language
are contained in a LangSci book. Here is how we could do this in
Python:

```python
import sys
import xml.etree.ElementTree as ET
from collections import Counter

xmlfile = sys.argv[1]
tree = ET.parse(xmlfile)
root = tree.getroot()

languages = (l.text for l in root.findall(".//language"))
langfreqs = Counter(languages)
print("\n".join("{}: {}".format(c,l) for (l,c) in langfreqs.most_common(10)))
```

If you call this little script with the path to an lsp-xml file as a
command-line argument, a list of the ten most frequent languages with
their example counts will be printed. For example, it will print the
following for `data/klamer.xml` at the time of writing:

```
50: Abui
44: Teiwa
40: Kamang
30: Western Pantar
18: Wersing
15: Adang
10: Blagar
7: Tobelo
3: Klon
3: Kaera
```

If you rather want a JSON representation of the language frequencies,
just replace the last line in the python code above by the following:

```python
print(json.dumps(langfreqs))
```

Or let's say we want to find out how many examples there are in a
book. One simple approach is to find all `<example>` elements and just
count them:

```python
examples = root.findall(".//example")
print(len(examples))
```

If we run that script on the XML files in the data directory, we get
(at the time of writing):

```
16 cangemi.xml
561 handschuh.xml
491 klamer.xml
327 wilbur.xml
```

Beware, however, that this rough count also includes empty `<example>`
elements that are used as mere containers for subexamples.

If you want to dive a bit deeper, you could have a look at
[our demo script](https://github.com/langsci/lsp-xml/blob/master/code/explore-lspxml.py)
`code/explore-lspxml.py` that can output more accurate counts
and convert lsp-xml examples to simple HTML tables. It provides a
simple Python class for example sentences that mirrors some aspects of
the XML structure discussed above.

Here is how you can use it on the command line. If you provide the
path to an lsp-xml file as the single argument, it will print the
number of glossed and unglossed example sentences in that file.

```
$ ./code/explore-lspxml.py data/handschuh.xml

data/handschuh.xml:
369 glossed examples
24 unglossed examples

$ ./code/explore-lspxml.py data/klamer.xml

data/klamer.xml:
352 glossed examples
102 unglossed examples
```

If you provide an integer `i` as an additional command-line argument,
it will look up the `i`-th example in the provided file and return it
as an HTML table. For example:

```
$ ./code/explore-lspxml.py data/wilbur.xml 55

Converting example 55 from data/wilbur.xml to HTML:
<table>
<tr><td>mikkir</td><td>málle</td><td>li-j</td></tr>
<tr><td>which</td><td>blood/nom.sg</td><td>be-3sg.pst</td></tr>
<tr><td colspan="3">‘Which (kind of) blood was it?’</tr>
</table>
```

In HTML, this will be rendered as:

<table>
<tr><td>mikkir</td><td>málle</td><td>li-j</td></tr>
<tr><td>which</td><td>blood/nom.sg</td><td>be-3sg.pst</td></tr>
<tr><td colspan="3">‘Which (kind of) blood was it?’</tr>
</table>


## Project ideas: What can you do with it?

Some ideas for applications:

* A language guessing game: show a random word from an example with a
  language label and let the player guess from four options which
  language it might be from.

* Generate a lexicon for a language by collecting all word or morpheme
  glosses.

* Find interesting ways of visualizing glossed linguistic example
  sentences, using e.g. interactive tables where the user can show or
  hide certain information, like translations or metadata.
