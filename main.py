from Instagram.Instagram import Instagram
from time import sleep
from Instagram.Application.Gui import *

user = '01201287564'
password = "MohabAshraf@30121946"
target = "reta.mounir"

like = 3
comment = False
follow_account = 3
login_way = 2
download_state = True
# login_way = get_login_way()
# user, password = get_user_and_password()
# target = get_target_account()
# follow_account = get_follow()
# like = get_like()
# comment = get_comment()
# download_state = get_download_state()
with Instagram() as bot:
    bot.get_land_page()
    bot.login(way=login_way, user=user, password=password)
    bot.move_to_profile(target=target)
    bot.follow_account(choice=follow_account)
    bot.get_first_photo()
    bot.do_work(like=like, comment=comment, prev=True, download=download_state)
    sleep(5)
