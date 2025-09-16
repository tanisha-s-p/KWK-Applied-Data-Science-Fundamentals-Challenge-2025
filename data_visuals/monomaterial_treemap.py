import pandas as pd
import matplotlib.pyplot as plt
import squarify

df = pd.read_csv('final_data.csv')

category_stats = df.groupby('parent_category').agg({'is_mono_no_elastane': ['count', 'sum']}).reset_index()

category_stats.columns = ['parent_category', 'total_products', 'mono_products']

category_stats['mono_percentage'] = (category_stats['mono_products'] / category_stats['total_products']) * 100

category_stats = category_stats.sort_values('mono_percentage', ascending=False)

labels = [f"{row['parent_category']}\n{row['mono_percentage']:.1f}%" for _, row in category_stats.iterrows()]

sizes = category_stats['total_products'].values
colors = plt.cm.viridis(category_stats['mono_percentage'] / 100)
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
squarify.plot(sizes=sizes, label=labels, color=colors, alpha=0.8, ax=ax)

ax.set_title('Mono-Material (no elastane) Percentage by Product Parent Category', fontsize=14, fontweight='bold')

# color bar code
norm = plt.Normalize(0, 100)
sm = plt.cm.ScalarMappable(cmap='viridis', norm=norm)
sm.set_array([])

cbar_ax = fig.add_axes([0.90, 0.15, 0.03, 0.7])
cbar = plt.colorbar(sm, cax=cbar_ax)
cbar.set_label('Mono-Material Percentage (%)', fontsize=12)

plt.tight_layout(rect=[0, 0, 0.9, 1])
plt.show()
