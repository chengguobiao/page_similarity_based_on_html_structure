#!usr/bin/env python
#encoding:utf-8
from __future__ import division

'''
__Author__:沂水寒城
Common paths shingle
功能：使用Shingle算法来处理页面的xpath路径，之后计划使用Jaccard系数来计算文档对之间的相似度
'''

import math 
from get_all_node_xpath import *
from page_shot import *
from count_labels import *

def tv_distance(document1, document2):
    '''
    输入为两个html文档
    输出为距离
    '''
    distance=0
    distance1=0
    distance2=0
    tag_dict1=count_labels_func(document1)
    tag_dict2=count_labels_func(document2)
    for key in tag_dict1:
        distance1+=math.pow(tag_dict1[key], 2)
        distance2+=math.pow(tag_dict2[key], 2)
        distance+=math.pow((tag_dict1[key]-tag_dict2[key]), 2)
    # print tag_dict1
    # print tag_dict2
    one=math.pow(distance1, 0.5)
    two=math.pow(distance2, 0.5)
    # return math.pow(distance, 0.5), one, two
    return 1-math.pow(distance, 0.5)/max(one, two)


if __name__ == '__main__':
    with open('baidu.txt') as baidu:
        document1=baidu.read()
    with open('jd.txt') as jd:
        document2=jd.read()
    # distance, one, two=tv_distance(document1, document2)
    similarity=tv_distance(document1, document2)
    print similarity