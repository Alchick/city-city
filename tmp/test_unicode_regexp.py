# coding: utf8
import re
a = u'баба с возу, кобыле легче'
patt = re.compile(u'[а-я]')
rezult = re.findall(patt, a)
print a, len(a)
print rezult
for i in rezult:
    print i.encode('utf-8')
