import os
import sys
import init
import json
import util.timeUtil
from datetime import datetime, timedelta

import shutil

pulllist_file = "pull_list.json"
now = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
oldPR_list = []
oldpr = 0
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
