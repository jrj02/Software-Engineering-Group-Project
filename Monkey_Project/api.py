import requests


class API:
    @staticmethod
    def send_post_request(endpoint, data):
        try:
            response = requests.post(endpoint, data=data)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error in sending POST request: {e}")
            return None

    @staticmethod
    def retrieve_get_data(endpoint, data):
        try:
            response = requests.get(endpoint, data=data)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error in retrieving GET request: {e}")
            return None
