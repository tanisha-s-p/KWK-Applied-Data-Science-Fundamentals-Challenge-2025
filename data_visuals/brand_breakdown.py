import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('final_data.csv')

brand_groups = df.groupby('brand')
material_percentages = []

for brand, group in brand_groups:
    total = len(group)

    mono_elastane = ((group['is_mono_incl_elastane'] & ~group['is_mono_no_elastane']).sum() / total) * 100

    blend_mask = group['is_mono_incl_elastane'] == False
    two_materials = ((group['n_materials'] == 2) & blend_mask).sum() / total * 100
    three_plus_materials = ((group['n_materials'] >= 3) & blend_mask).sum() / total * 100

    material_percentages.append({
        'brand': brand,
        'Mono (No Elastane)': group['is_mono_no_elastane'].sum() / total * 100,
        'Mono (≤5% Elastane)': mono_elastane,
        '2-Material Blends': two_materials,
        '3+ Material Blends': three_plus_materials,
        'avg_price': group['price'].mean()
    })

#convert dictionary list to df
plot_df = pd.DataFrame(material_percentages).set_index('brand')

colors = ['#7BC950', '#FEBCEA', '#FA9C56', '#D52941']

fig, ax1 = plt.subplots(figsize=(14, 10))

material_cols = ['Mono (No Elastane)', 'Mono (≤5% Elastane)', '2-Material Blends', '3+ Material Blends']
plot_df[material_cols].plot(kind='bar', stacked=True, ax=ax1, color=colors, width=0.7, rot=45)

ax1.set_xlabel('Brand', fontsize=12)
ax1.set_ylabel('Percentage of Products (%)', fontsize=12)
ax1.set_title('Material Composition and Average Price by Brand', fontsize=14, fontweight='bold', pad=20)
ax1.set_ylim(0, 110)
ax1.set_yticks(np.arange(0, 101, 10))

# add price axis
ax2 = ax1.twinx()
ax2.plot(range(len(plot_df)), plot_df['avg_price'], 'ko-', linewidth=2, markersize=8, label='Average Price')
ax2.set_ylabel('Average Price ($)', fontsize=12)

max_price = max(plot_df['avg_price'])
ax2.set_ylim(0, max_price * 1.2) # *1.2 to add space for label

for i, price in enumerate(plot_df['avg_price']):
    offset = max(plot_df['avg_price']) * 0.05
    ax2.text(i, price + offset, f'${price:.0f}', ha='center', va='bottom', fontweight='bold', fontsize=10, bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))

# merges legend of both axes to create 1
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, bbox_to_anchor=(1.15, 1), loc='upper left')

plt.tight_layout()
plt.show()
