import requests
import csv

# Parameters
base_url = 'https://api.numista.com/api/v3'
# PUT YOUR API KEY HERE
api_key = ''

def fetch_coin_data(coin_id):
    response = requests.get(
        f"{base_url}/types/{coin_id}",
        headers={'Numista-API-Key': api_key}
    )
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for coin {coin_id}")
        return None


def search_coins_by_query(query, page):
    response = requests.get(
        f"{base_url}/types",
        params={
            'category': 'coin',
            'q': query,
            'count': 50,
            'lang': 'en',
            'page': page
        },
        headers={'Numista-API-Key': api_key}
    )
    if response.status_code == 200:
        return response.json().get('types', [])
    else:
        print(f"Failed to search for coins with query '{query}' on page {page}")
        return []

# I am not using all the possible fields
def write_to_csv(coins_data):
    with open('coins.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['ID', 'Obverse Copyright', 'Obverse License', 'Obverse Picture', 'Reverse Copyright', 'Reverse License', 'Reverse Picture', 'Issuer'])
        writer.writeheader()
        for coin in coins_data:
            id = coin['id']
            obverse = coin.get('obverse', {})
            reverse = coin.get('reverse', {})
            o_copyright = obverse.get('picture_copyright', '')
            obverse_license = obverse.get('picture_license_name', '')
            obverse_picture = obverse.get('picture', '')
            r_copyright = reverse.get('picture_copyright', '')
            reverse_license = reverse.get('picture_license_name', '')
            reverse_picture = reverse.get('picture', '')
            issuer = coin['issuer'].get('name', '')
            writer.writerow({'ID': id, 'Obverse Copyright': o_copyright, 'Obverse License': obverse_license, 'Obverse Picture': obverse_picture, 'Reverse Copyright': r_copyright, 'Reverse License': reverse_license, 'Reverse Picture': reverse_picture, 'Issuer': issuer})

def is_valid_license(license_name):
    valid_licenses = ['CC0', 'CC BY-NC-SA', 'CC BY', 'CC BY-SA', 'CC BY-NC'] # I only want to filter for certain liscenses as I will be using the images and want to give proper credit.
    return license_name in valid_licenses

if __name__ == "__main__":
    query = '1923'  # Adjust the search query
    page = 1

    coins_data = []

    while True:
        search_results = search_coins_by_query(query, page)
        if not search_results:
            break  

        for result in search_results:
            coin_id = result['id']

            # Check if coin is standard circulation type, remove if you want commems and non-circulated! 
            type = result['type'] 
            coin_data = fetch_coin_data(coin_id)
            if coin_data:
                obverse = coin_data.get('obverse', {})
                reverse = coin_data.get('reverse', {})
                obverse_license = obverse.get('picture_license_name', '')
                reverse_license = reverse.get('picture_license_name', '')
                if is_valid_license(obverse_license) and is_valid_license(reverse_license) and type == 'Standard circulation coins' :
                    coins_data.append(coin_data)

        page += 1  # Increment page number for next iteration

    write_to_csv(coins_data)
    print("CSV file generated successfully!")

    # POTENTIALLY WANT TO CHECK :             "type": 'Standard circulation coin', AND MIN YEAR/MAX YEAR
