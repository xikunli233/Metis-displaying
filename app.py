"""
Metis 6000 / 7000 Automation Line Configurator
------------------------------------------------
Features:
- Front view only
- No scaling; original image pixels are used directly
- Tail end (10 cm) at the far left, no spec card
- Images directory: assets/images/
- Naming: {img_key}.png
"""

from pathlib import Path
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# =============================================================================
# Global constants
# =============================================================================
BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / "assets" / "images"
IMG_DIR.mkdir(parents=True, exist_ok=True)

MAX_ANALYZERS = 4
MIN_ANALYZERS = 1

BRAND = "#1E5EB8"
BRAND_DARK = "#0F3D7A"
BRAND_LIGHT = "#E8F1FB"

SEPARATOR_COLOR = (200, 210, 225, 255)

# =============================================================================
# Tail end part (fixed 10 cm, far left, no spec card)
# =============================================================================
TAIL_MODEL = dict(
    display="Tail End",
    group="Tail",
    line="Tail End",
    L=100,          # 10 cm
    W=350,
    H=800,
    img="tail_end",
    specs={},
    show_card=False,
)

# =============================================================================
# Product data
# =============================================================================
MODELS = {
    # ---------------- Pre-analytical modules ----------------
    "SH80": dict(
        display="SH80",
        group="Pre",
        line="Pre-analytical",
        L=520, W=926, H=1055,
        img="sh80",
        show_card=True,
        specs={
            "Throughput": "500 tubes/hour",
            "Dimensions (L×W×H)": "520 × 926 × 1055 mm",
            "Features": [
                "Auto-retest",
                "Auto-barcode scanning",
                "Real-time emergency",
                "Real-time prompting",
            ],
        },
    ),
    "SH80+SHC200": dict(
        display="SH80 + SHC200",
        group="Pre",
        line="Pre-analytical",
        L=1200, W=1050, H=1750,
        img="sh80_shc200",
        show_card=True,
        specs={
            "Throughput": "320 tubes/hour",
            "Dimensions (L×W×H)": "1200 × 1050 × 1750 mm",
            "Centrifuge (optional)": "Max 80 tubes/batch; 3000–4000 rpm; 5–20 ℃ refrigeration",
            "Features": [
                "Auto-decapping and disposing",
                "Auto-balancing and centrifuging",
            ],
        },
    ),
    "SH600e": dict(
        display="SH600e",
        group="Pre",
        line="Pre-analytical",
        L=1170, W=1140, H=1450,
        img="sh600e",
        show_card=True,
        specs={
            "Throughput": "400 tubes/hour",
            "Dimensions (L×W×H)": "1170 × 1140 × 1450 mm",
            "Centrifuge": "Max 80 tubes/batch; 3000–4000 rpm; 5–20 ℃ refrigeration",
            "Features": [
                "Auto-decapping and disposing",
                "Auto-balancing and centrifuging",
                "Tray-based or tilt pour (optional)",
            ],
        },
    ),
    "SH600": dict(
        display="SH600",
        group="Pre",
        line="Pre-analytical",
        L=1170, W=1140, H=1450,
        img="sh600",
        show_card=True,
        specs={
            "Throughput": "400 tubes/hour",
            "Dimensions (L×W×H)": "1170 × 1140 × 1450 mm",
            "Centrifuge": "Max 80 tubes/batch; 3000–4000 rpm; 5–20 ℃ refrigeration",
            "Features": [
                "Auto-decapping, disposing and recapping",
                "Auto-balancing and centrifuging",
                "Tray-based or tilt pour (optional)",
                "Visual recognition to evaluate centrifuging status and serum volume",
                "Automatic reconstitution QC (with CS 700)",
            ],
        },
    ),

    # ---------------- Analyzers ----------------
    "MAGICL 6200": dict(
        display="MAGICL 6200",
        group="CLIA",
        line="CLIA",
        L=1100, W=930, H=1200,
        img="magicl_6200",
        show_card=True,
        specs={
            "Throughput": "400 T/h",
            "Dimensions (L×W×H)": "1100 × 930 × 1200 mm",
            "Features": [
                "Fastest 12 min",
                "4-stage separation",
                "205 incubators",
                "30-reagent tray with RFID reader and 4–8 ℃ refrigeration",
                "Disposable plastic cuvettes with feeder",
                "Double consumable system",
                "Vortex mixing",
                "Collision / liquid level / clog detection",
            ],
            "Water Consumption": "20 L/h",
        },
    ),
    "MAGICL 8500": dict(
        display="MAGICL 8500",
        group="CLIA",
        line="CLIA",
        L=1100, W=930, H=1200,
        img="magicl_8500",
        show_card=True,
        specs={
            "Throughput": "600 T/h",
            "Dimensions (L×W×H)": "1100 × 930 × 1200 mm",
            "Features": [
                "Fastest 12 min",
                "4-stage separation",
                "244 incubators",
                "30-reagent tray with RFID reader and 4–8 ℃ refrigeration",
                "Disposable plastic cuvettes with feeder",
                "Double consumable system",
                "Vortex mixing",
                "Collision / liquid level / clog detection",
            ],
            "Water Consumption": "30 L/h",
        },
    ),
    "CA 5700": dict(
        display="CA 5700",
        group="Coagulation",
        line="Coagulation",
        L=1100, W=922, H=1340,
        img="ca_5700",
        show_card=True,
        specs={
            "Throughput": "400 T/h",
            "Dimensions (L×W×H)": "1100 × 922 × 1340 mm",
            "Features": [
                "Fastest 3 min",
                "Filter wheel spectrometer",
                "20 incubators",
                "40-reagent tray with barcode reader and 4–8 ℃ refrigeration",
                "Disposable plastic cuvettes with feeder",
            ],
        },
    ),
    "CM 1000": dict(
        display="CM 1000",
        group="Chemistry",
        line="Clinical Chemistry",
        L=1100, W=930, H=1200,
        img="cm_1000",
        show_card=True,
        specs={
            "Throughput": "1000 T/h",
            "Dimensions (L×W×H)": "1100 × 930 × 1200 mm",
            "Features": [
                "Fastest 12.3 min",
                "16 wavelengths with holographic concave flat field grating splitting",
                "103-reagent tray with barcode reader and 4–8 ℃ refrigeration",
                "270 quartz cuvettes with dry heating and 8-stage washing",
                "Collision / liquid level / clog detection",
            ],
            "Water Consumption": "35 L/h",
        },
    ),
    "CM 1600": dict(
        display="CM 1600",
        group="Chemistry",
        line="Clinical Chemistry",
        L=1100, W=930, H=1200,
        img="cm_1600",
        show_card=True,
        specs={
            "Throughput": "1600 T/h",
            "Dimensions (L×W×H)": "1100 × 930 × 1200 mm",
            "Features": [
                "Fastest 9.15 min",
                "16 wavelengths with holographic concave flat field grating splitting",
                "107-reagent tray with barcode reader and 4–8 ℃ refrigeration",
                "277 quartz cuvettes with dry heating and 8-stage washing",
                "Collision / liquid level / clog detection",
            ],
            "Water Consumption": "67 L/h",
        },
    ),

    # ---------------- Post-analytical module ----------------
    "CS 700": dict(
        display="CS 700",
        group="Post",
        line="Post-analytical",
        L=1020, W=1135, H=1450,
        img="cs_700",
        show_card=True,
        specs={
            "Capacity": "4500 tubes",
            "Throughput": "1200 tubes/hour",
            "Dimensions (L×W×H)": "1020 × 1135 × 1450 mm",
            "Features": ["2–8 ℃ refrigeration"],
        },
    ),
}

PRE_OPTIONS = ["SH80", "SH80+SHC200", "SH600e", "SH600"]
ANALYZER_OPTIONS = ["MAGICL 6200", "MAGICL 8500", "CA 5700", "CM 1000", "CM 1600"]
POST_OPTION = "CS 700"

# Connection order (right to left): Post → Pre → CLIA → Coagulation → Chemistry → Tail
ORDER_RTL = ["Post", "Pre", "CLIA", "Coagulation", "Chemistry", "Tail"]

LINE_LABEL_EN = {
    "CLIA": "Immunoassay",
    "Coagulation": "Hemostasis",
    "Clinical Chemistry": "Clinical Chemistry",
}


# =============================================================================
# Font helper
# =============================================================================
_FONT_CANDIDATES = [
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/msyhbd.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/System/Library/Fonts/PingFang.ttc",
]


def _font(size: int):
    for p in _FONT_CANDIDATES:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


# =============================================================================
# Title generation
# =============================================================================
def apply_modifier(text: str, pre_key: str, has_post: bool) -> str:
    if pre_key in ("SH80", "SH80+SHC200"):
        return text
    if pre_key == "SH600e":
        return text if has_post else text.replace("Powerful", "Intelligent")
    if pre_key == "SH600":
        if has_post:
            return text.replace("Powerful", "Intelligent and Powerful")
        return text.replace("Powerful", "Intelligent")
    return text


def make_title(pre_key: str, analyzer_keys: list, has_post: bool) -> str:
    lines = {MODELS[k]["line"] for k in analyzer_keys}
    uniq_models = set(analyzer_keys)
    n = len(analyzer_keys)

    # ---- Single product line ----
    if len(uniq_models) == 1:
        line = MODELS[analyzer_keys[0]]["line"]
        pl_en = LINE_LABEL_EN[line]
        if n == 1:
            en = f"Automation Supplement for the Laboratory's {pl_en}"
        else:
            en = f"Powerful Automation Supplement for the Laboratory's {pl_en}"
        return apply_modifier(en, pre_key, has_post)

    # ---- Mixed product lines ----
    if lines == {"CLIA", "Clinical Chemistry"}:
        core = "Essential Diagnostic Requirements"
    else:
        core = "Comprehensive Diagnostic Requirements"

    en = f"Powerful Automation System to Cover {core} from The Lab"
    return apply_modifier(en, pre_key, has_post)


# =============================================================================
# Image loading / placeholder
# =============================================================================
def _placeholder(model: dict, w: int, h: int) -> Image.Image:
    img = Image.new("RGBA", (w, h), (232, 241, 251, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w - 1, h - 1], outline=(30, 94, 184, 255), width=max(2, w // 200))
    label = model["display"]
    f = _font(max(11, min(30, w // 8)))
    bbox = d.textbbox((0, 0), label, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((w - tw) / 2, (h - th) / 2 - bbox[1]), label, font=f, fill=(30, 94, 184, 255))
    return img


def _load(model: dict) -> Image.Image | None:
    """Try {img_key}.png, fall back to legacy {img_key}_front.png."""
    for name in (f"{model['img']}.png", f"{model['img']}_front.png"):
        path = IMG_DIR / name
        if path.exists():
            try:
                return Image.open(path).convert("RGBA")
            except Exception:
                continue
    return None


# =============================================================================
# Front-view composition (no scaling, original pixels)
# =============================================================================
def compose_pipeline(modules):
    """Compose the front view without any scaling.
    Returns (canvas, total_length_m, max_depth_m, footprint_m2).
    """
    imgs = []
    for m in modules:
        img = _load(m)
        if img is None:
            img = _placeholder(m, 300, 420)
        imgs.append(img)

    total_w = sum(im.width for im in imgs)
    max_h = max(im.height for im in imgs)

    canvas = Image.new("RGBA", (total_w, max_h), (255, 255, 255, 255))
    d = ImageDraw.Draw(canvas)

    x = 0
    for i, im in enumerate(imgs):
        # Bottom-aligned (equivalent to top-aligned when all images are the same height)
        canvas.paste(im, (x, max_h - im.height), im)
        # 1px separator between units
        if i < len(imgs) - 1:
            d.line([x + im.width, 0, x + im.width, max_h - 1],
                   fill=SEPARATOR_COLOR, width=1)
        x += im.width

    # ---- Footprint badge (top-left corner) ----
    total_mm = sum(m["L"] for m in modules)
    len_m = total_mm / 1000.0
    dep_m = max(m["W"] for m in modules) / 1000.0
    area = len_m * dep_m

    badge_font = _font(34)
    badge_text = f"Footprint  {len_m:.2f} m × {dep_m:.2f} m  =  {area:.2f} m²"
    tb = d.textbbox((0, 0), badge_text, font=badge_font)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    pad = 16
    x0, y0 = 16, 16
    d.rounded_rectangle(
        [x0, y0, x0 + tw + 2 * pad, y0 + th + 2 * pad],
        radius=14, fill=(30, 94, 184, 235),
    )
    d.text((x0 + pad, y0 + pad - tb[1]), badge_text, font=badge_font, fill=(255, 255, 255, 255))

    return canvas, len_m, dep_m, area


# =============================================================================
# Page config & styles
# =============================================================================
st.set_page_config(
    page_title="Metis 6000 / 7000 Line Configurator",
    page_icon="🧪",
    layout="wide",
)

st.markdown(
    f"""
    <style>
    html, body, [class*="css"], .stMarkdown, .stSelectbox, .stSlider,
    button, input, label, textarea {{
        font-family: 'Microsoft YaHei UI', 'Microsoft YaHei', 'PingFang SC',
                     'Helvetica Neue', Arial, sans-serif !important;
    }}

    .main-title {{
        background: linear-gradient(90deg, {BRAND_DARK} 0%, {BRAND} 55%, #3B82F6 100%);
        color: #fff;
        padding: 22px 30px;
        border-radius: 14px;
        margin-bottom: 18px;
        box-shadow: 0 6px 20px rgba(30, 94, 184, .25);
    }}
    .main-title h1 {{
        margin: 0; font-size: 30px; font-weight: 700; letter-spacing: .5px;
    }}
    .main-title p {{
        margin: 6px 0 0 0; font-size: 14px; opacity: .88;
    }}

    .result-title {{
        background: {BRAND_LIGHT};
        border-left: 6px solid {BRAND};
        border-radius: 10px;
        padding: 16px 22px;
        margin: 8px 0 18px 0;
    }}
    .result-title .en {{
        font-size: 22px; font-weight: 700; color: {BRAND_DARK}; line-height: 1.35;
    }}

    .spec-card {{
        background: #fff;
        border: 1px solid #DBEAFE;
        border-top: 4px solid {BRAND};
        border-radius: 10px;
        padding: 12px 14px 14px 14px;
        height: 100%;
        box-shadow: 0 2px 8px rgba(30, 94, 184, .07);
    }}
    .spec-card .name {{
        font-size: 16px; font-weight: 700; color: {BRAND_DARK};
        margin-bottom: 2px; line-height: 1.3;
    }}
    .spec-card .line {{
        display: inline-block; font-size: 11px; color: {BRAND};
        background: {BRAND_LIGHT}; border-radius: 20px;
        padding: 1px 9px; margin-bottom: 9px;
    }}
    .spec-card .row {{
        display: flex; font-size: 12.5px; line-height: 1.65;
        color: #334155; margin-bottom: 2px;
    }}
    .spec-card .k {{
        color: #64748B; flex: 0 0 auto; margin-right: 6px; white-space: nowrap;
    }}
    .spec-card .v {{ flex: 1; word-break: break-word; }}
    .spec-card ul {{
        margin: 4px 0 0 0; padding-left: 15px;
        font-size: 12.5px; color: #334155; line-height: 1.65;
    }}
    .spec-card li {{ margin-bottom: 1px; }}

    section[data-testid="stSidebar"] {{
        background: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# Sidebar: configuration
# =============================================================================
with st.sidebar:
    st.markdown("### 🔧 Pipeline Configuration")
    st.caption("Required: Pre-analytical module + at least 1 analyzer")

    pre_key = st.selectbox(
        "Pre-analytical Module",
        PRE_OPTIONS,
        index=0,
        format_func=lambda k: MODELS[k]["display"],
    )

    st.markdown("---")
    n_analyzer = st.slider("Number of Analyzers", MIN_ANALYZERS, MAX_ANALYZERS, 1, 1)

    analyzer_keys = []
    for i in range(n_analyzer):
        a = st.selectbox(
            f"Analyzer {i + 1}",
            ANALYZER_OPTIONS,
            index=min(i, len(ANALYZER_OPTIONS) - 1),
            key=f"analyzer_{i}",
        )
        analyzer_keys.append(a)

    st.markdown("---")
    cs_available = (pre_key == "SH600")
    has_post = st.checkbox(
        f"Post-analytical Module {POST_OPTION}",
        disabled=not cs_available,
        help="CS 700 can only be combined with SH600"
        if not cs_available else "SH600 + CS 700 unlocked",
    )
    if not cs_available:
        has_post = False
        st.caption("⚠️ CS 700 can only be combined with SH600")
    else:
        st.caption("✅ Current configuration supports CS 700")


# =============================================================================
# Assemble modules (right to left; tail end at far left)
# =============================================================================
groups = {"Post": [], "Pre": [], "CLIA": [], "Coagulation": [], "Chemistry": [], "Tail": []}

if has_post:
    groups["Post"].append(MODELS[POST_OPTION])
groups["Pre"].append(MODELS[pre_key])
for k in analyzer_keys:
    groups[MODELS[k]["group"]].append(MODELS[k])
groups["Tail"].append(TAIL_MODEL)

modules_rtl = []
for g in ORDER_RTL:
    modules_rtl.extend(groups[g])

modules_ltr = list(reversed(modules_rtl))   # canvas left → right

# =============================================================================
# Main area
# =============================================================================
st.markdown(
    """
    <div class="main-title">
        <h1>Metis 6000 / 7000 Automation Line Configurator</h1>
        <p>Select a pre-analytical module and analyzers to generate the front view, footprint and full specifications in real time</p>
    </div>
    """,
    unsafe_allow_html=True,
)

title_en = make_title(pre_key, analyzer_keys, has_post)
st.markdown(
    f"""
    <div class="result-title">
        <div class="en">{title_en}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

img, len_m, dep_m, area = compose_pipeline(modules_ltr)

c1, c2, c3 = st.columns(3)
c1.metric("Total Length", f"{len_m:.2f} m")
c2.metric("Max Depth", f"{dep_m:.2f} m")
c3.metric("Footprint", f"{area:.2f} m²")

st.image(img, use_container_width=True)

st.markdown("#### 📋 Module Specifications")

# ---- Render spec cards only for modules with show_card=True ----
card_modules = [m for m in modules_ltr if m.get("show_card", True)]
weights = [m["L"] for m in card_modules]
cols = st.columns(weights, gap="small")

for col, m in zip(cols, card_modules):
    with col:
        rows_html = ""
        for k, v in m["specs"].items():
            if isinstance(v, list):
                items = "".join(f"<li>{x}</li>" for x in v)
                rows_html += (
                    f'<div class="row"><span class="k">{k}</span>'
                    f'<span class="v"></span></div><ul>{items}</ul>'
                )
            else:
                rows_html += (
                    f'<div class="row"><span class="k">{k}</span>'
                    f'<span class="v">{v}</span></div>'
                )

        st.markdown(
            f"""
            <div class="spec-card">
                <div class="name">{m['display']}</div>
                <div class="line">{m['line']}</div>
                {rows_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")
st.caption(
    "Images directory: assets/images/  |  Naming: {img_key}.png  |  "
    "Total length = sum of unit lengths + 10 cm tail end  |  Composite view is not scaled"
)
