import igraph as ig
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define your source and destination nodes
source = "A"
destination = "D"

df = pd.DataFrame({
    'source': ['A', 'A', 'A', 'A', 'C'],
    'target': ['B', 'C', 'D', 'E', 'D'],
    'weight': [ 1 ,  2 ,  8 ,  4 ,  5 ]
})

labels = list(set(df['source']) | set(df['target']))
labels.sort()

g = ig.Graph(directed=True)
g.add_vertices(len(labels))
g.vs["label"] = labels

# Generate the graph
g = g.TupleList(df.itertuples(index=False),
                        directed=True,
                        edge_attrs='weight',
                        vertex_name_attr='label')  # Remove 'weights=True'

# # to add manualy
# g.es['weight'] = [] # for new g and not for exist
# routs = [(2, "A", "B"), (1, "A", "C"), (5, "B", "D"), (4, "C", "D"), (7, "C", "E"), (3, "D", "F"), (2, "E", "F")]
# for rout in routs:
#     for rout1 in rout[1:]:
#         if rout1 not in g.vs["label"]:
#             g.add_vertices(1)
#             g.vs["label"] = g.vs["label"] + [rout1]
#     g.add_edges([tuple([g.vs.find(label=name).index for name in rout[1:]])])
#     g.es['weight'] = g.es['weight'][:-1] + [rout[0]]

# Choose a layout algorithm (e.g., Kamada-Kawai)
g.layout("kamada_kawai")

fig, ax = plt.subplots(1, 1, figsize=(8, 4))
# Plot the graph with edge weights displayed
width = g.es["weight"]
width_norm = np.array(width) / max(width)
ig.plot(g, target= ax, edge_label= g.es["weight"], edge_width= width_norm*2)
ax.set_title(f"igraph auto from panda")

# Find all simple paths between source and destination
all_paths = g.get_all_simple_paths(g.vs.find(label=source).index, g.vs.find(label=destination).index)
resoults = []
print("All possible routes from source to destination sort by weights:")
for path in all_paths:
    total_weight = 0
    for i in range(len(path)-1):
        total_weight += g.es[g.get_eid(path[i], path[i+1])]['weight']
    names = [g.vs[e]["label"] for e in path]
    resoults.append({
                    "path": names,
                    "total_weight": total_weight,
                    "num_routs": len(path) - 1
                    })
sort_resoults_by_weight = sorted(resoults, key=lambda d: d['total_weight'])
for resoult in sort_resoults_by_weight:
    print(resoult)

plt.show()
