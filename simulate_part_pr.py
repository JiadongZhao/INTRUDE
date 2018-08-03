import os
from datetime import datetime, timedelta

from git import *
import fetch_raw_diff
from comparer import *
import main

def fetch_pull_from_local(pull):
    # repo = 'Chatie/wechaty'
    # pull = get_pull(repo, '1182')
    # pull = get_pull(repo, num)

    repo = pull["base"]["repo"]["full_name"]
    repo_url = 'https://github.com/%s' % repo
    repo_path = '/DATA/luyao/repo/%s' % repo
    
    pull_id = pull["node_id"]
    
    if not os.path.exists(repo_path):
        os.system('git clone %s %s' % (repo_url, repo_path))
    os.system('git -C %s remote add %s %s' % (repo_path, pull_id, pull["head"]["repo"]["html_url"]))
    os.system('git -C %s fetch %s' % (repo_path, pull_id))


def generate_part_pull(pull):
    repo = pull["base"]["repo"]["full_name"]
    repo_path = '/DATA/luyao/repo/%s' % repo

    fetch_pull_from_local(pull)
    
    out = '/DATA/luyao/commit_diff'

    commits = get_pull_commit(pull)
    
    if len(commits[0]["parents"]) > 1:
        raise Exception('have multi parents %s' % commits[0]['sha'])
    
    root_sha = commits[0]["parents"][0]["sha"]
    
    total_message = ''
    
    all_p = []
    
    for c in commits:
        message = c['commit']['message']
        total_message += message + '\n'
        ti = datetime.strptime(c['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ")
        
        out_file = out + '/' + root_sha + '_' + c['sha'] + '.txt'        
        os.system('git -C %s diff %s %s > %s' % (repo_path, root_sha, c['sha'], out_file))
        
        p = commits_to_pull(message, total_message, ti, open(out_file).read())
        
        if p:
            all_p.append(p)
    
    return all_p

def commits_to_pull(message, total_message, ti, raw_diff):
    pull = {}
    pull['number'] = None
    pull['title'] = message
    pull['body'] = total_message
    pull['file_list'] = fetch_raw_diff.parse_files(raw_diff)
    pull['time'] = ti
    pull['merge_commit_flag'] = True
    if len(pull['file_list']) == 0:
        return None
    return pull


def simulate(repo, num1, num2):    
    p1 = get_pull(repo, num1)
    p2 = get_pull(repo, num2)
    
    all_pa = generate_part_pull(p1)
    all_pb = generate_part_pull(p2)
    
    max_s = -1
    
    l_a, l_b = len(all_pa), len(all_pb)
    num_a, num_b = 0, 0
    now_a, now_b = None, None
    
    while True:
        pa = all_pa[num_a] if num_a < l_a else None
        pb = all_pb[num_b] if num_b < l_b else None
        if not (pa or pb):
            break
        
        if (pb is None) or (pa and (pa['time'] < pb['time'])):
            num_a += 1
            now_a = pa
        else:
            num_b += 1
            now_b = pb
        
        if now_a and now_b:
            # print([x['file_list'] for x in now_a['file_list']])
            # print([x['file_list'] for x in now_b['file_list']])
            
            ret = calc_sim(now_a, now_b)
            s = m.predict_proba([sim_to_vet(ret)])[0][1]
            
            print(ret)
            print(s)
            print('-------------------')
            
            max_s = max(max_s, s)
    
    
    '''
    for part1 in all_pa:
        for part2 in all_pb:
            ret = calc_sim(part1, part2)
            s = m.predict_proba([sim_to_vet(ret)])[0][1]
            max_s = max(max_s, s)
    '''
    
    return max_s

m = main.classify()

def run(s):
    r, n1, n2 = s.split()
    main.init_model_with_repo(r)
    simulate(r, n1, n2)
    
    
if __name__ == '__main__':
    # fetch_pull_from_local()
    # stimulate('angular/angular.js', '2522', '3025')
    # print(simulate('JuliaLang/julia', '16942', '16917'))
    
    result = []
    
    with open('data/msr_multi_commits.txt') as f:
        pairs = f.readlines()
        pairs = sorted(pairs, key=lambda x: x[0])
        
        last_repo = None
        for pair in pairs:
            r, n1, n2, z = pair.split()
            if r != last_repo:
                main.init_model_with_repo(r)
                last_repo = r
            
            print('run on ', r, n1, n2)
            try:
                t = simulate(r, n1, n2)
            except:
                continue

            if t > 0:
                with open('detection/msr_multi_commits_result_tmp.txt', 'a+') as f:
                    print(pair, ':', t, 'ori=', z, file=f)
                
            result.append((pair, t))
    
    result = sorted(result, key=lambda x: x[1], reverse=True)
    
    with open('detection/msr_multi_commits_result.txt', 'w') as f:
        print(result, file=f)
    
            
    