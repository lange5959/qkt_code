# coding=utf-8


dict = {u"大": u"我们的python学习"}
print dict
# {'asdf': '\xe6\x88\x91\xe4\xbb\xac\xe7\x9a\x84python\xe5\xad\xa6\xe4\xb9\xa0'}
import json
print json.dumps(dict, encoding="UTF-8", ensure_ascii=False)




# a = '大'.decode('utf-8')
# print 'a:  ' , a,type(a)
# print dict[a], type(dict[a])

# print dict['大'] == "我们的python学习"


# print dict.decode("unicode-escape").encode("utf-8")



