from Instagram.Instagram import Instagram
from time import sleep

# user = "bot124316@gmail.com"
# password = "mohabashraf123456789___"
# target = "_mohab_ashraf_0"
user = "01201287564"
password = "MohabAshraf@30121946"
target = "reta.mounir"
like = 3
comment = False
follow_account = 3
login_way = 2
with Instagram() as bot:
    bot.get_land_page()
    bot.login(way=login_way, user=user, password=password)
    bot.move_to_profile(target=target)
    bot.follow_account(choice=follow_account)
    bot.get_first_photo()
    bot.do_work(like=like, comment=comment, prev=True)
    sleep(5)