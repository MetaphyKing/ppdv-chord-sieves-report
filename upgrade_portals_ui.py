r"""
Upgrades:
1. C:\dev\chrono-torque-report\*.html:
   - Fixes .hero-banner-wrap img so the 2160x864 banner stretches 100% edge-to-edge across the entire banner outline frame (width: 100%; height: auto; display: block; object-fit: cover;).
   - Adds companion link to https://ppdv-chord-sieves-report.vercel.app and https://chord-sieves-report.vercel.app.
2. C:\dev\chord-sieves-report\index.html:
   - Replaces the static unclickable 2-column grid with a 3-Mode Interactive Scientific Studio & Fullscreen Lightbox Reader:
     * Mode A (Default): Interactive Stage & Chapter Reader (Left Chapter TOC P1..P10 + Large Readable Stage + 1-Page / 2-Page Spread toggle + Prev/Next + Click-to-Fullscreen).
     * Mode B: Side-by-Side 2-Column Folio Grid where EVERY page card and EVERY PPDV x CHORD-SIEVES 4-panel plate is clickable (`cursor: zoom-in`) with hover badge and opens in the Fullscreen High-DPI Lightbox Modal (with Zoom 100%/150%/200%, Prev/Next arrows, keyboard navigation, and Download).
     * Mode C: Embedded Native Browser PDF Viewer.
3. C:\dev\bama-cortical-report\index.html:
   - Adds companion links to https://ppdv-chord-sieves-report.vercel.app, https://chord-sieves-report.vercel.app, and https://chrono-torque-report.vercel.app in the sidebar.
"""
from pathlib import Path
import subprocess

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# ---------------------------------------------------------------------------
# 1. Upgrade C:\dev\chrono-torque-report (Full-width Hero Banner + Cross-links)
# ---------------------------------------------------------------------------
ct_repo = Path(r"C:\dev\chrono-torque-report")
for html_file in ct_repo.glob("*.html"):
    txt = html_file.read_text(encoding="utf-8")
    # Fix .hero-banner-wrap img to stretch 100% edge-to-edge across the frame
    old_css = """  .hero-banner-wrap img {
    width: 100%;
    max-height: 340px;
    object-fit: contain;
    display: block;
  }"""
    new_css = """  .hero-banner-wrap img {
    width: 100%;
    height: auto;
    object-fit: cover;
    display: block;
  }"""
    if old_css in txt:
        txt = txt.replace(old_css, new_css)
    elif old_css.replace("\n", "\r\n") in txt:
        txt = txt.replace(old_css.replace("\n", "\r\n"), new_css.replace("\n", "\r\n"))

    if html_file.name == "index.html" and "ppdv-chord-sieves-report.vercel.app" not in txt:
        target_btn = '<a href="chrono_torque_public_verifier_sdk.zip" class="btn secondary" download>&#128230; Download 6-Gate Verifier SDK (.zip)</a>'
        replacement_btn = (
            target_btn
            + '\n      <a href="https://ppdv-chord-sieves-report.vercel.app" class="btn secondary" target="_blank" rel="noopener">&#127757; PPDV &times; CHORD-SIEVES 3D World Showcase &rarr;</a>'
            + '\n      <a href="https://chord-sieves-report.vercel.app" class="btn secondary" target="_blank" rel="noopener">&#128301; CHORD-SIEVES v2.4 Portal &rarr;</a>'
            + '\n      <a href="https://bama-cortical-report.vercel.app" class="btn secondary" target="_blank" rel="noopener">&#129504; BAMA v3.1 Portal &rarr;</a>'
        )
        txt = txt.replace(target_btn, replacement_btn)
    html_file.write_text(txt, encoding="utf-8")


# ---------------------------------------------------------------------------
# 2. Upgrade C:\dev\chord-sieves-report\index.html (Interactive Studio + Lightbox)
# ---------------------------------------------------------------------------
cs_repo = Path(r"C:\dev\chord-sieves-report")
cs_index = cs_repo / "index.html"

CS_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CHORD-SIEVES v2.4 — Autonomous Exoplanet Discovery &amp; Interactive Scientific Studio</title>
<style>
  :root {
    --bg: #060a12;
    --panel: #0f172a;
    --panel-alt: #0b1120;
    --border: #1e293b;
    --border-bright: #334155;
    --accent: #10b981;
    --accent-cyan: #06b6d4;
    --accent-gold: #f59e0b;
    --text: #f8fafc;
    --muted: #94a3b8;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: "Inter", "Segoe UI", system-ui, -apple-system, sans-serif;
    background: radial-gradient(circle at 50% 0%, #0f1f38 0%, #060a12 65%);
    color: var(--text);
    line-height: 1.55;
    min-height: 100vh;
  }
  /* Sticky Top Navigation Bar */
  .topbar {
    position: sticky;
    top: 0;
    z-index: 200;
    background: rgba(6, 10, 18, 0.92);
    backdrop-filter: blur(14px);
    border-bottom: 1px solid rgba(6, 182, 212, 0.3);
    padding: 10px 22px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
  }
  .topbar-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 800;
    font-size: 0.95rem;
    color: #fff;
  }
  .topbar-pill {
    background: linear-gradient(135deg, #10b981, #059669);
    color: #042f2e;
    font-weight: 800;
    font-size: 0.72rem;
    padding: 3px 9px;
    border-radius: 6px;
    letter-spacing: 0.05em;
  }
  .topbar-links {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
  }
  header.hero {
    background: linear-gradient(180deg, rgba(15, 23, 42, 0.85) 0%, rgba(6, 10, 18, 0.95) 100%);
    border-bottom: 1px solid var(--border);
    padding: 26px 20px 22px;
    text-align: center;
  }
  .badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-bottom: 12px;
  }
  .badge {
    font-size: 0.73rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 4px 11px;
    border-radius: 999px;
    background: rgba(16, 185, 129, 0.14);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.35);
  }
  .badge.cyan {
    background: rgba(6, 182, 212, 0.14);
    color: #22d3ee;
    border-color: rgba(6, 182, 212, 0.35);
  }
  h1 {
    font-size: clamp(1.35rem, 2.6vw, 2.05rem);
    max-width: 1020px;
    margin: 0 auto 8px;
    font-weight: 800;
    color: #ffffff;
  }
  .subtitle {
    color: var(--muted);
    max-width: 880px;
    margin: 0 auto 16px;
    font-size: 0.93rem;
  }
  .cta-row {
    display: flex;
    flex-wrap: wrap;
    gap: 9px;
    justify-content: center;
  }
  .btn {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 9px 15px;
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.84rem;
    text-decoration: none;
    cursor: pointer;
    border: 1px solid transparent;
    transition: all 0.15s ease;
  }
  .btn:hover { transform: translateY(-1px); opacity: 0.95; }
  .btn-primary { background: #10b981; color: #042f2e; }
  .btn-cyan { background: #06b6d4; color: #083344; }
  .btn-gold { background: linear-gradient(135deg, #f59e0b, #d97706); color: #050811; }
  .btn-outline {
    background: #1e293b;
    color: #e2e8f0;
    border: 1px solid #334155;
  }
  .btn-outline:hover { border-color: var(--accent-cyan); color: #fff; }
  .container {
    max-width: 1340px;
    margin: 0 auto;
    padding: 22px 18px 60px;
  }
  .kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(185px, 1fr));
    gap: 12px;
    margin-bottom: 26px;
  }
  .kpi {
    background: var(--panel);
    border: 1px solid var(--border);
    border-top: 3px solid var(--accent);
    border-radius: 10px;
    padding: 13px;
    text-align: center;
  }
  .kpi .num { font-size: 1.4rem; font-weight: 800; color: #ffffff; }
  .kpi .lbl {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--muted);
    margin-top: 4px;
  }
  .section-hdr {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
    margin: 24px 0 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
  }
  .section-hdr h2 { font-size: 1.22rem; color: #ffffff; }

  /* Clickable Showcase & Folio Cards */
  .showcase-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(520px, 1fr));
    gap: 18px;
    margin-bottom: 30px;
  }
  @media (max-width: 640px) {
    .showcase-grid { grid-template-columns: 1fr; }
  }
  .folio-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 11px;
    overflow: hidden;
    cursor: zoom-in;
    position: relative;
    transition: transform 0.16s ease, border-color 0.16s ease, box-shadow 0.16s ease;
  }
  .folio-card:hover {
    transform: translateY(-2px);
    border-color: var(--accent-cyan);
    box-shadow: 0 12px 32px rgba(6, 182, 212, 0.22);
  }
  .folio-card-hdr {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 9px 14px;
    font-size: 0.8rem;
    font-weight: 700;
    color: #e2e8f0;
    background: var(--panel-alt);
    border-bottom: 1px solid var(--border);
  }
  .zoom-pill {
    font-size: 0.72rem;
    padding: 3px 9px;
    border-radius: 999px;
    background: rgba(6, 182, 212, 0.18);
    color: #22d3ee;
    border: 1px solid rgba(6, 182, 212, 0.4);
    font-weight: 700;
  }
  .folio-card img {
    width: 100%;
    height: auto;
    display: block;
    background: #070b14;
  }
  .folio-card.white-page img {
    background: #ffffff;
  }

  /* Interactive Folio Studio Toolbar */
  .studio-toolbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
    background: var(--panel);
    border: 1px solid var(--border-bright);
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 18px;
  }
  .mode-group {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    background: #070b14;
    padding: 4px;
    border-radius: 9px;
    border: 1px solid var(--border);
  }
  .mode-btn {
    background: transparent;
    color: var(--muted);
    border: none;
    padding: 8px 14px;
    border-radius: 6px;
    font-size: 0.83rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.15s ease;
  }
  .mode-btn:hover { color: #fff; }
  .mode-btn.active {
    background: linear-gradient(135deg, #06b6d4, #0284c7);
    color: #042f2e;
    box-shadow: 0 2px 10px rgba(6, 182, 212, 0.35);
  }
  .reader-controls {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
  }
  .ctrl-btn {
    background: #1e293b;
    color: #f8fafc;
    border: 1px solid #334155;
    padding: 7px 13px;
    border-radius: 7px;
    font-size: 0.82rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.15s ease;
  }
  .ctrl-btn:hover { border-color: var(--accent-cyan); color: #22d3ee; }
  .ctrl-btn.primary {
    background: rgba(16, 185, 129, 0.18);
    border-color: rgba(16, 185, 129, 0.5);
    color: #34d399;
  }
  .page-indicator {
    font-family: "JetBrains Mono", Consolas, monospace;
    font-size: 0.85rem;
    font-weight: 800;
    color: #22d3ee;
    padding: 0 8px;
  }

  /* Mode 1: Interactive Stage + Chapter TOC Reader */
  .stage-workspace {
    display: grid;
    grid-template-columns: 290px 1fr;
    gap: 18px;
    align-items: start;
  }
  @media (max-width: 960px) {
    .stage-workspace { grid-template-columns: 1fr; }
  }
  .toc-sidebar {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px;
    position: sticky;
    top: 68px;
  }
  .toc-hdr {
    font-size: 0.76rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--accent-cyan);
    font-weight: 800;
    margin-bottom: 10px;
    padding-bottom: 6px;
    border-bottom: 1px solid var(--border);
  }
  .toc-item {
    display: flex;
    align-items: flex-start;
    gap: 9px;
    width: 100%;
    text-align: left;
    background: transparent;
    border: 1px solid transparent;
    color: var(--muted);
    padding: 8px 10px;
    border-radius: 8px;
    font-size: 0.8rem;
    cursor: pointer;
    margin-bottom: 4px;
    transition: all 0.14s ease;
  }
  .toc-item:hover {
    background: rgba(30, 41, 59, 0.65);
    color: #fff;
  }
  .toc-item.active {
    background: rgba(6, 182, 212, 0.15);
    border-color: rgba(6, 182, 212, 0.45);
    color: #ffffff;
    font-weight: 700;
  }
  .toc-pnum {
    font-family: "JetBrains Mono", monospace;
    font-size: 0.72rem;
    font-weight: 800;
    padding: 2px 6px;
    border-radius: 4px;
    background: rgba(16, 185, 129, 0.18);
    color: #34d399;
    flex-shrink: 0;
  }
  .stage-canvas {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .stage-bar {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
  }
  .stage-title {
    font-size: 0.98rem;
    font-weight: 800;
    color: #fff;
  }
  .stage-spread {
    display: grid;
    grid-template-columns: 1fr;
    gap: 16px;
    width: 100%;
    max-width: 880px;
    margin: 0 auto;
  }
  .stage-spread.two-up {
    grid-template-columns: 1fr 1fr;
    max-width: 100%;
  }
  @media (max-width: 800px) {
    .stage-spread.two-up { grid-template-columns: 1fr; }
  }
  .stage-page-wrap {
    position: relative;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 16px 44px rgba(0, 0, 0, 0.7);
    border: 1px solid rgba(148, 163, 184, 0.3);
    cursor: zoom-in;
    background: #fff;
  }
  .stage-page-wrap img {
    width: 100%;
    height: auto;
    display: block;
  }
  .stage-zoom-hint {
    position: absolute;
    bottom: 12px;
    right: 12px;
    background: rgba(6, 10, 18, 0.88);
    color: #22d3ee;
    border: 1px solid rgba(6, 182, 212, 0.5);
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 0.76rem;
    font-weight: 700;
    pointer-events: none;
    box-shadow: 0 4px 14px rgba(0,0,0,0.5);
  }

  /* Mode 2: 2-Column All-Pages Grid */
  .folio-grid {
    display: none;
    grid-template-columns: repeat(auto-fit, minmax(480px, 1fr));
    gap: 18px;
  }
  @media (max-width: 560px) {
    .folio-grid { grid-template-columns: 1fr; }
  }

  /* Mode 3: Embedded Native PDF Viewer */
  .pdf-embed-wrap {
    display: none;
    width: 100%;
    height: 84vh;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--border-bright);
    background: #0b1120;
  }
  .pdf-embed-wrap iframe {
    width: 100%;
    height: 100%;
    border: none;
  }

  /* Fullscreen High-DPI Lightbox Modal */
  .lightbox-overlay {
    display: none;
    position: fixed;
    inset: 0;
    z-index: 9999;
    background: rgba(3, 6, 12, 0.94);
    backdrop-filter: blur(10px);
    flex-direction: column;
  }
  .lightbox-overlay.open {
    display: flex;
  }
  .lightbox-topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 22px;
    background: rgba(15, 23, 42, 0.95);
    border-bottom: 1px solid var(--border-bright);
    flex-wrap: wrap;
    gap: 10px;
  }
  .lightbox-title {
    font-size: 0.95rem;
    font-weight: 800;
    color: #fff;
  }
  .lightbox-actions {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
  }
  .lightbox-body {
    flex: 1;
    overflow: auto;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding: 20px;
  }
  .lightbox-body img {
    max-width: 94vw;
    height: auto;
    border-radius: 6px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.85);
    background: #fff;
    transition: width 0.15s ease, max-width 0.15s ease;
  }
  .lightbox-body img.zoomed-150 {
    max-width: none;
    width: 1350px;
  }
  .lightbox-body img.zoomed-200 {
    max-width: none;
    width: 1850px;
  }

  footer {
    text-align: center;
    padding: 28px 16px;
    border-top: 1px solid var(--border);
    color: var(--muted);
    font-size: 0.84rem;
  }
</style>
</head>
<body>

<nav class="topbar">
  <div class="topbar-brand">
    <span class="topbar-pill">CHORD-SIEVES v2.4</span>
    <span>Metaphy LLC Autonomous Exoplanet Observatory &amp; Ephemeris Self-Audit Studio</span>
  </div>
  <div class="topbar-links">
    <a class="btn btn-cyan" style="padding:6px 12px;font-size:0.78rem" href="https://ppdv-chord-sieves-report.vercel.app" target="_blank" rel="noopener">&#127757; PPDV &times; CHORD-SIEVES 3D World Showcase &rarr;</a>
    <a class="btn btn-outline" style="padding:6px 12px;font-size:0.78rem" href="https://bama-cortical-report.vercel.app" target="_blank" rel="noopener">BAMA v3.1 Portal &rarr;</a>
    <a class="btn btn-outline" style="padding:6px 12px;font-size:0.78rem" href="https://chrono-torque-report.vercel.app" target="_blank" rel="noopener">CHRONO-TORQUE v2.0 Portal &rarr;</a>
  </div>
</nav>

<header class="hero">
  <div class="badge-row">
    <span class="badge">U.S. PATENT PENDING (64/180,009)</span>
    <span class="badge cyan">845 PRIMARY RECORDS (386 TIC HOSTS &bull; 390 UNION)</span>
    <span class="badge">2,170 / 4,957 (43.78%) ON-TIME &bull; 0 WRONG IN 2,592 COVERED</span>
    <span class="badge cyan">80-KERNEL QEG5 ASTRO-PRIME ARENA (20,480 B)</span>
  </div>
  <h1>CHORD-SIEVES v2.4: Autonomous Exoplanet Discovery, 3-Zone Quadratic Flank-Bridge Vetting &amp; Continuous TESS Ephemeris Self-Audit Engine</h1>
  <p class="subtitle">
    Principal Architect: <strong>Logan Smith</strong> (Metaphy LLC) &bull; Co-Designed with <code>@AURA</code> (Gemini 4 Argon), <code>@LUMEN</code> (Gemma 4 E4B), &amp; <code>@BBB</code> (Qwen 3.5 9B) &bull; Peer-Reviewed by <code>@GROK</code>
  </p>
  <div class="cta-row">
    <a class="btn btn-primary" href="/BAMA_CHORD_SIEVES_Exoplanet_Report.pdf" download>&#128196; Download 10-Page Scientific Report (PDF)</a>
    <a class="btn btn-cyan" href="/chord_sieves_public_verifier_sdk.zip" download>&#128230; Download Read-Only Public Verifier SDK (.zip)</a>
    <a class="btn btn-outline" href="/arxiv/chord_sieves_arxiv_preprint.tex" download>Download Two-Column LaTeX Source (.tex)</a>
    <a class="btn btn-gold" href="https://ppdv-chord-sieves-report.vercel.app" target="_blank" rel="noopener">&#10024; PPDV &times; CHORD-SIEVES 3D World Showcase &rarr;</a>
  </div>
</header>

<main class="container">
  <div class="kpi-grid">
    <div class="kpi"><div class="num">845 / 386</div><div class="lbl">Primary Records / TIC Hosts (390 Union)</div></div>
    <div class="kpi"><div class="num">809 / 25 / 11</div><div class="lbl">ExoFOP Cat A / Cat B / Cat C</div></div>
    <div class="kpi"><div class="num">600 (65 &le;1.6R<sub>&oplus;</sub>)</div><div class="lbl">Shirt-Sleeve Cut (0&ndash;35&deg;C)</div></div>
    <div class="kpi"><div class="num">8 (&ge;85%) / 6 KX02</div><div class="lbl">Competing Solutions (3 Host Stars)</div></div>
    <div class="kpi"><div class="num">2,170 / 4,957</div><div class="lbl">On-Time (43.78% | 0 Wrong in 2,592)</div></div>
    <div class="kpi"><div class="num">1,261</div><div class="lbl">Marked Follow-Up Registry Objects</div></div>
  </div>

  <!-- Bidirectional Symbiosis Showcase with Click-to-Fullscreen Plates -->
  <div class="section-hdr">
    <h2>Bidirectional Symbiosis Showcase: <em>Prompting Python Data Visualization</em> (Aleinikov, 2026) &times; CHORD-SIEVES 3D World Pipeline</h2>
    <a class="btn btn-cyan" style="padding:7px 13px;font-size:0.8rem" href="https://ppdv-chord-sieves-report.vercel.app" target="_blank" rel="noopener">Open Full Interactive Showcase Portal &rarr;</a>
  </div>
  <p style="color: var(--muted); font-size: 0.9rem; margin-bottom: 14px;">
    Uniting Aleksei Aleinikov&rsquo;s <em>Prompting Python Data Visualization</em> (Orange Education / AVA&trade;, ISBN <code>978-9349887992</code>; Chapters 14, 15 &amp; 18 Adaptive Hexbin, Bootstrap 95% CI, <code>PngInfo</code> Visualization Passports, and Honesty Linters) with CHORD-SIEVES&rsquo;s <strong>Closed-Loop Spherical (cos &phi;) Pixel-to-Telemetry Feedback Engine</strong> and <strong>3-Zone Local Quadratic Flank Bridge</strong>. <em>Click either 4-panel HD plate below to inspect in Fullscreen High-DPI mode.</em>
  </p>
  <div class="showcase-grid">
    <div class="folio-card" onclick="openCustomLightbox('assets/tic_271478281_08_ppdv_3d_world_plate.png', 'TIC 271478281.08 (ESI 0.984 • +20.8°C / +69.4°F) — 4-Panel PPDV × CHORD-SIEVES Diagnostic Plate')">
      <div class="folio-card-hdr">
        <span>TIC 271478281.08 (ESI 0.984 &bull; +20.8&deg;C / +69.4&deg;F)</span>
        <span class="zoom-pill">&#128269; Click for Fullscreen</span>
      </div>
      <img src="assets/tic_271478281_08_ppdv_3d_world_plate.png" alt="TIC 271478281.08 PPDV x CHORD-SIEVES 4-Panel Plate" loading="eager">
    </div>
    <div class="folio-card" onclick="openCustomLightbox('assets/tic_52005579_04_ppdv_3d_world_plate.png', 'TIC 52005579.04 (ESI 0.978 • +21.5°C / +70.7°F) — 4-Panel PPDV × CHORD-SIEVES Diagnostic Plate')">
      <div class="folio-card-hdr">
        <span>TIC 52005579.04 (ESI 0.978 &bull; +21.5&deg;C / +70.7&deg;F)</span>
        <span class="zoom-pill">&#128269; Click for Fullscreen</span>
      </div>
      <img src="assets/tic_52005579_04_ppdv_3d_world_plate.png" alt="TIC 52005579.04 PPDV x CHORD-SIEVES 4-Panel Plate" loading="eager">
    </div>
  </div>

  <!-- Interactive 10-Page Scientific Folio Studio -->
  <div class="section-hdr">
    <h2>10-Page Print-Exact Scientific Report Studio (Interactive Reader &amp; Fullscreen Zoom)</h2>
    <span style="color: var(--muted); font-size: 0.84rem;">All 4 Public Verifier Gates Passed (SHA-256: <code>c7237583ff...255ba5</code>) &bull; Click any page to enlarge fullscreen</span>
  </div>

  <div class="studio-toolbar">
    <div class="mode-group" role="tablist">
      <button class="mode-btn active" id="btn-mode-stage" onclick="setFolioMode('stage')">&#128214; Interactive Chapter Stage (1-Up / 2-Up)</button>
      <button class="mode-btn" id="btn-mode-grid" onclick="setFolioMode('grid')">&#128450;&#65039; Side-by-Side 10-Page Grid (Click to Enlarge)</button>
      <button class="mode-btn" id="btn-mode-pdf" onclick="setFolioMode('pdf')">&#128196; Native Browser PDF Viewer</button>
    </div>
    <div class="reader-controls" id="stage-controls">
      <button class="ctrl-btn" onclick="stepPage(-1)">&larr; Prev Page</button>
      <span class="page-indicator" id="page-counter-lbl">Page 1 / 10</span>
      <button class="ctrl-btn" onclick="stepPage(1)">Next Page &rarr;</button>
      <button class="ctrl-btn" id="btn-spread-toggle" onclick="toggleSpreadMode()">&#128214; Switch to 2-Page Book Spread</button>
      <button class="ctrl-btn primary" onclick="openPageLightbox(currentPageIdx)">&#128269; Enlarge Fullscreen</button>
    </div>
  </div>

  <!-- MODE 1: Interactive Stage & Chapter TOC Reader -->
  <div class="stage-workspace" id="view-stage">
    <aside class="toc-sidebar">
      <div class="toc-hdr">Report Chapters (Pages 1&ndash;10)</div>
      <div id="toc-list"></div>
    </aside>
    <div class="stage-canvas">
      <div class="stage-bar">
        <div class="stage-title" id="stage-active-title">PAGE 1 &mdash; Abstract, 386 Primary / 390 Union TIC Hosts &amp; KPI Summary</div>
        <div style="display:flex;gap:8px;">
          <button class="ctrl-btn" onclick="openPageLightbox(currentPageIdx)">&#128269; Click Page or Here for Fullscreen Zoom</button>
        </div>
      </div>
      <div class="stage-spread" id="stage-spread-box">
        <div class="stage-page-wrap" onclick="openPageLightbox(currentPageIdx)">
          <img id="stage-img-primary" src="assets/pages/page-1.webp" alt="Report Page 1">
          <span class="stage-zoom-hint">&#128269; Click to Enlarge Fullscreen (High-DPI)</span>
        </div>
        <div class="stage-page-wrap" id="stage-page-secondary" style="display:none;" onclick="openPageLightbox(Math.min(9, currentPageIdx+1))">
          <img id="stage-img-secondary" src="assets/pages/page-2.webp" alt="Report Page 2">
          <span class="stage-zoom-hint">&#128269; Click to Enlarge Fullscreen (High-DPI)</span>
        </div>
      </div>
    </div>
  </div>

  <!-- MODE 2: Side-by-Side 2-Column All-Pages Grid (All Clickable for Fullscreen) -->
  <div class="folio-grid" id="view-grid"></div>

  <!-- MODE 3: Native Browser PDF Viewer -->
  <div class="pdf-embed-wrap" id="view-pdf">
    <iframe src="/BAMA_CHORD_SIEVES_Exoplanet_Report.pdf" title="CHORD-SIEVES 10-Page Scientific Report PDF"></iframe>
  </div>
</main>

<!-- Fullscreen High-DPI Lightbox Modal -->
<div class="lightbox-overlay" id="lightbox-modal" onclick="handleOverlayClick(event)">
  <div class="lightbox-topbar">
    <div class="lightbox-title" id="lb-title">PAGE 1</div>
    <div class="lightbox-actions">
      <button class="ctrl-btn" id="lb-prev-btn" onclick="stepLightbox(-1)">&larr; Prev</button>
      <button class="ctrl-btn" onclick="setLightboxZoom('100')">100% Fit</button>
      <button class="ctrl-btn" onclick="setLightboxZoom('150')">150% Zoom</button>
      <button class="ctrl-btn" onclick="setLightboxZoom('200')">200% Ultra-Zoom</button>
      <button class="ctrl-btn" id="lb-next-btn" onclick="stepLightbox(1)">Next &rarr;</button>
      <a class="ctrl-btn primary" id="lb-download-btn" href="/BAMA_CHORD_SIEVES_Exoplanet_Report.pdf" download>Download PDF &darr;</a>
      <button class="ctrl-btn" style="background:#dc2626;border-color:#ef4444;color:#fff;" onclick="closeLightbox()">&#10005; Close (ESC)</button>
    </div>
  </div>
  <div class="lightbox-body" id="lb-body">
    <img id="lb-img" src="assets/pages/page-1.webp" alt="Fullscreen Preview">
  </div>
</div>

<footer>
  &copy; 2026 Logan Smith (Metaphy LLC) &bull; Protected under U.S. Provisional Patent Application No. 64/180,009 (Confirmation #2200) &bull; All Rights Reserved.
</footer>

<script>
const REPORT_PAGES = [
  { num: 1, src: "assets/pages/page-1.webp", title: "Abstract, 386 Primary / 390 Union TIC Hosts & KPI Summary" },
  { num: 2, src: "assets/pages/page-2.webp", title: "80-Kernel BAMA Astro-Prime QEG5 Cartridge (20,480 B)" },
  { num: 3, src: "assets/pages/page-3.webp", title: "11-Stage Autonomous CHORD-SIEVES Discovery Cascade" },
  { num: 4, src: "assets/pages/page-4.webp", title: "3-Zone Quadratic Flank Bridge & Stage 3.5 Vetting Math" },
  { num: 5, src: "assets/pages/page-5.webp", title: "845-Record Discovery Catalog & 1,261-Object Marked Registry" },
  { num: 6, src: "assets/pages/page-6.webp", title: "Pipeline Priors, KX02 Ceiling & Mutual Hill Stability Audit" },
  { num: 7, src: "assets/pages/page-7.webp", title: "Self-Audit Ledger v2.4.0 (2,170 / 4,957 On-Time) & Catchup" },
  { num: 8, src: "assets/pages/page-8.webp", title: "Multi-Agent Co-Design & @GROK Peer-Review Resolution" },
  { num: 9, src: "assets/pages/page-9.webp", title: "Read-Only Public Verifier SDK & Direct Recount Receipt" },
  { num: 10, src: "assets/pages/page-10.webp", title: "Conclusions, Period-Alias Disambiguation & Patent 64/180,009" }
];

let currentPageIdx = 0;
let isTwoUpSpread = false;
let lbMode = "pages"; // "pages" | "custom"
let lbPageIdx = 0;

function initStudio() {
  // Build TOC
  const tocEl = document.getElementById("toc-list");
  tocEl.innerHTML = REPORT_PAGES.map((p, idx) => `
    <button class="toc-item ${idx === 0 ? 'active' : ''}" id="toc-btn-${idx}" onclick="selectStagePage(${idx})">
      <span class="toc-pnum">P${p.num}</span>
      <span>${p.title}</span>
    </button>
  `).join("");

  // Build 2-Column Grid with click-to-enlarge
  const gridEl = document.getElementById("view-grid");
  gridEl.innerHTML = REPORT_PAGES.map((p, idx) => `
    <div class="folio-card white-page" onclick="openPageLightbox(${idx})">
      <div class="folio-card-hdr">
        <span>PAGE ${p.num} &mdash; ${p.title}</span>
        <span class="zoom-pill">&#128269; Click to Enlarge</span>
      </div>
      <img src="${p.src}" alt="Page ${p.num}" loading="lazy">
    </div>
  `).join("");

  updateStageRender();
}

function selectStagePage(idx) {
  currentPageIdx = Math.max(0, Math.min(REPORT_PAGES.length - 1, idx));
  updateStageRender();
}

function stepPage(delta) {
  const step = isTwoUpSpread ? delta * 2 : delta;
  currentPageIdx = Math.max(0, Math.min(REPORT_PAGES.length - 1, currentPageIdx + step));
  updateStageRender();
}

function toggleSpreadMode() {
  isTwoUpSpread = !isTwoUpSpread;
  const btn = document.getElementById("btn-spread-toggle");
  const spreadBox = document.getElementById("stage-spread-box");
  const secWrap = document.getElementById("stage-page-secondary");
  if (isTwoUpSpread) {
    spreadBox.classList.add("two-up");
    secWrap.style.display = "block";
    btn.innerHTML = "&#128196; Switch to 1-Page Large Reader";
  } else {
    spreadBox.classList.remove("two-up");
    secWrap.style.display = "none";
    btn.innerHTML = "&#128214; Switch to 2-Page Book Spread";
  }
  updateStageRender();
}

function updateStageRender() {
  const p1 = REPORT_PAGES[currentPageIdx];
  document.getElementById("stage-img-primary").src = p1.src;
  if (isTwoUpSpread && currentPageIdx + 1 < REPORT_PAGES.length) {
    const p2 = REPORT_PAGES[currentPageIdx + 1];
    document.getElementById("stage-page-secondary").style.display = "block";
    document.getElementById("stage-img-secondary").src = p2.src;
    document.getElementById("page-counter-lbl").textContent = `Pages ${p1.num}–${p2.num} / 10`;
    document.getElementById("stage-active-title").textContent = `PAGES ${p1.num}–${p2.num} — ${p1.title} • ${p2.title}`;
  } else {
    if (isTwoUpSpread) {
      document.getElementById("stage-page-secondary").style.display = "none";
    }
    document.getElementById("page-counter-lbl").textContent = `Page ${p1.num} / 10`;
    document.getElementById("stage-active-title").textContent = `PAGE ${p1.num} — ${p1.title}`;
  }
  REPORT_PAGES.forEach((_, idx) => {
    const btn = document.getElementById(`toc-btn-${idx}`);
    if (btn) {
      const active = idx === currentPageIdx || (isTwoUpSpread && idx === currentPageIdx + 1);
      btn.classList.toggle("active", active);
    }
  });
}

function setFolioMode(mode) {
  document.getElementById("btn-mode-stage").classList.toggle("active", mode === "stage");
  document.getElementById("btn-mode-grid").classList.toggle("active", mode === "grid");
  document.getElementById("btn-mode-pdf").classList.toggle("active", mode === "pdf");

  document.getElementById("view-stage").style.display = mode === "stage" ? "grid" : "none";
  document.getElementById("stage-controls").style.display = mode === "stage" ? "flex" : "none";
  document.getElementById("view-grid").style.display = mode === "grid" ? "grid" : "none";
  document.getElementById("view-pdf").style.display = mode === "pdf" ? "block" : "none";
}

function openPageLightbox(idx) {
  lbMode = "pages";
  lbPageIdx = Math.max(0, Math.min(REPORT_PAGES.length - 1, idx));
  renderLightbox();
  document.getElementById("lightbox-modal").classList.add("open");
}

function openCustomLightbox(src, title) {
  lbMode = "custom";
  const img = document.getElementById("lb-img");
  img.src = src;
  img.style.background = "#070b14";
  document.getElementById("lb-title").textContent = title;
  document.getElementById("lb-prev-btn").style.display = "none";
  document.getElementById("lb-next-btn").style.display = "none";
  document.getElementById("lb-download-btn").href = src;
  document.getElementById("lightbox-modal").classList.add("open");
}

function renderLightbox() {
  const p = REPORT_PAGES[lbPageIdx];
  const img = document.getElementById("lb-img");
  img.src = p.src;
  img.style.background = "#ffffff";
  document.getElementById("lb-title").textContent = `PAGE ${p.num} OF 10 — ${p.title}`;
  document.getElementById("lb-prev-btn").style.display = "inline-flex";
  document.getElementById("lb-next-btn").style.display = "inline-flex";
  document.getElementById("lb-download-btn").href = "/BAMA_CHORD_SIEVES_Exoplanet_Report.pdf";
}

function stepLightbox(delta) {
  if (lbMode !== "pages") return;
  lbPageIdx = (lbPageIdx + delta + REPORT_PAGES.length) % REPORT_PAGES.length;
  renderLightbox();
}

function setLightboxZoom(level) {
  const img = document.getElementById("lb-img");
  img.classList.remove("zoomed-150", "zoomed-200");
  if (level === "150") img.classList.add("zoomed-150");
  if (level === "200") img.classList.add("zoomed-200");
}

function closeLightbox() {
  document.getElementById("lightbox-modal").classList.remove("open");
}

function handleOverlayClick(e) {
  if (e.target.id === "lightbox-modal" || e.target.id === "lb-body") {
    closeLightbox();
  }
}

document.addEventListener("keydown", (e) => {
  const modalOpen = document.getElementById("lightbox-modal").classList.contains("open");
  if (modalOpen) {
    if (e.key === "Escape") closeLightbox();
    if (e.key === "ArrowRight") stepLightbox(1);
    if (e.key === "ArrowLeft") stepLightbox(-1);
  } else {
    if (e.key === "ArrowRight") stepPage(1);
    if (e.key === "ArrowLeft") stepPage(-1);
  }
});

initStudio();
</script>

</body>
</html>
"""
cs_index.write_text(CS_HTML, encoding="utf-8")


# ---------------------------------------------------------------------------
# 3. Cross-link C:\dev\bama-cortical-report\index.html
# ---------------------------------------------------------------------------
bama_index = Path(r"C:\dev\bama-cortical-report\index.html")
bama_txt = bama_index.read_text(encoding="utf-8")
if "ppdv-chord-sieves-report.vercel.app" not in bama_txt:
    old_top_action = '<a class="btn-pdf primary" href="/BAMA_Cortical_Amplification_Report.pdf" download="BAMA_Cortical_Amplification_Report.pdf">Download PDF &darr;</a>'
    new_top_action = (
        old_top_action
        + '\n    <a class="btn-pdf outline" href="https://chord-sieves-report.vercel.app" target="_blank" rel="noopener">CHORD-SIEVES &nearr;</a>'
        + '\n    <a class="btn-pdf outline" href="https://chrono-torque-report.vercel.app" target="_blank" rel="noopener">CHRONO-TORQUE &nearr;</a>'
        + '\n    <a class="btn-pdf outline" style="border-color:#C9A84C;color:#C9A84C;" href="https://ppdv-chord-sieves-report.vercel.app" target="_blank" rel="noopener">PPDV &times; 3D World Showcase &nearr;</a>'
    )
    bama_txt = bama_txt.replace(old_top_action, new_top_action)
    bama_index.write_text(bama_txt, encoding="utf-8")


# ---------------------------------------------------------------------------
# 4. Render Headless Edge Previews for Visual Self-Inspection (K61 Gate)
# ---------------------------------------------------------------------------
out_dir = Path(r"C:\Users\logan\.gemini\antigravity-cli\brain\223437e1-5a82-461a-bcd8-f1a694efcf5a")
ct_preview = out_dir / "chrono_torque_full_banner_preview.png"
cs_preview = out_dir / "chord_sieves_interactive_studio_preview.png"

subprocess.run(
    [EDGE, "--headless=new", "--disable-gpu", "--window-size=1440,1200", f"--screenshot={ct_preview}", (ct_repo / "index.html").as_uri()],
    check=True,
)
subprocess.run(
    [EDGE, "--headless=new", "--disable-gpu", "--window-size=1440,1650", f"--screenshot={cs_preview}", cs_index.as_uri()],
    check=True,
)
print(f"[OK] Rendered Previews: CT={ct_preview.stat().st_size:,} B | CS={cs_preview.stat().st_size:,} B")
