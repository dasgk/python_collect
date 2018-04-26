# -*- coding: utf-8 -*-
import redis
from scrapy.utils.project import get_project_settings
class CsdnBlogRedis(object):
    def redis_sadd(key,value):
        settings = get_project_settings()
        r = redis.Redis(host=settings['REDIS_HOST'], port=settings['REDIS_PORT'])
        # 处理文章详情
        r.sadd(key, value)
    def redis_sismember(key,value):
        settings = get_project_settings()
        r = redis.Redis(host=settings['REDIS_HOST'], port=settings['REDIS_PORT'])
        # 处理文章详情
        return  r.sismember(key, value)