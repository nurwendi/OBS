import re

def update_file():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the right place to insert media settings in UI
    # Before: <!-- PREVIEW & PRESETS KANAN -->
    # We will inject a new <section class="admin-card">
    media_controls_html = """
      <section class="admin-card media-section">
        <div class="card-header">
          <svg class="header-icon" viewBox="0 0 24 24" width="22" height="22" stroke="currentColor" stroke-width="2" fill="none"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>
          <h2>Media Logo (Atas)</h2>
        </div>
        <div id="media-panels"></div>
      </section>
"""
    if "media-section" not in content:
        content = content.replace("<!-- PREVIEW & PRESETS KANAN -->", media_controls_html + "\n      <!-- PREVIEW & PRESETS KANAN -->")

    # If old checkLogo is there, remove it
    old_logo_html = """            <div class="setting-group toggle-control">
              <label class="switch-container">
                <input type="checkbox" id="check-logo" checked>
                <span class="switch-slider"></span>
              </label>
              <label for="check-logo">Tampilkan Logo Kanan Atas</label>
            </div>"""
    content = content.replace(old_logo_html, "")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

update_file()
