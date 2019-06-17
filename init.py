
import platform


if (platform.system() == 'Windows'):
    LOCAL_DATA_PATH = 'C:\\Users\\annik\\Documents\\REUSE\\INTRUDE\\PR_data'  # backslashes are escape characters, so doubles are needed
    experiment_param_filePath = '.\\data\\test_repo_list.txt'
    PR_pairList_filePath_prefix = '.\\data\\consecutive_PR_pairs_'
    repos = [line.rstrip('\n') for line in open(".\\data\\test_repo_list.txt")]
    dupPR_result_filePath_prefix = '.\\data\\dupPR_'
else:
    if (platform.system() == 'Linux'):
        LOCAL_DATA_PATH = '/DATA/luyao'
    else:
        LOCAL_DATA_PATH = '/Users/shuruiz/Work/researchProjects'
     # monitored_repoList_filePath = 'data/2000forks-repoList.csv'
    monitored_repoList_filePath = 'data/test_repo_list.txt'
    PR_pairList_filePath_prefix = 'data/consecutive_PR_pairs_'
    PR_candidate_List_filePath_prefix = 'data/candidate_PR_'
    PR_candidate_List_filePath_prefix = LOCAL_DATA_PATH +'/PRCandidate/candidate_'
    repos = [line.rstrip('\n') for line in open(monitored_repoList_filePath)]
    dupPR_result_filePath_prefix = LOCAL_DATA_PATH + '/dupPR/repo_'


pr_date_difference_inDays= 365

# print('monitored_repoList_filePath:' + monitored_repoList_filePath)
# print('LOCAL_DATA_PATH:' + LOCAL_DATA_PATH)
# print('PR_candidate_List_filePath_prefix:' + PR_candidate_List_filePath_prefix)


