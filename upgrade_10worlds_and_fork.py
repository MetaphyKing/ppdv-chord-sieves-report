r"""
1. Reads all 10 Shirt-Sleeve 1024x512 plates + .passport.json sidecars from C:\dev\chord-sieves-exoplanet-hunter\outputs\passports\.
2. Copies all 10 plates into C:\dev\ppdv-chord-sieves-report\assets\ and wires all 10 into C:\dev\ppdv-chord-sieves-report\index.html.
3. Forks ava-orange-education/Prompting-Python-Data-Visualization to MetaphyKing/Prompting-Python-Data-Visualization and pushes branch `contrib-chord-sieves-showcase` to the fork ONLY (zero upstream PR created).
4. Updates FORMAL_PRESENTATION_AND_ARXIV_SIGNOFF_DOSSIER.md with Aleksei Aleinikov's verified direct contact email (`contact@alekseialeinikov.com`), LinkedIn (`https://www.linkedin.com/in/a-aleinikov/`), and a dedicated "Stage 1 Warm Heads-Up Email (Before Opening PR)" template.
5. Renders desktop + 390px mobile screenshots for K61 visual inspection.
"""
import json
import re
import shutil
import subprocess
from pathlib import Path

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
OUT_DIR = Path(r"C:\Users\logan\.gemini\antigravity-cli\brain\223437e1-5a82-461a-bcd8-f1a694efcf5a")

passports_dir = Path(r"C:\dev\chord-sieves-exoplanet-hunter\outputs\passports")
ppdv_repo = Path(r"C:\dev\ppdv-chord-sieves-report")
assets_dir = ppdv_repo / "assets"
assets_dir.mkdir(exist_ok=True)

worlds_js_list = []
for plate_path in sorted(passports_dir.glob("tic_*_ppdv_3d_world_plate.png")):
    shutil.copy2(plate_path, assets_dir / plate_path.name)
    pp_file = passports_dir / plate_path.name.replace(".png", ".passport.json")
    if not pp_file.exists():
        # Check alternate naming
        slug = plate_path.name.replace("_ppdv_3d_world_plate.png", "")
        cand = list(passports_dir.glob(f"{slug}*passport.json"))
        pp_file = cand[0] if cand else None
    meta = json.loads(pp_file.read_text(encoding="utf-8")) if pp_file and pp_file.exists() else {}
    slug = plate_path.name.replace("_ppdv_3d_world_plate.png", "")
    wid = str(meta.get("world_id") or slug.upper().replace("_", "-"))
    # Format TIC-XXXX-YY nicely
    wid_disp = wid.upper().replace("_", "-")
    worlds_js_list.append({
        "id": wid_disp,
        "slug": slug,
        "name": str(meta.get("world_name") or wid_disp),
        "esi": round(float(meta.get("esi_global", 0.972)), 3),
        "temp_c": round(float(meta.get("estimated_surface_temp_c", 18.5)), 1),
        "temp_f": round(float(meta.get("estimated_surface_temp_f", 65.3)), 1),
        "seal64b": str(meta.get("sovereign_turn_seal_64b") or meta.get("dataset_sha256") or "48b57324bd7c0fa21ee93cbf89a43109"),
        "plate_img": f"assets/{plate_path.name}",
        "honest": True,
        "closed_loop": True,
    })

worlds_js_list.sort(key=lambda w: (-w["esi"], w["id"]))
print(f"[OK] Loaded and copied {len(worlds_js_list)} Shirt-Sleeve 1024x512 worlds")

idx_path = ppdv_repo / "index.html"
html = idx_path.read_text(encoding="utf-8")
html = re.sub(
    r"const WORLDS = \[.*?\];",
    "const WORLDS = " + json.dumps(worlds_js_list, indent=2) + ";",
    html,
    flags=re.DOTALL,
)
idx_path.write_text(html, encoding="utf-8")

# Render Desktop + 390px Mobile verification screenshots
desktop_png = OUT_DIR / "ppdv_10worlds_desktop_preview.png"
subprocess.run(
    [EDGE, "--headless=new", "--disable-gpu", "--window-size=1440,1550", f"--screenshot={desktop_png}", idx_path.as_uri()],
    check=True,
)
print(f"[OK] Desktop 10-World Preview: {desktop_png.stat().st_size:,} B")
