import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('final_data.csv')

green = "#7AC74F"
orange = "#FA9C56"

# pie chart 1
mono_elastane_count = df['is_mono_incl_elastane'].sum()

blend_count = len(df) - mono_elastane_count

categories = ['Mono Materials\n(including ≤5% elastane)', 'Blended Materials']
counts = [mono_elastane_count, blend_count]
colors = [green, orange]

plt.figure(figsize=(8, 8))
plt.pie(counts, labels=categories, colors=colors, autopct='%1.1f%%', startangle=90)
plt.title('The Optimistic Lense\nWhat is the proportion of Mono (incl ≤5% elastane) in New Arrivals')
plt.axis('equal')
plt.show()

# pie chart 2
strict_mono_count = df['is_mono_no_elastane'].sum()

blend_count1 = len(df) - strict_mono_count

categories_3 = ['Strict Mono-material\n(No Elastane)', 'All Blends']
counts_3 = [strict_mono_count, blend_count1]
colors_3 = [green, orange]

plt.figure(figsize=(8, 8))
plt.pie(counts_3, labels=categories_3, colors=colors_3, autopct='%1.1f%%', startangle=90)
plt.title('The Critical Lense\nWhat is the proportion of Mono (no elastane) in New Arrivals')
plt.show()

