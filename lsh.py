import numpy as np

from sklearn.metrics.pairwise import cosine_similarity

def lsh(space, n_sets=10, n_hyp=5):
    space = np.array(space)
    tables = []
    planes = []
    for s in range(n_sets):
        hash_table = {}
        plane_norms = np.random.rand(n_hyp, space.shape[1]) - 0.5
        for i, d in enumerate(space):
            _hash = ''.join((d @ plane_norms.T > 0).astype(int).astype(str))
            if _hash not in hash_table.keys(): hash_table[_hash] = []
            hash_table[_hash].append(i)

        tables.append(hash_table)
        planes.append(plane_norms)

    return tables, planes

def predict(query, space, tables, planes, k=3):
    space = np.array(space)
    neighbours = []
    for hash_table, plane_norms in zip(tables, planes):
        _hash = ''.join((space[query] @ plane_norms.T > 0).astype(int).astype(str))
        neighbours.extend([e for e in hash_table[_hash] if e not in neighbours])

    neighbours = np.array(neighbours)
    sims = cosine_similarity([space[query]], space[neighbours])[0]
    scores = { k: v for k,v in zip(neighbours, sims) }
    del scores[query]
    scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True)[:k])
    
    return scores





