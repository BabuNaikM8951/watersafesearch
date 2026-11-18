
import requests
from connection_settings import connection_url, auth

def test_connection():
    try:
        url = connection_url()

        print("Connecting to:", url)

        response = requests.get(
            url,
            auth=auth(),
            timeout=15
        )

        print("HTTP status:", response.status_code)

        if response.status_code == 200:
            data = response.json()

            print("Successfully connected to OpenSearch!")
            print("Cluster:", data.get("cluster_name"))
            print("Version:", data.get("version", {}).get("number"))

        else:
            print("Connection failed.")
            print(response.text[:500])

    except requests.exceptions.RequestException as error:
        print("Connection error:", error)

    except ValueError as error:
        print("Configuration error:", error)


if __name__ == "__main__":
    test_connection()
