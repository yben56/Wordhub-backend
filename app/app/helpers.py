import requests

def postman(method, url, headers=None, body=None):
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=body)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=body)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError("Unsupported HTTP method")

        return {
            "status" : response.status_code,
            "body" : response.json()
        }
    except requests.exceptions.RequestException as e:
         return {
            "status" : response.status_code,
            "body" : {'error': str(e)}
        }
    
    #headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer YOUR_TOKEN'}
    #body = {'b': 2}