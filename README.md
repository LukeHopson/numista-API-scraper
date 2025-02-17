# numista-API-scraper
A simple python script that scrapes coins from Numista's API and writes to a .CSV file.

Requires a Numista API key to use. 

Will retreive all coins and their information from a specific search query. (Reminder that free API users only get 2000 requests a month).
# Useage
Adjust your search query here:
```
if __name__ == "__main__":
    query = '1923'  
    page = 1
```

I am also checking for the license of the images for each coin to ensure I can use them without conflict. This reduces the amount of coins retrived considerably, but you can easily add or remove valid licenses by altering the 'valid_licenses' array. 
```
def is_valid_license(license_name):
    valid_licenses = ['CC0', 'CC BY-NC-SA', 'CC BY', 'CC BY-SA', 'CC BY-NC'] 
    return license_name in valid_licenses
```

If you want to retrieve all coins regardless of license, remove the logic from the following if-block:
```
if is_valid_license(obverse_license) and is_valid_license(reverse_license):
    coins_data.append(coin_data)
```

Currently, I'm only using it to retrieve the fields: 'ID', 'Obverse Copyright', 'Obverse License', 'Obverse Picture', 'Reverse Copyright', 'Reverse License', 'Reverse Picture', 'Issuer'.
It is possible to get other coin info (like weight, size, material) from the Numista API response by modifying the write_to_csv method. Simply add any deatils you want from here: 
https://en.numista.com/api/doc/index.php#tag/Catalogue/operation/getType

