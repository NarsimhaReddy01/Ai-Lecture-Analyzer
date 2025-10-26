import redis

r = redis.Redis(host='localhost', port=6379)
r.set('key', 'value')
print(r.get('key'))
