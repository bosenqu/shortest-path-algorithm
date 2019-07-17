'''
Bosen Qu
July 15, 2019
Dijkstra’s Shortest Path Algorithm: finds the shortest
path to a given start point in a graph
'''
# An example of graph
graph = [("A", [("B", 6), ("D", 1)]),
         ("B", [("A", 6), ("C", 5), ("D", 2), ("E", 2)]),
         ("C", [("B", 5), ("E", 5)]),
         ("D", [("A", 1), ("B", 2), ("E", 1)]),
         ("E", [("B", 2), ("C", 5), ("D", 1)])]

# A Graph is a (listof (tuple Str (listof (tuple Str, Int)))

# A ForwardTable is a (dictof Str (list Int, (listof Str)))

# get_unvisited(g) returns a list of node that is unvisited
#   from graph g
# get_unvisited: Graph -> listof(Str)
def get_unvisited(g):
    if g == []:
        return g
    return [g[0][0]] + get_unvisited(g[1:])

# set_table(g) returns an empty forwaring table that are used
#   later to describe the graph
# set_table: Graph Str ForwardTable -> ForwardTable     
def set_table(g, start, val):
    if g == []:
        return val
    if g[0][0] == start:
        val[g[0][0]] = [0, [start]]
    else:
        val[g[0][0]] = [None, None]
    return set_table(g[1:], start, val)   

# update_neighbors(cur_node, neighbors, table, path) updates
#   the shortest path of cur_node's neighbors
# update_neighbors: Str (listof (tuple Str Int)) ForwardTable (listof Str) ->
#                   ForwardTable
def update_neighbors(cur_node, neighbors, table, path):
    if neighbors == []:
        return table
    distance_to_last_node = table[cur_node][0]
    distance_curr = neighbors[0][1]
    if table[neighbors[0][0]][0] == None or \
       distance_to_last_node + distance_curr < table[neighbors[0][0]][0]:
        table[neighbors[0][0]][0] = distance_to_last_node + distance_curr
        table[neighbors[0][0]][1] = path + [neighbors[0][0]]
    return update_neighbors(cur_node, neighbors[1:], table, path)

# shortest_path_neighbors(g, neighbors, unvisited, visited, table, path)
#   returns the shortest path table from all neighbors
# shortest_path_neighbors: Graph (listof (tuple Str Int)) (listof Str) (listof Str)
#                          ForwardTable listof(Str) -> ForwardTable
def shortest_path_neighbors(g, neighbors, unvisited, visited, table, path):
    if neighbors == []:
        return table
    if neighbors[0][0] in visited:
        return shortest_path_neighbors(g, neighbors[1:], unvisited, visited, table, path)
    update_table = shortest_path_node(g, neighbors[0][0], unvisited, visited, table, path)
    return shortest_path_neighbors(g, neighbors[1:], unvisited, visited, update_table, path)   

# shortest_path_node(g, neighbors, unvisited, visited, table, path)
#   returns the forwarding table from start
# shortest_path_node: Graph Str (listof Str) (listof Str) ForwardTable 
#                     (listof Str) -> ForwardTable
def shortest_path_node(g, start, unvisited, visited, table, path):
    if unvisited == []:
        return table
    neighbors = list(filter(lambda x: x[0] == start, graph))[0][1]
    neighbors.sort(key = lambda x: x[1])
    unvisited.remove(start)
    visited.append(start)
    path += [start]
    return shortest_path_neighbors(g, neighbors, unvisited, visited,
                                   update_neighbors(start, neighbors, table, path), path)

# shortest_path(g, start) returns the forwarding table computed from start
# shortest_path: Graph Str -> ForwardTable
def shortest_path(g, start):
    return shortest_path_node(g, start, get_unvisited(graph), [], set_table(graph, start, {}), [])