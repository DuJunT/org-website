import redis
import time

r = redis.Redis(host='127.0.0.1',port=6379,db=0,decode_responses=True)

r.set('name','ddd')
r.expire('name',1)
time.sleep(2)

print(r.get('name'))