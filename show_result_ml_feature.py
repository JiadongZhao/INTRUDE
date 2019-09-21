import classify

file = 'evaluation/random_sample_select_pr_result_0424.txt'
out = open(file + '.out', 'w')

c = classify.classify()

with open(file) as f:
    for l in f.readlines():
        r, n1, n2, proba= l.split()
        classify.init_model_with_repo(r)
        feature_vector = classify.get_sim(r, n1, n2)
        proba_from_c = c.predict_proba([feature_vector])[0][1]
        
        print("\t".join([r, n1, n2] + ["%.15f" % proba_from_c] + ["%.2f" % x for x in feature_vector]), file=out)

out.close()