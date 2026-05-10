# Toteutus

## Yleisrakenne

Sovellus luo labyrintteja ruudukossa, jossa huoneet on yhdistetty suorin käytävin.

Sovelluksessa on kaksi päämoduulia:
1. `planar_graph`, jonka `PlanarGraph`-luokka hoitaa pistejoukon triangulaation ja muuta verkkoon liittyvää laskentaa.
2. `labyrinth`, joka hoitaa huoneiden generoimisen ja käytävien luomisen

Lisäksi on moduulit `condition` ja `edge`, joissa on Delaunay-algoritmissa käytettäviä geometrisia testejä ja algoritmissa käytettävä tietorakenne. 

Aluksi generoidaan `n` määrä huoneita (suorakulmioita) ruudukkoon, niin että huoneet eivät ole päällekkäin. Generoitu huone testataan validiksi ja generointia jatketaan kunnes huoneita on `n` kappaletta. Jos generoitu huone ei ole validi maksimiyrityskertojen jälkeen, kasvatetaan ruudukon kokoa.

Yhteydet huoneiden välillä generoidaan laskemalle ensin Delaunayn triangulaatio huoneiden keskipisteille tasossa. Triangulaatio on toteutettu Guibasin ja Stolfin hajota-ja-hallitse algoritmin avulla.

Tämän jälkeen lasketaan triangulaation pienin virittävä alipuu ja tähän lisätään satunnaisesti sivuja triangulaatiosta, jotta labyrintissa olisi myös syklejä.

Ruudukossa suoritetaan A\*-haku yhteyksien löytämiseksi ja luodaan käytäväruudut. Käytäviä luodessa pidetään huolta, että sivuja ei ole kaksi samoissa koordinaateissa ja pidetään kirjaa metadatasta, kuten siitä, onko ruuduilla yhteinen sivu (piirretään eri tavalla).

Lopuksi labyrintti piirretään Matplotlib-kirjaston avulla käymällä läpi ruudukon huoneiden ja käytäväruutujen sivut.

## Tarkemmin Guibasin ja Stolfin algoritmista

Algoritmissa triangulaatio on konveksi, suunnattu tasoverkko. Sen perustietorakenne on quad-edge, joka koostuu neljästä kaaresta: sivu, sama sivu vastakkaiseen suuntaan (`sym`), tasoverkon duaalin sivu (`rot`, käännetty 90 astetta vastapäivään) ja se vastakkaiseen suuntaan (`tor`).

Quad-edgen yksittäinen sivu neljästä on toteutettu Edge-luokkana. Sivuille on määritelty niiden lähtöpiste (`org`) ja seuraava sivu, jolla on sama lähtopiste (`onext`), sekä tietenkin linkit quad-edgen muihin sivuihin. Jotkin attribuutit, kuten sivun lähtöpiste `e.org`, ovat sivun attribuutteja, kun taas esim. sivun päätepiste `e.dest` on sama kuin päinvastaisen sivun lähtopiste `e.sym.org`.

Sivuille on määritelty monia muita derivoituja attribuutteja. Esimerkiksi `e.lnext` on seuraava sivu, jolla on sama monikulmio vasemmalle puolella.

Sivuja voidaan yhdistää topologisesti toisiinsa `splice` funktiolla, joka linkittää sivujen `onext` attribuutit toisiinsa. Sivujen välille voidaan luoda uusi yhdistävä sivu `connect` funktiolla, ja sivu voidaan poistaa tasoverkosta `delete_quad_edge` funktiolla. On otettava huomioon, että pisteiden numeerisilla arvoilla ei ole vaikutusta sivujen topologisiin yhteyksiin, joten kaksi sivua, joilla on sama lähtöpiste, eivät ole automaattisesti yhteyksissä toisiinsa jos niitä ei linkitä `splice`:n avulla.

Lisäksi sivuilla on lisäattribuutteja kuten `radius`, jotka liittyvät Delaunayn triangulaation duaaliin, Voronoin diagrammiin.

Itse algoritmi ottaa syötteekseen pistejoukon. Funktio `_delaunay` jakaa joukon rekursiivisesti x-koordinaatin mukaan aina kahtia, kunnes päästään alkutapauksiin, jossa joukossa on 2 tai 3 pistettä.

Kaksi joukkoa liitetään rekursiivisesti yhteen seuraavasti, kunnes saadaan koko pistejoukon triangulaatio:

Käydään molempien joukkojen sivut läpi, kunnes löydetään molempien joukkojen yhteinen alin tangentti ja yhdistetään ne sivulla oikealta vasemmalle (`basel`, siis base left, termit on otettu artikkelista).

Tämän jälkeen molemmilta puolilta poistetaan sivuja jotka eivät läpäise `incircle`-testiä ja liikutaan ylöspäin, jonka jälkeen lisätään uusi `basel` puoliskojen välille. Silmukka toistuu kunnes `basel` on ylin tangentti.

Lopulta algoritmi on yhdistänyt kaikki puolikkaat toisiinsa, ja lopputuloksena saadaan koko pistejoukon triangulaatio. Funktio palauttaa kaksi sivua molemmilta puolilta kuviota. (Lisäksi totetuksessa kaikista sivuista pidetään kirjaa algoritmin aikana).

### Voronoi ja pienin virittävä alipuu

Kun triangulaatio on valmis, saadaan samalla Voronoin diagrammi sen duaalina. Diagrammin sivuilla ei kuitenkaan ole tässä vaiheessa koordinaatteja, vaan ne saadaan käymällä kaikki kolmiot läpi ja laskemalla kolmion ympäri piirretyn ympyrän keskipiste.

Lisäksi triangulaation pienin virittävä alipuu lasketaan Primin algoritmilla.

## Aikavaativuus

Syötteillä `n = 1000, 10000, 100000, 1000000` ja terminaalin tulosteesta voidaan empiirisesti todeta seuraavat aikavaativuudet:
- Delaunayn triangulaatio: O(n log n)
- Voronoin diagrammi (ympyröiden keskipisteet ja säteet): O(n)
- Primin algoritmi: O(n log n) 

En testannut muita, kuten huoneiden luontia tai A\*.

## Puutteita

Etenkin `labyrinth`-moduulin koodi ei ole kovin selkeää ja esim. osa funktioista muuttaa globaalia tilaa ja osa palauttaa tuloksen. Lisäksi kyseistä moduulia ei ole testattu melkein ollenkaan.

## Lähteet

Delaunayn triangulaation algoritmi ja tietorakenteet perustuvat melkein täysin tähän artikkeliin:

[Leonidas Guibas and Jorge Stolfi. 1985. Primitives for the manipulation of general subdivisions and the computation of Voronoi. ACM Trans. Graph. 4, 2 (April 1985), 74–123.](https://dl.acm.org/doi/10.1145/282918.282923)

Inspiraatiota antoivat nämä blogipostaukset:
- [Procedurally Generated Dungeons](https://vazgriz.com/119/procedurally-generated-dungeons/)
- [Visualizing Delaunay Triangulation](https://ianthehenry.com/posts/delaunay/) (Toteuttaa artikkelin toisen, iteratiivisen algoritmin)

Eniten käytetyt Wikipedia-artikkelit:
- [Prim's algorithm](https://en.wikipedia.org/wiki/Prim%27s_algorithm)
- [Circumcircle](https://en.wikipedia.org/wiki/Circumcircle#Circumcenter_coordinates) (kaava ulkoympyröiden keskipisteiden laskemiseen)
- [A\* search algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm)

## Laajojen kielimallien käyttö

Käytin Google Geminin chat-mallia tiedonhakuun `incircle` ja `ccw/orient2d`-testien nopeasta laskemisesta ja docstringien ulkoasusta.