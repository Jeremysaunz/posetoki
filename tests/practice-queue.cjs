const assert = require('node:assert/strict');
const { build } = require('../dist/practice-queue.js');
const pool = Array.from({ length: 120 }, (_, key) => ({ key, id: `PT${String(key + 1).padStart(3, '0')}` }));
const keys = items => items.map(item => item.key);
let checks = 0;
for (let n = 0; n < 100; n++) {
  const queue = build(pool, 120);
  assert.equal(new Set(keys(queue)).size, 120);
  const recent = queue.slice(0, 100).map(item => item.id);
  const next = build(pool, 20, { recent });
  assert(next.every(item => !recent.includes(item.id)));
  const pinned = build(pool, 120, { recent, firstKey: 50 });
  assert.equal(pinned[0].key, 50);
  assert.equal(new Set(keys(pinned)).size, 120);
  checks += 4;
}
assert.deepEqual(keys(build(pool, 5, { shuffled: false })), [0, 1, 2, 3, 4]);
assert.deepEqual(keys(build(pool, 5, { shuffled: false, firstKey: 50 })), [50, 0, 1, 2, 3]);
const one = [{ key: 'local-photo', id: undefined }];
assert.equal(build(one, 20, { firstKey: 'local-photo' }).length, 20);
assert.equal(build([], 5).length, 0);
const small = pool.slice(0, 12);
const repeated = build(small, 20);
assert.equal(new Set(keys(repeated.slice(0, 12))).size, 12);
assert.notEqual(repeated[11].key, repeated[12].key);
const allViewed = pool.map(item => item.id);
assert.deepEqual(keys(build(pool, 5, { recent: allViewed })), [0, 1, 2, 3, 4]);
checks += 7;
console.log(`${checks} checks passed: unique cycles, recent avoidance, pinned starts, sequential order and single-photo repeats.`);
