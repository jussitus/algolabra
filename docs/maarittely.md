# Määrittelydokumentti
Tämä on määrittely kurssilla "Aineopintojen harjoitustyö: Algoritmit ja tekoäly" toteutettavalle harjoitustyölle.

## Aihe ja toteutus

Harjoitustyön aiheena on luolastojen/labyrinttien generointi. Labyrintit (dungeons) ovat monien pöytä- ja tietokoneroolipelien keskeinen tapahtumapaikka. Niiden voidaan katsoa koostuvan huoneista (tai luolista, yms.) ja huoneita yhdistävistä käytävistä. Hyvän labyrintin läpikäyminen vie aikaa, eli reitti kahden mielivaltaisen huoneen välillä voi kiertää euklidisesti pidempää reittiä. Hyvässä labyrintissa on kuitenkin myös pieniä syklejä, jottei läpikäydessä tarvitse peruutella liikaa.

Ohjelma toteutaan Pythonilla.

Harjoitustyön toteutus koostuu muutamasta eri vaiheesta.

Sen ydin on Delaunayn triangulaatio, joka jakaa pistejoukon konveksin verhon (convex hull, tässä tapauksessa ulkopisteistä muodostuva monikulmio) kolmioihin, niin että kaikki muut pisteet ovat kolmion kärjille piirretyn ympyrän ulkopuolella. Ohjelmassa pisteet ovat huoneiden keskipisteitä (tai jokin muu huoneen tietty piste) ja kolmioiden sivut mahdollisia yhteyksiä huoneiden välillä.

Labyrintin muodostus tapahtuu alustavasti näin:

Lasketaan pisteiden ja sivujen muodostaman verkon pienin virittävä puu Primin algoritmilla. Lisätään satunnaisesti joitain kaaria alkuperäisestä verkosta, jotta saadaan syklejä.

Itse huoneet sijoittuvat ruudukkoon. Huoneilla on jokin satunnainnen koko, esim. \[1-5\] x \[1-5\]. Käytävät muodostetaan ruudukossa verkon kaarien mukaisesti jotain polunetsintäalgoritmia käyttäen, esim. A\*. Käytävien muodostus tapahtuu iteratiivisesti ja jo luotujen käytäväruutujen paino on pieni tai nolla, jolloin reitinhaku suosii niiden uusiokäyttöä. Huoneiden läpi voi kulkea, mutta huoneruudut eivät muutu käytäväruuduiksi.

Kokonaisuudessaan ohjelma toimii näin:

1. Syöte on pisteiden määrä `n`. Generoidaan satunnaisesti joukko ruudukon pisteitä ja huoneita, niin että huoneet eivät ole ruudukossa päällekkäin.
2. Lasketaan pisteiden Delaunayn triangulaatio. <- ydinalgoritmi
3. Askeleesta 2. saadaan kaksi triangulaation sivua. Käydään triangulaatio läpi ja muodostetaan verkon vieruslista.
4. Lasketaan verkon pienin virittävä puu. Lisätään satunnaisia kaaria koko verkosta.
5. Muodostetaan ruudukossa käytäviä huoneiden välillä polunetsintäalgoritmilla.
6. Tulostetaan labyrintti jotain Python grafiikkakirjastoa käyttäen.

Lopullinen tulos on ruudukko, jossa jotkin ruudut muodostavat suorakulmiomaisia huoneita ja huoneiden välillä on käytäväruutuja.

## Algoritmi

Aion laskea Delaunayn triangulaation toteuttamalla Guibasin ja Stolfin hajota ja hallitse -algoritmin:

[Leonidas Guibas and Jorge Stolfi. 1985. Primitives for the manipulation of general subdivisions and the computation of Voronoi. ACM Trans. Graph. 4, 2 (April 1985), 74–123.](http://mesh.brown.edu/DGP/pdfs/Guibas-tog85.pdf)

(Tarkemmin tietorakenteista ja algoritmista myöhemmin [tässä dokumentissa](algoritmin_kuvaus.md)).

Artikkelissa käytetään tietorakennetta quad-edge (nelisivu?). Tässä toteutuksessa ei kuitenkaan tarvita sen kaikkia komponentteja ja funktioita, koska algoritmissa ei poiketa duaalin (Voronoin diagrammin) puolelle.

Algoritmi jakaa pistejoukon rekursiivisesti aina kahteen kunnes päästään perustapauksiin, joissa pisteitä on 2 tai 3. Kun nämä on kolmioitu, aletaan puolikkaita yhdistämään, jolloin joudutaan poistamaan sivuja vasemmasta ja oikeasta puolikkaasta ja lisäämään sivuja vasemman ja oikean puolikaan välille.

Päätökset tehdään `InCircle` (onko piste kolmen pisteen muodostaman ympyrän sisällä tai kehällä) ja CCW (muodostaako kolme pistettä suunnatun kolmion vastapäivään) -testien avulla. Algoritmi antaa kaksi sivua, jotka ovat uloimpien pisteiden vasemmanpuoleisimmasta pisteestä vastapäivään lähtevä sivu ja oikeanpuoleisimmasta pisteestä myötäpäivään lähtevä sivu.

Lisäksi aion käyttää [tätä Ian Henryn blogipostausta](https://ianthehenry.com/posts/delaunay/), joka käsittelee Guibasin ja Stolfin algoritmeissa käytettävää tietorakennetta (yksinkertaisempaa versiota) ja toteuttaa Delaunayn triangulaation artikkelissa esitetyllä toisella iteratiivisella algoritmilla.

Ohjelman muista vaiheista otin neuvoa [tästä blogipostauksesta](https://vazgriz.com/119/procedurally-generated-dungeons/).

Aikavaativuus

V = pisteet, E = sivut

- Pisteiden ja huoneiden sijoittelu `O(|V|)`
- Guibasin ja Stolfin algoritmin aikavaativuus on `O(|V| log|V|)`
- - oletettavasti puolitus `O(log |V|)` kertaa ja lomitus `O(|V|)`
- Vieruslistan muodostus on `O(|E|)`(?), Primin algoritmi `O(|E| log|V|)`
- A\* on O(|E| log|V|)


## Muuta

Opinto-ohjelma
- Tietojenkäsittelytieteen kandidaatti

Vertaisarvioinnin kielet
- Pythonin lisäksi voin vertaisarvioida muilla samankaltaisilla kielillä kirjoitettua koodia (JS, C, Java, jne.)
- Haskellista olen suorittanut joskus Functional Programming I/II-kurssit, joten ehkä myös sillä

Dokumentaation kieli
- Dokumentaatio on suomeksi, koodi englanniksi
