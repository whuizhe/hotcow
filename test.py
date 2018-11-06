import re
import requests
"""
S 卖盘
B 买盘
M 中性盘
"""
S1, S2 = 0, 0
B1 ,B2 = 0 ,0
M1, M2 = 0, 0
for i in range(0, 101):
    url_open = requests.get(f'http://stock.gtimg.cn/data/index.php?appn=detail&action=data&c=sh603032&p={i}')
    url_info = url_open.text
    if url_info:
        a = re.search('\".*\"', url_info)
        for m in a.group().replace('"', '').split('|'):
            ms = m.split('/')
            if i == 0 and ms[0] == '0':
                continue
            if ms[-1] == 'S':
                S1 += int(ms[4]) # 手
                S2 += int(ms[5]) # 金
            elif ms[-1] == 'B':
                B1 += int(ms[4])  # 手
                B2 += int(ms[5])  # 金
            else:
                M1 += int(ms[4])  # 手
                M2 += int(ms[5])  # 金

print(S1, S2)
print(B1 ,B2)
print(M1, M2)






