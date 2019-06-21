import os
import sys

from datetime import datetime, timedelta
from sklearn.utils import shuffle

from clf import *
from git import *
from comp import *

c = classify()

cite = {}
renew_pr_list_flag = False

speed_up = False
filter_larger_number = False
filter_out_too_old_pull_flag = True
filter_already_cite = False
filter_create_after_merge = False
filter_overlap_author = False
filter_out_too_big_pull_flag = False
filter_same_author_and_already_mentioned = True

filter_version_number_diff = True


def get_time(t):
    return datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ")


last_detect_repo = None


def speed_up_check(p1, p2):
    if set(p2['title'].lower().split()) & set(p1['title'].lower().split()):
        return True

    try:
        if set([x['name'] for x in fetch_pr_info(p1)]) & set([x['name'] for x in fetch_pr_info(p2)]):
            return True
    except:
        pass

    if check_pattern(p1, p2) == 1:
        return True
    return False


def check_pro_pick(p1, p2):
    if set([x[1] for x in pull_commit_sha(p1)]) & set([x[1] for x in pull_commit_sha(p2)]):
        return True
    return False


def check_subset(p1, p2):
    s1 = set([x[1] for x in pull_commit_sha(p1)])
    s2 = set([x[1] for x in pull_commit_sha(p2)])
    return s1.issubet(s2) or s2.issubet(s1)


def check_pro_pick_with_num(r, n1, n2):
    return check_pro_pick(get_pull(r, n1), get_pull(r, n2))


def have_commit_overlap(p1, p2):
    t = set(pull_commit_sha(p1)) & set(pull_commit_sha(p2))
    p1_user = p1["user"]["id"]
    p2_user = p2["user"]["id"]
    for x in t:
        if (x[1] == p1_user) or (x[1] == p2_user):
            return True
    return False


# returns similarity score and feature vector
def get_topK(repo, num1, topK=10, print_progress=False, use_way='new'):
    global last_detect_repo
    if last_detect_repo != repo:
        last_detect_repo = repo
        init_model_with_repo(repo)

    pulls = get_repo_info(repo, 'pull', renew=False)
    print("get all " + str(len(pulls)) + "  prs for repo " + repo)

    print("get pr " + str(num1))
    pullA = get_pull(repo, num1)

    if filter_already_cite:
        cite[str(pullA["number"])] = get_another_pull(pullA)

    results = {}
    results_featureVector = {}
    tot = len(pulls)
    cnt = 0

    pull_v = {}

    # check if any flags are active & violated
    for pull in pulls:
        feature_vector = {}
        cnt += 1

        # too many changed files check
        if filter_out_too_big_pull_flag:
            if check_large(pull):
                continue

        if filter_out_too_old_pull_flag:
            #             time_diff = abs((get_time(pullA["updated_at"]) - get_time(pull["updated_at"])).days)
            #  updated_at is not reliable, see example: https://github.com/jquery/jquery/pull/1002
            time_diff = abs((get_time(pullA["created_at"]) - get_time(pull["created_at"])).days)
            # print ("time diff" + str(time_diff))
            if time_diff >= 2 * 365:  # more than 2 years
                continue

        if filter_larger_number:
            if int(pull["number"]) >= int(num1):
                continue

        if filter_same_author_and_already_mentioned:
            # same author
            if pull["user"]["id"] == pullA["user"]["id"]:
                continue

            # case of following up work (not sure)
            if str(pull["number"]) in (get_pr_and_issue_numbers(pullA["title"]) + \
                                       get_pr_and_issue_numbers(pullA["body"])):
                continue

        # load events of both PRs, check if one referenced the other
        # EX: https://github.com/akinnae/curly-train/pull/1
        # cross-reference check
        if filter_already_cite:
            # "cite" cases
            if (str(pull["number"]) in cite.get(str(pullA["number"]), [])) or \
                    (str(pullA["number"]) in cite.get(str(pull["number"]), [])):
                continue

        if filter_create_after_merge:
            # create after another is merged
            if (pull["merged_at"] is not None) and \
                    (get_time(pull["merged_at"]) < get_time(pullA["created_at"])) and \
                    ((get_time(pullA["created_at"]) - get_time(pull["merged_at"])).days >= 14):
                continue

        if speed_up:
            if not speed_up_check(pullA, pull):
                continue

        if filter_overlap_author:
            if check_pro_pick(pullA, pull):
                continue
            if have_commit_overlap(pullA, pull):
                continue

        if filter_version_number_diff:
            if check_version_numbers(pullA, pull):
                continue

        if print_progress:
            if cnt % 100 == 0:
                print('progress = ', 1.0 * cnt / tot)
                sys.stdout.flush()

        if use_way == 'new':
            print("compare " + str(pullA['number']) + " " + str(pull['number']))
            feature_vector = get_pr_sim_vector(pullA, pull)
            results_featureVector[pull["number"]] = feature_vector
            results[pull["number"]] = c.predict_proba([feature_vector])[0][1]
        elif 'leave' in use_way:
            feature_vector = leave_feat(pullA, pull, use_way)
            results[pull["number"]] = c.predict_proba([feature_vector])[0][1]
        elif use_way == 'old':
            results[pull["number"]] = old_way(pullA, pull)

    result = [(x, y) for x, y in sorted(results.items(), key=lambda x: x[1], reverse=True)][:topK]
    # result_fv = [(x,y) for x, y in sorted(results_featureVector.items(), key=lambda x: x[1], reverse=True)][:topK]

    if (len(result) == 0):
        return result, None
    else:
        return result, results_featureVector[result[0][0]]


def run_list(repo, renew=False, run_num=200, rerun=False):
    init_model_with_repo(repo)
    pulls = get_repo_info(repo, 'pull', renew_pr_list_flag)

    all_p = set([str(pull["number"]) for pull in pulls])
    select_p = all_p

    log_path = 'evaluation/' + repo.replace('/', '_') + '_stimulate_detect.log'
    out_path = 'evaluation/' + repo.replace('/', '_') + '_run_on_select_all.txt'

    print('-----', file=open(out_path, 'w+'))

    for pull in pulls:
        num1 = str(pull["number"])

        if num1 not in select_p:
            continue

        print('Run on PR #%s' % num1)

        topk, featureVector_list = get_topK(repo, num1)
        if len(topk) == 0:
            continue

        num2, prob = topk[0][0], topk[0][1]
        vet = (pull, get_pull(repo, num2))

        with open(out_path, 'a+') as outf:
            print("\t".join([repo, str(num1), str(num2), "%.4f" % prob] + \
                            ["%.4f" % f for f in vet] + \
                            ['https://www.github.com/%s/pull/%s' % (repo, str(num1)), \
                             'https://www.github.com/%s/pull/%s' % (repo, str(num2))]
                            ),
                  file=outf)

        with open(log_path, 'a+') as outf:
            print(repo, num1, ':', topk, file=outf)


def detect_one(repo, num):
    print('analyzing ', repo, num)
    speed_up = True
    filter_create_after_merge = True

    ret, feature_vector = get_topK(repo, num, 1, True)
    if len(ret) < 1:
        print("no result")
        return -1, -1, -1
    else:
        return ret[0][0], ret[0][1], feature_vector
        # return ret[0][0], ret[0][1]


if __name__ == "__main__":
    # detect one PR
    if len(sys.argv) == 3:
        r = sys.argv[1].strip()
        n = sys.argv[2].strip()
        detect_one(r, n)

    # detection on history (random sampling)
    if len(sys.argv) == 2:
        speed_up = True
        filter_create_after_merge = True
        filter_larger_number = True
        r = sys.argv[1].strip()
        run_list(r)
