from prawcrawlernocomment import Prawcraw
from concurrent.futures import ThreadPoolExecutor

ID = "uP8aJyccBDKnvoze4SAQrA"
SECRET = "ebZR13TAbAvp20CCt4pydqE_-RBlSA"
NAME = "YiJiang0908"
PW = "One000908."
topic = "education+learning"
topic2 = "university+college"
topic3 = "college+major"
topic4 = "study"
topic5 = "school"
topic6 = "study center"
topic7 = "university+major"
topic8 = "CSmajor"
topic9 = "course"
topic10 = "class"

pc = Prawcraw(ID, SECRET, NAME, PW)
rl1 = pc.getsubreddits(topic)
rl2 = pc.getsubreddits(topic2)
rl3 = pc.getsubreddits(topic3)
rl4 = pc.getsubreddits(topic4)
rl5 = pc.getsubreddits(topic5)
rl6 = pc.getsubreddits(topic6)
rl7 = pc.getsubreddits(topic7)
rl8 = pc.getsubreddits(topic8)
rl9 = pc.getsubreddits(topic9)
rl10 = pc.getsubreddits(topic10)
rl1.extend(rl2)
rl1.extend(rl3)
rl1.extend(rl4)
rl1.extend(rl5)
rl1.extend(rl6)
rl1.extend(rl7)
rl1.extend(rl8)
rl1.extend(rl9)
rl1.extend(rl10)
#rl6.extend(rl7)

rl = list(set(rl1))

#print("We have "+str(len(rl))+" Subreddits")

threads = []
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(pc.getdata, subreddit_name) for subreddit_name in rl]
    for future in futures:
        future.result()