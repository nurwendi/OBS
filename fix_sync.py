import re

def fix_sync():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update UI: Remove file input, add helper text
    old_input = """              <div class="input-group">
                <label>File Media (Upload atau URL)</label>
                <input type="file" id="file-media-${lowerPos}" accept="image/*,video/*" class="small-input" style="margin-bottom: 8px;">
                <input type="text" id="url-media-${lowerPos}" class="small-input" placeholder="Atau masukkan URL / Base64">
              </div>"""
    
    new_input = """              <div class="input-group">
                <label>Nama File / URL URL Media</label>
                <input type="text" id="url-media-${lowerPos}" class="small-input" placeholder="Ketik nama file (contoh: logo.png)">
                <small style="color:var(--text-muted); font-size:12px; margin-top:5px; display:block;">
                  * Taruh file gambar/video di dalam folder yang sama, lalu ketik nama filenya di atas (contoh: <b>logo.png</b> atau <b>animasi.webm</b>). 
                  Jangan gunakan tombol upload karena batas sinkronisasi OBS (ntfy.sh) akan penuh.
                </small>
              </div>"""
    content = content.replace(old_input, new_input)

    # 2. Update JS: Remove file input listener
    file_listener_regex = r"const fileInput = document\.getElementById\(`file-media-\$\{lowerPos\}`\);\s*"
    content = re.sub(file_listener_regex, "", content)
    
    file_change_listener = r"""          fileInput\.addEventListener\('change', \(e\) => \{[\s\S]*?\}\);\s*"""
    content = re.sub(file_change_listener, "", content)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

fix_sync()
