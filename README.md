# Structured data from LangSci books

## About

This repository provides linguistic example sentences in XML
format that were extracted from open access books published with
[Language Science Press](http://langsci-press.org/).
There are both glossed and unglossed sentences, depending on the
original source.

The actual data files are located in the `data` directory. Their structure
is described by the RELAX NG schema in `schemas/LinguisticExamples.rnc`.

## Documentation

For a short and gentle introduction to linguistic example sentences
and their XML representation in this repository, have a look at our
[user guide](https://github.com/langsci/lsp-xml/blob/master/doc/user-guide.md).

In addition, we provide some
[Python demo code](https://github.com/langsci/lsp-xml/blob/master/code/explore-lspxml.py)
that illustrates how the XML files can be parsed and used. The
[user guide](https://github.com/langsci/lsp-xml/blob/master/doc/user-guide.md)
also contains a short description of the demo code.

## Data sources

The files in the `data` directory are named after the main author or
editor of the book from which the examples were extracted.
In particular:

- `cangemi.xml`: examples from
  [Prosodic detail in Neapolitan Italian](http://langsci-press.org/catalog/book/16)
  by Francesco Cangemi.

- `dahl.xml`: examples from
  [Grammaticalization in the North](http://langsci-press.org/catalog/book/73)
  by Östen Dahl.

- `handschuh.xml`: examples from
  [A typology of marked-S languages](http://langsci-press.org/catalog/book/18)
  by Corinna Handschuh.

- `klamer.xml`: examples from
  [The Alor-Pantar languages: History and typology](http://langsci-press.org/catalog/book/22)
  edited by Marian Klamer.

- `schackow.xml`: examples from
  [A grammar of Yakkha](http://langsci-press.org/catalog/book/66)
  by Diana Schackow.

- `wilbur.xml`: examples from
  [A grammar of Pite Saami](http://langsci-press.org/catalog/book/17)
  by Joshua Wilbur.

## License

Copyright: (c) Language Science Press 2014-2015.

All data, code and documentation in this repository is published under the
[Creative Commons Attribution 4.0 Licence](http://creativecommons.org/licenses/by/4.0/)
(CC BY 4.0).
