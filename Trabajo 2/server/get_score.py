import pandas as pd

ref_categories = ['mths_since_last_credit_pull_d:>75', 'mths_since_issue_d:>122', 'mths_since_earliest_cr_line:>434', 'total_rev_hi_lim:>79,780', 
                  'total_rec_int:>7,260', 'total_pymnt:>25,000', 'out_prncp:>15,437', 'revol_util:>1.0', 'inq_last_6mths:>4', 'dti:>35.191', 
                  'annual_inc:>150K', 'int_rate:>20.281', 'term:60', 'purpose:major_purch__car__home_impr', 'verification_status:Not Verified', 
                  'home_ownership:MORTGAGE', 'grade:G']	

def get_score(dic, woe_transform):
    X_input_caracteristicas = pd.DataFrame(dic, index=[0])
    #input_caracteristicas
    # first create a transformed test set through our WoE_Binning custom class
    X_input_woe_transformed = woe_transform.fit_transform(X_input_caracteristicas)
    # insert an Intercept column in its beginning to align with the # of rows in scorecard
    X_input_woe_transformed.insert(0, 'Intercept', 1)
    X_input_woe_transformed.head()

    # get the list of our final scorecard scores
    df_scorecard = pd.read_csv("df_scorecard.csv")
    scorecard_scores = df_scorecard['Score - Final']
    # check the shapes of test set and scorecard before doing matrix dot multiplication
    print(X_input_woe_transformed.shape)
    print(scorecard_scores.shape)

    X_input_woe_transformed = pd.concat([X_input_woe_transformed, pd.DataFrame(dict.fromkeys(ref_categories, [0] * len(X_input_woe_transformed)), 
                                                                            index = X_input_woe_transformed.index)], axis = 1)

    scorecard_scores = scorecard_scores.values.reshape(102, 1)
    print(X_input_woe_transformed.shape)
    print(scorecard_scores.shape)

    # matrix dot multiplication of test set with scorecard scores
    y_score = X_input_woe_transformed.dot(scorecard_scores)
    y_score.head()
    return y_score[0][0]