"""
 wp_artical_post.py - get the ArticalPost class will post the artical to 
 the wordpress..
"""

from utils.config_manager import ConfigManager
config_obj = ConfigManager.get_instance()
config = config_obj.dataMap
from .auth import BasicAuth
import datetime
import urllib.request
import os
import json
import requests
import base64

class ArticlePost(object):
    def __init__(self):
        self.postsurl = config['wp_posts']
        self.reqsesion = requests.session()
        self.basic_auth = BasicAuth.auth

    def postarticle(self,title,categories,status,description,featurimg,url):

        if status == 'show':
            return description

        header = {
                'Content-Type' : 'application/json',
                'Authorization': 'Basic {basic_auth}'.format(basic_auth=self.basic_auth)
                }
        article = {}
        article['date'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        article['title'] = title

        article['content'] = { 
            #'rendered': '<p>%s</p>\n <h3><a href="%s">To Read More ...</a></h3>' % (description,url), 
            'raw':  description,
            'protected': False,
            'rendered': description 
            }

        article['status'] = status
        article['featured_media'] = featurimg
        article['author'] = '1'
        article['categories'] = categories
         
        article=json.dumps(article)
        #print (article)
        

        postarticle = self.reqsesion.post(
            url=self.postsurl, 
            headers=header, 
            data=article,
            auth=(config['wp_username'],config['wp_password'])
        )

        print(postarticle.status_code)
        if postarticle.status_code == 200 or postarticle.status_code == 201:
            return json.loads(postarticle.text)
        return str({'status': 'Failed to post article'})
        
