# import nltk
# nltk.download()
from git import *

import init
import util.timeUtil
import datetime

import detect

detect.speed_up = True
detect.filter_larger_number = True
detect.filter_out_too_old_pull_flag = True
detect.filter_already_cite = False
detect.filter_create_after_merge = True
detect.filter_overlap_author = False
detect.filter_out_too_big_pull_flag = False
detect.filter_same_author_and_already_mentioned = True
detect.filter_version_number_diff = True

add_flag = True


#
# get all open PRs to compare this repo to
#
def getCandidatePRs(repo):
    # todo get all open 1) LOCAL PR 2) new PR 3) list as output
    #  check local open PRs

    candidatePR_input_file = init.PR_candidate_List_filePath_prefix + repo.replace('/', '.') + '.txt'
    print(candidatePR_input_file)

    has = set()
    prCandidate_list = []
    if os.path.exists(candidatePR_input_file):
        if not add_flag:
            raise Exception('file already exists!')
        with open(candidatePR_input_file) as f:
            for t in f.readlines():
                r, n = t.strip().split()
                has.add((r, n))
        print("length : " + str(len(has)))
        return has

    # get all pr
    pull_list = get_repo_info(repo, 'pull', renew=True)  # get all info about all PRs, sort by ID
    pull_list = sorted(pull_list, key=lambda x: int(x['number']), reverse=True)
    print("length : " + str(len(pull_list)))

    for current_pr in pull_list:  # iterate through PRs
        current_pr_id = current_pr['number']
        current_pr_createdAt = current_pr['created_at']

        # get date for today, if the pr was created 1 yr ago, then stop
        now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        if (current_pr['state'] == 'closed'):
            #             print("closed pr " + str(current_pr_id))
            continue

        if (util.timeUtil.days_between(now, current_pr_createdAt) > init.pr_date_difference_inDays):
            print("older than " + init.pr_date_difference_inDays + " days " + str(current_pr_id) + "stop")
            break
        print('current pr :' + str(
            current_pr_id) + " created_at: " + current_pr_createdAt + " in repo:" + repo)  # set PR as the one to compare with consecutives (below)

        prCandidate_list.append((repo, str(current_pr_id)))

    print("length of pr candidates: " + str(len(prCandidate_list)))
    for pair in prCandidate_list:
        with open(candidatePR_input_file, 'a') as f:  # opens file for appending
            print("\t".join(pair), file=f)  # print pairs, separated by tabs, and followed by filename

    return prCandidate_list




def work():
    cnt = 0
    for repo in init.repos:
        print("get open PRs from repo: " + repo)
        getCandidatePRs(repo)

        candidatePR_input_file = init.PR_candidate_List_filePath_prefix + repo.replace('/', '.') + '.txt'
        try:
            with open(candidatePR_input_file) as f:
                for t in f.readlines():
                    repo, pr_id = t.split()
                    cnt += 1
                    dupPR_id, similarity, feature_vector = detect.detect_one(repo, pr_id)
                    if (dupPR_id == -1 and similarity == -1 and feature_vector == -1): continue
                    with open(init.dupPR_result_filePath_prefix + repo.replace('/', '.') + '.txt', 'a') as outf:
                        print(repo, str(pr_id), str(dupPR_id), "%.4f" % similarity)
                        print("\t".join(
                            [repo, str(pr_id),
                             str(dupPR_id)] + ["%.15f" % similarity] + ["%.2f" % x for x in feature_vector]), file=outf)
        except FileNotFoundError:
            print("file not exist, continue")
            continue


if __name__ == "__main__":
    work()
