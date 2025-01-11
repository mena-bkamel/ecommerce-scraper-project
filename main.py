from e_commerce import Amazon
from store_data import Data
import time

start_time = time.time()
header = ['Description', 'Price', 'Rating', 'ReviewCount', 'Url']
product_name = "ultrawide monitor"
amazon = Amazon()
data = Data()

result = amazon.scrape_amazon("ultrawide monitor")
save_to_csv = data.save_to_csv("ultrawide monitor", header, result)

end_time = time.time()

elapsed_time = end_time - start_time
print(f"Total execution time: {elapsed_time:.4f} seconds")


