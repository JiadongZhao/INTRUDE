import numpy as np
fileName = '/Users/shuruiz/Work/researchProjects/INTRUDE/data/PR_count.csv'
list_repo = []
list_repo_1 = []
list_repo_2 = []
list_repo_3 = []
with open(fileName) as f:
    lineList = f.readlines()
    for line in lineList:
        repo, pr_num = line.split()
        if(repo == "repo"): continue
        if(int(pr_num) < 11): break
        # print(repo + "," + pr_num)
        list_repo.append(line)


    l = np.array(list_repo)
    n = 3

    res = l.reshape((len(l) // n), n).T
    count = 1
    for list_tmp in res:
        if(count == 1):
            list_repo_1 = list_tmp
            with open('/Users/shuruiz/Work/researchProjects/INTRUDE/data/repo_PR_1.txt', 'w') as f:
                for item in list_repo_1:
                    f.write("%s" % item.replace("https://api.github.com/repos/",""))
        if(count == 2):
            list_repo_2 =list_tmp
            with open('/Users/shuruiz/Work/researchProjects/INTRUDE/data/repo_PR_2.txt', 'w') as f:
                for item in list_repo_2:
                    f.write("%s" % item.replace("https://api.github.com/repos/",""))
        if(count == 3):
            list_repo_3=list_tmp
            with open('/Users/shuruiz/Work/researchProjects/INTRUDE/data/repo_PR_3.txt', 'w') as f:
                for item in list_repo_3:
                    f.write("%s" % item.replace("https://api.github.com/repos/",""))
        count +=1
    print(res)

