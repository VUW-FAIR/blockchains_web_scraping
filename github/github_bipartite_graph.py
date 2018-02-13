import csv
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt

names = []
repos = []
#the set is to ensure we have a collection of repo names without duplicates
repos_set = set()

with open("github_contributors_output.csv", 'r', encoding="utf-8") as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if(len(row) > 1): #if not empty line
            #simplifying string so it doesn't include all the directory information
            repos_array = (row[1].replace("[", "").replace("]","").replace("'", "").replace("\"", "").replace("\\", "").replace(".GitHubScraping", "")\
                .replace("all_contributorscontributors_page", "").replace(".json", "")).split(",")

            repos_array = [r[:-2] for r in repos_array] #remove contributor page number (at end)

            if(len(repos_array) > 12): #if they've contributed to more than one repo
                print(repos_array)
                names.append(row[0])
                repos.append(repos_array)
                for r in repos_array:
                    repos_set.add(r)


print(repos_set)
print(len(names))

B = nx.Graph()

color_map = []

#add half the nodes
B.add_nodes_from(names, bipartite=0)

#colour half the nodes yellow
count = 0
for node in B.nodes:
    color_map.append('yellow')
    count +=1

#add the rest of the nodes
B.add_nodes_from(repos_set, bipartite=1)

#colour the rest of the nodes red
count2 = 0
for node in B.nodes:
    if(count2 >= count):
        color_map.append('red')
    count2 += 1

#add edges between nodes
for i in range(0, len(names)):
    for r in repos[i]:
        B.add_edge(names[i], r, line=0.1)

nx.draw(B, with_labels=True,  node_color = color_map, font_size = 7, node_size = 1000)
plt.show()



# Example to make a simple Bipartite graph as below:
# B = nx.Graph()
# B.add_nodes_from(['A', 'B', 'C', 'D', 'E'], bipartite=0)
# B.add_nodes_from([1, 2, 3, 4], bipartite=1)
# B.add_edges_from([('A', 1), ('B', 1), ('C', 1), ('C', 3), ('D', 2), ('E', 3), ('E', 4)])
#
# nx.draw(B, with_labels=True)
# plt.show()
# #plt.savefig("graph.png")