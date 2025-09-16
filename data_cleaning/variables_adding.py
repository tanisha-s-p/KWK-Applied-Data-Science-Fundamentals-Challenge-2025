import pandas as pd
import ast


df = pd.read_csv('master_fashion_data_with_material_normalization.csv')

# string representation of lists -> python lists
df['Body materials_normalized'] = df['Body materials_normalized'].apply(ast.literal_eval)
df['Body materials_original'] = df['Body materials_original'].apply(ast.literal_eval)

# remove rows with no materials listed
print(f"Original number of rows: {len(df)}")
df = df[df['Body materials_normalized'].apply(len) > 0]
print(f"Number of rows after removing empty material entries: {len(df)}")

preferred_terms = [
    'recycled cotton', 'organic hemp', 'organic linen', 'lyocell',
    'recycled wool', 'econyl', 'organic cotton', 'recycled nylon',
    'monocel', 'recycled pet', 'recycled polyester', 'linen', 'hemp', 'modal'
]

def is_material_preferred(material_str):

    material_lower = material_str.lower()
    for term in preferred_terms:
        if term in material_lower:
            return True
    return False

def is_mono_no_elastane(material_list):

    if len(material_list) == 1:
        return True
    return False

def is_mono_incl_elastane(material_list):

    if len(material_list) == 1:
        return True
    elif len(material_list) == 2:
        materials = [m[1] for m in material_list]
        if 'elastane' in materials:
            # check if non elastane material is more than 95%
            for percentage, material in material_list:
                if material != 'elastane':
                    return percentage >= 95
    return False

def get_preferred_type(original_list):

    for percentage, material in original_list:
        if is_material_preferred(material):
            return material
    return ""

def get_elastane_gt_5(normalized_list):

    for percentage, material in normalized_list:
        if material == 'elastane':
            return percentage > 5
    return False

def get_n_materials(normalized_list):

    return len(normalized_list)

def has_recycled(original_list):

    original_str = str(original_list).lower()
    return 'recycled' in original_str


def get_main_material(normalized_list):
    if not normalized_list:
        return None

    main_material = max(normalized_list, key=lambda x: x[0])
    return main_material[1]

def calculate_pct_preferred(original_list):

    total_preferred_pct = 0.0
    for percentage, material in original_list:
        if is_material_preferred(material):
            total_preferred_pct += percentage
    return total_preferred_pct

def get_pct_synthetics(normalized_list):

    synthetic_materials = {'polyester', 'nylon', 'acrylic', 'polyamide', 'polyurethane', 'elastane'}
    total_synth_pct = 0.0
    for percentage, material in normalized_list:
        if material in synthetic_materials:
            total_synth_pct += percentage
    return total_synth_pct

def get_pct_elastane(normalized_list):

    for percentage, material in normalized_list:
        if material == 'elastane':
            return percentage
    return 0.0


df['is_mono_no_elastane'] = df['Body materials_normalized'].apply(is_mono_no_elastane)
df['is_mono_incl_elastane'] = df['Body materials_normalized'].apply(is_mono_incl_elastane)
df['preferred_material_type'] = df['Body materials_original'].apply(get_preferred_type)
df['elastane_gt_5'] = df['Body materials_normalized'].apply(get_elastane_gt_5)
df['n_materials'] = df['Body materials_normalized'].apply(get_n_materials)
df['has_recycled'] = df['Body materials_original'].apply(has_recycled)
df['has_preferred_material'] = df['preferred_material_type'].astype(bool)
df['main_material'] = df['Body materials_normalized'].apply(get_main_material)
df['pct_preferred'] = df['Body materials_original'].apply(calculate_pct_preferred)
df['pct_synthetics'] = df['Body materials_normalized'].apply(get_pct_synthetics)
df['pct_elastane'] = df['Body materials_normalized'].apply(get_pct_elastane)

output_filename = 'master_fashion_data_enhanced.csv'
df.to_csv(output_filename, index=False)