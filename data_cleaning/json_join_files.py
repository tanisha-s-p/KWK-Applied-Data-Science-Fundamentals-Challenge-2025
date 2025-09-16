import pandas as pd

files = {
    "Hollister": r"C:\Users\phadk\Documents\web_scraping_kwk\hollister\output.json",
    "Mexx": r"C:\Users\phadk\Documents\web_scraping_kwk\mexx\output1.json",
    "C&A": r"C:\Users\phadk\Documents\web_scraping_kwk\ca\output.json",
    "Superdry": r"C:\Users\phadk\Documents\web_scraping_kwk\superdry\output.json",
    "Marks & Spencer": r"C:\Users\phadk\Documents\web_scraping_kwk\ms\output.json"
}

dfs = []

# looping through each file to add brand name as first column
for brand, filepath in files.items():
    df = pd.read_json(filepath)
    df.insert(0, "brand", brand)
    dfs.append(df)


merged_df = pd.concat(dfs, ignore_index=True)

merged_df.to_csv("master_fashion_data.csv", index=False)