import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# ============================================================
# Roughness kernel
# ============================================================
def roughness(delta_f, cbw=100):
    x = delta_f / cbw
    return np.exp(-3.5 * x) - np.exp(-5.75 * x)

# ============================================================
# Parameters
# ============================================================
f0 = 200.0
partials = np.arange(1, 31)

intervals = [
    ("Major third (5:4)", 5/4, "#ff6b6b"),
    ("Perfect fourth (4:3)", 4/3, "#ffb74d"),
    ("Perfect fifth (3:2)", 3/2, "#81c784"),
    ("Octave (2:1)", 2.0, "#64b5f6"),
]

# Reverse for display order (bottom to top)
intervals = list(reversed(intervals))

# ============================================================
# Create Panel C only - interaction density
# ============================================================
fig, ax = plt.subplots(figsize=(12, 6), facecolor='#000000')

fA = partials[:, None] * f0
x = np.linspace(0, 200, 600)
r_curve = roughness(x)
r_curve_max = r_curve.max()

ys = []

for name, ratio, color in intervals:
    fB = partials[None, :] * f0 * ratio
    delta_vals = np.abs(fA - fB).flatten()
    delta_vals = delta_vals[delta_vals <= 200]

    kde = gaussian_kde(delta_vals, bw_method=0.035)
    y = kde(x) * len(delta_vals)
    ys.append(y)

    ax.plot(x, y, linewidth=2.5, color=color, label=name)

    # Fundamental Δf marker
    delta_f_fund = abs(f0 - ratio * f0)
    ax.axvline(delta_f_fund, linestyle=":", linewidth=1.5, color=color, alpha=0.5)

# Add ear roughness sensitivity curve (scaled)
y_max = max(np.max(y) for y in ys)
ax.plot(
    x,
    r_curve / r_curve_max * y_max,
    "--",
    color="white",
    linewidth=2,
    label="Ear roughness sensitivity",
    alpha=0.8
)

ax.set_xlabel("Frequency difference Δf (Hz, within one octave)", fontsize=14, color='white')
ax.set_ylabel("Interaction density", fontsize=14, color='white')
ax.set_facecolor('#000000')
ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['right'].set_color('white')
ax.tick_params(axis='x', colors='white', labelsize=12)
ax.tick_params(axis='y', colors='white', labelsize=12)
ax.grid(True, alpha=0.3, color='white', linestyle='-', linewidth=0.5)

legend = ax.legend(loc='upper left', fontsize=11, framealpha=0.9)
legend.get_frame().set_facecolor('#1a1a1a')
legend.get_frame().set_edgecolor('white')
for text in legend.get_texts():
    text.set_color('white')

plt.tight_layout()
plt.savefig("src/content/blog/musical-consonance-from-frequency-interactions/thumbnail.png",
            dpi=150, bbox_inches="tight", facecolor='#000000')
print("Thumbnail saved!")
