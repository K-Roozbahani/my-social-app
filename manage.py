import datetime
import datamanager
from models import User, Post, Profile


class ProfileManager:

    def __init__(self, already_exist=False):
        self._is_login = False
        if not already_exist:
            self._profile = self.create()
        else:
            self._profile = self._login()
        self._all_posts = datamanager.init_list_all_posts(self._profile)
        print(self._profile.view_profile)

    @classmethod
    def _check_password(cls, profile: Profile, password):
        if profile.password == password:
            print('verify password')
            return True
        else:
            print('password dose not match')
            return False

    def _login(self):
        user_id = input('username: ')
        password = (input('password: ')).strip()
        profile = []
        try:
            for data in datamanager.get_user_and_profile_generic(user_id):
                profile.append(data)

        except ValueError:
            print('User dose not exist')

        if self._check_password(profile[1], password):
            self._is_login = True
            return profile[1]
        else:
            print('password error')

    def create(self):
        print('Welcome to my app, enter your Specifications')
        user_id = input('username: ').strip()
        if datamanager.is_exist(user_id):
            raise FileExistsError('user already exist')

        first_name = input('first name: ').strip()
        last_name = input('last name: ')
        email_address = input('email address: ').strip()

        password = input('password: ')
        confirm_password = input('confirm password: ').strip()
        if password != confirm_password:
            raise ValueError('Password not match')

        user = User(user_id, first_name, last_name, email_address)
        profile = Profile(user, password)
        datamanager.save(profile, new_user=True)
        self._is_login = True
        return profile

    def find_friend(self):
        pass

    def follow(self):
        pass

    def unfollow(self):
        pass

    def add_post(self):
        title = input('title: ')
        context = input('context: ')
        new_post = Post(self._profile.user_id, title, context)
        self._profile.add_new_post(new_post)
        datamanager.add_new_post(new_post)
        print('publish new post')
        datamanager.save(self._profile, )
        datamanager.save(self._profile)

    def view_profile(self):
        print(self._profile.view_profile)
        for post in self._profile.posts:
            print(post)

    @property
    def posts(self):
        for post in self._profile.posts:
            yield str(post) + '-' * 10

    @property
    def all_posts_generic(self):
        list_posts = self._all_posts.items()
        list_posts = sorted(list_posts, reverse=True)
        for post in list_posts:
            post = datamanager.get_post(self._all_posts[post])
            yield post

