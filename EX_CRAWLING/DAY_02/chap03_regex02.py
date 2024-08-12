import re

tel_checker = re.compile(r'^(\d{2,3})-(\d{3,4})-(\d{4})$')

print(tel_checker.match('02-123-4567'))
match_groups = tel_checker.match('02-123-4567').groups()
print(match_groups)

match_groups = tel_checker.match('02-123-4567').group()
print(match_groups)

print(tel_checker.match('053-950-45678'))
print(tel_checker.match('053950-4567'))


tel_number = '053-950-4567'
tel_number = tel_number.replace('-', '')
print(tel_number)

tel_checker1 = re.compile(r'^(\d{2,3})(\d{3,4})(\d{4})$')
print(tel_checker1.match(tel_number))
print(tel_checker1.match('0239501234'))

tel_checker = re.compile(r'^(\d{2,3})-(\d{3,4})-(\d{4})$')
m = tel_checker.match('02-123-4567')

print(m.groups())
print('group() : ', m.group())
print('group(0) : ', m.group(0))
print('group(1) : ', m.group(1))
print('group(2, 3) : ', m.group(2, 3))
print('start() : ', m.start())
print('end() : ', m.end())

cell_phone = re.compile('^(01(?:0|1|[6-9]))-(\d{3,4})-(\d{4})$')

print(cell_phone.match('010-123-4567'))
print(cell_phone.match('019-1234-5678'))
print(cell_phone.match('001-123-4567'))
print(cell_phone.match('010-1234567'))
