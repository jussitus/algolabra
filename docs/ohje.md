# Käyttöohje

Alkutoimenpiteet:

`poetry install`

Ohjelman voi ajaa seuraavasti:

`poetry run python src/lab.py -n 100`

Säädettäviä parametreja:

```
-n, --num-rooms: huoneiden lukumäärä
-s, --seed: huoneiden satunnaisgeneroinnin siemenluku 
-Md, --max-dim: huoneen sivun enimmäispituus
-md, --min-dim: huoneen sivun vähimmäispituus
-g, --gap: vähimmäisetäisyys huoneiden välillä
-sh, --shape: labyrintin muoto, vaihtoehdot ovat "square" ja "circle"
```

