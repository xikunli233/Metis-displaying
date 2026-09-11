"""
Metis 6000 / 7000 流水线配置展示系统（仅正视图 + 实体尾端部件版）
------------------------------------------------
图片资源目录：assets/images/
命名规则：{img_key}.png
尾端部件：tail_end.png（固定长度 100 mm，位于最左端，不显示参数卡片）
"""

from pathlib import Path
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# =============================================================================
# 全局常量
# =============================================================================
BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / "assets" / "images"
IMG_DIR.mkdir(parents=True, exist_ok=True)

TARGET_WIDTH = 1800
MAX_ANALYZERS = 4
MIN_ANALYZERS = 1

BRAND = "#1E5EB8"
BRAND_DARK = "#0F3D7A"
BRAND_LIGHT = "#E8F1FB"

SEPARATOR_COLOR = (200, 210, 225, 255)

# =============================================================================
# 尾端部件（固定 10 cm，位于最左端，不显示参数卡片）
# =============================================================================
TAIL_MODEL = dict(
    display="尾端模块",
    group="Tail",
    line="Tail End",
    line_cn="尾端",
    L=100,          # 10 cm
    W=350,
    H=800,
    img="tail_end",
    specs={},       # 空，不展示
    show_card=False,
)

# =============================================================================
# 产品数据
# =============================================================================
MODELS = {
    # ---------------- 前处理模块 ----------------
    "SH80": dict(
        display="SH80",
        group="Pre",
        line="Pre-analytical",
        line_cn="前处理",
        L=520, W=926, H=1055,
        img="sh80",
        show_card=True,
        specs={
            "吞吐量": "500 管/小时",
            "尺寸 (L×W×H)": "520 × 926 × 1055 mm",
            "特点": [
                "自动复测",
                "自动条码扫描",
                "实时急诊",
                "实时提示",
            ],
        },
    ),
    "SH80+SHC200": dict(
        display="SH80 + SHC200",
        group="Pre",
        line="Pre-analytical",
        line_cn="前处理",
        L=1200, W=1050, H=1750,
        img="sh80_shc200",
        show_card=True,
        specs={
            "吞吐量": "320 管/小时",
            "尺寸 (L×W×H)": "1200 × 1050 × 1750 mm",
            "离心机（选配）": "最大 80 管/次；3000–4000 rpm；5–20 ℃ 制冷",
            "特点": [
                "自动开盖与丢弃",
                "自动平衡与离心",
            ],
        },
    ),
    "SH600e": dict(
        display="SH600e",
        group="Pre",
        line="Pre-analytical",
        line_cn="前处理",
        L=1170, W=1140, H=1450,
        img="sh600e",
        show_card=True,
        specs={
            "吞吐量": "400 管/小时",
            "尺寸 (L×W×H)": "1170 × 1140 × 1450 mm",
            "离心机": "最大 80 管/次；3000–4000 rpm；5–20 ℃ 制冷",
            "特点": [
                "自动开盖与丢弃",
                "自动平衡与离心",
                "托盘式或倾倒式（选配）",
            ],
        },
    ),
    "SH600": dict(
        display="SH600",
        group="Pre",
        line="Pre-analytical",
        line_cn="前处理",
        L=1170, W=1140, H=1450,
        img="sh600",
        show_card=True,
        specs={
            "吞吐量": "400 管/小时",
            "尺寸 (L×W×H)": "1170 × 1140 × 1450 mm",
            "离心机": "最大 80 管/次；3000–4000 rpm；5–20 ℃ 制冷",
            "特点": [
                "自动开盖、丢弃与再盖帽",
                "自动平衡与离心",
                "托盘式或倾倒式（选配）",
                "视觉识别评估离心状态与血清量",
                "自动复溶 QC（配合 CS 700）",
            ],
        },
    ),

    # ---------------- 分析仪 ----------------
    "MAGICL 6200": dict(
        display="MAGICL 6200",
        group="CLIA",
        line="CLIA",
        line_cn="化学发光",
        L=1100, W=930, H=1200,
        img="magicl_6200",
        show_card=True,
        specs={
            "吞吐量": "400 T/h",
            "尺寸 (L×W×H)": "1100 × 930 × 1200 mm",
            "特点": [
                "最快 12 分钟",
                "4 级分离",
                "205 个孵育位",
                "30 位试剂盘，RFID 读取，4–8 ℃ 冷藏",
                "一次性塑料比色杯 + 供杯器",
                "双耗材系统",
                "涡旋混匀",
                "碰撞 / 液面 / 堵针检测",
            ],
            "耗水量": "20 L/h",
        },
    ),
    "MAGICL 8500": dict(
        display="MAGICL 8500",
        group="CLIA",
        line="CLIA",
        line_cn="化学发光",
        L=1100, W=930, H=1200,
        img="magicl_8500",
        show_card=True,
        specs={
            "吞吐量": "600 T/h",
            "尺寸 (L×W×H)": "1100 × 930 × 1200 mm",
            "特点": [
                "最快 12 分钟",
                "4 级分离",
                "244 个孵育位",
                "30 位试剂盘，RFID 读取，4–8 ℃ 冷藏",
                "一次性塑料比色杯 + 供杯器",
                "双耗材系统",
                "涡旋混匀",
                "碰撞 / 液面 / 堵针检测",
            ],
            "耗水量": "30 L/h",
        },
    ),
    "CA 5700": dict(
        display="CA 5700",
        group="Coagulation",
        line="Coagulation",
        line_cn="凝血",
        L=1100, W=922, H=1340,
        img="ca_5700",
        show_card=True,
        specs={
            "吞吐量": "400 T/h",
            "尺寸 (L×W×H)": "1100 × 922 × 1340 mm",
            "特点": [
                "最快 3 分钟",
                "滤光轮光谱仪",
                "20 个孵育位",
                "40 位试剂盘，条码读取，4–8 ℃ 冷藏",
                "一次性塑料比色杯 + 供杯器",
            ],
        },
    ),
    "CM 1000": dict(
        display="CM 1000",
        group="Chemistry",
        line="Clinical Chemistry",
        line_cn="临床生化",
        L=1100, W=930, H=1200,
        img="cm_1000",
        show_card=True,
        specs={
            "吞吐量": "1000 T/h",
            "尺寸 (L×W×H)": "1100 × 930 × 1200 mm",
            "特点": [
                "最快 12.3 分钟",
                "16 波长全息凹面平场光栅分光",
                "103 位试剂盘，条码读取，4–8 ℃ 冷藏",
                "270 个石英比色杯，干式加热 + 8 阶清洗",
                "碰撞 / 液面 / 堵针检测",
            ],
            "耗水量": "35 L/h",
        },
    ),
    "CM 1600": dict(
        display="CM 1600",
        group="Chemistry",
        line="Clinical Chemistry",
        line_cn="临床生化",
        L=1100, W=930, H=1200,
        img="cm_1600",
        show_card=True,
        specs={
            "吞吐量": "1600 T/h",
            "尺寸 (L×W×H)": "1100 × 930 × 1200 mm",
            "特点": [
                "最快 9.15 分钟",
                "16 波长全息凹面平场光栅分光",
                "107 位试剂盘，条码读取，4–8 ℃ 冷藏",
                "277 个石英比色杯，干式加热 + 8 阶清洗",
                "碰撞 / 液面 / 堵针检测",
            ],
            "耗水量": "67 L/h",
        },
    ),

    # ---------------- 后处理模块 ----------------
    "CS 700": dict(
        display="CS 700",
        group="Post",
        line="Post-analytical",
        line_cn="后处理",
        L=1020, W=1135, H=1450,
        img="cs_700",
        show_card=True,
        specs={
            "容量": "4500 管",
            "吞吐量": "1200 管/小时",
            "尺寸 (L×W×H)": "1020 × 1135 × 1450 mm",
            "特点": ["2–8 ℃ 冷藏"],
        },
    ),
}

PRE_OPTIONS = ["SH80", "SH80+SHC200", "SH600e", "SH600"]
ANALYZER_OPTIONS = ["MAGICL 6200", "MAGICL 8500", "CA 5700", "CM 1000", "CM 1600"]
POST_OPTION = "CS 700"

# 联机顺序（从右到左）：后处理 → 前处理 → 发光 → 血凝 → 生化 → 尾端
ORDER_RTL = ["Post", "Pre", "CLIA", "Coagulation", "Chemistry", "Tail"]

LINE_LABEL_EN = {
    "CLIA": "Immunoassay",
    "Coagulation": "Hemostasis",
    "Clinical Chemistry": "Clinical Chemistry",
}
LINE_LABEL_CN = {
    "CLIA": "免疫",
    "Coagulation": "凝血",
    "Clinical Chemistry": "生化",
}


# =============================================================================
# 字体工具
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
# 标题生成
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


def make_title(pre_key: str, analyzer_keys: list, has_post: bool):
    lines = {MODELS[k]["line"] for k in analyzer_keys}
    uniq_models = set(analyzer_keys)
    n = len(analyzer_keys)

    if len(uniq_models) == 1:
        line = MODELS[analyzer_keys[0]]["line"]
        pl_en = LINE_LABEL_EN[line]
        pl_cn = LINE_LABEL_CN[line]
        if n == 1:
            en = f"Automation Supplement for the Laboratory's {pl_en}"
            cn = f"针对实验室{pl_cn}的自动化补充"
        else:
            en = f"Powerful Automation Supplement for the Laboratory's {pl_en}"
            cn = f"针对实验室{pl_cn}的强力自动化补充"
        return apply_modifier(en, pre_key, has_post), cn

    if lines == {"CLIA", "Clinical Chemistry"}:
        core_en = "Essential Diagnostic Requirements"
        core_cn = "基础诊断需求"
    elif lines == {"CLIA", "Coagulation", "Clinical Chemistry"}:
        core_en = "Comprehensive Diagnostic Requirements"
        core_cn = "全面诊断需求"
    else:
        core_en = "Comprehensive Diagnostic Requirements"
        core_cn = "全面诊断需求"

    en = f"Powerful Automation System to Cover {core_en} from The Lab"
    cn = f"覆盖{core_cn}的强大自动化系统"
    return apply_modifier(en, pre_key, has_post), cn


# =============================================================================
# 图片加载 / 占位图
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
    for name in (f"{model['img']}.png", f"{model['img']}_front.png"):
        path = IMG_DIR / name
        if path.exists():
            try:
                return Image.open(path).convert("RGBA")
            except Exception:
                continue
    return None


# =============================================================================
# 正视图合成（含实体尾端部件）
# =============================================================================
def compose_pipeline(modules):
    """合成正视图，返回 (合成图, 总长m, 最大深度m, 占地面积㎡)。"""
    total_mm = sum(m["L"] for m in modules)
    scale = TARGET_WIDTH / total_mm

    imgs = []
    for m in modules:
        w_px = max(6, int(round(m["L"] * scale)))
        img = _load(m)
        if img is None:
            h_px = max(24, int(round(m["H"] * scale)))
            img = _placeholder(m, w_px, h_px)
        else:
            h_px = max(24, int(round(img.height * w_px / img.width)))
            img = img.resize((w_px, h_px), Image.LANCZOS)
        imgs.append(img)

    total_w = sum(im.width for im in imgs)
    max_h = max(im.height for im in imgs)

    canvas = Image.new("RGBA", (total_w, max_h), (255, 255, 255, 255))
    d = ImageDraw.Draw(canvas)

    x = 0
    for i, im in enumerate(imgs):
        canvas.paste(im, (x, max_h - im.height), im)
        if i < len(imgs) - 1:
            d.line([x + im.width, 0, x + im.width, max_h - 1],
                   fill=SEPARATOR_COLOR, width=1)
        x += im.width

    # ---- 左上角占地面积标签 ----
    len_m = total_mm / 1000.0
    dep_m = max(m["W"] for m in modules) / 1000.0
    area = len_m * dep_m

    badge_font = _font(34)
    badge_text = f"占地面积  {len_m:.2f} m × {dep_m:.2f} m  =  {area:.2f} m²"
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
# 页面配置与样式
# =============================================================================
st.set_page_config(
    page_title="Metis 6000 / 7000 流水线配置器",
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
    .result-title .cn {{
        font-size: 15px; color: #475569; margin-top: 6px;
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
# 侧边栏：配置
# =============================================================================
with st.sidebar:
    st.markdown("### 🔧 流水线配置")
    st.caption("必选：前处理模块 + 至少 1 台分析仪")

    pre_key = st.selectbox(
        "前处理模块",
        PRE_OPTIONS,
        index=0,
        format_func=lambda k: MODELS[k]["display"],
    )

    st.markdown("---")
    n_analyzer = st.slider("分析仪数量", MIN_ANALYZERS, MAX_ANALYZERS, 1, 1)

    analyzer_keys = []
    for i in range(n_analyzer):
        a = st.selectbox(
            f"分析仪 {i + 1}",
            ANALYZER_OPTIONS,
            index=min(i, len(ANALYZER_OPTIONS) - 1),
            key=f"analyzer_{i}",
        )
        analyzer_keys.append(a)

    st.markdown("---")
    cs_available = (pre_key == "SH600")
    has_post = st.checkbox(
        f"后处理模块 {POST_OPTION}",
        disabled=not cs_available,
        help="CS 700 仅可与 SH600 组合使用" if not cs_available else "SH600 + CS 700 已解锁",
    )
    if not cs_available:
        has_post = False
        st.caption("⚠️ CS 700 只能与 SH600 组合")
    else:
        st.caption("✅ 当前配置支持 CS 700")


# =============================================================================
# 组装模块（按联机顺序：从右到左，尾端在最左端）
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

modules_ltr = list(reversed(modules_rtl))

# =============================================================================
# 主区域
# =============================================================================
st.markdown(
    """
    <div class="main-title">
        <h1>Metis 6000 / 7000 自动化流水线配置器</h1>
        <p>选择前处理模块与分析仪组合，实时生成正视图、占地面积与完整参数</p>
    </div>
    """,
    unsafe_allow_html=True,
)

title_en, title_cn = make_title(pre_key, analyzer_keys, has_post)
st.markdown(
    f"""
    <div class="result-title">
        <div class="en">{title_en}</div>
        <div class="cn">{title_cn}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

img, len_m, dep_m, area = compose_pipeline(modules_ltr)

c1, c2, c3 = st.columns(3)
c1.metric("总长度", f"{len_m:.2f} m")
c2.metric("最大深度", f"{dep_m:.2f} m")
c3.metric("占地面积", f"{area:.2f} m²")

st.image(img, use_container_width=True)

st.markdown("#### 📋 模块参数")

# ---- 只对 show_card=True 的模块渲染参数卡片，尾端模块被过滤掉 ----
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
                <div class="line">{m['line_cn']} · {m['line']}</div>
                {rows_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")
st.caption(
    "图片资源目录：assets/images/ ｜ 命名规则：{img_key}.png ｜ "
    "总长度 = 各仪器长度之和 + 尾端 10 cm"
)
