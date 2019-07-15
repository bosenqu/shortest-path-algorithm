graph = [("A", [("B", 6), ("D", 1)]),
         ("B", [("A", 6), ("C", 5), ("D", 2), ("E", 2)]),
         ("C", [("B", 5), ("E", 5)]),
         ("D", [("A", 1), ("B", 2), ("E", 1)]),
         ("E", [("B", 2), ("C", 5), ("D", 1)])]

def get_unvisited(g):
    if g == []:
        return g
    return [g[0][0]] + get_unvisited(g[1:])

def set_table(g, start, val):
    if g == []:
        return val
    if g[0][0] == start:
        val[g[0][0]] = [0, [start]]
    else:
        val[g[0][0]] = [None, None]
    return set_table(g[1:], start, val)   

def update_neighbers(cur_node, neighbers, table, path):
    if neighbers == []:
        return table
    distance_to_last_node = table[cur_node][0]
    distance_curr = neighbers[0][1]
    if table[neighbers[0][0]][0] == None or \
       distance_to_last_node + distance_curr < table[neighbers[0][0]][0]:
        table[neighbers[0][0]][0] = distance_to_last_node + distance_curr
        table[neighbers[0][0]][1] = path + [neighbers[0][0]]
    return update_neighbers(cur_node, neighbers[1:], table, path)

def shortest_path_neighbers(g, neighbers, unvisited, visited, table, path):
    if neighbers == []:
        return table
    if neighbers[0][0] in visited:
        return shortest_path_neighbers(g, neighbers[1:], unvisited, visited, table, path)
    update_table = shortest_path_node(g, neighbers[0][0], unvisited, visited, table, path)
    return shortest_path_neighbers(g, neighbers[1:], unvisited, visited, update_table, path)   

def shortest_path_node(g, start, unvisited, visited, table, path):
    if unvisited == []:
        return table
    neighbers = list(filter(lambda x: x[0] == start, graph))[0][1]
    neighbers.sort(key = lambda x: x[1])
    unvisited.remove(start)
    visited.append(start)
    return shortest_path_neighbers(g, neighbers, unvisited, visited,
                                   update_neighbers(start, neighbers, table, path + [start]),
                                   path + [start])

def shortest_path(g, start):
    return shortest_path_node(g, start, get_unvisited(graph), [], set_table(graph, start, {}), [])