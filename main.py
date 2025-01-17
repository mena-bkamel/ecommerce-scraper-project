from e_commerce import Amazon, Ebay, Target
from store_data import DataSaving
import time


product_name = "dell laptop"
amazon = Amazon()
ebay = Ebay()
target = Target()

data = DataSaving()

# save_amazon_to_csv = data.save_to_csv(product_name, amazon.header_row, amazon.scrape_amazon(product_name))
# save_ebay_to_csv = data.save_to_csv(product_name, ebay.header_row, ebay.scrape_ebay(product_name))
# save_target_to_csv = data.save_to_csv(product_name, target.header_row, target.scrape_target(product_name))

records = target.scrape_target(product_name)
db_name, table_name, col_names = data.create_db()

