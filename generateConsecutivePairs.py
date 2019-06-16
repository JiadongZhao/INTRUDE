from git import *
import init


# # load list of repos from file
#
# if (platform.system() == 'Windows'):
#     repos = [line.rstrip('\n') for line in open(".\\data\\test_repo_list.txt")]
# else:
#     repos = [line.rstrip('\n') for line in open("./data/test_repo_list.txt")]
# # repos = ['Idnan/bash-guide']


# takes: string, string, list of lists
# returns: list of tuples
def getConsecutivePRPairs(repo, prID, pull_list):
    pull_list = list(filter(lambda x: (int(x['number']) < int(prID)), pull_list))       # list all earlier PRs
    pull_list = sorted(pull_list, key=lambda x: str(x['created_at']), reverse=True)     # sort pull list by creation date

    # narrow to pr pairs generated within a year
    num = 0
    str_date = ''
    for pull_element in pull_list:
        if pull_element['number'] == prID:
            str_date = pull_element['created_at']
    str_date = str(int(str_date[:4], 10) - 1) + str_date[4:]        # set str_date to one year earlier than the PR date
    for pull_element in pull_list:
        num += 1                                                    # iterate counter for size of new pull list
        if pull_element['created_at'] < str_date:                   # once we get to PRs older than a year, break and create new pull list
            pull_list = pull_list[:num]
            break
    # alternative: only look at the 10 most recent PRs
    # pull_list = pull_list[:10]

    pull_list = [x['number'] for x in pull_list]                    # narrow list to just PR IDs
    pr_pair_list = []
    for old_pr in pull_list:
        # old_pr = str(old_pr)
        pr_pair_list.append((repo, str(prID), str(old_pr)))         # create (and return) a new list of tuples of the form (repo name, original PR ID, ID of PR we're comparing)
    return pr_pair_list


# returns: ---
def work():
    add_flag = False

    has = set()

    for repo in init.repos:
        file = init.PR_pairList_filePath_prefix + repo.replace('/', '.') + '.txt'
        # todo: change the dir path to DATA/
        # todo: set file path by OS

        if os.path.exists(file):
            if not add_flag:
                raise Exception('file already exists!')
            with open(file) as f:
                for t in f.readlines():
                    r, n = t.strip().split()
                    has.add((r, n))

        # get all pr
        pull_list = get_repo_info(repo, 'pull')                      # get all info about all PRs, sort by ID
        pull_list = sorted(pull_list, key=lambda x: int(x['number']), reverse=True)
        # for pull in pull_list:
        #    print(pull)

        for pull_element in pull_list:                               # iterate through PRs
            pr_id = pull_element['number']
            print('current pr :' + str(pr_id) + " in repo:" + repo)  # set PR as the one to compare with consecutives (below)

            # Get consecutive pr pairs
            result = getConsecutivePRPairs(repo, pr_id, pull_list)   # get a list of tuples of the form (repo, pr_id, ID of consecutive PR we're comparing with)
            for pair in result:
                with open(file, 'a') as f:                           # opens file for appending
                    print("\t".join(pair), file=f)                   # print pairs, separated by tabs, and followed by filename


if __name__ == "__main__":
     work()
