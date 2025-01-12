from e_commerce import Amazon, Ebay
from store_data import Data
import time

amazon_header = ['Description', 'Price', 'Rating', 'ReviewCount', 'Url']
ebay_header = ['Title', 'SubTitle', 'Rating', 'ItemPrice', 'TrendingPrice', 'ItemLink']

product_name = "dell laptop"
# amazon = Amazon()
ebay = Ebay()

data = Data()

result = ebay.scrape_ebay(product_name)
save_to_csv = data.save_to_csv(product_name, ebay_header, result)

end_time = time.time()



