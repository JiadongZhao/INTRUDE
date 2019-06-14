
import platform


if (platform.system() == 'Linux'):
    LOCAL_DATA_PATH = '/DATA/luyao'
    monitored_repoList_filePath = 'data/2000forks-repoList.csv'
    PR_pairList_filePath_prefix = 'data/consecutive_PR_pairs_'
elif (platform.system() == 'Windows'):
    LOCAL_DATA_PATH = 'C:\\Users\\annik\\Documents\\REUSE\\INTRUDE\\PR_data'  # backslashes are escape characters, so doubles are needed
    experiment_param_filePath = '.\\data\\test_repo_list.txt'
    PR_pairList_filePath_prefix = '.\\data\\consecutive_PR_pairs_'
else:
    LOCAL_DATA_PATH = '/Users/shuruiz/Work/researchProjects'
    monitored_repoList_filePath = 'data/2000forks-repoList.csv'
    PR_pairList_filePath_prefix = 'data/consecutive_PR_pairs_'


print('monitored_repoList_filePath:' + monitored_repoList_filePath)
print('LOCAL_DATA_PATH:' + LOCAL_DATA_PATH)




