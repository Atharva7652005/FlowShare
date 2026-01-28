const storageInput = document.getElementById('storageInput');
const getBtn = document.getElementById('getBtn');
const loading = document.getElementById('loading');
const msg = document.getElementById('msg');
const result = document.getElementById('result');

function setLoading(active) {
    loading.style.display = active ? 'inline-block' : 'none';
    getBtn.disabled = active;
}

function humanFileSize(size) {
    if (!size && size !== 0) return '';
    if (size < 1024) return size + ' B';
    const i = Math.floor(Math.log(size) / Math.log(1024));
    const units = ['B', 'KB', 'MB', 'GB', 'TB'];
    return (size / Math.pow(1024, i)).toFixed(i ? 1 : 0) + ' ' + units[i];
}

async function fetchFiles(id) {
    setLoading(true);
    msg.textContent = '';
    result.innerHTML = '';
    try {
        const res = await fetch('/api/rooms/' + encodeURIComponent(id) + '/files', { method: 'GET' });
        if (res.status === 404) {
            msg.className = 'error'; msg.textContent = 'No room found with that storage ID.';
            return;
        }
        if (!res.ok) {
            const txt = await res.text().catch(() => null);
            msg.className = 'error'; msg.textContent = 'Error: ' + (txt || res.status);
            return;
        }
        const data = await res.json();
        if (!data?.files || data.files.length === 0) {
            msg.className = 'muted'; msg.textContent = 'No files stored for this ID.';
            return;
        }
        msg.className = 'muted'; msg.textContent = 'Found ' + data.files.length + ' file(s).';

        data.files.forEach(f => {
            const el = document.createElement('div'); el.className = 'file-item';
            let url = f.download_url || ('/api/download?storage_id=' + encodeURIComponent(id) + '&filename=' + encodeURIComponent(f.filename));
            el.innerHTML = `
          <div class="file-meta">
            <div class="icon">${(f.filename || 'F')[0].toUpperCase()}</div>
            <div>
              <div style="font-weight:600">${f.filename}</div>
              <div class="muted" style="font-size:13px">${humanFileSize(f.size)}</div>
            </div>
          </div>
          <div style="display:flex;gap:8px">
            <a class="download" href="${url}" target="_blank" rel="noopener">Download</a>
          </div>
        `;
            result.appendChild(el);
        });
    } catch (err) {
        console.error(err);
        msg.className = 'error'; msg.textContent = 'Network error while fetching files.';
    } finally {
        setLoading(false);
    }
}

getBtn.addEventListener('click', () => {
    const id = (storageInput.value || '').trim();
    if (!/^\d{4}$/.test(id)) {
        msg.className = 'error'; msg.textContent = 'Please enter a valid 4-digit storage ID.';
        return;
    }
    fetchFiles(id);
});

storageInput.addEventListener('keydown', e => { if (e.key === 'Enter') getBtn.click(); });