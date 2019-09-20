
import mysql.connector
import os,sys
import numpy as np

file_dir = os.path.dirname(__file__)
print(file_dir)
sys.path.append(file_dir)


# Connect to MySQL database
with open(file_dir+'/input/mysqlParams.txt') as f:
    MYSQL_USER, MYSQL_PASS, MYSQL_HOST, PORT = f.read().splitlines()
conn = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASS, host=MYSQL_HOST, database='fork', port=PORT)
cur = conn.cursor()
cur.execute("SELECT * FROM duppr_pair WHERE notes LIKE '%FP%'")  # get info about pr pair
FP_PR_info = cur.fetchall()

FP_PR_list = []
for str in FP_PR_info:
    FP_PR_list.append((str[1],str[2],str[3]))


FP_file_all_path = file_dir+'/data/clf/marked_FP.txt'
with open(FP_file_all_path, mode='wt') as f:
    for t in FP_PR_list:
        f.write('\t'.join(s for s in t) + '\n')
        


 
list_prs = []
list_prs_1 = []
list_prs_2 = []
with open(FP_file_all_path) as f:
    lineList = f.readlines()
    for line in lineList:
        repo, pr1,pr2= line.split()
        list_prs.append(line)


    l = np.array(list_prs)
    n = 2

    res = l.reshape((len(l) // n), n).T
    count = 1
    for list_tmp in res:
        if(count == 1):
            list_prs_1 = list_tmp
            with open(file_dir+'/data/clf/Marked_FP_test.txt', 'w') as f:
                for item in list_prs_1:
                    f.write("%s" % item)
        if(count == 2):
            list_prs_2 =list_tmp
            with open(file_dir+'/data/clf/Marked_FP_train.txt', 'w') as f:
                for item in list_prs_2:
                    f.write("%s" % item)

        count +=1


### Regenerate training/testing FP file

filenames = [file_dir+'/data/clf/Marked_FP_test.txt', file_dir + '/data/clf/consecutive_NonDupPR_pairs_testing.txt']
with open(file_dir+'/data/clf/latest_NonDupPR_testing.txt', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)

filenames = [file_dir+'/data/clf/Marked_FP_train.txt', file_dir + '/data/clf/consecutive_NonDupPR_pairs_training.txt']
with open(file_dir+'/data/clf/latest_NonDupPR_training.txt', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)