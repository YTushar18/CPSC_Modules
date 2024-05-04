import random
def simple_randomized_vertex_cover(edges):
    vertex_cover = set()
    remaining_edges = edges.copy()

    while remaining_edges:
        edge = random.choice(remaining_edges)
        vertex_cover.update(edge)
        # Remove all edges adjacent to these vertices
        remaining_edges = [e for e in remaining_edges if e[0] not in edge and e[1] not in edge]

    return vertex_cover

# Example graph represented as a list of edges
edges = [(1, 2), (2, 3), (3, 4), (4, 5), (1, 5)]
print("Vertex Cover found by Simple Randomization:", simple_randomized_vertex_cover(edges))
