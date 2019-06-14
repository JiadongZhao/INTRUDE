
import platform


if (platform.system() == 'Windows'):
    LOCAL_DATA_PATH = 'C:\\Users\\annik\\Documents\\REUSE\\INTRUDE\\PR_data'  # backslashes are escape characters, so doubles are needed
    experiment_param_filePath = '.\\data\\test_repo_list.txt'
    PR_pairList_filePath_prefix = '.\\data\\consecutive_PR_pairs_'
    repos = [line.rstrip('\n') for line in open(".\\data\\test_repo_list.txt")]
else:
    monitored_repoList_filePath = 'data/2000forks-repoList.csv'
    PR_pairList_filePath_prefix = 'data/consecutive_PR_pairs_'
    repos = [line.rstrip('\n') for line in open("./data/test_repo_list.txt")]
    if (platform.system() == 'Linux'):
        LOCAL_DATA_PATH = '/DATA/luyao'
    else:
        LOCAL_DATA_PATH = '/Users/shuruiz/Work/researchProjects'



print('monitored_repoList_filePath:' + monitored_repoList_filePath)
print('LOCAL_DATA_PATH:' + LOCAL_DATA_PATH)


