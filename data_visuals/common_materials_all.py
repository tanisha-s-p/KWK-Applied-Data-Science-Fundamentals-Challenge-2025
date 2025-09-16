import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('final_data.csv')

material_counts = df['main_material'].value_counts()

plt.figure(figsize=(14, 8))

bars = plt.bar(material_counts.index, material_counts.values, color='#FEBCEA')

plt.title('Main material of all products in dataset', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Main Material', fontsize=12)
plt.ylabel('Number of Products', fontsize=12)
plt.xticks(rotation=45, ha='right')

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.5, f'{int(height)}', ha='center', va='bottom', fontsize=10)

plt.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()
