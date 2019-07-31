import json
import requests


# Authentication info

with open('input/authParams.txt') as f:
    USERNAME, TOKEN = f.read().splitlines()


# def make_github_comment(REPO, PR_NUMBER, PR_NUMBER2, FEATURES, body=None):
def make_github_comment(REPO, PR_NUMBER, PR_NUMBER2, body=None):
    '''Create a comment on github.com using the given parameters.'''
    # Our url to create comments via POST
    url = 'https://api.github.com/repos/%s/issues/%i/comments' % (REPO, PR_NUMBER)
    # Create an authenticated session to create the comment
    headers = {
        "Authorization": "token %s" % TOKEN,
    }
    # Create our comment
    data = {'body': """__Hi there! This pull request looks like it might be a duplicate of #%i, since it has _the same issue number_ and _a similar title_.___

To improve our bot, you can help us out by clicking one of the options below: 
- This pull request __is a duplicate__, so this comment was __useful__. [check](http://forks-insight.com/INTRUDE-survey?repo=aa&pr1=1&pr2=2&response=dup_useful)
- This pull request is __not a duplicate__, but this comment was __useful__ nevertheless. [check](http://forks-insight.com/INTRUDE-survey?repo=aa&pr1=1&pr2=2&response=notDup_useful)
- This pull request is __not a duplicate__, so this comment was __not useful__. [check](http://forks-insight.com/INTRUDE-survey?repo=aa&pr1=1&pr2=2&response=notDup_notUseful)
- I do not need this service, so this comment was __not useful__. [check](http://forks-insight.com/INTRUDE-survey?repo=aa&pr1=1&pr2=2&response=stopBother)

This bot is currently in its alpha stage, and we are only sending at most one comment per repository. If you are interested in using our bot in the future, please <a href="http://forks-insight.com/INTRUDE-subscribe" target="_blank">subscribe</a>.
If you would like to learn more, see our <a href="http://forks-insight.com/INTRUDE-welcome" target="_blank">web page</a>.
                    """ % PR_NUMBER2}
# """ % ((FEATURES,), PR_NUMBER2)}

    r = requests.post(url, json.dumps(data), headers=headers)
    if r.status_code == 201:
        print('Successfully created comment "%s"' % body)
    else:
        print('Could not create comment "%s"' % body)
        print('Response:', r.content)