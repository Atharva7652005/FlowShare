const storageIdEl = document.getElementById('storageId');
const createRoomBtn = document.getElementById('createRoom');
const copyBtn = document.getElementById('copyBtn');
const dropArea = document.getElementById('dropArea');
const fileInput = document.getElementById('fileInput');
const pickFiles = document.getElementById('pickFiles');
const fileList = document.getElementById('fileList');
const uploadBtn = document.getElementById('uploadBtn');
const statusEl = document.getElementById('status');
const toast = document.getElementById('toast');

let storageId = null;
let files = []; // array of File objects

function showToast(msg, timeout = 3500) {
    toast.textContent = msg; toast.style.display = 'block';
    clearTimeout(toast._t);
    toast._t = setTimeout(() => toast.style.display = 'none', timeout);
}
function humanFileSize(size) {
    if (size < 1024) return size + ' B';
    const i = Math.floor(Math.log(size) / Math.log(1024));
    const units = ['B', 'KB', 'MB', 'GB', 'TB'];
    return (size / Math.pow(1024, i)).toFixed(i ? 1 : 0) + ' ' + units[i];
}
function renderFileList() {
    fileList.innerHTML = '';
    if (files.length === 0) {
        fileList.innerHTML = '<div class="muted">No files selected</div>'; return;
    }
    files.forEach((f, idx) => {
        const el = document.createElement('div'); el.className = 'file-item';
        el.innerHTML = `
        <div class="file-meta">
          <div class="file-icon-placeholder">${f.name[0]?.toUpperCase() || 'F'}</div>
          <div>
            <div class="file-name">${f.name}</div>
            <div class="file-size">${humanFileSize(f.size)}</div>
          </div>
        </div>
        <div class="actions">
          <button class="ghost" data-idx="${idx}" style="color: #ff6b6b; border-color: rgba(255,107,107,0.3)">Remove</button>
        </div>
      `;
        fileList.appendChild(el);
    });
}

function genId() {
    return String(Math.floor(1000 + Math.random() * 9000));
}

createRoomBtn.addEventListener('click', () => {
    storageId = genId();
    storageIdEl.textContent = storageId;
    showToast('Room created — ID: ' + storageId);
});

copyBtn.addEventListener('click', async () => {
    if (!storageId) return showToast('No storage ID to copy');
    try {
        await navigator.clipboard.writeText(storageId);
        showToast('Copied storage ID');
    } catch {
        showToast('Copy failed — select & copy manually');
    }
});

pickFiles.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', (e) => {
    addFiles(e.target.files);
    fileInput.value = '';
});

function addFiles(fileListObj) {
    const incoming = Array.from(fileListObj);
    incoming.forEach(f => {
        const exists = files.some(x => x.name === f.name && x.size === f.size && x.lastModified === f.lastModified);
        if (!exists) files.push(f);
    });
    renderFileList();
}

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(ev => {
    dropArea.addEventListener(ev, e => { e.preventDefault(); e.stopPropagation(); });
});
['dragenter', 'dragover'].forEach(ev => {
    dropArea.addEventListener(ev, () => dropArea.classList.add('dragover'));
});
['dragleave', 'drop'].forEach(ev => {
    dropArea.addEventListener(ev, () => dropArea.classList.remove('dragover'));
});
dropArea.addEventListener('drop', e => {
    if (e.dataTransfer?.files?.length) addFiles(e.dataTransfer.files);
});

fileList.addEventListener('click', (e) => {
    const btn = e.target.closest('button[data-idx]');
    if (!btn) return;
    const idx = Number(btn.dataset.idx);
    files.splice(idx, 1);
    renderFileList();
});

uploadBtn.addEventListener('click', async () => {
    if (!storageId) { showToast('Please create a room (Storage ID) first'); return; }
    if (files.length === 0) { showToast('Please select at least one file'); return; }

    uploadBtn.disabled = true; statusEl.textContent = 'Uploading...';
    try {
        const fd = new FormData();
        fd.append('storage_id', storageId);
        files.forEach(f => fd.append('files', f));
        const res = await fetch('/api/upload/', { method: 'POST', body: fd });
        if (!res.ok) {
            const txt = await res.text().catch(() => null);
            throw new Error(txt || 'Upload failed with status ' + res.status);
        }
        const data = await res.json().catch(() => null);
        statusEl.textContent = '';
        showToast((data?.message) || 'Upload successful');

        files = []; renderFileList();
        if (data?.storage_id) {
            showToast('Files stored at ID: ' + data.storage_id);
        }
    } catch (err) {
        statusEl.textContent = '';
        console.error(err);
        showToast('Upload error: ' + (err.message || err));
    } finally {
        uploadBtn.disabled = false;
    }
});

renderFileList();