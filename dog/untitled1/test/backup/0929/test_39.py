from requests_toolbelt import MultipartEncoder
import requests

m = MultipartEncoder(
    fields={'field0': 'value', 'field1': 'value',
            'field2': ('filename', open('C:\Users\jack\Desktop\icup.txt', 'rb'), 'text/plain')}
    )

r = requests.post('http://192.168.0.34/img', data=m,
                  headers={'Content-Type': m.content_type})
print r.status_code
print r.content
