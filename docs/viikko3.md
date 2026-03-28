# Viikko 2

### Mitä olen tehnyt tällä viikolla?

Vaihdoin incircle-/ccw-testit omaan toteutukseen (`condition_calc.py`). Näköjään determinantti supistuu 3x3- ja 2x2-tapauksiin, joiden laskeminen on riittävän nopeaa myös Pythonilla, jopa vähän nopeampaa kuin edellisen C-kirjaston kutsuminen. Huono puoli on, että nyt determinantti on tarkka vain kokonaisluvuille, mutta tässä ohjelmassa sillä ei ole väliä.

Korjasin bugeja Voronoin diagrammin geometrian laskemisessa.

Refaktoroin Labyrinth-luokkaa. Tähän on mennyt paljon kurssin kannalta aikaa turhaan, kun siinä käytettävä (A\*) on vain pieni osa luokan toiminnasta.

Jaoin yksikkötestit ja triangulaation invarianttitestit omiin tiedostoihin. Tein lisää yksikkötestejä.

Siirryin takaisin matplotlibin käyttöön. Labyrintin parametrit voi nyt syöttää komentoriviltä.

Siirryin Pythonin logging-moduulin käyttöön. 

Aloitin testausraportin teon.

### Miten ohjelma on edistynyt?

Lopputuloksen kannalta ei oikein mitenkään.

### Mitä opin tällä viikolla / tänään?



### Mikä jäi epäselväksi tai tuottanut vaikeuksia?

Labyrinth-luokan toteutus on 

### Mitä teen seuraavaksi?

Teen lisää yksikkötestejä Edge- ja PlanarGraph-luokille. Yritän saada Labyrinth-luokan sellaiseen kuntoon, että sen piirtäminen halutussa asussa on helppoa.

### Aikaa meni

n. 12 tuntia
