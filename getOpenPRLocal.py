import init
import sys, os
import json

local_pr_data_dir = init.local_pr_data_dir
# def getCandidatePRs(repo):
#     candidatePR_input_file = init.PR_candidate_List_filePath_prefix + repo.replace('/', '.') + '.txt'
#     print(candidatePR_input_file)

output = local_pr_data_dir + 'openPRList.txt'


def getOpenPRs():
    for path, dirs, files in os.walk(local_pr_data_dir):
        for dir in dirs:
            for sub_path, sub_dirs, sub_files in os.walk(path + dir):
                for sub_dir in sub_dirs:
                    for sub_sub_path, sub_sub_dirs, sub_sub_files in os.walk(sub_path + '/' + sub_dir):
                        for name in sub_sub_files:
                            if (name == 'pull_list.json'):
                                repo = sub_sub_path.replace(local_pr_data_dir, '')
                                # json1_data = json.loads(name)[0]
                                with open(sub_sub_path + '/' + name) as json_file:
                                    prList = json.load(json_file)
                                    for pr in prList:
                                        if (pr['state'] == 'open'):
                                            print(repo + ',' + str(pr['number']) + ',' + pr['created_at'] + ',' + pr[
                                                'url'])
                                            with open(output, 'a') as f:
                                                f.write(
                                                    repo + ',' + str(pr['number']) + ',' + pr['created_at'] + ',' + pr[
                                                        'url'] + '\n')



if __name__ == "__main__":
    getOpenPRs()
