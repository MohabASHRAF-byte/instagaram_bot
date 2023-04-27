def get_login_way():
    x = int(input("Enter login with \n"
                  "1 - UserName and password \n"
                  "2 - Facebook\n"))
    return x


def get_user_and_password():
    x = input("Enter user name\t")
    xx = input("Enter password\t")
    return x, xx


def get_target_account():
    x = input("Enter the user you want\t")
    return x


def get_like():
    print(
        'choose option\n'
        '1 - like all photos \n'
        '2 - unlike all photos \n'
        '3 - keep like state for all photos \n'
    )
    x = int(input())
    return x


def get_follow():
    print(
        'choose option\n'
        '1 - follow account\n'
        '2 - unfollow account\n'
        '3 - keep follow state\n'
    )
    x = int(input(""))
    return x


def get_comment():
    print(
        'make comment ?\n'
        '1 - yes\n'
        '2 - no\n'
    )
    x = int(input())
    if x == '1':
        return True
    return False


def get_download_state():
    print(
        'download all photos\n'
        '1 - yes\n'
        '2 - no\n'
    )
    x = int(input())
    if x == '1':
        return True
    return False
