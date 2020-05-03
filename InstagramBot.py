from selenium import webdriver
from time import sleep
import os

class CheckInsta:
    def __init__(self, usr, pwd):
        self.driver = webdriver.Chrome()
        self.usr = usr
        self.driver.get("https://instagram.com")
        sleep(2)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]").send_keys(usr)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(pwd)
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        sleep(4)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        sleep(2)

    def get_instagram_stats(self):
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.usr)).click()
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}/following')]".format(self.usr)).click()
        following = self._get_names()
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}/followers')]".format(self.usr)).click()
        followers = self._get_names()
        
        noFollowBack = [user for user in following if user not in followers]
        notFollowing = [user for user in followers if user not in following]
        print("Followers not following you back: \n")
        print('\n'.join('{} : {}'.format(*k) for k in enumerate(noFollowBack, start=1)))
        print("\n")
        print("Followers you are not following back: \n")
        print('\n'.join('{} : {}'.format(*k) for k in enumerate(notFollowing, start=1)))

        self.driver.execute_script("alert('Congrats! List Outputted')")

    def _get_names(self):
        sleep(2)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]") 
        prevHeight, height = 0, 1
        while prevHeight != height:
            prevHeight = height
            sleep(1)
            height = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # closing out follower/following dialog
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button").click()
        return names

# Simply paste your usr and pwd as a string if you don't want to use Environement variables
usr = os.environ.get('INSTA_USR')
pwd = os.environ.get('INSTA_PWD')
followerBot = CheckInsta(usr, pwd)
followerBot.get_instagram_stats()