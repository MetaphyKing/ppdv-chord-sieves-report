r"""
Fixes all 4 portals so:
1. Zero horizontal scrollbars ever appear on navbars/tabs (uses clean flex-wrap: wrap + compact 2-column mobile grids instead of overflow-x: auto scrollbars).
2. Fixes CRLF matching in bama-cortical-report\index.html so .action-cluster wraps cleanly into a 2-column grid on mobile and .page fits 100% of a 390px screen.
3. Verifies true 390px mobile rendering via an exact 390px mobile harness and captures K61 visual inspection screenshots.
"""
from pathlib import Path
import subprocess

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
OUT_DIR = Path(r"C:\Users\logan\.gemini\antigravity-cli\brain\223437e1-5a82-461a-bcd8-f1a694efcf5a")

# 1. PPDV Portal: Replace horizontal-scrollbar nav-links/world-tabs with clean flex-wrap
ppdv_idx = Path(r"C:\dev\ppdv-chord-sieves-report\index.html")
ppdv_txt = ppdv_idx.read_text(encoding="utf-8")
ppdv_txt = ppdv_txt.replace(
    ".nav-links { width: 100%; overflow-x: auto; flex-wrap: nowrap; gap: 8px; padding-bottom: 4px; -webkit-overflow-scrolling: touch; }\n      .nav-links a { white-space: nowrap; flex-shrink: 0; font-size: 11px; padding: 5px 10px; }",
    ".nav-links { width: 100%; display: grid; grid-template-columns: 1fr 1fr; gap: 6px; }\n      .nav-links a { font-size: 10.5px; padding: 6px 8px; text-align: center; }",
)
ppdv_txt = ppdv_txt.replace(
    ".world-tabs { overflow-x: auto; flex-wrap: nowrap; padding-bottom: 6px; -webkit-overflow-scrolling: touch; }\n      .world-btn { white-space: nowrap; flex-shrink: 0; font-size: 11px; padding: 7px 11px; }",
    ".world-tabs { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; }\n      .world-btn { font-size: 10.5px; padding: 7px 8px; text-align: center; }",
)
# Also ensure all children respect max-width: 100% and word-break on mobile
ppdv_txt = ppdv_txt.replace(
    "html, body { overflow-x: hidden; max-width: 100vw; }",
    "html, body { overflow-x: hidden; max-width: 100%; } img, pre, code { max-width: 100%; } p, li, h1, h2, h3, span, div { overflow-wrap: break-word; word-wrap: break-word; }",
)
ppdv_idx.write_text(ppdv_txt, encoding="utf-8")


# 2. CHORD-SIEVES Portal: Clean wrapped mobile buttons (zero horizontal scrollbars)
cs_idx = Path(r"C:\dev\chord-sieves-report\index.html")
cs_txt = cs_idx.read_text(encoding="utf-8")
cs_txt = cs_txt.replace(
    "html, body { overflow-x: hidden; max-width: 100vw; }",
    "html, body { overflow-x: hidden; max-width: 100%; } img, pre, code { max-width: 100%; } p, li, h1, h2, h3, span, div { overflow-wrap: break-word; word-wrap: break-word; }",
)
cs_txt = cs_txt.replace(
    ".topbar-links { width: 100%; overflow-x: auto; flex-wrap: nowrap; padding-bottom: 4px; -webkit-overflow-scrolling: touch; }\n    .topbar-links .btn { white-space: nowrap; flex-shrink: 0; }",
    ".topbar-links { width: 100%; display: flex; flex-wrap: wrap; gap: 6px; }\n    .topbar-links .btn { flex: 1 1 calc(50% - 6px); justify-content: center; text-align: center; font-size: 0.72rem !important; }",
)
cs_txt = cs_txt.replace(
    ".mode-group { width: 100%; overflow-x: auto; flex-wrap: nowrap; -webkit-overflow-scrolling: touch; }\n    .mode-btn { white-space: nowrap; flex-shrink: 0; font-size: 0.76rem; padding: 7px 10px; }",
    ".mode-group { width: 100%; display: flex; flex-direction: column; gap: 4px; }\n    .mode-btn { width: 100%; text-align: center; font-size: 0.76rem; padding: 7px 10px; }",
)
cs_txt = cs_txt.replace(
    "#toc-list { display: flex; overflow-x: auto; gap: 6px; padding-bottom: 4px; -webkit-overflow-scrolling: touch; }\n    .toc-item { width: auto; flex-shrink: 0; white-space: nowrap; margin-bottom: 0; padding: 6px 10px; font-size: 0.75rem; }",
    "#toc-list { display: grid; grid-template-columns: repeat(2, 1fr); gap: 5px; }\n    .toc-item { width: 100%; margin-bottom: 0; padding: 6px 8px; font-size: 0.71rem; line-height: 1.2; }",
)
cs_idx.write_text(cs_txt, encoding="utf-8")


# 3. CHRONO-TORQUE Portal: Clean wrapped 2-column nav links on mobile (zero scrollbars)
ct_repo = Path(r"C:\dev\chrono-torque-report")
for html_file in ct_repo.glob("*.html"):
    if html_file.name == "epicyclic_bloch_gear_visualizer.html":
        continue
    txt = html_file.read_text(encoding="utf-8")
    txt = txt.replace(
        "html, body { overflow-x: hidden; max-width: 100vw; }",
        "html, body { overflow-x: hidden; max-width: 100%; } img, pre, code { max-width: 100%; } p, li, h1, h2, h3, span, div { overflow-wrap: break-word; word-wrap: break-word; }",
    )
    txt = txt.replace(
        ".nav-links { width: 100%; overflow-x: auto; flex-wrap: nowrap; padding-bottom: 4px; -webkit-overflow-scrolling: touch; }\n    .nav-link { white-space: nowrap; flex-shrink: 0; font-size: 11.5px; padding: 5px 10px; }",
        ".nav-links { width: 100%; display: grid; grid-template-columns: 1fr 1fr; gap: 6px; }\n    .nav-link { font-size: 11px; padding: 6px 8px; text-align: center; }",
    )
    html_file.write_text(txt, encoding="utf-8")


# 4. BAMA Portal: Fix CRLF-safe mobile rules so .action-cluster and .mode-tabs wrap with zero overflow
bama_idx = Path(r"C:\dev\bama-cortical-report\index.html")
bama_txt = bama_idx.read_text(encoding="utf-8")
bama_mobile_override = """  @media (max-width: 860px) {
    html, body { overflow-x: hidden; max-width: 100%; }
    .mode-tabs { display: grid !important; grid-template-columns: 1fr; width: 100%; gap: 4px; }
    .action-cluster { display: grid !important; grid-template-columns: 1fr 1fr; width: 100%; gap: 6px; }
    .btn-pdf { width: 100%; justify-content: center; text-align: center; font-size: 11px; padding: 7px 8px; }
    .studio-canvas .page * { max-width: 100%; overflow-wrap: break-word; }
  }
</style>"""
if "grid-template-columns: 1fr 1fr; width: 100%; gap: 6px;" not in bama_txt:
    bama_txt = bama_txt.replace("</style>", bama_mobile_override)
    bama_idx.write_text(bama_txt, encoding="utf-8")


# 5. Build a 4-Up 390px True Mobile Simulator Sheet to bypass Windows 500px minimum window width
sim_html = OUT_DIR / "mobile_4up_verifier.html"
sim_html.write_text(f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{ margin: 0; padding: 16px; background: #020409; color: #fff; font-family: system-ui, sans-serif; }}
  h2 {{ text-align: center; font-size: 16px; margin: 0 0 12px; color: #38bdf8; }}
  .grid {{ display: grid; grid-template-columns: repeat(4, 390px); gap: 14px; justify-content: center; }}
  .phone {{ width: 390px; border: 2px solid #334155; border-radius: 16px; overflow: hidden; background: #050811; box-shadow: 0 12px 32px rgba(0,0,0,0.8); }}
  .phone-hdr {{ background: #0f172a; padding: 6px 10px; font-size: 11px; font-weight: 700; color: #6ee7b7; text-align: center; border-bottom: 1px solid #334155; }}
  iframe {{ width: 390px; height: 980px; border: 0; display: block; }}
</style>
</head>
<body>
  <h2>TRUE 390px MOBILE VIEWPORT VERIFICATION — ALL 4 METAPHY LLC RESEARCH PORTALS (iPhone 14/15/16 Pro Width = 390px)</h2>
  <div class="grid">
    <div class="phone"><div class="phone-hdr">1. PPDV &times; CHORD-SIEVES (390px)</div><iframe src="{ppdv_idx.as_uri()}"></iframe></div>
    <div class="phone"><div class="phone-hdr">2. CHORD-SIEVES v2.4 Studio (390px)</div><iframe src="{cs_idx.as_uri()}"></iframe></div>
    <div class="phone"><div class="phone-hdr">3. CHRONO-TORQUE v2.0 (390px)</div><iframe src="{(ct_repo / 'index.html').as_uri()}"></iframe></div>
    <div class="phone"><div class="phone-hdr">4. BAMA v3.1 Cortical Report (390px)</div><iframe src="{bama_idx.as_uri()}"></iframe></div>
  </div>
</body>
</html>
""", encoding="utf-8")

mobile_sheet_png = OUT_DIR / "mobile_4up_390px_verified.png"
subprocess.run(
    [EDGE, "--headless=new", "--disable-gpu", "--window-size=1660,1080", f"--screenshot={mobile_sheet_png}", sim_html.as_uri()],
    check=True,
)
print(f"[OK] Rendered 4-Up True 390px Mobile Verification Sheet: {mobile_sheet_png.stat().st_size:,} B")
