#encoding=utf-8
'''
Created on 2016年5月1日

@author: fengjunfeng
'''
import pprint
if __name__ == '__main__':
    maxPageDict = {}
    for line in file("pages.list"):
        if line.find("pageNumber") == -1:
            continue
        line = line.replace("：", ":")
        line = line.strip().split()
        line = line[1:]
#         print line
        cityNo = line[0].split(":")[1].strip(",")
        maxPageNo = line[1].split(":")[1]
        
        if cityNo in maxPageDict and  int(maxPageDict[cityNo]) < int(maxPageNo):
            maxPageDict[cityNo] = maxPageNo
        else:
            maxPageDict[cityNo] = maxPageNo
            
    pprint.pprint( maxPageDict)
    pass