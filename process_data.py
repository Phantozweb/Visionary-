import json

with open('lenskart.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

start_marker = '<script id="__NEXT_DATA__" type="application/json">'
end_marker = '</script>'

start_index = html_content.find(start_marker)
end_index = html_content.find(end_marker, start_index)

if start_index != -1 and end_index != -1:
    json_string = html_content[start_index + len(start_marker):end_index]
    data = json.loads(json_string)
    product_list = data['props']['pageProps']['data']['productListData']

    grouped_products = {}
    for product in product_list:
        model_name = product.get('productModelName')
        if model_name not in grouped_products:
            grouped_products[model_name] = {
                "productName": product.get('productName'),
                "productModelName": model_name,
                "classification": product.get('classification'),
                "variations": []
            }
        
        # Add all color options from the product to the main list of variations
        if 'colorOptions' in product:
            for color_option in product['colorOptions']:
                # Avoid adding duplicate color options
                if not any(v['id'] == color_option['id'] for v in grouped_products[model_name]['variations']):
                    grouped_products[model_name]['variations'].append(color_option)

    final_data = list(grouped_products.values())

    with open('lenskartdata.json', 'w') as f:
        json.dump(final_data, f, indent=4)