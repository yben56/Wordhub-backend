
'''
from app.helpers import postman
data = postman('GET', 'http://localhost:3000/database/Words.json')
return Response({
    'error' : False,
    'message' : '',
    'data' : data
}, status=200)
'''