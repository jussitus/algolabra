# Käyttöohje

Alkutoimenpiteet:

`poetry install`

Ohjelman voi ajaa seuraavasti:

`poetry run python src/main_labyrinth.py -n 100`

Säädettäviä parametreja:

```
  -n, --num-rooms: huoneiden lukumäärä
  -s, --seed: huoneiden satunnaisgeneroinnin siemenluku 
  -Md, --max-dim: huoneen sivun enimmäispituus
  -md, --min-dim: huoneen sivun vähimmäispituus
  -g, --gap: vähimmäisetäisyys huoneiden välillä
  -sh, --shape: labyrintin muoto, vaihtoehdot ovat "square" ja "circle"
  -c, --cycle-score: kuinka paljon pienimpään virittävään alipuuhun lisätään triangulaation kaaria (luo syklejä), 0-1.0
```

## Delaunayn ja Voronoin visualisaatio

Triangulaatiota voi visualisoida ajamalla:

`poetry run python src/main_visualize.py -n 25 -d`

Parametreja:

```
  -n N                 pisteiden lukumäärä
  -s, --seed SEED      siemenluku
  -d, --delaunay       piirtää Delaunayn triangulaation
  -v, --voronoi        piirtää Voronoin diagrammin (ilman äärettomyyteen jatkuvia sivuja)
  -c, --circumcircles  piirtää ulkoympyrät
```