# Määrittelydokumentti
Tämä on määrittely kurssilla "Aineopintojen harjoitustyö: Algoritmit ja tekoäly" toteutettavalle harjoitustyölle.

## Aihe ja toteutus

Harjoitustyön aiheena on luolastojen/labyrinttien generointi. Labyrintit (dungeons) ovat monien pöytä- ja tietokoneroolipelien keskeinen tapahtumapaikka. Niiden voidaan katsoa koostuvan huoneista (tai luolista, yms.) ja huoneita yhdistävistä käytävistä. Hyvän labyrintin läpikäyminen vie aikaa, eli reitti kahden mielivaltaisen huoneen välillä ei välttämättä mene seuraavaan euklidisesti lähimmän huoneen kautta. Hyvässä labyrintissa on kuitenkin myös pieniä syklejä, jottei läpikäydessä tarvitse peruutella liikaa.

Harjoitustyön toteutus koostuu muutamasta eri vaiheesta.

Sen ydin on Delaunayn triangulaatio, joka jakaa pistejoukon konveksin verhon (convex hull, tässä tapauksessa ulkopisteistä muodostuva monikulmio) kolmioihin, niin että kaikki muut pisteet ovat kolmion kärjille piirretyn ympyrän ulkopuolella. Ohjelmassa pisteet ovat huoneiden keskipisteitä (tai jokin muu huoneen tietty piste) ja kolmioiden sivut mahdollisia yhteyksiä huoneiden välillä.

Labyrintin muodostus tapahtuu alustavasti näin:

Lasketaan pisteiden ja sivujen muodostaman verkon pienin virittävä puu. Lisätään satunnaisesti joitain kaaria alkuperäisestä verkosta, jotta saadaan syklejä.

Itse huoneet sijoittuvat ruudukkoon. Huoneilla on jokin satunnainnen koko, esim. \[1-5\] x \[1-5\]. Käytävät muodostetaan ruudukossa verkon kaarien mukaisesti jotain reitinhakualgoritmia käyttäen, esim. A\*. Käytävien muodostus tapahtuu iteratiivisesti ja jo luotujen käytäväruutujen paino on pieni tai nolla, jolloin reitinhaku suosii niiden uusiokäyttöä. Huoneiden läpi voi kulkea, mutta huoneruudut eivät muutu käytäväruuduiksi.

Kokonaisuudessaan ohjelma toimii näin:

1. Generoidaan joukko ruudukon pisteitä ja huoneita, niin että huoneet eivät ole ruudukossa päällekkäisiä.
2. Lasketaan pisteiden Delaunayn triangulaatio. <- ydinalgoritmi
3. Lasketaan triangulaation pienin virittävä puu.
4. Muodostetaan ruudukossa käytäviä huoneiden välillä reitinhakualgotimilla.

Lopullinen tulos on ruudukko, jossa jotkin ruudut muodostavat suorakulmiomaisia huoneita ja huoneiden välillä on käytäväruutuja.

## Delaunayn triangulaation algoritmi

Aion laskea Delaunayn triangulaation toteuttamalla Guibasin ja Stolfin hajota ja hallitse -algoritmin:

[Leonidas Guibas and Jorge Stolfi. 1985. Primitives for the manipulation of general subdivisions and the computation of Voronoi. ACM Trans. Graph. 4, 2 (April 1985), 74–123.](http://mesh.brown.edu/DGP/pdfs/Guibas-tog85.pdf)

Artikkelissa tietorakenteena käytetään

## Muuta

Opinto-ohjelma
- Tietojenkäsittelytieteen kandidaatti

Vertaisarvioinnin kielet
- Pythonin lisäksi voin vertaisarvioida muilla samankaltaisilla kielillä kirjoitettua koodia (JS, C, Java, jne.)
- Haskellista olen suorittanut joskus Functional Programming I/II-kurssit, joten ehkä myös sillä
