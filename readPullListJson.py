import init
import json
from datetime import datetime
import os
from util import localfile
import util.timeUtil
import scraper

# api = GitHub(app)
api = scraper.GitHubAPI()

LOCAL_DATA_PATH = init.LOCAL_DATA_PATH


def getOldOpenPRs(repo):
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    old_openPR_list = []

    file = init.local_pr_data_dir + repo + '/pull_list.json'
    latest_pr = 0
    with open(file) as json_file:
        data = json.load(json_file)
        latest_pr = data[0]['number']

        for pr in data:
            number = pr['number']
            state = pr['state']
            created_at = pr['created_at']
            if (state == 'open'):
                if (util.timeUtil.days_between(created_at, now) < 2 * 365):
                    old_openPR_list.append(number)
        if len(old_openPR_list) > 0:
            return min(old_openPR_list)
        else:
            return latest_pr


# with open(file, 'w') as write_file:
#     write_file.write()


def get_repo_info(repo, type, renew):
    filtered_result = []

    tocheck_pr = getOldOpenPRs(repo)

    save_path = LOCAL_DATA_PATH + '/pr_data/' + repo + '/%s_list.json' % type
    if type == 'fork':
        save_path = LOCAL_DATA_PATH + '/result/' + repo + '/forks_list.json'

    if (os.path.exists(save_path)) and (not renew):
        try:
            return localfile.get_file(save_path)
        except:
            pass

    print('start fetch new list for ', repo, type)
    if (type == 'pull') or (type == 'issue'):
        page_index = 1
        while (True):
            ret = api.requestPR('repos/%s/%ss' % (repo, type), state='all', page=page_index)
            numPR = init.numPRperPage
            for pr in ret:
                if (pr['number'] >= tocheck_pr):
                    filtered_result.append(pr)
                else:
                    print('get all ' + str(len(filtered_result)) + ' prs')
                    localfile.write_to_file(save_path,filtered_result)
                    return filtered_result
            if (len(filtered_result) < numPR):
                print('get all ' + len(filtered_result) + ' prs -- after page ' + page_index)
                localfile.write_to_file(save_path, filtered_result)
                return filtered_result
            else:
                page_index += 1
                numPR += init.numPRperPage
    else:
        if type == 'branch':
            type = 'branche'
        ret = api.request('repos/%s/%ss' % (repo, type), True)

    localfile.write_to_file(save_path, ret)
    return ret


if __name__ == "__main__":
    get_repo_info('Idnan/bash-guide', 'pull', True)
