# encoding=utf-8
import re
pricePattern = re.compile(r"<b>.*?<")
string = """{"121320":{"title":"<div class=\\"num numc0\\">&nbsp;<\\/div>\\n<div class=\\"title1\\">\\n<div title=\\" \\u80af\\u5e1d\\u4e9a\\u5730\\u677f\\u65d7\\u8230\\u5e97>> \\u9500\\u552e\\" class=\\"dhidden\\"> <a isconvert=1 href=\\"http:\\/\\/kentier.tmall.com\\/\\" target=\\"_blank\\">\\u80af\\u5e1d\\u4e9a\\u5730\\u677f\\u65d7\\u8230\\u5e97>><\\/a> \\u9500\\u552e<\\/div>\\n<span class=\\"mprice\\">\\uffe599<\\/span>\\n<div class=\\"clear\\"><\\/div>\\n<\\/div>\\n<div class=\\"titles2\\">\\n<div title=\\"\\u8fd0\\u8425\\uff1a\\u6c5f\\u82cf\\u80af\\u5e1d\\u4e9a\\u6728\\u4e1a\\u6709\\u9650\\u516c\\u53f8\\" class=\\"title2 dhidden\\">\\u8fd0\\u8425\\uff1a\\u6c5f\\u82cf\\u80af\\u5e1d\\u4e9a\\u6728\\u4e1a\\u6709\\u9650\\u516c\\u53f8<\\/div>\\n<em class=\\"salez\\">7.9\\u6298<\\/em>\\n<div class=\\"clear\\"><\\/div>\\n<\\/div>\\n","btn":" <div class=\\"item buy-btn\\"><a isconvert=\\"1\\" href=\\"http:\\/\\/detail.tmall.com\\/item.htm?id=37718654633\\" class=\\"b-btn\\" target=\\"_blank\\"><b>79.00<\\/b><\\/a><\\/div>\\n"}}"""

match = pricePattern.search(string)
print match.group()[3:-1]
