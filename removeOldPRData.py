import os
import sys
import init
import json
import util.timeUtil
from datetime import datetime, timedelta

import shutil

repo_for_training = ["symfony/symfony",
                     "kubernetes/kubernetes",
                     "twbs/bootstrap",
                     "rust-lang/rust",
                     "nodejs/node",
                     "symfony/symfony-docs",
                     "scikit-learn/scikit-learn",
                     "zendframework/zendframework",
                     "servo/servo",
                     "pandas-dev/pandas",
                     "saltstack/salt",
                     "mozilla-b2g/gaia",
                     "rails/rails",
                     "joomla/joomla-cms",
                     "angular/angular.js",
                     "ceph/ceph",
                     "ansible/ansible",
                     "facebook/react",
                     "elastic/elasticsearch",
                     "docker/docker",
                     "cocos2d/cocos2d-x",
                     "django/django",
                     "hashicorp/terraform",
                     "emberjs/ember.js",
                     "JuliaLang/julia",
                     "dotnet/corefx"]

def remove_oldPR_rawdata():
    pulllist_file = "pull_list.json"
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    oldPR_list = []
    oldpr = 0


    for subdir, dirs, files in os.walk(init.local_pr_data_dir):
        for subdir_tmp in dirs:
            print(subdir_tmp)
            for subdir_1, dirs_1, files_1 in os.walk(os.path.join(subdir, subdir_tmp)):
                for repo in dirs_1:
                    print(subdir_tmp + "/" + repo)
                    if (subdir_tmp + "/" + repo) in repo_for_training:
                        print("repo is usedful for training model, skip "+ subdir_tmp + "/" + repo)
                        continue
                    for subdir_2, dirs_2, files_2 in os.walk(subdir_1 + "/" + repo):
                        if len(dirs_2) == 0:
                            break
                        # get old pr list
                        if os.path.exists(subdir_2 + "/" + pulllist_file):
                            with open(subdir_2 + "/" + pulllist_file, 'r') as f:
                                datastore = json.load(f)
                                for pr in datastore:
                                    if (util.timeUtil.days_between(now, pr['created_at']) > 366):
                                        oldpr = pr['number']
                                        break
                                for pr in datastore:
                                    prid = pr['number']
                                    filepath = subdir_2 + "/" + str(prid)
                                    if (prid <= oldpr and os.path.exists(filepath)):
                                        # oldPR_list.append(prid)
                                        # delete old pr dir
                                        shutil.rmtree(filepath)
                                        print("delete " + filepath)
                                break



import os
import fnmatch

def removeFile_byPattern():
    # Get a list of all the file paths that ends with .txt from in specified directory


    # Get a list of all files in directory
    for train_repo in repo_for_training:
        for rootDir, subdirs, filenames in os.walk('/DATA/luyao/pr_data/'+train_repo):
            # Find the files that matches the given patterm
            for sd in subdirs:
                for srootDir, ssubdirs, sfilenames in os.walk('/Users/shuruiz/Work/researchProjects/pr_data/' + train_repo+"/"+sd):
                    # for filename in fnmatch.filter(sfilenames, 'added*.tsv'):
                    for filename in fnmatch.filter(sfilenames, 'delete*.tsv'):
                        try:
                            os.remove(os.path.join('/Users/shuruiz/Work/researchProjects/pr_data/' + train_repo+"/"+sd+'/', filename))
                            print('remove')
                        except OSError:
                            print("Error while deleting file")



if __name__ == "__main__":
    removeFile_byPattern()