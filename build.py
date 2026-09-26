import re

def build():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. CSS
    css = """
    .watermark-container {
      position: absolute;
      top: 40px;
      z-index: 50;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .watermark-left { left: 40px; }
    .watermark-center { left: 50%; transform: translateX(-50%); }
    .watermark-right { right: 40px; }
    .watermark-media {
      object-fit: contain;
      transition: all 0.3s ease;
    }
    .media-settings-panel {
      background: rgba(255,255,255,0.02);
      padding: 15px;
      border-radius: 10px;
      border: 1px solid var(--border-color);
      margin-bottom: 15px;
    }
    .media-settings-panel h3 {
      font-size: 15px;
      margin-bottom: 15px;
      color: var(--primary-color);
    }
    """
    content = content.replace("</style>", css + "\n</style>")

    # 2. Overlay HTML
    overlay_old = """    <div id="overlay-watermark" class="overlay-watermark">
      <img src="logo.png" alt="Broadcast Logo">
    </div>"""
    overlay_new = """    <div id="watermark-left" class="watermark-container watermark-left" style="display: none;"></div>
    <div id="watermark-center" class="watermark-container watermark-center" style="display: none;"></div>
    <div id="watermark-right" class="watermark-container watermark-right" style="display: none;"></div>"""
    content = content.replace(overlay_old, overlay_new)

    preview_old = """              <div id="overlay-watermark-preview" class="overlay-watermark">
                <img src="logo.png" alt="Broadcast Logo">
              </div>"""
    preview_new = """              <div id="preview-watermark-left" class="watermark-container watermark-left" style="display: none;"></div>
              <div id="preview-watermark-center" class="watermark-container watermark-center" style="display: none;"></div>
              <div id="preview-watermark-right" class="watermark-container watermark-right" style="display: none;"></div>"""
    content = content.replace(preview_old, preview_new)

    # 3. Admin UI (remove old checkbox, add media panels container)
    checkbox_old = """          <div class="setting-group flex-group">
            <div class="toggle-control">
              <label class="switch-container">
                <input type="checkbox" id="check-logo" checked>
                <span class="switch-slider"></span>
              </label>
              <label for="check-logo">Tampilkan Logo Watermark</label>
            </div>
          </div>"""
    content = content.replace(checkbox_old, "")

    admin_ui_insert = """
        <div class="divider"></div>
        <div class="card-header">
          <svg class="header-icon" viewBox="0 0 24 24" width="22" height="22" stroke="currentColor" stroke-width="2" fill="none"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>
          <h2>Media Logo (Atas)</h2>
        </div>
        <div id="media-panels"></div>
"""
    # Insert right before </section> of controls-section
    content = content.replace("        </div>\n      </section>", "        </div>" + admin_ui_insert + "\n      </section>")

    # 4. State
    state_old = """    let state = {
      text: "Selamat datang di Live Streaming! ★ Jangan lupa follow, like, dan share.",
      speed: 150,
      fontSize: 28,
      theme: "theme-cyberpunk",
      isPaused: false,
      badgeVisible: true,
      badgeText: "LIVE",
      clockVisible: true,
      logoVisible: true,
      separator: "★",
      alertActive: false,
      badgeBgColor: "#7928ca",
      badgeTextColor: "#ffffff",
      badgeType: "text",
      badgeLogoUrl: "logo.png"
    };"""
    
    state_new = """    let state = {
      text: "Selamat datang di Live Streaming! ★ Jangan lupa follow, like, dan share.",
      speed: 150,
      fontSize: 28,
      theme: "theme-cyberpunk",
      isPaused: false,
      badgeVisible: true,
      badgeText: "LIVE",
      clockVisible: true,
      separator: "★",
      alertActive: false,
      badgeBgColor: "#7928ca",
      badgeTextColor: "#ffffff",
      badgeType: "text",
      badgeLogoUrl: "logo.png",
      mediaLeft: { enabled: false, type: 'image', url: '', opacity: 100, size: 150 },
      mediaCenter: { enabled: false, type: 'image', url: '', opacity: 100, size: 150 },
      mediaRight: { enabled: true, type: 'image', url: 'logo.png', opacity: 100, size: 95 }
    };"""
    content = content.replace(state_old, state_new)

    # Remove references to old logo logic
    content = content.replace("const previewOverlayWatermark = document.getElementById('overlay-watermark-preview');", "")
    content = content.replace("const overlayWatermark = document.getElementById('overlay-watermark');", "")
    content = content.replace("const checkLogo = document.getElementById('check-logo');", "")
    content = content.replace("previewOverlayWatermark.style.display = state.logoVisible ? 'block' : 'none';", "")
    content = content.replace("checkLogo.checked = state.logoVisible;", "")
    content = content.replace("""      checkLogo.addEventListener('change', (e) => {
        state.logoVisible = e.target.checked;
        broadcastState();
      });""", "")

    # 5. JS
    js = """
      const mediaPositions = ['Left', 'Center', 'Right'];
      
      function initMediaPanels() {
        const container = document.getElementById('media-panels');
        if (!container) return;
        
        mediaPositions.forEach(pos => {
          const lowerPos = pos.toLowerCase();
          const html = `
            <div class="media-settings-panel">
              <h3>Logo ${pos === 'Left' ? 'Kiri' : pos === 'Center' ? 'Tengah' : 'Kanan'} Atas</h3>
              <div class="setting-group toggle-control" style="margin-bottom: 15px;">
                <label class="switch-container">
                  <input type="checkbox" id="check-media-${lowerPos}">
                  <span class="switch-slider"></span>
                </label>
                <label for="check-media-${lowerPos}">Tampilkan</label>
              </div>
              <div class="input-group">
                <label>File Media (Upload atau URL)</label>
                <input type="file" id="file-media-${lowerPos}" accept="image/*,video/*" class="small-input" style="margin-bottom: 8px;">
                <input type="text" id="url-media-${lowerPos}" class="small-input" placeholder="Atau masukkan URL / Base64">
              </div>
              <div class="settings-grid">
                <div class="setting-group">
                  <div class="label-with-value">
                    <label>Ukuran (px)</label>
                    <span id="val-size-${lowerPos}" class="badge-value">150px</span>
                  </div>
                  <input type="range" id="range-size-${lowerPos}" min="50" max="800" step="10">
                </div>
                <div class="setting-group">
                  <div class="label-with-value">
                    <label>Transparansi (%)</label>
                    <span id="val-opacity-${lowerPos}" class="badge-value">100%</span>
                  </div>
                  <input type="range" id="range-opacity-${lowerPos}" min="10" max="100" step="5">
                </div>
              </div>
            </div>
          `;
          container.insertAdjacentHTML('beforeend', html);
        });
      }

      function setupMediaListeners() {
        mediaPositions.forEach(pos => {
          const lowerPos = pos.toLowerCase();
          const stateKey = `media${pos}`;
          
          const check = document.getElementById(`check-media-${lowerPos}`);
          if (!check) return;
          const fileInput = document.getElementById(`file-media-${lowerPos}`);
          const urlInput = document.getElementById(`url-media-${lowerPos}`);
          const sizeRange = document.getElementById(`range-size-${lowerPos}`);
          const opacityRange = document.getElementById(`range-opacity-${lowerPos}`);
          
          check.checked = state[stateKey].enabled || false;
          urlInput.value = state[stateKey].url || '';
          sizeRange.value = state[stateKey].size || 150;
          opacityRange.value = state[stateKey].opacity || 100;
          document.getElementById(`val-size-${lowerPos}`).textContent = `${state[stateKey].size || 150}px`;
          document.getElementById(`val-opacity-${lowerPos}`).textContent = `${state[stateKey].opacity || 100}%`;
          
          check.addEventListener('change', (e) => { state[stateKey].enabled = e.target.checked; broadcastState(); });
          urlInput.addEventListener('input', (e) => { state[stateKey].url = e.target.value; broadcastState(); });
          sizeRange.addEventListener('input', (e) => {
            state[stateKey].size = parseInt(e.target.value);
            document.getElementById(`val-size-${lowerPos}`).textContent = `${state[stateKey].size}px`;
            broadcastState();
          });
          opacityRange.addEventListener('input', (e) => {
            state[stateKey].opacity = parseInt(e.target.value);
            document.getElementById(`val-opacity-${lowerPos}`).textContent = `${state[stateKey].opacity}%`;
            broadcastState();
          });
          
          fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = (event) => {
              state[stateKey].url = event.target.result;
              state[stateKey].type = file.type.startsWith('video') ? 'video' : 'image';
              urlInput.value = 'File tersimpan (Base64)';
              broadcastState();
            };
            reader.readAsDataURL(file);
          });
        });
      }

      function renderMediaElement(containerId, data) {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        if (!data || !data.enabled || !data.url) {
          container.style.display = 'none';
          container.innerHTML = '';
          return;
        }
        
        container.style.display = 'flex';
        container.innerHTML = '';
        
        const isVideo = data.type === 'video' || data.url.match(/\.(mp4|webm|ogg)$/i) || data.url.startsWith('data:video');
        
        let el = document.createElement(isVideo ? 'video' : 'img');
        if (isVideo) {
          el.autoplay = true;
          el.loop = true;
          el.muted = true;
        }
        el.src = data.url;
        el.className = 'watermark-media';
        el.style.width = `${data.size}px`;
        el.style.opacity = data.opacity / 100;
        
        container.appendChild(el);
      }
    """
    
    # inject JS functions before applyStateToPreview
    content = content.replace("function applyStateToPreview() {", js + "\n      function applyStateToPreview() {")
    
    # Apply media in applyStateToPreview
    apply_js = """
        if (typeof renderMediaElement === 'function') {
          renderMediaElement('watermark-left', state.mediaLeft);
          renderMediaElement('watermark-center', state.mediaCenter);
          renderMediaElement('watermark-right', state.mediaRight);
          renderMediaElement('preview-watermark-left', state.mediaLeft);
          renderMediaElement('preview-watermark-center', state.mediaCenter);
          renderMediaElement('preview-watermark-right', state.mediaRight);
        }
"""
    content = content.replace("previewMarqueeItems[0].textContent = finalString;", apply_js + "\n        previewMarqueeItems[0].textContent = finalString;")
    
    # Init media panels on DOM load
    init_call = """
      initMediaPanels();
      setupMediaListeners();
      applyStateToPreview();
      renderPresets();
    """
    content = content.replace("applyStateToPreview();\n      renderPresets();", init_call)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

build()
