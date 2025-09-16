import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('final_data.csv')


elastane_by_category = df.groupby('parent_category')['pct_elastane'].mean().reset_index()
elastane_by_category = elastane_by_category.sort_values('pct_elastane', ascending=True)


fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

categories = elastane_by_category['parent_category'].tolist()
values = elastane_by_category['pct_elastane'].tolist()
N = len(categories)

angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

values += values[:1]

ax.plot(angles, values, color='#FD5ECD', linewidth=2, linestyle='solid')
ax.fill(angles, values, color='#FEBCEA', alpha=0.3)

ax.set_ylim(0, max(values) * 1.6)

#adds labels for each category
for angle, value, category in zip(angles[:-1], values[:-1], categories):
    rotation_angle = np.degrees(angle)
    ha = 'left'
    if angle == 0:
        ha = 'center'
    elif angle == np.pi:
        ha = 'center'
    elif angle > np.pi:
        ha = 'right'
    ax.text(angle, max(values) * 1.35, category, ha=ha, va='center', rotation_mode='anchor', rotation=rotation_angle if rotation_angle < 90 else rotation_angle + 180, fontsize=12, fontweight='bold')

#adds value labels  at each point
for angle, value in zip(angles[:-1], values[:-1]):
    ax.text(angle, value, f'{value:.1f}%', ha='center', va='center', fontsize=10, fontweight='bold',bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))


ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
#removes default axis labels
ax.set_yticklabels([])
ax.set_xticklabels([])
ax.grid(True, color='gray', alpha=0.3)

plt.title('Average Elastane Percentage by Product Category', fontsize=16, fontweight='bold', pad=10)
plt.tight_layout()
plt.show()
