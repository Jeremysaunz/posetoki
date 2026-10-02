const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '../dist');
const poses = JSON.parse(fs.readFileSync(path.join(root, 'pose-library.json')));
assert.equal(poses.length, 120);
assert.equal(new Set(poses.map(pose => pose.id)).size, 120);
assert.equal(new Set(poses.map(pose => pose.image)).size, 120);
const hashes = new Set();
for (const pose of poses) {
  assert(fs.existsSync(path.join(root, pose.image)));
  assert(fs.existsSync(path.join(root, pose.thumb)));
  const hash = crypto.createHash('sha256').update(fs.readFileSync(path.join(root, pose.image))).digest('hex');
  assert(!hashes.has(hash), `Duplicated file: ${pose.id}`);
  hashes.add(hash);
  for (const lang of ['ko', 'ja', 'en', 'zh-TW']) {
    assert(pose.name[lang]?.length > 1, `${pose.id}: missing ${lang} name`);
    assert(pose.focus[lang]?.length > 1, `${pose.id}: missing ${lang} focus`);
  }
  assert(pose.width > 0 && pose.height > 0);
}
for (const category of ['ST', 'WK', 'DY', 'TR', 'CH', 'FL', 'LY', 'FP', 'DA', 'EM']) {
  assert.equal(poses.filter(pose => pose.category === category).length, 12);
}
assert.equal(poses.filter(pose => pose.legacy !== null).length, 21);
console.log('120 distinct image files, 10 categories of 12, four-language metadata, thumbnails and legacy links verified.');
