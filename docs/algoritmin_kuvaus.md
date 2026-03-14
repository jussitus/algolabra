!!KESKEN!!

Kaikkea quad-edgen komponentteja ei tarvita 2D Delaunayn triangulaatiossa, esim. Voronoin diagrammissa ei tarvitse liikkua, joten `e Flip`, `e Rot`, yms. ei tarvitse toteuttaa. Ehkä järkevämpää toteuttaa jokainen suunnattu sivu omana olionaan.

Splice

MakeEdge

RemoveEdge

Kuvaus itse algoritmista joka jakaa pisteet kahteen (vas ja oik) joukkon kunnes päästään perustapauksiin n=2 tai n=3, D trianguloi ne, ja sitteen lomittaa puolikkaat takaisin kokonaiseksi D triangulaatioksi
