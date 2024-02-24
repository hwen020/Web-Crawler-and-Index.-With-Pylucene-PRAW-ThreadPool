import praw
import json
from prawcore.exceptions import Forbidden
LIMIT = 1000
class Prawcraw:
    def __init__(self, ID, SECRET, NAME, PW):
        # Authorized Reddit Instances
        self.reddit = praw.Reddit(client_id = ID,
                                  client_secret = SECRET,
                                  user_agent = "cs242projcectGroup7 v1.0 (by /u/YiJiang0908)",
                                  username = NAME,
                                  password = PW)
    
    def getsubreddits(self, TOPIC):
        # Search about our topic and get the list of subreddits about our topic
        params = {'limit':LIMIT}
        sublist = []
        relate_subreddits = self.reddit.subreddits.search(TOPIC, **params)
        for sub_name in relate_subreddits:
            sublist.append(sub_name)
        # print (len(sublist))
        # here return will be a list of instances
        return sublist
    
    def getsubname(self, TOPIC):
        params = {'limit':LIMIT}
        namelist = []
        relate_subreddits = self.reddit.subreddits.search(TOPIC, **params)
        for sub_name in relate_subreddits:
            namelist.append(sub_name.display_name)
        #print(namelist)
        # here return will be a list of instances
        return namelist
    
    # get posts with tag(hot, controversial) from an instance
    def getposts(self, subname, tag):
        # sub name is an instance from getsubreddits()
        if tag == "hot":
            posts = subname.hot(limit=LIMIT)
        elif tag == "controversial":
            posts = subname.controversial(time_filter="year", limit=LIMIT)
        else:
            raise ValueError("Invalid category. Choose 'controversial' or 'hot'.")
        
        postlist = []
        try:
            for post in posts:
                postdict = {"id":post.id, 
                            "title":post.title, 
                            "selftext":post.selftext, 
                            "score":post.score, 
                            "url":post.permalink, 
                            "hyperlink":post.url
                            }
                postlist.append(postdict)
            return postlist
        except:
            print("not work beacuse of praw's limitation")
            return []
    
    def getdata(self, subredditinstance):
        postlist = []
        hotposts = self.getposts(subredditinstance, 'hot')
        for eachhpost in hotposts:
            postlist.append(eachhpost)
        conpost = self.getposts(subredditinstance, 'controversial')
        for eachcpost in conpost:
            if eachcpost not in postlist:
                postlist.append(eachcpost)
        fn = "RedditData/"+ subredditinstance.display_name + ".json"
        with open(fn, 'w', encoding='utf-8',newline='\n') as fw:
            json.dump(postlist, fw, indent=1, ensure_ascii=False)
        fw.close()
        