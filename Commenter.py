# imports
import random
from time import sleep

from instapy import InstaPy
from instapy import smart_run

from instapy.comment_util import verify_commenting, comment_image
from instapy.like_util import check_link
from instapy.util import highlight_print, web_address_navigator
from selenium import webdriver
from pynput.keyboard import Key, Controller

# login credentials
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains

insta_username = ''
insta_password = ''

# get an InstaPy session!
# set headless_browser=True to run InstaPy in the background
session = InstaPy(username=insta_username,
                  password=insta_password,
                  headless_browser=False)

def get_comment_btn(browser):
    comment_input = browser.find_elements_by_xpath('//form/button')
    return comment_input

def interaction(session, url):
    if session.aborting:
        return session

    message = "Starting to interact by given URL..."
    highlight_print(session.username, message, "feature", "info", session.logger)

    commented = 0

    if "https://www.instagram.com/p/" not in url:
        url = "https://www.instagram.com/p/" + url

    session.logger.info("--> {}".format(url.encode("utf-8")))

    try:
        inappropriate, user_name, is_video, reason, scope = check_link(
            session.browser,
            url,
            session.dont_like,
            session.mandatory_words,
            session.mandatory_language,
            session.is_mandatory_character,
            session.mandatory_character,
            session.check_character_set,
            session.ignore_if_contains,
            session.logger,
        )

        web_address_navigator(session.browser, url)

        if session.delimit_commenting:
            (
                session.commenting_approved,
                disapproval_reason,
            ) = verify_commenting(
                session.browser,
                session.max_comments,
                session.min_comments,
                session.comments_mandatory_words,
                session.logger,
            )
        if session.commenting_approved:
            comment_state, msg = comment_image(
                session.browser,
                user_name,
                session.comments,
                session.blacklist,
                session.logger,
                session.logfolder,
            )

            comment_btn = get_comment_btn(session.browser)

            ActionChains(session.browser) \
                .move_to_element(comment_btn[0]) \
                .click() \
                .perform()

            if comment_state is True:
                commented += 1
        else:
            session.logger.info(disapproval_reason)


    except NoSuchElementException as err:
        session.logger.error("Invalid Page: {}".format(err))


with smart_run(session):
    """ Activity flow """
    # general settings
    # get my followers
    #followers = session.grab_followers(username=insta_username, amount="full", live_match=True, store_locally=True)  # amount="full", live_match=True,
    followers = session.grab_following(username=insta_username, amount="full", live_match=True, store_locally=True)
    #print(followers)
    # session.set_do_like(enabled=False)
    # session.set_do_follow(enabled=False)
    # session.set_do_comment(enabled=True, percentage=100)
    #
    for i in range(0, len(followers), 2):
        print('@'+followers[i]+'  @'+followers[i+1]+'\n')
        session.set_comments(['@'+followers[i]+' @'+followers[i+1]])
        interaction(session,"https://www.instagram.com/p/CEsN-vHHBBt/")
        sleep(random.randint(20, 30))
    #   session.interact_by_URL(urls=["https://www.instagram.com/p/CEsN-vHHBBt/"])
    #     sleep(15)


