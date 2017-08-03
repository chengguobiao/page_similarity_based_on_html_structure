#!usr/bin/env python
#encoding:utf-8
from __future__ import division

'''
__Author__:沂水寒城
CTSS-----Common Tag Sequence Shingle
功能：使用Shingle算法来处理页面解析得到的标签序列，之后计划使用Jaccard系数来计算文档对之间的相似度
存在的问题：
1.在使用HTMLParser解析页面的时候出现编码错误
2.精度不够，感觉计算出来的页面相似度大都相近
'''
import os
import re
import math
import json
import numpy as np 
import lxml 
import lxml.html as HTML  
import lxml.etree as etree  
from get_all_node_xpath import *
from htmlparser_get_tags import *
from get_all_tag import get_all_tags2_list
from lcts_algorithm import *


common_tag_list=['html', 'head', 'body', 'div', 'title', 'link', 'comment', 'meta', 'iframe', 'ul', 'p', 'header','h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                 'a', 'form', 'li', 'span', 'style', 'label', 'table', 'frame']


common_dict={'div':'a','iframe':'b','ul':'c','p':'d','h1':'e','h2':'f','h3':'g','h4':'h','h5':'i','h6':'j','header':'k','a':'l','link':'m',
          'form':'n','head':'o','body':'p','html':'q','li':'r','title':'s','span':'t','style':'u','label':'v','table':'w','comment':'x',
          'comment()':'x','frame':'y','meta':'z'}



def w_shingle_slice_genetor(html, w=3):
    '''
    使用CTSS算法来处理页面的标签序列，映射为字符串后，分割单位为w，默认为3
    '''
    map_dict=construct_replace_map_dict(common_tag_list, common_dict)
    fail_count=0
    w_shingle_slice_list=[]
    w_shingle_slice_dict={}
    filter_tag_list=get_all_tags2_list(html)
    tag_content=''.join(filter_tag_list)
    start_tag_list, end_tag_list=get_tags(tag_content, start_tag_list=None, end_tag_list=None)
    tag_list, tag_sequence=merge_two_lists_space(start_tag_list, end_tag_list)
    tag_string=transform_tag2_string(map_dict, tag_list)
    for i in range(len(tag_string)-w+1):
        w_shingle_slice_list.append('/'.join(tag_string[i:i+w]))

    for one_slice in w_shingle_slice_list:  #统计标签shingle出现的频数
        if one_slice in w_shingle_slice_dict:
            w_shingle_slice_dict[one_slice]+=1
        else:
            w_shingle_slice_dict[one_slice]=1
    print fail_count
    return list(set(w_shingle_slice_list)), w_shingle_slice_dict  #对结果去重


def w_shingle_slice_genetor_test(html, w=3):
    '''
    使用CTSS算法来处理页面的标签序列，分割单位为w，默认为3
    '''
    fail_count=0
    w_shingle_slice_list=[]
    w_shingle_slice_dict={}
    filter_tag_list=get_all_tags2_list(html)
    tag_content=''.join(filter_tag_list)
    # try:
    #     start_tag_list, end_tag_list=get_tags(html, start_tag_list=None, end_tag_list=None)
    #     tag_list, tag_sequence=merge_two_lists_space(start_tag_list, end_tag_list)
    #     tag_list=tag_sequence.split(' ')
    #     for i in range(len(tag_list)-w+1):
    #         w_shingle_slice_list.append('/'.join(tag_list[i:i+w]))
    # except:
    #     fail_count+=1
    start_tag_list, end_tag_list=get_tags(tag_content, start_tag_list=None, end_tag_list=None)
    tag_list, tag_sequence=merge_two_lists_space(start_tag_list, end_tag_list)
    tag_list=tag_sequence.split(' ')
    for i in range(len(tag_list)-w+1):
        w_shingle_slice_list.append('/'.join(tag_list[i:i+w]))
    # htree, all_xpath_list=get_clean_allnodes_xpath(html)  #得到页面html的xpath列表
    # new_list, pattern_xpath_list=get_page_tree_xpath(all_xpath_list)  #对得到的xpath列表去除[*]和()返回模式路径列表
    # print '--------------------------------------------------------------------------'
    # print pattern_xpath_list
    # for one_new_xpath in pattern_xpath_list:
    #     for i in range(len(one_new_xpath)-w+1):
    #         w_shingle_slice_list.append('/'.join(one_new_xpath[i:i+w]))  #将标签结点以'/'连接成一个字符串
    for one_slice in w_shingle_slice_list:  #统计标签shingle出现的频数
        if one_slice in w_shingle_slice_dict:
            w_shingle_slice_dict[one_slice]+=1
        else:
            w_shingle_slice_dict[one_slice]=1
    print fail_count
    return list(set(w_shingle_slice_list)), w_shingle_slice_dict  #对结果去重


def Jaccard_similarity(document1, document2):
    '''
    使用Jaccard系数来计算文档对之间的相似度
    输入为：两个文档经过上述处理之后形成的标签shingle列表
    输出为：相似度
    '''
    common_shingles_list=list(set(document1)&set(document2))
    total_shingles_list=document1+document2
    total_shingles_num=len(total_shingles_list)
    max_shingles_num=max(len(document1), len(document2))
    common_shingles_num=len(common_shingles_list)
    simple_similarity=common_shingles_num/max_shingles_num
    original_similarity=common_shingles_num/total_shingles_num
    return simple_similarity, original_similarity


def main_test(sourcefile='task/filepath.json', resultfile='result/CTSS.txt'):
    '''
    读取任务文件计算相似度写入结果文件中
    '''
    resultfile=open(resultfile, 'w')
    with open(sourcefile) as f:
        task_list=json.load(f)
    for one_task in task_list:
        one_url=one_task['url'].strip()
        one_path=one_task['path']
        try:
            with open(one_path) as op:
                one_html=op.read().decode('utf-8')
            one_page_list, one_page_dict=w_shingle_slice_genetor(one_html, w=3)
            for two_task in task_list:
                two_url=two_task['url'].strip()
                two_path=two_task['path']
                with open(two_path) as tp:
                    two_html=tp.read()        
                two_page_list, two_page_dict=w_shingle_slice_genetor(two_html, w=3)
                simple_similarity, original_similarity=Jaccard_similarity(one_page_list, two_page_list)
                line=one_url+'///'+two_url+'----->'+str(simple_similarity)+','+str(original_similarity)
                resultfile.write(line+'\n')
        except:
            print one_path
    resultfile.close()



if __name__ == '__main__':
    with open('baidu.txt') as f:
        html=f.read()
    w_shingle_slice_list, w_shingle_slice_dict=w_shingle_slice_genetor(html, w=3)
    # print '---------------------------------------------------------------------------------------'
    # print w_shingle_slice_list
    # print w_shingle_slice_dict
    main_test(sourcefile='task/filepath.json', resultfile='result/CTSS.txt')
    print '***********************************************结束了************************************************'