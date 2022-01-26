from datetime import datetime


dt = '10.05.2001'
a = datetime.strptime(dt,'%d.%m.%Y')
b = datetime.now()
print(a)
print(b)
c = str(b - a)
d = int(c.split(' ')[0])
print(d)


d1 = int(str(datetime.now() - datetime.strptime(dt,'%d.%m.%Y')).split(' ')[0])
print(d1)
