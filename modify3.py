import re

def update_file():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Move media-section inside controls-section
    # The end of controls-section is `      </section>` followed by `      <section class="admin-card media-section">`
    old_section_end = """        </div>
      </section>

      
      <section class="admin-card media-section">
        <div class="card-header">
          <svg class="header-icon" viewBox="0 0 24 24" width="22" height="22" stroke="currentColor" stroke-width="2" fill="none"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>
          <h2>Media Logo (Atas)</h2>
        </div>
        <div id="media-panels"></div>
      </section>"""
      
    new_section_end = """        </div>
        
        <div class="divider"></div>
        <div class="card-header">
          <svg class="header-icon" viewBox="0 0 24 24" width="22" height="22" stroke="currentColor" stroke-width="2" fill="none"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>
          <h2>Media Logo (Atas)</h2>
        </div>
        <div id="media-panels"></div>
        
      </section>"""

    content = content.replace(old_section_end, new_section_end)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

update_file()
