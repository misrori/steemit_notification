#!/home/mihaly/hadoop/anaconda3/bin/python
import feedparser
import itertools
import pickle
import os.path
import smtplib
#https://stackoverflow.com/questions/882712/sending-html-email-using-python
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def flattern(A):
    rt = []
    for i in A:
        if isinstance(i,list): rt.extend(flattern(i))
        else: rt.append(i)
    return rt

def get_links(name):
    my_url = 'https://streemian.com/rss/@'+name
    feed = feedparser.parse( my_url )
    return([f['id'] for f in feed['items'] ])


# In[6]:

# read the users
with open('/home/mihaly/PYTHON/steem_notification/names.txt', 'r') as fp:
    nevek=fp.readline().replace('\n', '').split(', ')

# read_hist_linkek
#check if a file is exist 

if os.path.exists('/home/mihaly/PYTHON/steem_notification/history_data'):
    with open ('/home/mihaly/PYTHON/steem_notification/history_data', 'rb') as fp:
        hist_link = pickle.load(fp)
else:
    with open('/home/mihaly/PYTHON/steem_notification/history_data', 'wb') as fp:
        hist_link =['']
        pickle.dump(hist_link, fp) 


# In[7]:

my_links=[]
for i in nevek:
    my_links.append(get_links(i))
my_links = [val for sublist in my_links for val in sublist]


# In[8]:

new_posts = list(set(my_links) - set(hist_link))
print('There are '+ str(len(new_posts))+ ' new posts')


# In[9]:

if len(new_posts) !=0:
    hist_link.append(new_posts)

    vege = flattern(hist_link)
    #write
    with open('/home/mihaly/PYTHON/steem_notification/history_data', 'wb') as fp:
        pickle.dump(vege, fp)


# In[33]:

if len(new_posts) !=0:
    import smtplib

    from email.message import EmailMessage
    from email.headerregistry import Address
    from email.utils import make_msgid

    # Create the base text message.
    msg = EmailMessage()
    me = "steemit@lan5025.com"
    you = "ormraat.pte@gmail.com"

    msg['Subject'] = "New posts"
    msg['From'] = Address("Steemit", "steemit")
    msg['To'] = Address("Orsos Mihaly", "ormraat.pte@gmail.com")

    msg.set_content("This is a new post : \n "+("\n".join(new_posts).replace('streemian', 'steemit')))
    s = smtplib.SMTP('localhost')

    s.send_message(msg)
    s.quit()


