import requests


def get_genera_name(genre):
    url = f"https://app.rakuten.co.jp/services/api/IchibaGenre/Search/20140222?format=json&genreId={genre}&applicationId=1018947431031079367"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get("parents", [])
        parent = data[0]["parent"]["genreName"]
        return parent
    else:
        return "Not found genre"
