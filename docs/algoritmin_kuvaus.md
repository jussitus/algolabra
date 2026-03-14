!!Karsi tämä kaikki pois ja käsittele vain yksittäistä sivuoliota!!

Delaunayn triangulaation duaali on Voronoin diagrammi. Voronoin diagrammi määrittää alueet (monikulmoita) joihin kuuluvat pisteet ovat lähempänä tiettyä Delaunayn kärkeä kuin muita kärkiä. Jokaisen suunnatun Delaunayn triangulaation sivun vasemmalla ja oikealla puolella on Voronoin diagrammiin kuuluva monikulmio.

Jokaisella sivulla (edge) on orientaatio, joko vastapäivään tai myötäpäivään (vastapäivään jos kuvio käännetään nurinpäin). Jokaiselle sivulle on määritelty:
- `e Org`, sivun alkupiste
- `e Dest`, sivun päätepiste
- `e Left`, sivun vasemalla puolella oleva tahko(?) (face) / Voronoin solu (Voronoi cell)
- `e Right`, sivun oikealla puolella oleva solu
- `e Flip`, sivu samaan suuntaan käänteisellä orientaatiolla
- `e Sym`, sivu samalla orientaatiolla käänteiseen suuntaan
- `e Onext`, seuraava sivu vastapäivään samalla lähtöpisteellä
- `e Lnext`, seuraava sivu kun liikutaan solun `e Left` ympäri vastapäivään
- `e Dual`, joka 

!!KESKEN!!

Artikkelin tietorakenne on quad-edge (nelisivu?). Jokaisessa quad-edgessa on kahdeksan komponenttia:
- `e`, suunnattu sivu lähtopisteestä `e Org` päätepisteeseen `e Dest`
- `e Sym`, suunnattu sivu pisteestä `e Dest` pisteeseen `e Org`
- `e Rot`,

!!KESKEN!!

Kaikkea ylläolevaa ei tarvita 2D Delaunayn triangulaatiossa, esim. Voronoin diagrammissa ei tarvitse liikkua, joten `e Flip`, `e Rot`, yms. ei tarvitse toteuttaa. Ehkä järkevämpää toteuttaa jokainen suunnattu sivu omana olionaan.

Splice

MakeEdge

RemoveEdge

Kuvaus itse algoritmista joka jakaa pisteet kahteen (vas ja oik) joukkon kunnes päästään perustapauksiin n=2 tai n=3, D trianguloi ne, ja sitteen lomittaa puolikkaat takaisin kokonaiseksi D triangulaatioksi
