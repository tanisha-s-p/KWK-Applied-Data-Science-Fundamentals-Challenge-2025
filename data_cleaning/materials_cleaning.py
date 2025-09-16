import pandas as pd
import re
import ast

df = pd.read_csv('master_fashion_data_cleaned.csv')

df['materials'] = df['materials'].fillna('').astype(str)

# normalise by material synonyms/standardized name
fiber_mapping = {
    "organic cotton": "cotton",
    "cotton": "cotton",
    "recycled polyester": "polyester",
    "polyester": "polyester",
    "nylon": "nylon",
    "polyamide": "nylon",
    "viscose": "viscose",
    "rayon": "viscose",
    "lyocell": "lyocell",
    "tencel": "lyocell",
    "linen": "linen",
    "hemp": "hemp",
    "elastane": "elastane",
    "spandex": "elastane",
    "acrylic": "acrylic",
    "polyurethane": "polyurethane",
    "pu": "polyurethane",
    "elastomultiester": "elastane",
    "modal": "viscose",
    "cashmere": "wool",
    "alpaca": "wool",
    "wool": "wool",
    "metallic": "other"
}


def normalize_fiber(raw_fiber):
    # [^a-zA-Z\s] removes all non-alphabetic characters (except spaces)
    clean_fiber = re.sub(r'[^a-zA-Z\s]', '', raw_fiber).lower().strip()

    #remove tencel trademark if present
    clean_fiber = re.sub(r'^\s*(tencel)\s*', '', clean_fiber)
    clean_fiber = clean_fiber.strip()

    return fiber_mapping.get(clean_fiber, clean_fiber)


def parse_composition_string(comp_str, normalize=True, preserve_original=False):

    if preserve_original:
        comp_str = comp_str.strip()
    else:
        comp_str = comp_str.lower().strip()

    if comp_str == "":
        return []

    # pattern matches superdry format (percent first) and normal format (fibre name first)
    pattern = r'(\d+)%\s*([a-zA-Z][a-zA-Z\s®™â„¢]*(?=\s*(?:\d+%|,|$)))|([a-zA-Z][a-zA-Z\s®™â„¢]*)\s*(\d+)%'
    matches = re.findall(pattern, comp_str)

    components = []
    for match in matches:
        if match[0] and match[1]:  # catch normal format
            pct = int(match[0])
            fiber_name = match[1].strip()
            # remove any trailing "and"
            fiber_name = re.sub(r'\s+and$', '', fiber_name)
            if normalize and not preserve_original:
                fiber_name = normalize_fiber(fiber_name)
            components.append((pct, fiber_name))
        elif match[2] and match[3]:  # catch superdry format
            pct = int(match[3])
            fiber_name = match[2].strip()

            fiber_name = re.sub(r'\s+and$', '', fiber_name)
            if normalize and not preserve_original:
                fiber_name = normalize_fiber(fiber_name)
            components.append((pct, fiber_name))

    # if one fibre and no percent assume 100%.
    if not components and comp_str:
        if normalize and not preserve_original:
            fiber_name = normalize_fiber(comp_str)
        else:
            fiber_name = comp_str
        components.append((100, fiber_name))

    return components


def aggregate_materials(material_list):
    ##
    # If there were two fibres of same fibre family in the material
    # for example, 43% polyamide, 20% alpaca, 20% wool, 14% acrylic, and 3% elastane,
    # wool and alpaca would both be standardized as wool (as their recycling process has almost negligible difference)
    # Thus its necessary that the value of these two fibres is added up to result in 40% wool in the final normalised
    # material string. Otherwise, it would be like [(20, wool), (20, wool)] within the string
    ###

    if not material_list:
        return []

    aggregated = {}
    # checks if fibre already exists in material tuple
    for pct, fiber in material_list:
        if fiber in aggregated:
            aggregated[fiber] += pct
        else:
            aggregated[fiber] = pct

    # convert back to list of tuples
    result = [(pct, fiber) for fiber, pct in aggregated.items()]
    result.sort(key=lambda x: x[0], reverse=True)
    return result


def extract_body_materials_hollister(material_str):
    # get only body
    pattern = r'body(?: and [a-z\s]+)?:([^/]*)'
    match = re.search(pattern, material_str, re.IGNORECASE)
    if match:
        body_comp = match.group(1).strip()

        original_components = parse_composition_string(body_comp, normalize=False, preserve_original=True)
        normalized_components = parse_composition_string(body_comp, normalize=True, preserve_original=False)
        aggregated_components = aggregate_materials(normalized_components)
        return original_components, aggregated_components
    else:
        return [], []


def extract_body_materials_mexx(material_str):

    original_components = parse_composition_string(material_str, normalize=False, preserve_original=True)
    normalized_components = parse_composition_string(material_str, normalize=True, preserve_original=False)
    aggregated_components = aggregate_materials(normalized_components)
    return original_components, aggregated_components


def extract_body_materials_ca(material_str):

    # convert string into python list
    try:
        materials_list = ast.literal_eval(material_str)
    except (ValueError, SyntaxError):
        materials_list = [material_str]

    if not isinstance(materials_list, list):
        materials_list = [materials_list]

    for item in materials_list:
        if not isinstance(item, str):
            continue
        if 'main part' in item.lower() or 'body' in item.lower():
            # only get text after 'main part' or body
            comp_str = re.sub(r'^.*?(?:main part|body)\s*:\s*', '', item, flags=re.IGNORECASE)
            comp_str = comp_str.replace('|', ',')

            original_components = parse_composition_string(comp_str, normalize=False, preserve_original=True)
            normalized_components = parse_composition_string(comp_str, normalize=True, preserve_original=False)
            aggregated_components = aggregate_materials(normalized_components)
            return original_components, aggregated_components

    # if body/main part tag not there
    if materials_list:
        first_item = materials_list[0]
        if isinstance(first_item, str):
            comp_str = re.sub(r'^[a-z ]+:', '', first_item, flags=re.IGNORECASE).strip()
            comp_str = comp_str.replace('|', ',')

            original_components = parse_composition_string(comp_str, normalize=False, preserve_original=True)
            normalized_components = parse_composition_string(comp_str, normalize=True, preserve_original=False)
            aggregated_components = aggregate_materials(normalized_components)
            return original_components, aggregated_components
    return [], []


def extract_body_materials_superdry(material_str):

    original_components = parse_composition_string(material_str, normalize=False, preserve_original=True)
    normalized_components = parse_composition_string(material_str, normalize=True, preserve_original=False)
    aggregated_components = aggregate_materials(normalized_components)
    return original_components, aggregated_components


def extract_body_materials_marks(material_str):
    # removes all text in brackets
    clean_str = re.sub(r'\([^)]*\)', '', material_str)

    # remove specific non-body parts and text after it
    clean_str = re.sub(r',\s*(?:Lining|Padding|Embroidery Threads|Cord trim|Wadding|stuffing).*', '', clean_str, flags=re.IGNORECASE)

    clean_str = clean_str.replace(' and ', ', ')

    # clean multiple commas and spaces
    clean_str = re.sub(r',\s*,', ',', clean_str).strip(' ,-')

    original_components = parse_composition_string(clean_str, normalize=False, preserve_original=True)
    normalized_components = parse_composition_string(clean_str, normalize=True, preserve_original=False)
    aggregated_components = aggregate_materials(normalized_components)

    return original_components, aggregated_components


def extract_body_materials(row):
    brand = row['brand']
    material_str = row['materials']

    if brand == 'Hollister':
        return extract_body_materials_hollister(material_str)
    elif brand == 'Mexx':
        return extract_body_materials_mexx(material_str)
    elif brand == 'C&A':
        return extract_body_materials_ca(material_str)
    elif brand == 'Superdry':
        return extract_body_materials_superdry(material_str)
    elif brand == 'Marks & Spencer':
        return extract_body_materials_marks(material_str)


df[['Body materials_original', 'Body materials_normalized']] = df.apply(lambda row: pd.Series(extract_body_materials(row)), axis=1)

output_filename = 'master_fashion_data_with_material_normalization.csv'
df.to_csv(output_filename, index=False)
