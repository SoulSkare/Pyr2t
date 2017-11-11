from tumblpy import Tumblpy


def post():
    YOUR_CONSUMER_KEY = ''
    YOUR_CONSUMER_SECRET = ''
    OAUTH_TOKEN = ''
    OAUTH_TOKEN_SECRET = ''

    # Get the final tokens from the database or wherever you have them stored

    t = Tumblpy(YOUR_CONSUMER_KEY, YOUR_CONSUMER_SECRET,
                OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    # Print out the user info, let's get the first blog url...
    blog_url = t.post('user/info')
    blog_url = blog_url['user']['blogs'][0]['url']
    print blog_url

    # Assume you are using the blog_url and Tumblpy instance from the previous sections
    source = 'http://www.factslides.com/imgs/lion2.jpg'
    state = 'published'
    type = 'photo'
    caption = 'TESSSTT CAPP'
    tags = ' "yay", "bay" '

    post = t.post('post', blog_url=blog_url, params={'type':type, 'state':state, 'caption':caption, 'source':source, 'tags':tags})
    print post
    return post