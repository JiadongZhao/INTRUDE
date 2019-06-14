import detect
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

# For precision
# outfile = 'evaluation/random_sample_select_pr_result_0424.txt'
# with open(outfile, 'w') as outf:
#     pass

cnt = 0

for repo in init.repos:
    file = init.PR_pairList_filePath_prefix + repo.replace('/', '.') + '.txt'
    with open(file) as f:
        for t in f.readlines():
            repo, pr_id = t.split()
            cnt += 1
            if (cnt < 20):
                continue

            dupPR_id, similarity = detect.detect_one(repo, pr_id)

            with open(init.dupPR_result_filePath_prefix + repo.replace('/', '.') + '.txt', 'a') as outf:
                print(repo, pr_id, dupPR_id, similarity, sep='\t', file=outf)
