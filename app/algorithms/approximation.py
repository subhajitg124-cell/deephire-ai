def approximate_vertex_cover(edges):
    cover = set()

    while edges:
        u, v = edges.pop()
        cover.add(u)
        cover.add(v)

        edges = [e for e in edges if u not in e and v not in e]

    return cover