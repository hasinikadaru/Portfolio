"""
patch.py — Run this once in your portfolio folder to fix all project pages.
Usage: python3 patch.py

What it does (mobile only, desktop untouched):
  1. Replaces <header id="site-nav"> with hamburger version on all project pages
  2. Adds hamburger CSS + mobile nav rules to each page's <style> block
  3. Adds hamburger JS before </body> on each page
  4. Fixes the stray << bug in project-cbna.html
"""

import re, os, shutil

FILES = [
    "project-taft.html",
    "project-kang.html",
    "project-butler.html",
    "project-manchirevula.html",
    "project-dormitory.html",
    "project-3bhk.html",
]

NAV_HTML = '''<header id="site-nav">
  <a href="index.html" class="nav-name">Hasini Kadaru <span>CPHC</span></a>
  <button class="nav-toggle" aria-label="Toggle menu">
    <span></span><span></span><span></span>
  </button>
  <ul>
    <li><a href="index.html">Home</a></li>
    <li><a href="work.html">Work</a></li>
    <li><a href="about.html">About</a></li>
    <li><a href="contact.html">Contact</a></li>
    <li><a href="Hasini_Kadaru_Resume_2026" download="Hasini_Kadaru_Resume_2026.pdf" style="color:#1a1814;font-weight:600;">Resume</a></li>
  </ul>
</header>'''

NAV_CSS = """
/* ── HAMBURGER NAV — MOBILE ONLY ── */
.nav-toggle { display:none; flex-direction:column; gap:5px; cursor:pointer; background:none; border:none; padding:4px; }
.nav-toggle span { display:block; width:24px; height:2px; background:#1a1814; transition:transform .3s,opacity .3s; }
.nav-toggle.open span:nth-child(1) { transform:translateY(7px) rotate(45deg); }
.nav-toggle.open span:nth-child(2) { opacity:0; }
.nav-toggle.open span:nth-child(3) { transform:translateY(-7px) rotate(-45deg); }
@media(max-width:768px){
  #site-nav { padding: 1rem 1.5rem !important; }
  #site-nav .nav-toggle { display:flex !important; }
  #site-nav ul { display:none !important; position:fixed !important; top:57px !important; left:0 !important; right:0 !important; background:rgba(247,244,239,0.98) !important; backdrop-filter:blur(12px) !important; flex-direction:column !important; gap:0 !important; border-bottom:1px solid #ddd9d3 !important; z-index:98 !important; }
  #site-nav ul.open { display:flex !important; }
  #site-nav ul li { border-bottom:1px solid #ddd9d3 !important; }
  #site-nav ul a { display:block !important; padding:1rem 1.5rem !important; font-size:.9rem !important; }
  .proj-nav-title { font-size:1rem !important; }
  .proj-nav-item { padding:1.2rem 1.5rem !important; }
}
"""

NAV_JS = """<script>
const navToggle = document.querySelector('.nav-toggle');
const navMenu = document.querySelector('#site-nav ul');
if(navToggle && navMenu){
  navToggle.addEventListener('click', () => {
    navToggle.classList.toggle('open');
    navMenu.classList.toggle('open');
  });
  navMenu.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      navToggle.classList.remove('open');
      navMenu.classList.remove('open');
    });
  });
}
</script>
"""

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Fix CBNA stray < bug
    if 'cbna' in filepath:
        content = content.replace('    <<li><a href="Hasini_Kadaru_Resume_2026"',
                                   '    <li><a href="Hasini_Kadaru_Resume_2026"')

    # Replace nav
    content = re.sub(r'<header id="site-nav">.*?</header>', NAV_HTML, content, flags=re.DOTALL)

    # Add CSS before last </style>
    idx = content.rfind('</style>')
    if idx != -1:
        content = content[:idx] + NAV_CSS + content[idx:]

    # Add JS before </body>
    content = content.replace('</body>', NAV_JS + '</body>')

    if content != original:
        # Backup original
        shutil.copy(filepath, filepath + '.bak')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Patched: {filepath}  (backup saved as {filepath}.bak)")
    else:
        print(f"  ⚠ No changes made to: {filepath} — check file exists and has expected nav structure")

print("=" * 60)
print("Portfolio Mobile Nav Patcher")
print("=" * 60)

for fname in FILES:
    if os.path.exists(fname):
        patch_file(fname)
    else:
        print(f"  ✗ NOT FOUND: {fname} — make sure you're running from the portfolio folder")

print()
print("Done. Check your site on mobile.")
print("To undo any file: rename the .bak file back to .html")
