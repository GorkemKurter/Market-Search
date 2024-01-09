import json

temp_button_list = [
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"203425626"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"202012311"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"203366093"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"203180204"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"201354625"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"202643216"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"202010810"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"201164909"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"202305520"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"202058245"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"201801014"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"202667125"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"202839787"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"201893579"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"201879243"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"201443274"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"202010852"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"201792922"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"203254229"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"203599431"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"201839711"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"202180664"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"203021042"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"202018558"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"202788250"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"201326612"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"201797101"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"201208595"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"201824802"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"200885249"}',
    '{"event_category":"productlist","event_action":"click","event_label":"product","productId":"201151256"}'
]

products_links_dict_list = []
for json_string in temp_button_list:
    dict_value = json.loads(json_string)
    products_links_dict_list.append(dict_value)
print(products_links_dict_list)
print(products_links_dict_list[0].get('productId'))
product_links_button = []
try:
    for product_id in products_links_dict_list:
        print(product_id)
        product_links_button.append(f"https://www.idealo.fr/prix/{product_id.get('productId')}")
    print(product_links_button)
except Exception as e:
    print(f"Error")
