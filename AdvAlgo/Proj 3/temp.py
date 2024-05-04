import random

def weighted_randomized_vertex_cover(edges, weights):
    vertex_cover = set()
    weighted_edges = random.choices(edges, weights=weights, k=len(edges))

    print("Before vertex_cover: ", vertex_cover)
    print("Before weighted_edges: ", weighted_edges)
    print("Before edges: ", edges)

    for edge in weighted_edges:
        vertex_cover.update(edge)

        edges = [e for e in edges if e[0] not in edge and e[1] not in edge]
    
        print("After vertex_cover", vertex_cover)
        print("After edges:", edges)
        print("/n")

    return vertex_cover

edges = [(1, 2), (2, 3), (3, 4), (4, 5), (1, 5)]
weights = [5, 1, 4, 3, 2]  # higher weights mean higher priority to cover
print("Vertex Cover found by Weighted Randomized:", weighted_randomized_vertex_cover(edges, weights))
