def apply_offline():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Badge text
    content = content.replace("Cloud Sync: Terhubung (ntfy.sh)", "Local Sync: Aktif (Offline Mode)")

    # 2. Update SYNC_TOPIC and SYNC_URL variables
    content = content.replace('const SYNC_TOPIC = "obs_ticker_hudi_558";', '// Mode Offline Murni')
    content = content.replace('const SYNC_URL = `https://ntfy.sh/${SYNC_TOPIC}`;', '')

    # 3. Disable SSE initCloudSync EXACT MATCH
    init_sync_old = """      function initCloudSync() {
        // SSE (Server-Sent Events) bekerja secara bawaan di semua modern browser & OBS CEF!
        const eventSource = new EventSource(`${SYNC_URL}/sse`);
        
        eventSource.onmessage = (event) => {
          try {
            const payload = JSON.parse(event.data);
            if (payload && payload.message) {
              const settings = JSON.parse(payload.message);
              applySettings(settings);
              localStorage.setItem('obs_ticker_settings', JSON.stringify(settings));
            }
          } catch (e) {
            console.error("Gagal membaca pesan cloud sync:", e);
          }
        };

        eventSource.onerror = () => {
          console.warn("Koneksi Cloud terputus, mencoba menghubungkan kembali...");
        };
      }"""
      
    init_sync_new = """      function initCloudSync() {
        console.log("Mode offline lokal. Sinkronisasi lewat memori internal OBS.");
      }"""
      
    content = content.replace(init_sync_old, init_sync_new)

    # 4. Remove fetch(SYNC_URL) EXACT MATCH
    fetch_old = """        // 2. Push ke ntfy.sh (Selesai dalam 0.05 detik tanpa server lokal)
        fetch(SYNC_URL, {
          method: 'POST',
          body: JSON.stringify(state)
        }).catch(err => console.warn("Pesan cloud tertunda, tetap menyimpan secara lokal.", err));"""
        
    fetch_new = """        // Mode offline tidak mengirim data ke server luar."""
    content = content.replace(fetch_old, fetch_new)

    # 5. Update help text
    old_help = "Jangan gunakan tombol upload karena batas sinkronisasi OBS (ntfy.sh) akan penuh."
    new_help = "File akan diload secara offline langsung oleh OBS."
    content = content.replace(old_help, new_help)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

apply_offline()
