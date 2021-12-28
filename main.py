import praw
import urllib.request
import os
import pandas as pd
import datetime

class RedditCollector:
    #a constructor to establish connection with reddit api
    def __init__(self, client_id, client_secret, user_agent, subreddits_list,limit, username, password):
    
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.subreddits_list = subreddits_list
        self.limit=limit
        self.reddit = praw.Reddit(client_id = self.client_id, client_secret = self.client_secret, user_agent = self.user_agent, username=username, password=password)
        print ('>>> Reddit User: ', self.reddit.user.me())


    def collect_data(self):
        print("fectching data:>>>>\n\n")
        allowed_image_extensions = ['.jpg', '.jpeg', '.png']
       
        self.image_urls = []
        self.image_titles = []
        self.image_scores = []
        self.image_timestamps = []
        self.image_ids = []

        self.txt_urls = []
        self.txt_titles = []
        self.txt_scores = []
        self.txt_timestamps = []
        self.txt_ids = []

        subreddit=self.reddit.subreddit(self.subreddits_list)
        posts=subreddit.hot(limit=self.limit)
        for post in posts:
            _, ext = os.path.splitext(post.url)
        
            if ext in allowed_image_extensions:
                self.image_urls.append(post.url.encode('utf-8'))
                self.image_titles.append(post.title.encode('utf-8'))
                self.image_scores.append(post.score)
                self.image_timestamps.append(datetime.datetime.fromtimestamp(post.created))
                self.image_ids.append(post.id)
            elif post.is_self:
                self.txt_urls.append(post.url.encode('utf-8'))
                self.txt_titles.append(post.title.encode('utf-8'))
                self.txt_scores.append(post.score)
                self.txt_timestamps.append(datetime.datetime.fromtimestamp(post.created))
                self.txt_ids.append(post.id)
        self.save_data(subreddit)
    

    def save_data(self,subreddit):
        print ('>>> Writing ', subreddit, ' data to disk... \n\n')
        print(len(self.txt_ids))
        dirpath = os.path.join('./', "ProgrammingHumour")
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)

        allowed_image_extensions = ['.jpg', '.jpeg', '.png']
        
        
        if len(self.image_ids) > 0:
            images_path = os.path.join(dirpath, 'images/')
            if not os.path.exists(images_path):
                os.mkdir(images_path)
        
        if len(self.txt_ids) > 0:
            txt_path = os.path.join(dirpath, 'txt/')
            if not os.path.exists(txt_path):
                os.mkdir(txt_path)
        img_list=[i.decode('utf-8') for i in self.image_urls]
        for index, url in enumerate(img_list):
            _, ext = os.path.splitext(url)
            
            
            if ext in allowed_image_extensions:
                try:
                    print ('>>> downloading ', img_list[index], ' in ', images_path + (self.image_titles[index]).decode('utf-8') + ext)
                    urllib.request.urlretrieve(img_list[index], images_path + (self.image_titles[index]).decode('utf-8') + ext)
                except:
                    print(">> Something error occured while downloading the file")

        self.export_to_csv(dirpath=dirpath)
        print ("\n>>> Done writing data !!! \n\n")

    def export_to_csv(self,dirpath):
        print("exporting data")
        if len(self.image_ids) > 0:
            images_path = os.path.join(dirpath, 'images', 'images.csv')
            dataframe = pd.DataFrame({
                'Title': self.image_titles,
                'Score': self.image_scores,
                'Url': self.image_urls,
                'Timestamp': self.image_timestamps,
                'ID': self.image_ids
            })
        csv = dataframe.to_csv(images_path, index=True, header=True)


        if len(self.txt_ids) > 0:
            txt_path = os.path.join(dirpath, 'txt', 'txt.csv')
            dataframe = pd.DataFrame({
                'Title': self.txt_titles,
                'Score': self.txt_scores,
                'Url': self.txt_urls,
                'Timestamp': self.txt_timestamps,
                'ID': self.txt_ids
            })
        csv = dataframe.to_csv(txt_path, index=True, header=True)




reddit_info = RedditCollector(
    client_id="c77ubGOBQCoFm6m_5LfwPw",
    client_secret="7qg3iViNaCBlCdqNV7Sp4DE85anNPA",
    subreddits_list="ProgrammerHumor",
    limit=100,
    user_agent="Your user Agent",
    username="Your username",
    password="Your Password"
)
reddit_info.collect_data()

