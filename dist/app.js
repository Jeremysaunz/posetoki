const $ = id => document.getElementById(id);
const t = key => window.PoseTokiI18n?.t(key) ?? key;
const lang = () => window.PoseTokiI18n?.lang ?? 'ko';
const locale = () => ({ ko: 'ko-KR', ja: 'ja-JP', en: 'en-US', 'zh-TW': 'zh-TW' }[lang()] ?? 'ko-KR');

const library = window.PoseTokiPoses;
const poses = library.map(pose => pose.name.ko);
const categories = {
  ST: '서기·체중 이동', WK: '걷기·달리기', DY: '점프·스포츠·춤',
  TR: '뻗기·굽히기·비틀기', CH: '의자·좌석', FL: '바닥·무릎·쪼그림',
  LY: '눕기·기대기', FP: '밀기·당기기·들기', DA: '일상·도구 사용', EM: '감정·의사 표현'
};
const levelKeys = { beginner: '초급', intermediate: '중급', advanced: '고급' };
const groups = { all: library.map((_, i) => i) };
Object.keys(categories).forEach(code => {
  groups[code] = groups.all.filter(i => library[i].category === code);
});
const legacyGroups = { standing: ['ST', 'TR'], motion: ['WK', 'DY', 'FP'], balance: ['ST', 'FP'], seated: ['CH', 'FL'] };

function posePool() {
  return (groups[$('poseCategory').value] ?? groups.all).filter(i =>
    $('poseLevel').value === 'all' || library[i].level === $('poseLevel').value);
}

function recentPoses() {
  try {
    const stored = JSON.parse(localStorage.getItem('posetoki-recent-poses') ?? '[]');
    return Array.isArray(stored) ? stored.filter(id => library.some(pose => pose.id === id)).slice(-120) : [];
  } catch { return []; }
}

function rememberPose() {
  if (mode !== 'preset') return;
  const id = library[queue[index].key].id;
  try { localStorage.setItem('posetoki-recent-poses', JSON.stringify([...recentPoses().filter(value => value !== id), id])); } catch {}
}

function poseDescription(i) {
  const pose = library[i];
  return `${t('관찰 목표')}: ${t(pose.focus.ko)} · ${t(levelKeys[pose.level])} · ${t('권장')} ${pose.seconds}${t('초')}`;
}
const goalKeys = { gesture: '동작선', balance: '무게중심', overlap: '겹침과 비례' };
let mode = 'preset';
let seconds = 60;
let preview = 0;
let ownPreview = 0;
let startPose = null;
let uploads = [];
let queue = [];
let index = 0;
let remaining = 3;
let preparing = true;
let paused = false;
let active = false;
let spent = 0;
let last = 0;
let interval = null;
let flip = false;
let zoomed = false;
let seen = new Set();
let audio = null;

function setPose(el, poseIndex) {
  const pose = library[poseIndex];
  el.style.backgroundImage = `url("${pose.image}")`;
  el.style.backgroundSize = 'contain';
  el.style.backgroundPosition = 'center';
  el.style.backgroundRepeat = 'no-repeat';
  el.style.aspectRatio = `${pose.width} / ${pose.height}`;
  el.setAttribute('role', 'img');
  el.setAttribute('aria-label', `${pose.id} · ${t(poses[poseIndex])}`);
}

function selectionText() {
  if (mode !== 'preset') return '';
  const pool = posePool();
  if (!pool.length) return t('이 조건의 포즈가 없어요. 유형이나 난이도를 바꿔주세요.');
  const repeated = Number($('count').value) > pool.length;
  const prefix = startPose === null
    ? t($('shuffle').checked
        ? '무작위 순서에서는 첫 포즈가 미리보기와 다를 수 있어요.'
        : '선택한 유형의 첫 포즈부터 순서대로 시작합니다.')
    : `${t('시작 포즈')}: ${library[startPose].id} · ${t(poses[startPose])}`;
  const note = $('shuffle').checked ? ` ${t('최근 본 포즈보다 덜 본 포즈를 먼저 보여줍니다.')}` : '';
  return `${prefix} · ${pool.length}${t('개 포즈')}${note}${repeated ? ` ${t('선택한 유형의 포즈를 반복합니다.')}` : ''}`;
}

function paintPreview() {
  const own = mode === 'own';
  $('previewPanel').classList.toggle('is-empty', own && !uploads.length);
  $('paperNote').hidden = own;
  $('previewSource').hidden = own;
  $('emptyPreview').hidden = !own || uploads.length > 0;
  if (own) {
    const photo = uploads[ownPreview];
    $('heroPhoto').style.backgroundImage = photo ? `url("${photo.url}")` : 'none';
    $('heroPhoto').style.aspectRatio = '1 / 2';
    $('heroPhoto').setAttribute('role', 'img');
    $('heroPhoto').setAttribute('aria-label', photo?.name ?? t('사진을 먼저 선택해주세요.'));
    $('imageLabel').textContent = photo
      ? `${t('내 사진')} ${ownPreview + 1} / ${uploads.length} · ${photo.name}`
      : t('사진을 먼저 선택해주세요.');
  } else {
    const available = posePool().length > 0;
    $('emptyPreview').hidden = available;
    $('emptyPreview').textContent = t('이 조건의 포즈가 없어요. 유형이나 난이도를 바꿔주세요.');
    if (available) {
      setPose($('heroPhoto'), preview);
      $('imageLabel').textContent = `${library[preview].id} / ${poses.length} · ${t(poses[preview])}`;
    } else {
      $('heroPhoto').style.backgroundImage = 'none';
      $('heroPhoto').removeAttribute('role');
      $('heroPhoto').removeAttribute('aria-label');
      $('imageLabel').textContent = t('포즈 없음');
    }
  }
  if (own) $('emptyPreview').textContent = t('내 사진을 선택하면 여기에서 미리 볼 수 있어요.');
  $('poseFocus').textContent = own || !posePool().length ? '' : poseDescription(preview);
  $('prevPreview').disabled = own ? uploads.length < 2 : posePool().length < 2;
  $('nextPreview').disabled = $('prevPreview').disabled;
  $('usePreview').disabled = !posePool().length;
  $('start').disabled = !own && !posePool().length;
  $('usePreview').textContent = t(startPose === preview ? '시작 포즈 선택 해제' : '지금 보는 포즈로 시작');
  $('poseSelection').textContent = selectionText();
}

function changePreview(step) {
  if (mode === 'own') {
    if (!uploads.length) return;
    ownPreview = (ownPreview + step + uploads.length) % uploads.length;
  } else {
    const ids = posePool();
    if (!ids.length) return;
    const at = Math.max(0, ids.indexOf(preview));
    preview = ids[(at + step + ids.length) % ids.length];
  }
  paintPreview();
}

function selectMode(next) {
  mode = next;
  $('presetTab').classList.toggle('selected', next === 'preset');
  $('ownTab').classList.toggle('selected', next === 'own');
  $('presetContent').hidden = next !== 'preset';
  $('ownContent').hidden = next !== 'own';
  $('error').textContent = '';
  paintPreview();
  updateEstimate();
}

function setTime(value, custom = false) {
  seconds = Number(value);
  $('customField').hidden = !custom;
  $('customBtn').classList.toggle('selected', custom);
  document.querySelectorAll('[data-time]').forEach(button => {
    button.classList.toggle('selected', !custom && Number(button.dataset.time) === seconds);
  });
  if (custom) $('customSeconds').value = String(seconds);
  updateEstimate();
}

function updateEstimate() {
  const count = Number($('count').value);
  const minutes = Math.round(count * seconds / 6) / 10;
  $('estimate').textContent = {
    ko: `${count}장 · 약 ${minutes}분`,
    ja: `${count}ポーズ・約${minutes}分`,
    en: `${count} poses · about ${minutes} min`,
    'zh-TW': `${count} 個姿勢 · 約 ${minutes} 分鐘`
  }[lang()];
  $('poseSelection').textContent = selectionText();
}

function renderUploadList() {
  $('uploadList').replaceChildren();
  uploads.forEach((photo, photoIndex) => {
    const row = document.createElement('div');
    row.className = 'upload-item';
    const img = document.createElement('img');
    img.src = photo.url;
    img.alt = '';
    const name = document.createElement('span');
    name.textContent = photo.name;
    const remove = document.createElement('button');
    remove.type = 'button';
    remove.textContent = t('삭제');
    remove.setAttribute('aria-label', `${photo.name} · ${t('삭제')}`);
    remove.onclick = () => {
      URL.revokeObjectURL(photo.url);
      uploads.splice(photoIndex, 1);
      ownPreview = Math.min(ownPreview, Math.max(0, uploads.length - 1));
      updateFileStatus();
      renderUploadList();
      paintPreview();
    };
    row.append(img, name, remove);
    $('uploadList').append(row);
  });
}

function updateFileStatus() {
  $('fileStatus').textContent = uploads.length
    ? {
        ko: `${uploads.length}장 준비 완료 · 사진은 이 기기에서만 사용됩니다.`,
        ja: `${uploads.length}枚準備完了・写真はこの端末内だけで使用します。`,
        en: `${uploads.length} photos ready · Photos stay on this device.`,
        'zh-TW': `已準備 ${uploads.length} 張 · 照片只會留在此裝置。`
      }[lang()]
    : t('사진은 서버로 전송되지 않습니다.');
}

async function addFiles(files) {
  $('error').textContent = '';
  let added = 0;
  for (const file of files) {
    if (!file.type.startsWith('image/')) continue;
    const url = URL.createObjectURL(file);
    const readable = await new Promise(resolve => {
      const image = new Image();
      image.onload = () => resolve(true);
      image.onerror = () => resolve(false);
      image.src = url;
    });
    if (readable) {
      uploads.push({ url, name: file.name });
      added++;
    } else {
      URL.revokeObjectURL(url);
    }
  }
  if (!added) $('error').textContent = t('읽을 수 있는 이미지 파일을 선택해주세요.');
  updateFileStatus();
  renderUploadList();
  paintPreview();
  $('files').value = '';
}

function shuffle(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

function buildQueue(pool, count, firstKey) {
  return window.PoseTokiQueue.build(pool, count, {
    firstKey, shuffled: $('shuffle').checked, recent: mode === 'preset' ? recentPoses() : []
  });
}

function tone() {
  if (!$('sound').checked) return;
  try {
    audio ??= new (window.AudioContext || window.webkitAudioContext)();
    audio.resume();
    const oscillator = audio.createOscillator();
    const gain = audio.createGain();
    oscillator.connect(gain);
    gain.connect(audio.destination);
    oscillator.frequency.value = 660;
    gain.gain.setValueAtTime(0.035, audio.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, audio.currentTime + 0.18);
    oscillator.start();
    oscillator.stop(audio.currentTime + 0.2);
  } catch {}
}

function start() {
  if (!Number.isFinite(seconds) || seconds < 5 || seconds > 3600) {
    $('error').textContent = t('5초에서 3600초 사이의 시간을 입력해주세요.');
    return false;
  }
  if (mode === 'own' && !uploads.length) {
    $('error').textContent = t('먼저 연습할 사진을 선택해주세요.');
    return false;
  }
  const pool = mode === 'own'
    ? uploads.map(photo => ({ ...photo, key: photo.url }))
    : posePool().map(key => ({ key, id: library[key].id, name: poses[key] }));
  if (!pool.length) {
    $('error').textContent = t('이 조건의 포즈가 없어요. 유형이나 난이도를 바꿔주세요.');
    return false;
  }
  const firstKey = mode === 'own' ? uploads[ownPreview]?.url ?? null : startPose;
  queue = buildQueue(pool, Number($('count').value), firstKey);
  index = 0;
  spent = 0;
  seen = new Set();
  preparing = true;
  remaining = 3;
  paused = false;
  active = true;
  flip = false;
  zoomed = false;
  $('pause').textContent = t('일시정지');
  $('error').textContent = '';
  $('session').showModal();
  render();
  last = performance.now();
  clearInterval(interval);
  interval = setInterval(tick, 100);
  try {
    audio ??= new (window.AudioContext || window.webkitAudioContext)();
    audio.resume();
  } catch {}
  return true;
}

function tick() {
  const now = performance.now();
  const delta = (now - last) / 1000;
  last = now;
  if (!active || paused) return;
  remaining -= delta;
  if (!preparing) spent += delta;
  if (remaining <= 0) {
    if (preparing) {
      preparing = false;
      remaining = seconds;
      seen.add(index);
      rememberPose();
      tone();
    } else {
      move(1);
      return;
    }
  }
  renderTimer();
}

function renderTimer() {
  const value = Math.max(0, Math.ceil(remaining));
  $('timer').textContent = `${String(Math.floor(value / 60)).padStart(2, '0')}:${String(value % 60).padStart(2, '0')}`;
  $('phase').textContent = paused ? t('잠깐 쉬어가는 중') : preparing ? t('연필을 준비하세요') : t('몸의 흐름을 관찰해보세요');
  $('timerBar').style.width = `${Math.max(0, remaining / (preparing ? 3 : seconds) * 100)}%`;
}

function transform() {
  const value = `scale(${flip ? -1 : 1}, 1) scale(${zoomed ? 1.4 : 1})`;
  $('sessionPhoto').style.transform = value;
  $('localPhoto').style.transform = value;
}

function render() {
  const photo = queue[index];
  $('progress').textContent = lang() === 'ko'
    ? `${index + 1} / ${queue.length} 포즈`
    : `${index + 1} / ${queue.length} ${t('poses')}`;
  $('sessionPhoto').hidden = mode === 'own';
  $('localPhoto').hidden = mode !== 'own';
  if (mode === 'own') {
    $('localPhoto').src = photo.url;
    $('localPhoto').alt = photo.name;
  } else {
    setPose($('sessionPhoto'), photo.key);
  }
  $('sessionSource').textContent = t(mode === 'own'
    ? '내 사진 · 서버 전송 없이 이 기기에서만'
    : 'AI 생성 예시 · 120가지 포즈 · 관절과 비례를 확인하세요');
  $('sessionFocus').textContent = mode === 'own' ? '' : poseDescription(photo.key);
  $('sessionSound').textContent = t($('sound').checked ? '♪ 전환음 켜짐' : '♪ 전환음 꺼짐');
  $('zoom').textContent = t(zoomed ? '− 축소' : '＋ 확대');
  transform();
  renderTimer();
}

function move(direction) {
  if (!active) return;
  if (index + direction >= queue.length) {
    finishSession();
    return;
  }
  index = Math.max(0, index + direction);
  preparing = false;
  remaining = seconds;
  seen.add(index);
  rememberPose();
  last = performance.now();
  tone();
  render();
}

function pause() {
  if (!active) return;
  paused = !paused;
  last = performance.now();
  $('pause').textContent = t(paused ? '계속 그리기' : '일시정지');
  renderTimer();
}

async function fullscreen() {
  try {
    if (document.fullscreenElement) await document.exitFullscreen();
    else await $('session').requestFullscreen();
  } catch {}
}

function history() {
  try {
    const entries = JSON.parse(localStorage.getItem('posetoki-history') || '[]');
    return Array.isArray(entries) ? entries : [];
  } catch {
    return [];
  }
}

function renderNextGoal() {
  const goal = history().find(entry => goalKeys[entry.goal]);
  $('nextGoal').textContent = goal ? `${t('지난번에 고른 다음 목표')}: ${t(goalKeys[goal.goal])}` : '';
}

function showInfo(title, content) {
  $('infoContent').replaceChildren();
  const heading = document.createElement('h2');
  heading.textContent = title;
  $('infoContent').append(heading, content);
  $('info').showModal();
}

function sessionSummary(count, total, saved) {
  const minutes = Math.floor(total / 60);
  const secondsPart = total % 60;
  const logged = total > 0 && saved;
  return {
    ko: `${count}개 포즈를 보고 ${minutes}분 ${secondsPart}초 연습했어요. ${logged ? '연습 기록은 이 기기에 남겼어요.' : '이번 기록은 저장되지 않았어요.'} 아래 사진을 눌러 복습하세요.`,
    ja: `${count}ポーズを見て、${minutes}分${secondsPart}秒練習しました。${logged ? '記録はこの端末に保存しました。' : '今回は記録を保存していません。'} 下の写真を選んで復習できます。`,
    en: `You viewed ${count} poses and practiced for ${minutes} min ${secondsPart} sec. ${logged ? 'This session was saved on this device.' : 'This session was not saved.'} Select a photo below to review it.`,
    'zh-TW': `你看了 ${count} 個姿勢，練習 ${minutes} 分 ${secondsPart} 秒。${logged ? '紀錄已儲存在此裝置。' : '這次沒有儲存紀錄。'} 點選下方照片即可複習。`
  }[lang()];
}

function finishSession() {
  if (!active) return;
  active = false;
  clearInterval(interval);
  if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
  $('session').close();
  const total = Math.round(spent);
  let recordId = null;
  let saved = false;
  if (total > 0) {
    try {
      recordId = `${Date.now()}-${Math.random().toString(36).slice(2)}`;
      const entries = history();
      entries.unshift({ id: recordId, date: new Date().toISOString(), seconds: total, count: seen.size, goal: '' });
      localStorage.setItem('posetoki-history', JSON.stringify(entries.slice(0, 100)));
      saved = true;
    } catch {}
  }
  const content = document.createElement('div');
  const copy = document.createElement('p');
  copy.className = 'info-copy';
  copy.textContent = sessionSummary(seen.size, total, saved);
  content.append(copy);
  const grid = document.createElement('div');
  grid.className = 'review-grid';
  const keys = new Set();
  [...seen].sort((a, b) => a - b).forEach(seenIndex => {
    const photo = queue[seenIndex];
    if (keys.has(photo.key)) return;
    keys.add(photo.key);
    const button = document.createElement('button');
    button.className = 'review-item';
    button.setAttribute('aria-label', `${t(photo.name)} · ${t('복습')}`);
    const image = mode === 'own' ? document.createElement('img') : document.createElement('div');
    if (mode === 'own') {
      image.src = photo.url;
      image.alt = photo.name;
    } else {
      image.className = 'pose-photo';
      setPose(image, photo.key);
    }
    const label = document.createElement('small');
    label.textContent = t(photo.name);
    button.append(image, label);
    button.onclick = () => {
      const detail = image.cloneNode();
      detail.style.height = '60vh';
      detail.style.width = '100%';
      const back = document.createElement('button');
      back.className = 'quiet';
      back.textContent = t('복습 목록으로');
      back.onclick = () => $('infoContent').replaceChildren(titleNode(t('오늘도, 한 걸음 그렸어요.')), content);
      $('infoContent').replaceChildren(detail, back);
    };
    grid.append(button);
  });
  content.append(grid);
  if (recordId) {
    const goalBox = document.createElement('div');
    goalBox.className = 'review-goal';
    const label = document.createElement('label');
    label.htmlFor = 'reviewGoal';
    label.textContent = t('다음 연습에서 볼 한 가지');
    const select = document.createElement('select');
    select.id = 'reviewGoal';
    [['', '선택하지 않음'], ...Object.entries(goalKeys)].forEach(([value, key]) => {
      const option = document.createElement('option');
      option.value = value;
      option.textContent = t(key);
      select.append(option);
    });
    const note = document.createElement('p');
    note.textContent = t('선택한 목표만 이 브라우저의 기록에 남습니다.');
    select.onchange = () => {
      try {
        const entries = history();
        const record = entries.find(item => item.id === recordId);
        if (record) {
          record.goal = select.value;
          localStorage.setItem('posetoki-history', JSON.stringify(entries));
          renderNextGoal();
        }
      } catch {
        note.textContent = t('이 브라우저에서는 기록을 저장할 수 없어요.');
      }
    };
    goalBox.append(label, select, note);
    content.append(goalBox);
  }
  showInfo(t('오늘도, 한 걸음 그렸어요.'), content);
}

function titleNode(value) {
  const heading = document.createElement('h2');
  heading.textContent = value;
  return heading;
}

function openHistory() {
  const content = document.createElement('div');
  const records = history();
  const summary = document.createElement('p');
  summary.className = 'info-copy';
  const totalPoses = records.reduce((sum, item) => sum + Number(item.count || 0), 0);
  const totalMinutes = Math.round(records.reduce((sum, item) => sum + Number(item.seconds || 0), 0) / 60);
  summary.textContent = records.length
    ? {
        ko: `누적 ${totalPoses}개 포즈 · 약 ${totalMinutes}분. 기록은 이 브라우저에만 저장됩니다.`,
        ja: `累計${totalPoses}ポーズ・約${totalMinutes}分。記録はこのブラウザにだけ保存されます。`,
        en: `Total: ${totalPoses} poses · about ${totalMinutes} min. Your log stays in this browser.`,
        'zh-TW': `累計 ${totalPoses} 個姿勢 · 約 ${totalMinutes} 分鐘。紀錄只保存在此瀏覽器。`
      }[lang()]
    : t('아직 연습 기록이 없어요. 첫 번째 선을 시작해볼까요? 기록은 이 브라우저에만 저장됩니다.');
  content.append(summary);
  records.slice(0, 15).forEach(record => {
    const row = document.createElement('div');
    row.className = 'history';
    const date = new Date(record.date).toLocaleString(locale());
    const minutes = Math.floor(record.seconds / 60);
    const secondsPart = record.seconds % 60;
    row.textContent = {
      ko: `${date} · ${record.count}개 포즈 · ${minutes}분 ${secondsPart}초`,
      ja: `${date} · ${record.count}ポーズ · ${minutes}分${secondsPart}秒`,
      en: `${date} · ${record.count} poses · ${minutes} min ${secondsPart} sec`,
      'zh-TW': `${date} · ${record.count} 個姿勢 · ${minutes} 分 ${secondsPart} 秒`
    }[lang()];
    if (goalKeys[record.goal]) {
      const goal = document.createElement('div');
      goal.className = 'record-goal';
      goal.textContent = `${t('다음 목표')}: ${t(goalKeys[record.goal])}`;
      row.append(goal);
    }
    content.append(row);
  });
  showInfo(t('나의 작은 연습 기록'), content);
}

function applyDeepLink() {
  const params = new URLSearchParams(location.search);
  const legacy = Number(params.get('pose'));
  const poseId = params.get('poseId');
  const poseIndex = poseId ? library.findIndex(pose => pose.id === poseId) : library.findIndex(pose => pose.legacy === legacy);
  const duration = Number(params.get('seconds'));
  const count = Number(params.get('count'));
  const category = params.get('category');
  if (groups[category]) $('poseCategory').value = category;
  if (poseIndex >= 0) {
    preview = poseIndex;
    startPose = preview;
    if (legacyGroups[category]) $('poseCategory').value = library[preview].category;
    if (!posePool().includes(preview)) $('poseCategory').value = 'all';
  }
  if (poseIndex < 0) preview = posePool()[0] ?? 0;
  if (Number.isInteger(duration) && duration >= 5 && duration <= 3600) {
    setTime(duration, ![30, 60, 180, 300].includes(duration));
  }
  if ([5, 10, 15, 20].includes(count)) $('count').value = String(count);
  updateEstimate();
  paintPreview();
}

function populateCategories(select) {
  select.replaceChildren();
  [['all', '전체 포즈'], ...Object.entries(categories)].forEach(([value, key]) => {
    const option = document.createElement('option');
    option.value = value;
    option.textContent = t(key);
    select.append(option);
  });
}

function renderLibrary() {
  if (!$('library').open) return;
  const category = $('libraryCategory').value;
  const level = $('libraryLevel').value;
  const query = $('librarySearch').value.trim().toLocaleLowerCase();
  const ids = groups.all.filter(i => {
    const pose = library[i];
    return (category === 'all' || pose.category === category)
      && (level === 'all' || pose.level === level)
      && (!query || `${pose.id} ${Object.values(pose.name).join(' ')}`.toLocaleLowerCase().includes(query));
  });
  $('librarySearch').placeholder = t('이름 또는 PT 번호로 찾기');
  $('libraryCount').textContent = `${ids.length} / ${library.length} ${t('개 포즈')}`;
  $('libraryGrid').replaceChildren();
  if (!ids.length) {
    const empty = document.createElement('p');
    empty.textContent = t('검색 결과가 없어요. 검색어나 필터를 바꿔주세요.');
    $('libraryGrid').append(empty);
  }
  ids.forEach(i => {
    const pose = library[i];
    const card = document.createElement('button');
    card.type = 'button';
    card.className = 'library-card';
    card.dataset.poseId = pose.id;
    card.setAttribute('aria-label', `${pose.id} · ${t(pose.name.ko)} · ${t('이 포즈로 시작')}`);
    const img = document.createElement('img');
    img.src = pose.thumb;
    img.alt = t(pose.name.ko);
    img.width = pose.width;
    img.height = pose.height;
    img.loading = 'lazy';
    img.decoding = 'async';
    const tag = document.createElement('small');
    tag.textContent = `${pose.id} · ${t(levelKeys[pose.level])} · ${pose.seconds}${t('초')}`;
    const title = document.createElement('strong');
    title.textContent = t(pose.name.ko);
    const focus = document.createElement('span');
    focus.textContent = t(pose.focus.ko);
    card.append(img, tag, title, focus);
    card.onclick = () => {
      selectMode('preset');
      $('poseCategory').value = category;
      $('poseLevel').value = level;
      preview = i;
      startPose = i;
      updateEstimate();
      paintPreview();
      $('library').close();
      $('usePreview').focus();
    };
    $('libraryGrid').append(card);
  });
}

function openLibrary() {
  $('libraryCategory').value = $('poseCategory').value;
  $('libraryLevel').value = $('poseLevel').value;
  $('librarySearch').value = '';
  $('library').showModal();
  renderLibrary();
}

function filterPractice() {
  preview = posePool()[0] ?? 0;
  startPose = null;
  updateEstimate();
  paintPreview();
}

populateCategories($('poseCategory'));
populateCategories($('libraryCategory'));
$('browseLibrary').onclick = openLibrary;
$('closeLibrary').onclick = () => $('library').close();
$('libraryCategory').onchange = renderLibrary;
$('libraryLevel').onchange = renderLibrary;
$('librarySearch').oninput = renderLibrary;

$('nextPreview').onclick = () => changePreview(1);
$('prevPreview').onclick = () => changePreview(-1);
$('presetTab').onclick = () => selectMode('preset');
$('ownTab').onclick = () => selectMode('own');
$('poseCategory').onchange = filterPractice;
$('poseLevel').onchange = filterPractice;
$('usePreview').onclick = () => {
  startPose = startPose === preview ? null : preview;
  paintPreview();
};
document.querySelectorAll('[data-time]').forEach(button => {
  button.onclick = () => setTime(Number(button.dataset.time));
});
$('customBtn').onclick = () => setTime(Number($('customSeconds').value), true);
$('customSeconds').oninput = () => setTime(Number($('customSeconds').value), true);
$('count').onchange = updateEstimate;
$('shuffle').onchange = updateEstimate;
$('files').onchange = event => addFiles(event.target.files);
$('drop').ondragover = event => { event.preventDefault(); $('drop').classList.add('drag'); };
$('drop').ondragleave = () => $('drop').classList.remove('drag');
$('drop').ondrop = event => {
  event.preventDefault();
  $('drop').classList.remove('drag');
  addFiles(event.dataTransfer.files);
};
$('start').onclick = start;
$('pause').onclick = pause;
$('next').onclick = () => move(1);
$('previous').onclick = () => move(-1);
$('mirror').onclick = () => { flip = !flip; transform(); };
$('zoom').onclick = () => { zoomed = !zoomed; render(); };
$('full').onclick = fullscreen;
$('sessionSound').onclick = () => { $('sound').checked = !$('sound').checked; render(); };
$('finish').onclick = finishSession;
$('session').addEventListener('cancel', event => { event.preventDefault(); finishSession(); });
$('closeInfo').onclick = () => $('info').close();
$('recordBtn').onclick = openHistory;

document.querySelectorAll('[data-course]').forEach(button => {
  button.onclick = () => {
    selectMode('preset');
    $('poseCategory').value = 'all';
    $('poseLevel').value = 'all';
    startPose = null;
    setTime(button.dataset.course === 'deep' ? 180 : button.dataset.course === 'warm' ? 30 : 60);
    $('count').value = button.dataset.course === 'deep' ? '5' : '10';
    updateEstimate();
    paintPreview();
    $('practice').scrollIntoView({ behavior: 'smooth' });
    $('start').focus({ preventScroll: true });
  };
});

document.addEventListener('keydown', event => {
  if (!$('session').open || ['INPUT', 'SELECT', 'TEXTAREA'].includes(event.target.tagName)) return;
  if (event.code === 'Space') { event.preventDefault(); pause(); }
  if (event.key === 'ArrowRight') { event.preventDefault(); move(1); }
  if (event.key === 'ArrowLeft') { event.preventDefault(); move(-1); }
  if (event.key.toLowerCase() === 'm') $('mirror').click();
  if (event.key.toLowerCase() === 'f') fullscreen();
});

window.addEventListener('posetoki-language', () => {
  for (const id of ['poseCategory', 'libraryCategory']) {
    const value = $(id).value;
    populateCategories($(id));
    $(id).value = value;
  }
  updateEstimate();
  updateFileStatus();
  renderUploadList();
  renderNextGoal();
  paintPreview();
  renderLibrary();
  if (active) {
    render();
    $('pause').textContent = t(paused ? '계속 그리기' : '일시정지');
  }
});
window.addEventListener('beforeunload', () => uploads.forEach(photo => URL.revokeObjectURL(photo.url)));
document.addEventListener('DOMContentLoaded', () => {
  applyDeepLink();
  updateFileStatus();
  renderNextGoal();
});

if (document.modelContext?.registerTool) {
  try {
    Promise.resolve(document.modelContext.registerTool({
      name: 'configure_practice',
      description: 'Set the curated-pose practice duration and pose count without starting the session.',
      inputSchema: {
        type: 'object',
        properties: {
          seconds: { type: 'integer', minimum: 5, maximum: 3600 },
          count: { type: 'integer', enum: [5, 10, 15, 20] }
        },
        required: ['seconds', 'count'],
        additionalProperties: false
      },
      annotations: { readOnlyHint: false, untrustedContentHint: false },
      execute(input) {
        if (!Number.isInteger(input.seconds) || input.seconds < 5 || input.seconds > 3600 ||
            ![5, 10, 15, 20].includes(input.count)) throw new Error('Invalid practice settings');
        if (active) throw new Error('Finish the current session first');
        selectMode('preset');
        setTime(input.seconds, ![30, 60, 180, 300].includes(input.seconds));
        $('count').value = String(input.count);
        updateEstimate();
        return { seconds: input.seconds, count: input.count, source: 'curated poses' };
      }
    })).catch(() => {});
  } catch {}
}
