from delaunay import delaunay
import random
import networkx as nx
import matplotlib.pyplot as plt
s = set()
random.seed(42)
for i in range(0,25):
    s.add((random.randint(0,25),random.randint(0,25)))
s = sorted(s)
#print(s)


l,r = delaunay(s)

es = []
for i in range(100):
    es.append(l)
    l = l.lnext


G = nx.Graph()

for e in es:
    a = e.org
    b = e.dest
    G.add_edge(a,b)

for e in G.edges():
    print(e)
pos = {node: node for node in G.nodes()}
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=5)
plt.show()
