# Testaus
(kesken)
Testauksessa käytetään Pytestiä. 

Testit voi ajaa komennolla `poetry run pytest`.

## Yksikkötestaus

Yksikkötestien testikattavuus:
<img src="testaus.png">

Yksikkötestit testaavat Edge- ja PlanarGraph-luokkien konstruktoreita ja metodeja hyvin pienillä syötteillä.

## Invarianttitestaus

Yksikkötestien lisäksi testataan Delaunay-triangulaatioon liittyviä geometrisia invariantteja, joista tärkein on, että jokaisen triangulaation kolmion määrittämän ympyrän kehän sisäpuolella ei ole muita pisteitä. Lisäksi kaikkien sivujen määrä voidaan laskea uloimmaisten sivujen lukumäärästä. Pienillä syötteillä testit toteutetaan `sympy`-kirjaston avulla, suuremilla syötteillä ohjelman oman `ccw`-testin avulla.
