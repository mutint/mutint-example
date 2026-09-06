"""The table both the page and the panel show: per sample, how many mutations it carries and
how many of those another sample carries too.

Two things worth copying rather than the table itself. **The calls come from
`calls_for_samples`**, which subtracts the experiment's designated ancestor -- an ancestral
mutation is in every sample, so left in, every sample would share everything. And **the rows
are tuples, not models**: `values_list` over two columns, which is the shape every derivation
in the suite moved to once fetching whole `MutationCall` rows was measured.
"""

import collections

from mutint_sample.mutation_matrix import sample_page_url
from mutint_sample.util import calls_for_samples, get_reseq_ordered_dict


def sample_sharing(experiment):
    """One row per sample, in the order the site lists samples.

    `mutations` is the number of distinct mutations the sample carries, `shared` how many of
    those at least one other sample in the experiment carries too, and `unique` the rest.
    """
    reseq_dict = get_reseq_ordered_dict(experiment.id)
    if not reseq_dict:
        return []
    pairs = (calls_for_samples(list(reseq_dict), experiment.id)
             .filter(present=True)
             .values_list("sample_id", "mutation_id")
             .iterator(chunk_size=2000))
    by_sample = collections.defaultdict(set)
    carriers = collections.Counter()
    for sample_id, mutation_id in pairs:
        if mutation_id not in by_sample[sample_id]:
            by_sample[sample_id].add(mutation_id)
            carriers[mutation_id] += 1

    rows = []
    for sample_id, sample in reseq_dict.items():
        mutations = by_sample.get(sample_id, set())
        shared = sum(1 for mutation_id in mutations if carriers[mutation_id] > 1)
        rows.append({
            "sample_id": sample_id,
            "label": sample.label,
            "url": sample_page_url(sample, experiment),
            "mutations": len(mutations),
            "shared": shared,
            "unique": len(mutations) - shared,
        })
    return rows
