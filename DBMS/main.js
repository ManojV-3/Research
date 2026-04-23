// ─── API Helper ──────────────────────────────────────────────────────────────

async function apiFetch(url, options = {}) {
  try {
    const defaults = {
      headers: { 'Content-Type': 'application/json' }
    };
    const response = await fetch(url, { ...defaults, ...options });
    const data = await response.json();
    if (!response.ok) {
      console.error('API error:', data);
      return data; // return so caller can check .error
    }
    return data;
  } catch (err) {
    console.error('Fetch error:', err);
    showToast('Network error. Please try again.', 'error');
    return null;
  }
}

// ─── Toast Notifications ──────────────────────────────────────────────────────

function showToast(message, type = 'success') {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.className = `toast ${type} show`;
  setTimeout(() => {
    toast.classList.remove('show');
  }, 3500);
}

// ─── Nav Toggle (mobile) ──────────────────────────────────────────────────────

function toggleNav() {
  document.getElementById('navLinks').classList.toggle('open');
}

// ─── Pub Type Labels ──────────────────────────────────────────────────────────

const TYPE_LABELS = {
  journal: '📰 Journal',
  conference: '🎙️ Conference',
  book_chapter: '📖 Book Chapter',
  book: '📚 Book'
};

const TYPE_TAGS = {
  journal: 'Journal Article',
  conference: 'Conference Paper',
  book_chapter: 'Book Chapter',
  book: 'Book'
};

// ─── Render Publication Card ─────────────────────────────────────────────────

function renderPubCard(p, showDelete = false) {
  const typeClass = `pub-type-${p.pub_type}`;
  const tag = TYPE_TAGS[p.pub_type] || p.pub_type;
  const deleteBtn = showDelete
    ? `<button class="btn-icon btn-danger" onclick="deletePub(${p.id})" title="Delete">🗑</button>`
    : '';

  return `
    <div class="pub-card ${typeClass}">
      <div class="pub-card-stripe"></div>
      <div class="pub-body">
        <span class="pub-type-tag">${tag}</span>
        <div class="pub-title">${escHtml(p.title)}</div>
        <div class="pub-meta">
          <span>👤 ${escHtml(p.faculty_name)}</span>
          <span class="pub-venue">📍 ${escHtml(p.publication_name)}</span>
          <span>📅 ${escHtml(p.pub_month)} ${p.pub_year}</span>
          ${p.issn_isbn ? `<span>🔢 ${escHtml(p.issn_isbn)}</span>` : ''}
          ${p.doi ? `<span>🔗 <a href="https://doi.org/${escHtml(p.doi)}" target="_blank">DOI</a></span>` : ''}
        </div>
      </div>
      ${deleteBtn ? `<div class="pub-actions">${deleteBtn}</div>` : ''}
    </div>
  `;
}

// ─── Escape HTML ──────────────────────────────────────────────────────────────

function escHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
