# CLLD datasets

## About Cross-Linguistic Linked Data (CLLD)

Human languages differ in many ways: in their vocabularies, in the
inventory of sounds they use to distinguish words, in the relative
arrangement of verbs and arguments, etc. Linguists systematically
explore the features that make languages different (and that they
share) in an attempt to understand the nature of the diversity of
human languages and also to find out whether there are universal
properties that every language on this planet has.

Several years ago, the joint effort of many linguists gave rise to the
[World Atlas of Language Structures](http://wals.info/) (WALS), an
online database of structural (phonological, grammatical, lexical)
properties of languages. For example, it allows users to
[compare languages by the number of consonants they have](http://wals.info/feature/1A)
and visualize this distribution on a world map.
There are almost [200 features](http://wals.info/feature) by which
you can compare [more than 2500 languages](http://wals.info/languoid).
For a more detailed explanation of WALS,
have a look at its [introductory chapter](http://wals.info/chapter/s1),
freely available online.

But the web interface is not the only way to access the WALS data.
The core functionality of comparing languages by certain features
has been extracted into a flexible framework for managing
*Cross-Linguistic Linked Data*: [CLLD](http://clld.org/).
WALS and other projects use this framework to store and visualize
typological linguistic data. In addition to the web interface,
many CLLD-based projects offer direct access to the data in several
formats (CSV, RDF, SQLite) under a CC-BY license.

An important prerequisite for CLLD and typological descriptions in
general is a way to uniquely identify languages (as well as language
families and dialects). For this purpose CLLD uses
[Glottolog](http://glottolog.org/), a comprehensive catalogue of the
world's languages that is itself available in several formats (RDF,
CSV) under CC BY-SA. The language descriptions provided by Glottolog
include geographic coordinates. This enables applications to visualize
linguistic feature distributions on a world map. If you want to learn
more about how Glottolog can be used in applications, have a look at this
[IPython Notebook](http://nbviewer.ipython.org/gist/xflr6/9050337/glottolog.ipynb)
by Sebastian Bank that interactively explores the Glottolog RDF data.

In the following, we will highlight some of the CLLD-based projects
and datasets. For a more complete list, have a look at the official
page about [CLLD datasets](http://clld.org/datasets.html).

## WALS

The [World Atlas of Language Structures](http://wals.info/) is the
project that initiated the development of all the tools discussed
here. The [source code](https://github.com/clld/wals3) of the web
application is available as well its [data](http://wals.info/download)
in CSV format (2 MB). The CSV file contains 2679 rows, one for each
language, and many columns that describe the language (name,
glottocode, language family, geographic coordinates) and list the
feature values for that language (e.g. size of the consonant
inventory, whether it is a tone language, etc.).

License: CC BY 4.0 (but CSV README says: CC BY-NC-ND 2.0 DE)

## WOLD

The [World Loanword Database](http://wold.clld.org/) is a database
that provides information about which words languages borrowed from
each other. To this end, the database holds information about words
and their meanings from 41 languages. You can browse meanings
(*concepts*) by category (*semantic field*): There are 24
[semantic fields](http://wold.clld.org/meaning), for example: kinship,
animals, body, motion, time. If you view a single concept, e.g.
[elephant](http://wold.clld.org/meaning/3-77), you get a list of words
from various languages with this meaning. Since geographic information
is associated with every language, the words can be visualized on a
world map (this is done using [leaflet](http://leafletjs.com/) on the
web frontend). It is also easy to get the data directly in
[GeoJSON format](http://wold.clld.org/meaning/3-77.geojson).

The data is [available for download](http://wold.clld.org/download)
in RDF format (87 MB, ZIP: 6 MB).

License: CC BY 3.0 DE

## APiCS

The [Atlas of Pidgin and Creole Language Structures](http://apics-online.info/)
is a WALS-like database of linguistic features but specifically for
Pidgin and Creole languages. The complete dataset is available as a
SQLite database (25 MB, ZIP: 5.6 MB). One interesting aspect of APiCS
is that it includes many glossed linguistic
[example sentences](http://apics-online.info/sentences) from various
languages. It is easy to access them via SQL. Here are a few sentences
in `src|imt|translation` format, just to get started:

```
sqlite> select markup_text, markup_gloss, description from sentence limit 10;

Isredeh mi kau bringi wan mannpikin.|yesterday 1SG cow deliver a male.young|Yesterday my cow delivered a bull calf.
Da mastra tikki mi wyfi na nitti lange trange hay.|DET.SG master take 1SG wife in night with strong eye|The master took my wife during the night with force.
A mama fon a pikin.|DET mother beat DET child|The mother beat the child.
A boi lobi a umapikin.|DET boy love DET girl|The boy loves the girl.
A téi dí páu páá.|3SG take DEF.SG stick quick|He took the stick quickly.
Wojo u mi á sa kai ku di faja.|eye for 1SG NEG M fall with DEF.SG fire|My eye can't stand the light.
Di mujɛɛ naki di womi.|DEF.SG woman hit DEF.SG man|The woman hit the man.
Den pikinnenge e lobi switi sii.|DET.PL child IPFV love/like sweet seeds|The children like sweets.
kooknot bring ail|coconut bring.forth oil|Coconuts produce oil. OR: The coconut produces oil.
Shi buy a nju cyar.|3SG buy DET new car|She bought a new car.
```

License: CC BY 3.0 (SQLite README says: CC BY-SA 3.0)

## ValPaL

The [Valency Patterns Leipzig](http://valpal.info/) is a database that
collects valency information for currently 36 languages. Like APiCS,
this dataset includes many linguistic example sentences, e.g. 170 for
[German](http://valpal.info/languages/german/examples) and 362 for
[Yucatec Maya](http://valpal.info/languages/yucatec-maya/examples).

License: CC BY 3.0

## eWAVE

The [Electronic World Atlas of Varieties of English](http://ewave-atlas.org/)
is a WALS-like database of linguistic features but specifically for
varieties of English. In addition to the distribution of feature
values across languages (or rather languoids) it includes many example
sentences, like *We might could do that* from Chicano English (Texas),
featuring a [double modal](http://ewave-atlas.org/parameters/121).
The value matrix [data](http://ewave-atlas.org/download) is available
for download in CSV format.

License: CC BY 3.0
