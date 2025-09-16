import pandas as pd
import re

df = pd.read_csv('master_fashion_data.csv')

# dictionary to normalise parent category to: tops, bottoms, outerwear, dresses & jumpsuits
parent_category_mapping = {
    'Accessories': 'Accessories',
    'Blouses': 'Tops',
    'Bottoms': 'Bottoms',
    'Businesswear': 'Outerwear',
    'Coats & Jackets': 'Outerwear',
    'Coats and jackets': 'Outerwear',
    'Dresses': 'Dresses & Jumpsuits',
    'Dresses & Jumpsuits': 'Dresses & Jumpsuits',
    'Dresses and skirts': 'Dresses & Jumpsuits',
    'Footwear': 'Footwear',
    'Hoodies and Sweatshirts': 'Tops',
    'Jackets': 'Outerwear',
    'Jeans': 'Bottoms',
    'Jumpers & Cardigans': 'Tops',  # FIXED
    'Knitwear': 'Tops',
    'Pants': 'Bottoms',
    'Shorts': 'Bottoms',
    'Skirts': 'Bottoms',
    'Sleepwear': 'Tops',
    'Sportswear': 'Bottoms',
    'Sweaters and cardigans': 'Tops',
    'Swimwear': 'Swimwear',
    'Tops': 'Tops',
    'Tops and shirts': 'Tops',
    'Trousers': 'Bottoms',
    'T-Shirts': 'Tops',
    'T-Shirts & Tops': 'Tops',
    'Young Fashion': 'Outerwear',
    'Blouse Embroidery Off White': 'Tops',
    'Blouse Puff Sleeve Gathering Pink': 'Tops',
    'Blouse Rosa Black': 'Tops',
    'Blouse Chamomile Tencel Green': 'Tops',
    'Blouse Heavy lace White': 'Tops',
    'Andrea High Waist / Skinny Jeans': 'Bottoms'
}

# dictionary to normalise child category to: skirt, shirt/blouse, bikinis, blazer, coat, jacket, dress,
    # hoodie/sweatshirt, jeans, shorts, skirt, sweater/cardigan, trousers/chinos, T-shirt
child_category_mapping = {
    'A line skirts': 'Skirt',
    'Babydoll Tops': 'Shirt/Blouse',
    'Bikinis': 'Bikinis',
    'Blazer': 'Blazer',
    'Blouses': 'Shirt/Blouse',
    'Business-Casual': 'Blazer',
    'Button-Down Shirts': 'Shirt/Blouse',
    'Cardigans': 'Sweater/Cardigan',
    'Casual dresses': 'Dress',
    'Coats': 'Coat',
    'Flare Jeans': 'Jeans',
    'High waist jeans': 'Jeans',
    'High waisted trousers': 'Trousers/Chinos',
    'Hoodies & Sweatshirts': 'Hoodie/Sweatshirt',
    'Jackets': 'Jacket',
    'Jeans': 'Jeans',
    'Jumpers': 'Sweater/Cardigan',
    'Knee Length Dresses': 'Dress',
    'Knitted dresses': 'Dress',
    'Leggings': 'Trousers/Chinos',
    'Lightweight jackets': 'Jacket',
    'Long trousers': 'Trousers/Chinos',
    'Long-Sleeve Tops': 'T-shirt',
    'Long-sleeved t-shirts': 'T-shirt',
    'Maxi Dresses': 'Dress',
    'Midi dresses': 'Dress',
    'Mini Dresses': 'Dress',
    'Petite jeans': 'Jeans',
    'Quilted jackets': 'Jacket',
    'Shirts & Blouses': 'Shirt/Blouse',
    'Shoes': 'Shoes',
    'Shorts': 'Shorts',
    'Skirts': 'Skirt',
    'Sleep Bottoms': 'Shorts',
    'Sports trousers': 'Trousers/Chinos',
    'Sweaters & Cardigans': 'Sweater/Cardigan',
    'Sweatpants': 'Trousers/Chinos',
    'Sweatshirts & Sweat jackets': 'Hoodie/Sweatshirt',
    'Swim Bottoms': 'Swim Bottoms',
    'Swim Tops': 'Swim Tops',
    'Tops': 'Shirt/Blouse',
    'T-Shirts': 'T-shirt',
    'Tube Tops': 'Tank/Cami',
    'Waistcoats': 'Shirt/Blouse'
}

# i used these dictionaries if either the parent or child category was empty
default_child_by_parent = {
    'Tops': 'Shirt/Blouse',
    'Bottoms': 'Trousers/Chinos',
    'Outerwear': 'Jacket',
    'Dresses & Jumpsuits': 'Dress',
    'Footwear': 'Shoes',
    'Swimwear': 'Swim Tops',
    'Accessories': 'Accessories',
    'Other': 'Other'
}

default_parent_to_child = {
    'Tops': 'Shirt/Blouse',
    'Bottoms': 'Trousers/Chinos',
    'Outerwear': 'Jacket',
    'Dresses & Jumpsuits': 'Dress',
    'Footwear': 'Shoes',
    'Swimwear': 'Swim Tops',
    'Accessories': 'Accessories',
}

keyword_to_child = {
    'waistcoat': 'Shirt/Blouse',
    'dress': 'Dress',
    'sweatshirt': 'Hoodie/Sweatshirt',
    't-shirt': 'T-shirt',
    't shirt': 'T-shirt',
    'tee': 'T-shirt',
    'shirt': 'Shirt/Blouse',
    'blouse': 'Shirt/Blouse',
    'jeans': 'Jeans',
    'jeggings': 'Jeans',
    'legging': 'Trousers/Chinos',
    'trouser': 'Trousers/Chinos',
    'pants': 'Trousers/Chinos',
    'shorts': 'Shorts',
    'skirt': 'Skirt',
    'jacket': 'Jacket',
    'coat': 'Coat',
    'blazer': 'Blazer',
    'sweater': 'Sweater/Cardigan',
    'cardigan': 'Sweater/Cardigan',
    'hoodie': 'Hoodie/Sweatshirt',
    'shoe': 'Shoes',
    'sandal': 'Shoes',
    'boot': 'Shoes',
    'bikini': 'Bikinis',
    'swim': 'Swim Tops',
    'top': 'Shirt/Blouse'
}

# used to match key word in product name to parent_category
keyword_to_parent = {
    'jeggings': 'Bottoms',
    'jeans': 'Bottoms',
    'pants': 'Bottoms',
    'trousers': 'Bottoms',
    'shorts': 'Bottoms',
    'skirt': 'Bottoms',
    'leggings': 'Bottoms',
    'dress': 'Dresses & Jumpsuits',
    'jumpsuit': 'Dresses & Jumpsuits',
    'top': 'Tops',
    'shirt': 'Tops',
    'blouse': 'Tops',
    'sweater': 'Tops',
    'cardigan': 'Tops',
    'hoodie': 'Tops',
    'sweatshirt': 'Tops',
    'jacket': 'Outerwear',
    'coat': 'Outerwear',
    'blazer': 'Outerwear',
    'shoe': 'Footwear',
    'boot': 'Footwear',
    'sandal': 'Footwear',
    'bikini': 'Swimwear',
    'swim': 'Swimwear'
}

# parent and child category normalisation
def map_categories(row):
    old_parent = str(row['parent_category']).strip()
    old_child = str(row['child_category']).strip() if pd.notna(row['child_category']) else ''
    product_name = str(row['product_name']).lower()

    # handling missing parent categories
    if old_parent == '' or old_parent == 'nan':
        # check for keywords
        for keyword, parent_guess in keyword_to_parent.items():
            if keyword in product_name:
                new_parent = parent_guess
                break
        else:
            # hard coded default
            new_parent = 'Bottoms'
    else:
        new_parent = parent_category_mapping.get(old_parent, 'Other')

    # special case
    if old_parent == 'Dresses and skirts':
        if 'skirt' in product_name:
            return 'Bottoms', 'Skirt'
        else:
            return 'Dresses & Jumpsuits', 'Dress'

    # if valid old child
    if old_child and old_child in child_category_mapping:
        return new_parent, child_category_mapping[old_child]

    # check for keyword
    for keyword, guess in keyword_to_child.items():
        if keyword in product_name:
            return new_parent, guess

    # default
    if new_parent in default_parent_to_child:
        return new_parent, default_parent_to_child[new_parent]

    return new_parent, 'Bottoms'


df[['parent_category', 'child_category']] = df.apply(lambda row: pd.Series(map_categories(row)), axis=1)

# delete accessories, swimwear, footwear
categories_to_delete = ['Accessories', 'Swimwear', 'Footwear']
df = df[~df['parent_category'].isin(categories_to_delete)]


def convert_to_usd(price_str):
    price_str = str(price_str).strip()

    # use regex to parse price
    match = re.search(r'([£€\$]?)\s*([\d,\.]+)', price_str)
    if not match:
        return None

    currency_symbol = match.group(1)
    numeric_value = match.group(2).replace(',', '.')

    try:
        numeric_value = float(numeric_value)
    except ValueError:
        return None

    conversion_rates = {
        '£': 1.36,
        '€': 1.17,
        '$': 1.00,
        '': 1.00  # default to USD
    }

    return round(numeric_value * conversion_rates.get(currency_symbol, 1.00), 2)


df['price_usd'] = df['price'].apply(convert_to_usd)

# remove original price column
df.drop('price', axis=1, inplace=True)

df.rename(columns={'price_usd': 'price'}, inplace=True)

df.to_csv('master_fashion_data_cleaned.csv', index=False)
