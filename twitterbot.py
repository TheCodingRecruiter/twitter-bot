import time
from selenium import webdriver
import configparser
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

config = configparser.ConfigParser()
config.read('../config/config.ini')
twittername = config['twitter']['user']
twitterpassword = config['twitter']['passw']

class TwitterBot:
    def __init__(self, username, password):
        self.twitterusername = username
        self.twitterpassword = password
        self.bot = webdriver.Chrome()

    def login(self):
        bot = self.bot
        bot.get('https://twitter.com/login')
        username = ''
        while not username:
            try:
                username = bot.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[1]/form/fieldset/div[1]/input')
                time.sleep(2)
                username.send_keys(self.twitterusername)
                password = bot.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[1]/form/fieldset/div[2]/input')
                time.sleep(1)
                password.send_keys(self.twitterpassword)
                time.sleep(1)
                bot.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[1]/form/div[2]/button').click()
                time.sleep(5)
            except:
                continue
    
    def get_tweet(self, hashtag, pages):
        bot = self.bot
        new_url = 'https://twitter.com/hashtag/x?f=live'
        new_url = new_url.split('x')
        new_url = (new_url[0] + hashtag + new_url[1])
        bot.get(new_url)
        time.sleep(8)
        link_tweets = []
        for i in range(1, pages):
            bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(4)
            tweets = bot.find_elements_by_css_selector('a.css-4rbku5.css-18t94o4.css-901oao.r-1re7ezh.r-1loqt21.r-1q142lx.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-3s2u2q.r-qvutc0')
            links = [elem.get_attribute('href') for elem in tweets]
            time.sleep(2)
            for link in links:
                link_tweets.append(link)
        
        return link_tweets

    def like_tweet(self, tweet):
        bot = self.bot
        for i in tweet:
            bot.get(i)
            try:
                time.sleep(4)
                crhs = bot.find_elements_by_css_selector('svg.r-4qtqp9.r-yyyyoo.r-50lct3.r-dnmrzs.r-bnwqim.r-1plcrui.r-lrvibr.r-1srniue')
                like = crhs[2]
                like.click()
                time.sleep(10)
            except Exception as ex:
                print(f'Error {ex}')
                time.sleep(4)

    def retweet_tweet(self, tweet):
        bot = self.bot
        for i in tweet:
            bot.get(i)
            try:
                time.sleep(4)
                crhs = bot.find_elements_by_css_selector('svg.r-4qtqp9.r-yyyyoo.r-50lct3.r-dnmrzs.r-bnwqim.r-1plcrui.r-lrvibr.r-1srniue')
                retweet = crhs[1]
                retweet.click()
                time.sleep(.5)
                bot.find_element_by_css_selector('div.css-1dbjc4n.r-1loqt21.r-18u37iz.r-1j3t67a.r-9qu9m4.r-o7ynqc.r-1j63xyz.r-13qz1uu').click()
                time.sleep(10)
            except Exception as ex:
                print(f'Error {ex}')
                time.sleep(4)

    def comment_tweet(self, tweet, message):
        bot = self.bot
        for i in tweet:
            bot.get(i)
            try:
                time.sleep(4)
                crhs = bot.find_elements_by_css_selector('svg.r-4qtqp9.r-yyyyoo.r-50lct3.r-dnmrzs.r-bnwqim.r-1plcrui.r-lrvibr.r-1srniue')
                comment = crhs[0]
                comment.click()
                time.sleep(1)
                comment_box = bot.find_element_by_css_selector('div.notranslate.public-DraftEditor-content')
                comment_box.send_keys(message)
                bot.find_element_by_css_selector('div.css-18t94o4.css-1dbjc4n.r-urgr8i.r-42olwf.r-sdzlij.r-1phboty.r-rs99b7.r-1w2pmg.r-1n0xq6e.r-1vuscfd.r-1dhvaqw.r-1fneopy.r-o7ynqc.r-6416eg.r-lrvibr').click()
                time.sleep(10)
            except Exception as ex:
                print(f'Error {ex}')
                time.sleep(4)



#EXAMPLES BELOW#

dj = TwitterBot(twittername, twitterpassword)
dj.login()
position = dj.get_tweet('python', 2)
dj.like_tweet(position)
dj.retweet_tweet(position)
dj.comment_tweet(position, 'Are you interested in a python developer opportunity that I have available right now?')

