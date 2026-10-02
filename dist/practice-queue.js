(function(root) {
  function shuffle(items, random) {
    for (let i = items.length - 1; i > 0; i--) {
      const j = Math.floor(random() * (i + 1));
      [items[i], items[j]] = [items[j], items[i]];
    }
    return items;
  }
  function build(pool, count, options = {}) {
    if (!pool.length || !Number.isInteger(count) || count < 1) return [];
    const { firstKey = null, shuffled = true, recent = [], random = Math.random } = options;
    const result = [];
    const first = pool.find(item => item.key === firstKey);
    if (first) result.push(first);
    let firstBatch = true;
    while (result.length < count) {
      let batch = pool.filter(item => !(firstBatch && first && item.key === first.key));
      if (shuffled) {
        shuffle(batch, random);
        if (firstBatch && recent.length) {
          const rank = new Map(recent.map((id, i) => [id, i]));
          batch.sort((a, b) => (rank.get(a.id) ?? -1) - (rank.get(b.id) ?? -1));
        }
      }
      if (result.length && batch.length > 1 && batch[0].key === result.at(-1).key) {
        [batch[0], batch[1]] = [batch[1], batch[0]];
      }
      result.push(...batch.slice(0, count - result.length));
      firstBatch = false;
    }
    return result;
  }
  if (typeof module !== 'undefined') module.exports = { build };
  else root.PoseTokiQueue = { build };
})(typeof window !== 'undefined' ? window : globalThis);
