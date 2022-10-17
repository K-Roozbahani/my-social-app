import datetime
from datamanager import change_date_for_save as change_date


class User:
    def __init__(self, user_id, first_name, last_name, email_address, date_join=datetime.date.today()):
        self._date_join = date_join
        self._id = user_id.lower()
        self._first_name = first_name.capitalize()
        self._last_name = last_name.capitalize()
        self._email = email_address.lower()

    @property
    def date_join(self):
        return self._date_join.strftime('%x')

    @property
    def user_id(self):
        return self._id

    # @user_id.setter
    # def user_id(self, user_id):
    #     self._id = user_id.lower()

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, last_name):
        self._first_name = last_name.capitalize()

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        self._last_name = last_name.capitalize()

    @property
    def full_name(self):
        return f'{self._first_name.capitalize()} {self.last_name.capitalize()}'

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email_address):
        self._email = email_address

    def __str__(self):
        return self._id

    def __eq__(self, other):
        if self._id == other:
            return True
        else:
            return False


class Post:
    def __init__(self, user_id, title: str, context: str, publish_date=datetime.datetime.now()):
        self._publish_date = publish_date
        self._owner = user_id
        self.title = title
        self.context = context
        self._like = 0
        self._like_list = []
        try:
            date = change_date(str(publish_date))
            self.patch = f'date/{user_id}/posts/{date}'
        except:
            print('Created post but can not save.')

    @property
    def publish_date(self):
        return self._publish_date

    @property
    def owner(self):
        return self._owner

    @property
    def like(self):
        return self._like

    @like.setter
    def like(self, user_id):
        if user_id not in self._like_list:
            self._like += 1
            self._like_list.append(user_id)

        else:
            print('You already liked this post')

    @property
    def liked_by(self):
        return self._like_list

    def __str__(self):
        c = '%c'
        return f'Owner: {self.owner} publish in <{self.publish_date.strftime(c)}>\n' \
               f'{self.title}\n' \
               f'  {self.context}\n' \
               f'\U00002764 {self.like}'


class Profile:
    def __init__(self, user: User, password):
        self._user = user
        self._password = password
        self._posts = []
        self.followers = []
        self.following = []

    @property
    def date_join(self):
        return self._user.date_join

    @property
    def user_id(self):
        return self._user.user_id

    @property
    def user(self):
        return self._user

    @property
    def full_name(self):
        return self._user.full_name

    @property
    def password(self):
        return str(self._password).strip()

    @property
    def view_profile(self):
        up_down = 'profile:\n' + '_' * 50 + '\n'
        profile = up_down + f'\t{self._user.user_id}\n\t{self._user.full_name}\n' \
                            f'\tPosts: {len(self.posts)}  Followers: {len(self.followers)}' \
                            f'   Following: {len(self.following)}' + '\n' + '_' * 50

        return profile

    @property
    def posts(self):
        return self._posts

    def add_new_post(self, new_post: Post):
        self._posts.append(new_post)

    def follow(self, user_id):
        if user_id not in self.following:
            self.following.append(user_id)
        # add to follower lists user_id

    def unfollow(self, user_id):
        if user_id not in self.following:
            raise FileNotFoundError('user does not exist')
        self.following.remove(user_id)

