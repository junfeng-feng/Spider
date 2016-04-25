#encoding=utf-8
def test(li):
    li += [12]
    return li
    
li = [2,3]
print test(li)