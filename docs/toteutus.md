# Toteutus
(kesken)
## Yleisrakenne

Sovellus luo labyrintteja ruudukossa, jossa huoneet on yhdistetty suorin käytävin.

Aluksi generoidaan `n` määrä huoneita (suorakulmioita) ruudukkoon, niin että huoneet eivät ole päällekkäin. Generoitu huone testataan validiksi ja generointia jatketaan kunnes huoneita on `n` kappaletta. Jos generoitu huone ei ole validi maksimiyrityskertojen jälkeen, kasvatetaan ruudukon kokoa.

(huoneiden Edge-olioista tähän)

Yhteydet huoneiden välillä generoidaan laskemalle Delaunayn triangulaatio huoneiden keskipisteille tasossa. Triangulaatio on toteutettu Guibasin ja Stolfin hajota-ja-hallitse algoritmin avulla. Algoritmissa triangulaatio on konveksi, suunnattu tasoverkko. Sen perustietorakenne on quad-edge, joka koostuu neljästä kaaresta: sivu, sama sivu vastakkaiseen suuntaan (`sym`), tasoverkon duaalin sivu (`rot`, käännetty 90 astetta vasemmalle) ja se vastakkaiseen suuntaan (`tor`).

Quad-edgen yksittäinen sivu neljästä on toteutettu Edge-luokkana. Sivuille on määritelty niiden lähtöpiste (`org`) ja seuraava sivu, jolla on sama lähtopiste (`onext`), sekä tietenkin linkit quad-edgen muihin sivuihin. Jotkin attribuutit, kuten sivun lähtöpiste `e.org`, ovat sivun attribuutteja, kun taas esim. sivun päätepiste saadaan `e.dest` on sama kuin päinvastaisen sivun lähtopiste `e.sym.org`.

Sivuille on määritelty monia muita derivoituja attribuutteja. Esimerkiksi `e.lnext` on seuraava sivu, jolla on sama monikulmio vasemmalle puolella.

Sivuja voidaan yhdistää topologisesti toisiinsa `splice` funktiolla, joka linkittää sivujen `onext` attribuutit toisiinsa. Sivujen välillë voidaan luoda uusi yhdistävä sivu `connect` funktiolla, ja sivu voidaan poistaa tasoverkosta `delete_quad_edge` funktiolla. On otettava huomioon, että pisteiden numeerisilla arvoilla ei ole vaikutusta sivujen topologisiin yhteyksiin, joten kaksi sivua, joilla on sama lähtöpiste, eivät ole automaattisesti yhteyksissä toisiinsa jos niitä ei linkitä `splice`:n avulla.

Lisäksi sivuilla on lisäattribuutteja kuten `origin`, jotka liittyvät Delaunayn triangulaation duaaliin, Voronoin diagrammiin. Voronoi-jutut eivät kuulu projektin määrittelyyn.

Itse algoritmi ottaa syötteekseen pistejoukon. Funktio `_delaunay` jakaa joukon rekursiivisesti x-koordinaatin mukaan aina kahtia, kunnes päästään alkutapauksiin, jossa joukossa on 2 tai 3 pistettä.

Kaksi joukkoa liitetään rekursiivisesti yhteen seuraavasti, kunnes saadaan koko pistejoukon triangulaatio:

Käydään molempien joukkojen sivut läpi, kunnes löydetään molempien alin piste ja yhdistetään ne sivulla oikealta vasemmalle (`basel`, siis base left, termit on kaikki otettu arkittelin pseudokoodista).

(loppu kuvaus tähän, voronoi, prim)

Labyrintin huoneiden yhteydet ovat huoneiden keskipisteiden Delaunayn triangulaatio pienin virittävä alipuu. Huoneet ja käytävät on toteutettu (ehkä epäviisaasti) osittain samalla tietorakenteella kuin algoritmissa (quad-edge). Ruudukossa, quad-edge:stä täysin erillään, suoritetaan A\*-haku yhteyksien löytämiseksi, ja luodaan käytäväruudut. Käytäviä luodessa pidetään huolta, että sivuja ei ole kaksi samoissa koordinaateissa ja pidetään kirjaa metadatasta, kuten siitä, onko ruuduilla yhteinen sivu (piirretään eri tavalla).

Lopuksi labyrintti piirretään Matplotlib-kirjaston avulla käymällä läpi ruudukon huoneiden ja käytäväruutujen sivut.


## Lähteet
Delaunayn triangulaation algoritmi ja tietorakenteet perustuvat melkein täysin tähän artikkeliin:

[Leonidas Guibas and Jorge Stolfi. 1985. Primitives for the manipulation of general subdivisions and the computation of Voronoi. ACM Trans. Graph. 4, 2 (April 1985), 74–123.](https://dl.acm.org/doi/10.1145/282918.282923)

Inspiraatiota antoivat nämä blogipostaukset (...)

Ennen kuin päädyin toteutettuun algoritmiin, kävin läpi artikkeleita, ja selailin tätäkin:
Two Algorithms for Constructing Delaunay Triangulation
D. T. Lee and B. J. Schachter

wp: [https://en.wikipedia.org/wiki/Prim%27s_algorithm], [https://en.wikipedia.org/wiki/Circumcircle#Circumcenter_coordinates], [https://en.wikipedia.org/wiki/A*_search_algorithm], [https://en.wikipedia.org/wiki/Best-first_search], jne.
