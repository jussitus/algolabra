# Testaus
(kesken)
Testauksessa käytetään Pytestiä. 

Testit voi ajaa komennolla `poetry run pytest`.

## Yksikkötestaus

Yksikkötestien testikattavuus:
```
Name                  Stmts   Miss Branch BrPart  Cover
-------------------------------------------------------
src/condition.py         12      0      0      0   100%
src/edge.py             102      8      6      2    89%
src/planar_graph.py     206     30     64      8    86%
-------------------------------------------------------
TOTAL                   320     38     70     10    87%
```

Yksikkötestit testaavat Edge- ja PlanarGraph-luokkien konstruktoreita ja metodeja hyvin pienillä syötteillä.

`condition`-moduulista testataan, että funktiot toimivat oikein yksittäisille syötteille ja rajatapauksille (lähinnä jos pisteet ovat janalla). `ccw` ja `incircle` testien lisäksi testataan, että näistä johdetut funktiot toimivat kuten pitäisi.

`edge`-moduulista testataan, että konstruktori toimii ja derivoidut operaattorit (`rnext`, jne.) toimivat oikein. Testataan myös, että sivujen yhteydet `splice` ym. funktioiden jäljiltä ovat oikein.

`planar_graph`-moodulin konstruktoria ja metodeja testataan pienillä syötteillä ja rajatapauksilla. Triangulaatio, Voronoin diagrammi, ja Primin pienin virittävä alipuu testataan yksittäin pienillä syötteillä.

## Invarianttitestaus

Yksikkötestien lisäksi testataan Delaunay-triangulaatioon liittyviä geometrisia invariantteja, joista tärkein on, että jokaisen triangulaation kolmion määrittämän ympyrän kehän sisäpuolella ei ole muita pisteitä. Lisäksi kaikkien sivujen määrä voidaan laskea uloimmaisten sivujen lukumäärästä. Pienillä syötteillä testit toteutetaan `sympy`-kirjaston avulla, suuremilla syötteillä ohjelman oman `incircle`-testin avulla.
