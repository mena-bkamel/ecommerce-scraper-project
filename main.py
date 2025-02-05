from e_commerce import Amazon, Ebay
from formating import ProductFormat
from store_data import SaveData

search_key = "air fryer"

amazon = Amazon()
ebay = Ebay()
store_data = SaveData()
amazon_record = amazon.scrape_amazon(search_key)
ebay_record = ebay.scrape_ebay(search_key)


def save_to_sqlite_db(data: list[tuple]):
    product_format = ProductFormat(product_name="str", price="float", url="str", platform="str")
    columns_db = product_format.format_columns_db().col_definition_db
    db_name, table_name, columns_list = store_data.create_db("multiple_ecommerce", "products", columns_db)
    store_data.insert_records(db_name, table_name, columns_list, data)


if __name__ == '__main__':
    all_products = amazon_record + ebay_record
    save_to_sqlite_db(all_products)
    store_data.save_to_csv('multiple_ecommerce', amazon.header_row, all_products)
    store_data.save_to_json("multiple_ecommerce", amazon.header_row, all_products)
