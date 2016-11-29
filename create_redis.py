import redis

# подключение к редису и заполнение его ключей сессиями из файла ( для получения идентичных данных )
r = redis.Redis(host='localhost', db=0)
pipe = r.pipeline()
for key in r.scan_iter():
    pipe.delete(key)
file = open('session.csv')
for session in file:
    pipe.set(session.replace('\n', ''), '')
pipe.execute()


