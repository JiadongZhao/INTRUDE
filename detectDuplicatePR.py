from git import *
import detect

import util.timeUtil
import datetime
import init

detect.speed_up = True
detect.filter_larger_number = True
detect.filter_out_too_old_pull_flag = True
detect.filter_already_cite = False
detect.filter_create_after_merge = True
detect.filter_overlap_author = False
detect.filter_out_too_big_pull_flag = False
detect.filter_same_author_and_already_mentioned = True
detect.filter_version_number_diff = True


cnt = 0
add_flag = False


def getCandidatePRs(repo):
    candidatePR_input_file = init.PR_candidate_List_filePath_prefix + repo.replace('/', '.') + '.txt'
    has = set()
    prCandidate_list = []
    if os.path.exists(candidatePR_input_file):
        if not add_flag:
            raise Exception('file already exists!')
        with open(candidatePR_input_file) as f:
            for t in f.readlines():
                r, n = t.strip().split()
                has.add((r, n))

    # get all pr
    pull_list = get_repo_info(repo, 'pull')  # get all info about all PRs, sort by ID
    pull_list = sorted(pull_list, key=lambda x: int(x['number']), reverse=True)

    for current_pr in pull_list:  # iterate through PRs
        current_pr_id = current_pr['number']
        current_pr_createdAt = current_pr['created_at']

        # get date for today, if the pr was created 1 yr ago, then stop
        now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        if (util.timeUtil.days_between(now, current_pr_createdAt) > init.pr_date_difference_inDays):
            break
        print('current pr :' + str(
            current_pr_id) + " created_at: " + current_pr_createdAt + " in repo:" + repo)  # set PR as the one to compare with consecutives (below)

        prCandidate_list.append((repo, str(current_pr_id)))

    for pair in prCandidate_list:
        with open(candidatePR_input_file, 'a') as f:  # opens file for appending
            print("\t".join(pair), file=f)  # print pairs, separated by tabs, and followed by filename

    return prCandidate_list


for repo in init.repos:

    getCandidatePRs(repo)

    candidatePR_input_file = init.PR_candidate_List_filePath_prefix + repo.replace('/', '.') + '.txt'

    with open(candidatePR_input_file) as f:
        for t in f.readlines():
            repo, pr_id  = t.split()
            cnt += 1
            # if (cnt < 20):
            #     continue

            dupPR_id, similarity = detect.detect_one(repo, pr_id)

            with open(init.dupPR_result_filePath_prefix + repo.replace('/', '.') + '.txt', 'a') as outf:
                print(repo, pr_id, dupPR_id, similarity, sep='\t', file=outf)
