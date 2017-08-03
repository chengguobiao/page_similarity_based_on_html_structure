#!usr/bin/env python
#encoding:utf-8
from __future__ import division

'''
__Author__:沂水寒城
功能：TV(Tag Vector)忽略了标签之间的顺序关系，这里将页面html清洗处理为标签的序列，接着使用
      LCTS(Longest Common Tag Subsequence)算法来计算文档对之间的最长公共标签子序列长度
'''
import os
import re
import math
import HTMLParser
import json
import numpy as np 
import lxml 
import lxml.html as HTML  
import lxml.etree as etree  
from get_all_node_xpath import *
from htmlparser_get_tags import *


common_tag_list=['html', 'head', 'body', 'div', 'title', 'link', 'comment', 'meta', 'iframe', 'ul', 'p', 'header','h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                 'a', 'form', 'li', 'span', 'style', 'label', 'table', 'frame']


common_dict={'div':'a','iframe':'b','ul':'c','p':'d','h1':'e','h2':'f','h3':'g','h4':'h','h5':'i','h6':'j','header':'k','a':'l','link':'m',
          'form':'n','head':'o','body':'p','html':'q','li':'r','title':'s','span':'t','style':'u','label':'v','table':'w','comment':'x',
          'comment()':'x','frame':'y','meta':'z'}


def construct_replace_map_dict(common_tag_list, common_dict):
    '''
    创建映射字典
    '''
    map_dict={}
    for one_tag in common_tag_list:
        temp_start='<'+one_tag+'>'
        temp_end='</'+one_tag+'>'
        if one_tag in common_dict.keys():
            map_dict[temp_start]=common_dict[one_tag]
        else:
            pass
    return map_dict


def transform_tag2_string(map_dict, tag_list):
    '''
    对输入的标签字典进行映射，变换为字符串
    '''
    new_list=[]
    for one_tag in tag_list:
        if one_tag in map_dict.keys():
            new_list.append(map_dict[one_tag])
        else:
            pass
    return ''.join(new_list)


def lcs(a, b):
    '''
    最长公共子序列
    '''
    longitud = [[0 for j in range(len(b)+1)] for i in range(len(a)+1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if x == y:
                longitud[i+1][j+1] = longitud[i][j] + 1
            else:
                longitud[i+1][j+1] = max(longitud[i+1][j], longitud[i][j+1])
    resultado = ""
    x, y = len(a), len(b)
    while x != 0 and y != 0:
        if longitud[x][y] == longitud[x-1][y]:
            x -= 1
        elif longitud[x][y] == longitud[x][y-1]:
            y -= 1
        else:
            assert a[x-1] == b[y-1]
            resultado = a[x-1] + resultado
            x -= 1
            y -= 1
    return resultado


def calculate_lcts_similarity_tag(document1, document2):
    '''
    计算两个输入的html文档之间的最长公共子序列,得到的是一个标签的序列，直接使用标签序列来计算相似度
    '''
    d1_start_tag_list, d1_end_tag_list=get_tags(document1, start_tag_list=None, end_tag_list=None)
    d1_tag_list, d1_tag_sequence=merge_two_lists(d1_start_tag_list, d1_end_tag_list)
    d2_start_tag_list, d2_end_tag_list=get_tags(document2, start_tag_list=None, end_tag_list=None)
    d2_tag_list, d2_tag_sequence=merge_two_lists(d2_start_tag_list, d2_end_tag_list)
    Common_tag_sequence=lcs(d1_tag_sequence, d2_tag_sequence)
    #Common_tag_sequence=lcs(''.join(d1_tag_sequence.split()), ''.join(d2_tag_sequence.split()))
    Common_tag_sequence_length=len(Common_tag_sequence)
    #Common_tag_sequence_length=len(Common_tag_sequence)
    max_tag_sequence_length=max(len(d1_tag_sequence), len(d2_tag_sequence))
    print '公共标签序列长度为：', Common_tag_sequence_length
    return Common_tag_sequence, Common_tag_sequence_length/max_tag_sequence_length


def calculate_lcts_similarity_string(document1, document2, map_dict):
    '''
    计算两个输入的html文档之间的最长公共子序列,对得到的标签序列进行映射变化为字符串进而计算相似度
    '''
    d1_start_tag_list, d1_end_tag_list=get_tags(document1, start_tag_list=None, end_tag_list=None)
    d1_tag_list, d1_tag_sequence=merge_two_lists(d1_start_tag_list, d1_end_tag_list)
    d2_start_tag_list, d2_end_tag_list=get_tags(document2, start_tag_list=None, end_tag_list=None)
    d2_tag_list, d2_tag_sequence=merge_two_lists(d2_start_tag_list, d2_end_tag_list)

    d1_tag_string=transform_tag2_string(map_dict, d1_tag_list)
    d2_tag_string=transform_tag2_string(map_dict, d2_tag_list)

    #Common_tag_sequence=lcs(d1_tag_sequence, d2_tag_sequence)
    Common_tag_string=lcs(d1_tag_string, d2_tag_string)
    # Common_tag_sequence_length=len(Common_tag_sequence)
    Common_tag_string_length=len(Common_tag_string)
    # max_tag_sequence_length=max(len(d1_tag_sequence), len(d2_tag_sequence))
    # return Common_tag_sequence, Common_tag_sequence_length/max_tag_sequence_length
    max_tag_string_length=max(len(d1_tag_string), len(d2_tag_string))
    print '公共标签序列字符串长度为：', Common_tag_string_length
    return Common_tag_string, Common_tag_string_length/max_tag_string_length



if __name__ == '__main__':
    map_dict=construct_replace_map_dict(common_tag_list, common_dict)

    with open('baidu.txt') as f1:

        baidu=f1.read()
    with open('jd.txt') as f2:
        jd=f2.read()
    Common_tag_sequence, lcts_similarity_tag=calculate_lcts_similarity_tag(baidu, jd)
    print Common_tag_sequence
    print 'Similarity is:', lcts_similarity_tag
    # a="curator Jacque Sauniere in D. Brown's novel The Da Vinci Code (Brown 2003, pp. 43, 60-61, and 189-192). In the Season 1 episode Sabotage (2005) of"
    # b="the television crime drama NUMB3RS, math genius Charlie Eppes mentions that the Fibonacci numbers are found in the structure of crystals and the spiral"
    #print (lcs(baidu, jd))
    print '---------------------------------------------------------------------------------'
    common_tag_string, lcts_similarity_string=calculate_lcts_similarity_string(baidu, jd)
    print common_tag_string
    print 'Similarity is:', lcts_similarity_string
