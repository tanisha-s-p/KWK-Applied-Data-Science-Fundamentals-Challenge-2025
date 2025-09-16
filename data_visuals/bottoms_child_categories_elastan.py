import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('final_data.csv')

bottoms_df = df[df['parent_category'] == 'Bottoms']

elastane_by_child_category = bottoms_df.groupby('child_category')['pct_elastane'].mean().reset_index()

elastane_by_child_category = elastane_by_child_category.sort_values('pct_elastane', ascending=False)

plt.figure(figsize=(12, 8))

bars = plt.bar(elastane_by_child_category['child_category'], elastane_by_child_category['pct_elastane'], color='#FA9C56', alpha=0.7, edgecolor='black')

plt.title('Average Elastane Percentage in Bottoms\nBy Child Category', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Child Category', fontsize=12)
plt.ylabel('Average Elastane Percentage (%)', fontsize=12)
plt.xticks(rotation=45, ha='right')

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.05,f'{height:.1f}%', ha='center', fontweight='bold')

plt.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()
