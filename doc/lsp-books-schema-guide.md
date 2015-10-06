# The LangSci Press Document Model

This is a short guide to the preliminary TEI-based XML schema used by
LangSci Press.

There are three main directions of development that will affect future
versions of the schema:

- Simplification: The current schema is defined as the union of
  several TEI modules. However, only a small subset of the elements
  and attributes defined in these modules is actually used. Future
  versions of the schema will explicitly exclude unused elements.

- Elaboration: The current description of the markup conventions used
  in LangSci documents strives to be as simple and light-weight as
  possible in order to speed up the development of prototype
  converters that can actually produce conformant XML documents from
  LaTeX sources. Future versions of the schema will elaborate the
  defined elements to provide additional structure.

- Source Extensions: The ability of a converter to capture semantic
  distinctions is limited by the markup conventions used in the
  original document. If the source document uses semantic rather than
  primarily print-oriented encoding conventions, the schema can be
  expanded to include more fine-grained semantic distinctions
  (e.g. reliable glossline type attributes in linguistic examples or
  elements like `<foreign>`, `<mentioned>`, `<term>`, `<gloss>`,
  `<cit>`, `<quote>`).

## Schema definition

The XML schema is directly based on the TEI P5 Guidelines and includes
the TEI modules `tei`, `header`, `core`, `textstructure`, `figures`,
`linking`, `analysis`, `iso-fs` and `nets`.

The preliminary schema is defined by the following ODD document.

```xml
<schemaSpec ident="LSP-preliminary" start="TEI">
  <moduleRef key="tei"/>
  <moduleRef key="header"/>
  <moduleRef key="core"/>
  <moduleRef key="textstructure"/>
  <moduleRef key="figures"/>
  <moduleRef key="linking"/>
  <moduleRef key="analysis"/>
  <moduleRef key="iso-fs"/>
  <moduleRef key="nets"/>
</schemaSpec>
```

The final version will exclude unused elements and probably include
SVG and MathML.

## Document structure

A LangSci document consists of a `<TEI>` root element with exactly two
children, `<teiHeader>` for document metainformation and `<text>` for
the main content. The latter is further subdivided into front matter
(title page), main matter and back matter (bibliography). The main
matter is wrapped in a `<body>` element (in the case of monographs) or
in a `<group>` element (in the case of collections). The latter
contains a sequence of `<text>` elements for the individual
contributions.

The typical top-level structure of a monograph thus looks as follows:

```xml
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
    <!-- metadata -->
  </teiHeader>
  <text>
    <front>
      <!-- front matter -->
    </front>
    <body>
      <!-- main matter -->
    </body>
    <back>
      <!-- back matter -->
    </back>
  </text>
</TEI>
```

## Header

The main purpose of the header is to provide extensive bibliographic
information about the document. The structure of the header is
determined by the TEI `header` module.

Headers for individual books are based on the following template:

```xml
<teiHeader>
  <fileDesc>
    <titleStmt>
      <title type="full">
        <title type="main">...</title>
        <title type="sub">...</title>
      </title>
      <author>...</author>  <!-- or <editor>...</editor> -->
      <respStmt>            <!-- typesetters -->
        <resp>typesetting</resp>
        <name>...</name>
      </respStmt>
      <respStmt>            <!-- proofreaders -->
        <resp>proofreading</resp>
        <name>...</name>
      </respStmt>
      <respStmt>            <!-- storage and cataloguing -->
        <resp>storage</resp>
        <orgName>Freie Universität Berlin</orgName>
      </respStmt>
      <respStmt>
        <resp>cataloguing</resp>
        <orgName>Freie Universität Berlin</orgName>
      </respStmt>
    </titleStmt>
    <editionStmt>
      <edition>...<date>...</date>...</edition>
    </editionStmt>
    <publicationStmt>
      <publisher>
        <ref type="url" target="http://langsci-press.org/">Language Science Press</ref>
      </publisher>
      <pubPlace>Berlin</pubPlace>
      <address>
        <addrLine>Habelschwerdter Allee 45</addrLine>
        <addrLine>14195 Berlin</addrLine>
        <addrLine>Germany</addrLine>
      </address>
      <date>...</date>
      <idno type="isbn">...</idno>
      <idno type="doi">...</idno>
      <availability>
        <p>This title can be downloaded at <ptr type="url" target="..."/></p>
        <p>Copyright <name>...</name> <date>...</date></p>
        <licence target="http://creativecommons.org/licenses/by/4.0/">Published under the Creative Commons Attribution 4.0 Licence (CC BY 4.0)</licence>
      </availability>
    </publicationStmt>
    <seriesStmt>
      <title>...</title> <!-- series title -->
      <respStmt>         <!-- series editors -->
        <resp>series editor</resp>
        <name>...</name>
      </respStmt>
    </seriesStmt>
    <sourceDesc>
      <p>Born digital.</p>
    </sourceDesc>
  </fileDesc>
  <encodingDesc>
    <!-- default rendition for elements will be set here -->
    <!-- application info  will be set here -->
  </encodingDesc>
</teiHeader>
```

Remarks:

- The source description could include a reference to the original
  LaTeX sources, possibly with date and version information.

- The backcover text is treated as front matter and is not included in
  the header.

## Textual elements
### Front matter

The front matter may contain a title page, a dedication, a preface, a
table of contents, an abstract and information about the author. All
elements except for the title page are optional. In particular, a
table of contents is typically omitted since the chapter and section
structure can be retrieved directly from the document body.

The title page repeats selected fields from the document
metainformation. The abstract and information about the author
correspond to the backcover text of printed LangSci books.

Here is a typical front matter skeleton, including only a title page:

```xml
<front>
  <titlePage>
    <docTitle>
      <titlePart type="main">...</titlePart>
      <titlePart type="sub">...</titlePart>
    </docTitle>
    <byline> <!-- author or editor -->
      <docAuthor>...</docAuthor>
    </byline>
    <docImprint>
      <publisher>Language Science Press</publisher>
      <pubPlace>Berlin</pubPlace>
      <date>...</date>
    </docImprint>
  </titlePage>
</front>
```

If the font matter includes a dedication, it is encoded as follows:

```xml
<div type="dedication">
  <p>...</p>
</div>
```

If the font matter includes a preface, it is encoded as follows:

```xml
<div type="preface">
  <head>Preface</head>
  <p>...</p>
</div>
```

If the front matter includes an abstract or summary, it is encoded as
follows:

```xml
<div type="abstract">
  <head>Abstract</head>
  <p>...</p>
</div>
```

If the front matter includes information about the author (for
monographs) or editor (for collections), it is encoded as follows:

```xml
<div type="authorinfo">
  <head>About the author</head> <!-- or: About the editor -->
  <p>...</p>
</div>
```

### Back matter

The back matter consists of the bibliography, appendices and indices
(all optional).

Bibliographies are wrapped in `<div type="bibliography">` elements and
consist of a `<listBibl>` element around a sequence of `<biblStruct>`
elements. The content of these elements is extracted from an
underlying BibTeX file.

Appendices are represented as regular chapters (`<div type="chapter">`)
that happen to occur in the back matter (i.e. they are contained in a
`<back>` element rather than a `<body>` element). There is no separate
appendix container.

```xml
<back>
  <!-- ... -->
  <div type="chapter" xml:id="..." n="...">
    <head>...</head>    <!-- Appendix A -->
    <p>...</p>
  </div>
  <div type="chapter" xml:id="..." n="...">
    <head>...</head>    <!-- Appendix B -->
    <p>...</p>
  </div>
  <!-- ... -->
</back>
```

There are currently no plans to include explicit indices in the XML
representation since they would be completely redundant. All
information relevant to indexing is stored directly at the indexed
elements via `<index indexName="...">` wrappers. This can be used to
construct indices in consumption formats like HTML or EPUB.

### Chapters, sections and headings

All textual subdivisions are encoded using unnumbered `<div>` elements
with optional `@type` and `@n` attributes, with the heading provided
in the first child in the form of a `<head>` element.

For example, chapters are encoded as follows:

```xml
<div xml:id="..." type="chapter" n="...">
  <head type="main">...</head>
  <head type="sub">...</head>
  <p>...</p>
  ...
</div>
```

### Paragraphs

Paragraphs are encoded as `<p>` elements. In order to support a simple
identifier-based referencing scheme, paragraphs typically come with
`@xml:id` and `@n` attributes.

### Page breaks

Points in the document that correspond to page breaks in its PDF
representation may be indicated using `<pb n="..."/>`
markers. However, this feature is currently not in use.

Remarks:

- There is currently no way to detect page breaks and insert `<pb/>`
  elements automatically. Page numbers in cross-reference targets
  might get replaced by paragraph or section numbers.

### Cross-references

Cross-references are encoded using `<ref>` elements that point to
identifiers in their `@target` attribute.

Example:

```xml
See <ref target="#sec2">section 2</ref>.
```

### Citations and quotations

Citations are encoded using `<ref type="citation">` elements
that point to `<biblStruct>` elements in the bibliography.
Quotations are encoded using `<q>` elements.

Remarks:

- Quoted phrases and citations are currently not formally linked.
  Thus the elements `<cit>` and `<quote>` are not used. Future
  versions of the schema may enable these elements (dependent on the
  availability of source extensions that allow for reliable links
  between quotes and citations).

### Font styles and emphasis

Emphasized words or phrases are encoded using `<emph>`. All other font
changes are encoded using `<hi>` with additional rendition attributes
(`@style` or `@rendition`), e.g. for small caps.

### Footnotes

Footnotes are indicated using the `<note>` element from the TEI module
`core`.

### Lists

Lists are encoded using the `<list>` element from the TEI module
`core`.

### Tables

Tables are encoded using the `<table>` element from the TEI module
`figures`.

Simple example:

```xml
<table rows="2" cols="2">
  <head>...</head>
  <row role="label">
    <cell>...</cell>
    <cell>...</cell>
  </row>
  <row>
    <cell>...</cell>
    <cell>...</cell>
  </row>
</table>
```

### Figures

Figures are encoded using `<figure>` and `<graphic>` from the TEI
module `figures`.

Simple example:

```xml
<figure>
  <graphic url="figure1.png"/>
  <!-- caption (title, heading): -->
  <head>...</head>
  <!-- legend (e.g. a paragraph of commentary): -->
  <p>...</p>
  <!-- description of the figure (alt text) -->
  <figDesc>...</figDesc>
</figure>
```

### Linguistic data structures
#### Example sentences

There are no elements in the TEI guidelines designed to capture
(possibly glossed) linguistic example sentences. However, we can
construct a TEI-conformant representation using standard elements like
`<list>`, `<item>`, `<l>`, `<w>` and `<m>` together with some custom
attribute values. Nested examples can be represented by nesting
`<list>` elements in `<item>` elements.

Simple example:

```xml
<list type="linguistic-example" n="...">
  <item n="...">
    <label>...</label>             <!-- language info, reference -->
    <pc type="judgment">...</pc>   <!-- grammaticality or acceptability judgment -->
    <l type="source">...</l>       <!-- list of <w> elements, possibly embedding <m> -->
    <l type="gloss">...</l>
    <l type="translation">...</l>
  </item>
</list>
```

Remarks:

- More structured alternative representations can be generated as
  well. However, using a TEI-conformant format by default allows
  LangSci documents to be processed by standard TEI tools.

- Some authors in linguistics tend to use example containers for
  generic list items (like tables, formulas, quotes etc.). Since we
  are using generic `<list>` elements to represent examples, this
  poses no problem.

- Acceptability judgments in the form of `<pc type="judgment">`
  elements may also occur within line elements (in particular
  `<l type="source">`) in order to indicate the acceptability of
  variants.

- Extension: examples may have a richer syntactic structure.
  This can be encoded using trees or feature structures as
  described below.

#### Trees

Trees are encoded using the *embedding tree* format from the TEI
module `nets`.

Simple example:

```xml
<eTree>
  <label>DP</label>
  <eTree>
    <label>D</label>
    <eLeaf>
      <label>the</label>
    </eLeaf>
  </eTree>
  <eTree>
    <label>NP</label>
    <eTree>
      <label>N</label>
      <eLeaf>
        <label>vessel</label>
      </eLeaf>
    </eTree>
  </eTree>
  <!-- ... -->
</eTree>
```

#### Feature structures (AVMs)

AVMs are encoded using feature structures, as defined in the TEI
module `iso-fs`.
