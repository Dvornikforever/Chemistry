from requests import get

print(get('http://localhost:5001/api/jobs').json())
print(get('http://localhost:5001/api/jobs/1').json())
print(get('http://localhost:5001/api/jobs/999').json())
print(get('http://localhost:5001/api/jobs/sdufkhxb').json())
