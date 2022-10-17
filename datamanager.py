import datetime

from models import User, Post, Profile
import os


def search_generic():
    with open('data/users.txt', 'r') as users:
        for user in users:
            yield user.strip()


def is_exist(user):
    if user in search_generic():
        return True
    return False


def get_post(patch):
    with open(patch, 'r') as file:
        user_id = file.readline().strip()
        date = file.readline().strip()
        title = file.readline().strip()
        context = file.readline().strip()
        new_post = Post(user_id, title, context, create_time(date))
        like = file.readline()
        for i in range(int(like)):
            new_post.like = file.readline().strip()
        return new_post


def get_user_and_profile_generic(user_id):
    if user_id not in search_generic():
        raise ValueError('user does not exist')
    with open(f'data/{user_id}/profile.txt') as f:
        # get user
        line_1 = f.readline().split(', ')
        date = line_1[3].split('/')
        date_join = datetime.date(year=int(date[0]), month=int(date[1]), day=int(date[2]))
        user = User(user_id=user_id,
                    first_name=line_1[1].split()[0],
                    last_name=line_1[1].split()[1],
                    email_address=line_1[2],
                    date_join=date_join
                    )
        yield user
        password = line_1[4]
        profile = Profile(user, password)

        # read posts
        post_list = os.listdir(f'data/{user_id}/posts/')
        for patch_post in post_list:
            post = get_post(f'data/{user_id}/posts/{patch_post}')
            profile.add_new_post(post)

        yield profile


def change_date_for_save(date_str: str):
    date_str = date_str.replace('.', '-')
    date_str = date_str.replace(' ', '_')
    date_str = date_str.replace(':', '-')
    return date_str


def create_time(date_str: str):
    date_str = date_str.split()
    date = date_str[0].split('-')
    time = date_str[1].split(':')
    date_time = datetime.datetime(year=int(date[0]), month=int(date[1]),
                                  day=int(date[2]), hour=int(time[0]),
                                  minute=int(time[1]), second=int(time[2].split('.')[0]),
                                  microsecond=int(time[2].split('.')[1])
                                  )
    return date_time


def save(profile: Profile, new_user=False):
    user = profile.user
    mod = 'w'
    if new_user and os.path.exists(f'data/{profile.user}'):
        os.remove(f'data/{profile.user}')

    if new_user:
        os.mkdir(f'data/{profile.user}')
        os.mkdir(f'data/{profile.user}/posts')
        mod = 'x'
    with open(f'data/{profile.user}/profile.txt', mod) as file:
        file.write(f'{user.user_id}, {user.full_name}, {user.email}, '
                   f'{user.date_join}, {profile.password}')
        # posts
        file.write(f'\n{str(len(profile.posts))}')
        posts_list = os.listdir(f'data/{user.user_id}/posts/')
        posts_list = ', '.join(posts_list)
        file.writelines(f'\n{posts_list}')

        # flowers
        file.writelines(f'\n{len(profile.followers)}')
        followers = ', '.join(profile.followers)
        file.write(f'\n{followers}')

        # following
        file.write(f'\n{profile.following}')
        following = ', '.join(profile.following)
        file.write(f'\n{following}')

    if os.path.exists('data/users.text') and is_exist(user.user_id):
        print('loading...')
    elif os.path.exists('data/users.text') and not is_exist(user.user_id):
        with open('data/users.text', 'a') as file:
            file.write(user.user_id)
            print('joined user')
    else:
        with open('data/users.txt', 'a') as file:
            file.write(user.user_id)
            print('create file and joined user')


def add_new_post(post: Post):
    name = change_date_for_save(str(post.publish_date))
    with open(f'data/{post.owner}/posts/{name}.txt', 'x') as file:
        file.write(post.owner + '\n')
        file.write(str(post.publish_date) + '\n')
        file.write(post.title + '\n')
        file.write(post.context + '\n')
        file.write(str(post.like) + '\n')
        file.write(', '.join(post.liked_by) + '\n')


def init_list_all_posts(profile: Profile):
    list_flowers = profile.followers
    list_flowers.append(profile.user_id)
    posts = dict()
    for user_id in list_flowers:
        post_list = os.listdir(f'data/{user_id}/posts/')
        for user_post in post_list:
            posts[user_post] = f'data/{user_id}/posts/{user_post}'

    return posts
