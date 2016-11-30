import redis

# подключение к редису и заполнение его ключей сессиями из файла ( для получения идентичных данных )
r = redis.Redis(host='localhost', db=0)
pipe = r.pipeline()
for key in r.scan_iter():
    pipe.delete(key)
for session in open('session.csv'):
    pipe.set(session.replace('\n', ''), '')
pipe.execute()


