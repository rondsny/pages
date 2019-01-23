# -*- coding:utf-8 -*-

import io
import sys
# import MySQLdb
from selenium import webdriver

browser = webdriver.Chrome()

# # 打开数据库连接
# db = MySQLdb.connect("localhost", "root", "123456", "mov", charset='utf8' )

"""
CREATE TABLE db_movies
(
    `id` INT UNSIGNED NOT NULL COMMENT 'id',
    `name` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '名称',
    `en_name` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '英文名称',
    `my_year` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '年份',
    `score` DOUBLE NOT NULL DEFAULT 0 COMMENT '分数',
    `director` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '导演',
    `writer` VARCHAR(1024) NOT NULL DEFAULT '' COMMENT '编剧',
    `actor` VARCHAR(1024) NOT NULL DEFAULT '' COMMENT '主演',
    `my_type` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '类型',
    `area` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '地区',
    `langauge` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '语言',
    `release_time` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '上映时间',
    `length` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '片长',
    `other_name` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '又名',
    `imdb` VARCHAR(255) NOT NULL DEFAULT '' COMMENT 'IMDb',
    `tags` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '常见标签',
    PRIMARY KEY(id)
) ENGINE=INNODB DEFAULT CHARSET=utf8;
"""

# info
# https://movie.douban.com/subject/26611804/

def subject(dbId, list):

    dict = {}

    name = ''
    en_name = ''
    my_year = 2018
    writer = '' ##
    actor = '' ##
    my_type = '' ##
    area = '' ##
    langauge = '' ##
    release_time = '' ##
    length = '' ##
    other_name = '' ##
    imdb = '' ##
    tags = ''
    l_tags = []

    # https://movie.douban.com/subject/30140571/
    id = dbId
    dbPath = "https://movie.douban.com/subject/%s/" % (id)
    browser.get(dbPath)
    browser.execute_script("$('span').css('display', 'inline');")

    # 导演
    elem = browser.find_element_by_xpath('//*[@id="info"]/span[1]/span[2]/a[1]')
    director = elem.text
    print(u"导演=%s" % director)

    # 编辑
    elem = browser.find_elements_by_xpath('//*[@id="info"]/span[2]/span[2]/a')
    for ele in elem:
        print(ele.text)

    # 主演
    print(u'\n主演:')
    elem = browser.find_elements_by_xpath('//*[@id="info"]/span[3]/span[2]/span[*]/a')
    for ele in elem:
        if ele.text:
            actor = actor + ele.text + " / "
            
    # 其它
    infos = browser.find_element_by_xpath('//*[@id="info"]')
    lines = infos.text.split('\n')
    for line in lines:
        # print(line.encode("GBK", 'ignore'))

        items = line.split(":")

        title = items[0].strip()
        cont  = items[1].strip()
        conts = cont.split("/")
        if title == u"编剧":
            writer = cont
        # elif title == u"主演":
        #     actor = cont
        elif title == u"类型":
            my_type = cont
        elif title == u"制片国家/地区":
            area = cont
        elif title == u"语言":
            langauge = cont
        elif title == u"上映日期":
            release_time = cont
        elif title == u"片长":
            length = cont
        elif title == u"又名":
            other_name = cont
        elif title == u"IMDb链接":
            imdb = cont

    ele = browser.find_element_by_xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong')
    score = int(ele.text)
    print(u"分数=%s" % score)
    
    ele = browser.find_element_by_xpath('//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span')
    rating = int(ele.text)
    print(u"评价人数=%s" % rating)
    
    ele = browser.find_element_by_xpath('//*[@id="content"]/h1/span[1]')
    name = ele.text
    names = name.split(" ", 1)
    if len(names)>1:
        name = names[0]
        en_name = names[1]

    ele = browser.find_element_by_xpath('//*[@id="content"]/h1/span[2]')
    my_year = float(ele.text.split('(')[1].split(')')[0])
    
    elem = browser.find_elements_by_xpath('//*[contains(@class, "tags-body")]/a')
    for ele in elem:
        if ele.text:
            val = ele.text.strip()
            tags = tags + val + " / "
            l_tags.append(val)
    
    sql = u"insert into db_movies \
    (`id`, `name`, `en_name`, `my_year`, `score`, `director`, `writer`, `actor`, `my_type`, `area`, `langauge`, `release_time`, `length`, `other_name`, `imdb`, `tags`) \
    values (%s,'%s','%s',%d,%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') on duplicate key update \
    `id`=values(`id`),\
    `name`=values(`name`),\
    `en_name`=values(`en_name`),\
    `my_year`=values(`my_year`),\
    `score`=values(`score`),\
    `director`=values(`director`),\
    `writer`=values(`writer`),\
    `actor`=values(`actor`),\
    `my_type`=values(`my_type`),\
    `area`=values(`area`),\
    `langauge`=values(`langauge`),\
    `release_time`=values(`release_time`),\
    `length`=values(`length`),\
    `other_name`=values(`other_name`),\
    `imdb`=values(`imdb`),\
    `tags`=values(`tags`) " % (id, name, en_name, my_year, score, director, writer, \
    actor, my_type, area, langauge, release_time, length, other_name, imdb, tags)

    # # 使用cursor()方法获取操作游标
    # cursor = db.cursor()
    # # 执行sql语句
    # cursor.execute(sql)
    # # 提交到数据库执行
    # db.commit()
    print(sql)
    
    l_area = []
    l_area2 = area.split('/')
    for val in l_area2:
        l_area.append(val.strip())
    
    dict["id"] = id
    dict["name"] = name
    dict["en_name"] = en_name
    dict["my_year"] = my_year
    dict["score"] = score
    dict["rating"] = rating
    dict["director"] = director
    dict["writer"] = writer
    dict["actor"] = actor
    dict["my_type"] = my_type
    # dict["l_my_type"] = l_my_type
    dict["area"] = area
    dict["l_area"] = l_area
    dict["langauge"] = langauge
    dict["release_time"] = release_time
    dict["length"] = length
    dict["other_name"] = other_name
    dict["imdb"] = imdb
    dict["tags"] = tags
    dict["l_tags"] = l_tags
    list.append(dict)

list = []
ids = [
27615441, # 网络迷踪
3878007, # 海王
20438964, # 无敌破坏王2
26147417, # 神奇动物：格林德沃之罪
3168101, # 毒液：致命守护者
26741061, # 胡桃夹子和四个王国
30140571, # 嗝嗝老师
26425063, # 无双
26636712, # 蚁人2：黄蜂女现身
26426194, # 巨齿鲨
27622447, # 小偷家族
26804147, # 摩天营救
26752088, # 我不是药神
26925317, # 动物世界
26416062, # 侏罗纪世界2
24773958, # 复仇者联盟3：无限战争
4920389, # 头号玩家
26752852, # 水形物语
20435622, # 环太平洋：雷霆再起
6390825, # 黑豹
26611804] # 三块广告牌
# ids = [6390825, 26611804]
for dbId in ids:
    subject(dbId, list)

print("list len = %s" % len(list))

totol = 0
dict_tag = {}
for item in list:
    dict_tag[item["name"]] = int(item["rating"])
    totol = totol + int(item["rating"])
#    for tag in item["l_area"]:
#       if tag in dict_tag:
#           dict_tag[tag] = dict_tag[tag] + 1
#       else:
#           dict_tag[tag] = 1


for key, val in sorted(dict_tag.items(), key=lambda item:item[1]):
    print("%s = %s" % (key, val))
print("totol = %s" % totol)
print("average = %s" % totol / 21)
# # 关闭数据库连接
# db.close()
