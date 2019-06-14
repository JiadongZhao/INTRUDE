from git import *

# load list of repos from file
repos = [line.rstrip('\n') for line in open(".\\data\\test_repo_list.txt")]
#todo: set file based on OS


def getConsecutivePRPairs(repo, prID, pull_list):
    pull_list = list(filter(lambda x: (int(x['number']) < int(prID)), pull_list))
    pull_list = sorted(pull_list, key=lambda x: int(x['number']), reverse=True)
    # set the number of pr pairs limitation
    #todo: alternative: find pr pairs generated within a year
    pull_list = pull_list[:10]

    pull_list = [x['number'] for x in pull_list]
    pr_pair_list = []
    for old_pr in pull_list:
        old_pr = str(old_pr)
        pr_pair_list.append((repo,str(prID), str(old_pr)))
    return pr_pair_list


def work():
    add_flag = False

    has = set()

    for repo in repos:
        file = 'data/consecutive_PR_pairs_' + repo.replace('/', '.') + '.txt'
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
        pull_list = get_repo_info(repo, 'pull')
        pull_list = sorted(pull_list, key=lambda x: int(x['number']), reverse=True)

        for pull_element in pull_list:
            pr_id = pull_element['number']
            print('current pr :' + str(pr_id) + " in repo:" + repo)
            # Get consecutive pr pairs
            result = getConsecutivePRPairs(repo, pr_id, pull_list)
            for pair in result:
                with open(file, 'a') as f:
                    print("\t".join(pair), file=f)


if __name__ == "__main__":
    work()
