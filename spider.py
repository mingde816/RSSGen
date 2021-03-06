# !/usr/bin/env python
# -*- coding:utf-8 -*-

import leancloud, auth
from datetime import datetime, timedelta
from leancloud import Object, Query, LeanCloudError
from lib import PyRSS2Gen
import recipe

Feed = Object.extend('FeedItem')
TestFeed = Object.extend('TestFeedItem')
FeedInfo = Object.extend('FeedInfo')
DebugLog = Object.extend('DebugLog')

def get_info(name):
    query = Query(FeedInfo).equal_to('name', name)
    try: info = query.first()
    except LeanCloudError, e:
        if e.code == 101:
            info = FeedInfo()
            info.set('name', name)
        else: raise(e)
    return info

def save_data(data):
    try: data.save()
    except LeanCloudError, e: print "Save feed error: %s" % str(e)

def set_feed_data(item, name, data):
    item = item()
    item.set('name', name)
    item.set('title', data[0])
    item.set('time', data[1])
    item.set('link', data[2])
    item.set('content', data[3])
    save_data(item)

def save_rss(name, recipe, item):
    info = get_info(name)
    rss = recipe(info=info)
    print('Spider %s' % name)
    count = 0
    for data in rss.get_item():
        count += 1
        set_feed_data(item, name, data)
    print('Spider over, add %s new feed' % count)
    if count > 0: save_data(info)
    if len(rss.log) == 0: return
    log = DebugLog()
    log.set('name', name)
    for key,value in rss.log: log.set(str(key), value)
    save_data(log)

def save():
    for r in rss_list():
        try: save_rss(r.name,r,Feed)
        except Exception as e: print('save %s fail : %s' % (r.name, str(e)))

def force_save(feed_name=None):
    for r in rss_list(all_feed=True):
        name = r.name
        if feed_name and feed_name != name: continue
        try: save_rss(r.name,r,Feed)
        except Exception as e: print('save %s fail : %s' % (r.name, str(e)))

def test_save(feed_name=None):
    for r in rss_list(all_feed=True):
        name = r.name
        if feed_name and feed_name != name: continue
        save_rss(name,r,TestFeed)

def rss_list(all_feed=False):
    if all_feed: return set(recipe.recipe_list)
    else: return (set(recipe.recipe_list) ^ set(recipe.hide_list))

def get_all_feed(name):
    query = Query(Feed)
    query.equal_to('name', name).descending("time")
    return query.find()

def show(name):
    rss = PyRSS2Gen.RSS2(title=name,link="https://github.com/miaowm5",description="RSSGen By Miaowm5")
    for e in get_all_feed(name):
        title = e.get('title')
        time = e.get('time')
        time = datetime(*(time.utctimetuple()[0:6]))
        link = e.get('link')
        content = e.get('content')
        item = PyRSS2Gen.RSSItem(title=title,pubDate=time,
          link=link,description=content)
        rss.items.append(item)
    return rss.to_xml(encoding='utf-8')

def clear():
    for r in rss_list():
        name = r.name
        oldest = datetime.now() - timedelta(days=r.oldest)
        remove = []
        query = Query(Feed)
        query.equal_to('name', name).less_than("time", oldest)
        for e in query.find():
            print('delete old feed: %s (%s)' % (e.get('title').encode('utf-8'), e.get('time')))
            e.destroy()