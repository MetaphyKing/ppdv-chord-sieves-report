from pathlib import Path
import shutil
import subprocess

repo = Path(r"C:\dev\chord-sieves-report")
assets = repo / "assets"
assets.mkdir(exist_ok=True)
for fn in ["tic_271478281_08_ppdv_3d_world_plate.png", "tic_52005579_04_ppdv_3d_world_plate.png"]:
    shutil.copy2(Path(r"C:\dev\ppdv-chord-sieves-report\assets") / fn, assets / fn)

idx = repo / "index.html"
html = idx.read_text(encoding="utf-8")
if "ppdv-chord-sieves-report.vercel.app" not in html:
    old_cta = '<a class="btn btn-outline" href="https://bama-cortical-report.vercel.app" target="_blank" rel="noopener">Companion BAMA v3.1 Systems Paper &rarr;</a>'
    new_cta = (
        old_cta
        + '\n    <a class="btn btn-outline" href="https://chrono-torque-report.vercel.app" target="_blank" rel="noopener">Companion CHRONO-TORQUE v2.0 Paper &rarr;</a>'
        + '\n    <a class="btn btn-cyan" href="https://ppdv-chord-sieves-report.vercel.app" target="_blank" rel="noopener">PPDV &times; CHORD-SIEVES 3D World Showcase &rarr;</a>'
    )
    html = html.replace(old_cta, new_cta)
    target_hdr = "<h2>10-Page Print-Exact Scientific Folio (High-DPI Raster Scans)</h2>"
    showcase_block = """<h2>Bidirectional Symbiosis Showcase: <em>Prompting Python Data Visualization</em> (Aleinikov, 2026) &times; CHORD-SIEVES 3D World Pipeline</h2>
    <a class="btn btn-cyan" style="padding:6px 12px;font-size:0.8rem" href="https://ppdv-chord-sieves-report.vercel.app" target="_blank" rel="noopener">Open Full Interactive Showcase Portal &rarr;</a>
  </div>
  <p style="color: var(--muted); font-size: 0.9rem; margin-bottom: 14px;">
    Uniting Aleksei Aleinikov&rsquo;s <em>Prompting Python Data Visualization</em> (Orange Education / AVA&trade;, ISBN <code>978-9349887992</code>; Chapters 14, 15 &amp; 18 Adaptive Hexbin, Bootstrap 95% CI, <code>PngInfo</code> Visualization Passports, and Honesty Linters) with CHORD-SIEVES&rsquo;s <strong>Closed-Loop Spherical (cos &phi;) Pixel-to-Telemetry Feedback Engine</strong> and <strong>3-Zone Local Quadratic Flank Bridge</strong> across our top Shirt-Sleeve Habitable Candidates (0&deg;C &le; T<sub>surf</sub> &le; +35&deg;C).
  </p>
  <div class="folio-grid" style="margin-bottom: 28px;">
    <div class="folio-card">
      <div class="folio-card-hdr"><span>TIC 271478281.08 (ESI 0.984 &bull; +20.8&deg;C / +69.4&deg;F)</span><span>4-Panel PPDV &times; CHORD-SIEVES Diagnostic Plate (1024&times;512 PBR)</span></div>
      <img src="assets/tic_271478281_08_ppdv_3d_world_plate.png" alt="TIC 271478281.08 PPDV x CHORD-SIEVES 4-Panel Plate" loading="eager">
    </div>
    <div class="folio-card">
      <div class="folio-card-hdr"><span>TIC 52005579.04 (ESI 0.978 &bull; +21.5&deg;C / +70.7&deg;F)</span><span>4-Panel PPDV &times; CHORD-SIEVES Diagnostic Plate (1024&times;512 PBR)</span></div>
      <img src="assets/tic_52005579_04_ppdv_3d_world_plate.png" alt="TIC 52005579.04 PPDV x CHORD-SIEVES 4-Panel Plate" loading="eager">
    </div>
  </div>

  <div class="section-hdr">
    <h2>10-Page Print-Exact Scientific Folio (High-DPI Raster Scans)</h2>"""
    html = html.replace(target_hdr, showcase_block)
    idx.write_text(html, encoding="utf-8")

edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
preview = assets / "pages" / "chord_sieves_ppdv_preview.png"
subprocess.run(
    [edge, "--headless=new", "--disable-gpu", "--window-size=1440,1450", f"--screenshot={preview}", idx.as_uri()],
    check=True,
)
print(f"[OK] Patched index.html & rendered preview ({preview.stat().st_size:,} B)")
