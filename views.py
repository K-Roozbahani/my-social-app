from manage import ProfileManager


def login(operation=None):
    profile = None
    is_exist = False
    if operation not in ('1', '2'):
        return False
    elif operation == '1':
        is_exist = True

    try:
        profile = ProfileManager(is_exist)
    except Exception:
        return False

    return profile


def maine():
    user_profile = None
    print('welcome to my app.')

    # login
    operation = input('\nif you have a account enter(1):\n'
                      ' else enter(2) for sing up: ')
    user_profile = login(operation)
    while not user_profile:
        operation = input('\nif you have a account enter(1):\n'
                          ' else enter(2) for sing up: ')
        user_profile = login(operation)

    # start working

    while True:
        operation = input('next post = 1\n'
                          'back post = 2\n'
                          'like = 3\n'
                          'search people = 4'
                          'exit() = 5\n')
        if operation == 1:
            pass
        elif operation == 2:
            pass
        elif operation == 3:
            pass
        elif operation == 4:
            pass
        elif operation == 5:
            break



maine()
