import requests, os
from dotenv import load_dotenv

load_dotenv()


async def search(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query.replace(" ", "+"),
        'key': os.getenv('google_api_key'),
        'cx': os.getenv('google_cse_id'),
        'num': 10  # Number of results to return
    }
    print("Checking:", url, params)

    response = requests.get(url, params=params)
    print("response:", response)
    if response.status_code == 200:
        urls = []
        search_results = response.json()
        if search_results and "items" in search_results:
            # with open(file_name, 'w') as file:
                for item in search_results['items']:
                    # file.write(item['link'] + "\n")
                    urls.append(item['link'])
        return urls;
    else:
        return None

