"""
scripts/compose_figures.py
Generate composite figures for the report by stitching existing PNGs.
Uses Pillow (PIL) — no re-rendering of charts needed.
"""

import os
from PIL import Image

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLOTS = os.path.join(BASE, "plots")
OUT = os.path.join(PLOTS, "composites")
os.makedirs(OUT, exist_ok=True)


def load(subdir, name):
    path = os.path.join(PLOTS, subdir, name)
    return Image.open(path)


def compose_grid(images, cols, gap=30, bg=(255, 255, 255)):
    """Arrange images in a grid with `cols` columns. All images resized to match."""
    # Resize all to same dimensions (use first image as reference)
    ref_w, ref_h = images[0].size
    resized = []
    for img in images:
        resized.append(img.resize((ref_w, ref_h), Image.LANCZOS))

    rows = (len(resized) + cols - 1) // cols
    canvas_w = cols * ref_w + (cols - 1) * gap
    canvas_h = rows * ref_h + (rows - 1) * gap
    canvas = Image.new("RGB", (canvas_w, canvas_h), bg)

    for idx, img in enumerate(resized):
        r, c = divmod(idx, cols)
        x = c * (ref_w + gap)
        y = r * (ref_h + gap)
        canvas.paste(img, (x, y))

    return canvas


# ─────────────────────────────────────────────────────────────────────────────
# Figure 2: 6 input-variable histograms (3x2)
# ─────────────────────────────────────────────────────────────────────────────
hist_names = [
    "Histogram_Attendance.png",
    "Histogram_Previous_Scores.png",
    "Histogram_Hours_Studied.png",
    "Histogram_Sleep_Hours.png",
    "Histogram_Tutoring_Sessions.png",
    "Histogram_Physical_Activity.png",
]
hists = [load("histograms", n) for n in hist_names]
fig2 = compose_grid(hists, cols=2, gap=40)
fig2.save(os.path.join(OUT, "Figure02_Histograms_Input_Variables.png"))
print("Saved Figure 2  — 3x2 histograms")

# ─────────────────────────────────────────────────────────────────────────────
# Figure 6: Violin — Motivation, Teacher Quality, Parental Education (1x3)
# ─────────────────────────────────────────────────────────────────────────────
v6 = [
    load("box_violin_plots", "BoxViolin_Motivation_Level.png"),
    load("box_violin_plots", "BoxViolin_Teacher_Quality.png"),
    load("box_violin_plots", "BoxViolin_Parental_Education_Level.png"),
]
fig6 = compose_grid(v6, cols=3, gap=30)
fig6.save(os.path.join(OUT, "Figure06_Violins_Motivation_Teacher_Education.png"))
print("Saved Figure 6  — 1x3 violins (Motivation, Teacher, Education)")

# ─────────────────────────────────────────────────────────────────────────────
# Figure 7: Violin — Peer Influence, Distance, Internet Access (1x3)
# ─────────────────────────────────────────────────────────────────────────────
v7 = [
    load("box_violin_plots", "BoxViolin_Peer_Influence.png"),
    load("box_violin_plots", "BoxViolin_Distance_from_Home.png"),
    load("box_violin_plots", "BoxViolin_Internet_Access.png"),
]
fig7 = compose_grid(v7, cols=3, gap=30)
fig7.save(os.path.join(OUT, "Figure07_Violins_Peer_Distance_Internet.png"))
print("Saved Figure 7  — 1x3 violins (Peer, Distance, Internet)")

# ─────────────────────────────────────────────────────────────────────────────
# Figure 8: Violin — Learning Disabilities, School Type, Extracurricular (1x3)
# ─────────────────────────────────────────────────────────────────────────────
v8 = [
    load("box_violin_plots", "BoxViolin_Learning_Disabilities.png"),
    load("box_violin_plots", "BoxViolin_School_Type.png"),
    load("box_violin_plots", "BoxViolin_Extracurricular_Activities.png"),
]
fig8 = compose_grid(v8, cols=3, gap=30)
fig8.save(os.path.join(OUT, "Figure08_Violins_Disabilities_School_Extracurricular.png"))
print("Saved Figure 8  — 1x3 violins (Disabilities, School, Extracurricular)")

# ─────────────────────────────────────────────────────────────────────────────
# Figure 9: Pie charts — Income, School, Disabilities, Education (2x2)
# ─────────────────────────────────────────────────────────────────────────────
pies = [
    load("pie_charts", "Pie_Family_Income.png"),
    load("pie_charts", "Pie_School_Type.png"),
    load("pie_charts", "Pie_Learning_Disabilities.png"),
    load("pie_charts", "Pie_Parental_Education_Level.png"),
]
fig9 = compose_grid(pies, cols=2, gap=40)
fig9.save(os.path.join(OUT, "Figure09_Pies_Demographics.png"))
print("Saved Figure 9  — 2x2 pie charts")

# ─────────────────────────────────────────────────────────────────────────────
# Figure 13: Bar charts — Access to Resources + Parental Involvement (1x2)
# ─────────────────────────────────────────────────────────────────────────────
bars = [
    load("bar_charts", "Bar_Access_to_Resources.png"),
    load("bar_charts", "Bar_Parental_Involvement.png"),
]
fig13 = compose_grid(bars, cols=2, gap=40)
fig13.save(os.path.join(OUT, "Figure13_Bars_Resources_Parental.png"))
print("Saved Figure 13 — 1x2 bar charts")

# ─────────────────────────────────────────────────────────────────────────────
# Figure 20: Density Contour + Bubble chart (1x2)
# ─────────────────────────────────────────────────────────────────────────────
adv = [
    load("advanced", "DensityContour_Previous_Exam.png"),
    load("advanced", "Bubble_Attendance_Score_Hrs.png"),
]
fig20 = compose_grid(adv, cols=2, gap=40)
fig20.save(os.path.join(OUT, "Figure20_DensityContour_Bubble.png"))
print("Saved Figure 20 — 1x2 density contour + bubble")

print(f"\nAll 7 composite figures saved to {OUT}")
