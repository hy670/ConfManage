import os
import IPy


class regular:
    denyregularlist= []
    f =open('./regular/regular.txt','r')
    for line in f:
        regular = line.strip().split(" ")
        print(regular)
    f.close()








