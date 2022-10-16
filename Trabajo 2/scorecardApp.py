import dill
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

#server
def prediccion_riesgo(dic):
    modelo= dill.load(open("/work/model2.pkl", "rb"))
    data=pd.DataFrame(data=dic,index=[0])
    prediccion=modelo.predict_proba(data)
    return prediccion[0][1]

st.write("""
# Conoce tu score crediticio!
Credit Scorecard
""")

term = 48
int_rate = st.slider('Selecciona el int_rate', min_value=7000, max_value=20000)
grade = st.selectbox(
    'Cual es tu grade?',
     ['A', 'B', 'C', 'D', 'F', 'G'])
emp_length = 1
home_ownership = 'OWN'
annual_inc = st.slider('Selecciona el annual_inc', min_value=0, max_value=150000, key='annual_inc')
verification_status = 'Not Verified'
purpose = 'car'
dti = st.slider('Selecciona el dti', min_value=1, max_value=35000, key='dti')
inq_last_6mths = 8.2
revol_util = 100.22
total_acc = 50.1
out_prncp = 11681
total_pymnt = 34919
total_rec_int = 10172
last_pymnt_amnt = 6234
tot_cur_bal = 1158254
total_rev_hi_lim = 12
mths_since_earliest_cr_line = 2
mths_since_issue_d = 5
mths_since_last_pymnt_d = 3
mths_since_last_credit_pull_d = 7
grade_A = 0
grade_B = 0
grade_C = 0
grade_D = 0
grade_E = 0
grade_F = 0
grade_G = 0

if grade == 'A': grade_A = 1
elif grade == 'B': grade_B = 1
elif grade == 'C': grade_C = 1
elif grade == 'D': grade_D = 1
elif grade == 'E': grade_E = 1
elif grade == 'F': grade_F = 1

home_ownership_MORTGAGE = 1
home_ownership_NONE = 0
home_ownership_OTHER = 0
home_ownership_OWN = 0
home_ownership_RENT = 0
verification_status_Not_Verified = 1
verification_status_Source_Verified = 0
verification_status_Verified = 0
purpose_car= 0
purpose_credit_card= 0
purpose_debt_consolidation= 0
purpose_educational= 0
purpose_home_improvement= 0
purpose_house= 0
purpose_major_purchase= 1
purpose_medical= 0
purpose_moving= 0
purpose_other= 0
purpose_renewable_energy= 0
purpose_small_business= 0
purpose_vacation= 0
purpose_wedding= 0
  
dic={
        'term': int(term),
        'int_rate': float(int_rate),
        'grade': str(grade),
        'emp_length':float(emp_length),
        'home_ownership': str(home_ownership),
        'annual_inc': float(annual_inc),
        'verification_status': str(verification_status),
        'purpose': str(purpose),
        'dti': float(dti),
        'inq_last_6mths': float(inq_last_6mths),
        'revol_util': float(revol_util),
        'total_acc': float(total_acc),
        'out_prncp': float(out_prncp),
        'total_pymnt': float(total_pymnt),
        'total_rec_int': float(total_rec_int),
        'last_pymnt_amnt': float(last_pymnt_amnt),
        'tot_cur_bal': float(tot_cur_bal),
        'total_rev_hi_lim': float(total_rev_hi_lim),
        'mths_since_earliest_cr_line': float(mths_since_earliest_cr_line),
        'mths_since_issue_d': float(mths_since_issue_d),
        'mths_since_last_pymnt_d':float(mths_since_last_pymnt_d),
        'mths_since_last_credit_pull_d': float(mths_since_last_credit_pull_d),
        'grade:A': grade_A,
        'grade:B': grade_B,
        'grade:C': grade_C,
        'grade:D': grade_D,
        'grade:E': grade_E,
        'grade:F': grade_F,
        'grade:G': grade_G,
        'home_ownership:MORTGAGE': home_ownership_MORTGAGE,
        'home_ownership:NONE': home_ownership_NONE,
        'home_ownership:OTHER': home_ownership_OTHER,
        'home_ownership:OWN': home_ownership_OWN,
        'home_ownership:RENT': home_ownership_RENT,
        'verification_status:Not Verified': verification_status_Not_Verified,
        'verification_status:Source Verified': verification_status_Source_Verified,
        'verification_status:Verified': verification_status_Verified,
        'purpose:car': purpose_car,
        'purpose:credit_card': purpose_credit_card,
        'purpose:debt_consolidation': purpose_debt_consolidation,
        'purpose:educational': purpose_educational,
        'purpose:home_improvement': purpose_home_improvement,
        'purpose:house': purpose_house,
        'purpose:major_purchase': purpose_major_purchase,
        'purpose:medical': purpose_medical,
        'purpose:moving': purpose_moving,
        'purpose:other': purpose_other,
        'purpose:renewable_energy': purpose_renewable_energy,
        'purpose:small_business': purpose_small_business,
        'purpose:vacation': purpose_vacation,
        'purpose:wedding': purpose_wedding,
    }


# create a list of all the reference categories, i.e. one category from each of the global features
ref_categories = ['mths_since_last_credit_pull_d:>75', 'mths_since_issue_d:>122', 'mths_since_earliest_cr_line:>434', 'total_rev_hi_lim:>79,780', 
                  'total_rec_int:>7,260', 'total_pymnt:>25,000', 'out_prncp:>15,437', 'revol_util:>1.0', 'inq_last_6mths:>4', 'dti:>35.191', 
                  'annual_inc:>150K', 'int_rate:>20.281', 'term:60', 'purpose:major_purch__car__home_impr', 'verification_status:Not Verified', 
                  'home_ownership:MORTGAGE', 'grade:G']	

# custom transformer class to create new categorical dummy features
class WoE_Binning(BaseEstimator, TransformerMixin):
    def __init__(self, X): # no *args or *kargs
        self.X = X
    def fit(self, X, y = None):
        return self #nothing else to do
    def transform(self, X):
        X_new = X.loc[:, 'grade:A': 'grade:G']
        X_new['home_ownership:OWN'] = X.loc[:,'home_ownership:OWN']
        X_new['home_ownership:MORTGAGE'] = X.loc[:,'home_ownership:MORTGAGE']
        X_new['home_ownership:OTHER_NONE_RENT'] = sum([X['home_ownership:OTHER'], X['home_ownership:NONE'], X['home_ownership:RENT']])
        X_new = pd.concat([X_new, X.loc[:, 'verification_status:Not Verified':'verification_status:Verified']], axis = 1)
        X_new['purpose:debt_consolidation'] = X.loc[:,'purpose:debt_consolidation']
        X_new['purpose:credit_card'] = X.loc[:,'purpose:credit_card']
        X_new['purpose:major_purch__car__home_impr'] = sum([X['purpose:major_purchase'], X['purpose:car'], X['purpose:home_improvement']])
        X_new['purpose:educ__ren_en__sm_b__mov'] = sum([X['purpose:educational'], X['purpose:renewable_energy'], X['purpose:small_business'], 
                                                        X['purpose:moving']])
        X_new['purpose:vacation__house__wedding__med__oth'] = sum([X['purpose:vacation'], X['purpose:house'], X['purpose:wedding'], 
                                                                   X['purpose:medical'], X['purpose:other']])
        X_new['term:36'] = np.where((X['term'] == 36), 1, 0)
        X_new['term:60'] = np.where((X['term'] == 60), 1, 0)
        X_new['int_rate:<7.071'] = np.where((X['int_rate'] <= 7.071), 1, 0)
        X_new['int_rate:7.071-10.374'] = np.where((X['int_rate'] > 7.071) & (X['int_rate'] <= 10.374), 1, 0)
        X_new['int_rate:10.374-13.676'] = np.where((X['int_rate'] > 10.374) & (X['int_rate'] <= 13.676), 1, 0)
        X_new['int_rate:13.676-15.74'] = np.where((X['int_rate'] > 13.676) & (X['int_rate'] <= 15.74), 1, 0)
        X_new['int_rate:15.74-20.281'] = np.where((X['int_rate'] > 15.74) & (X['int_rate'] <= 20.281), 1, 0)
        X_new['int_rate:>20.281'] = np.where((X['int_rate'] > 20.281), 1, 0)
        X_new['annual_inc:missing'] = np.where(X['annual_inc'].isnull(), 1, 0)
        X_new['annual_inc:<28,555'] = np.where((X['annual_inc'] <= 28555), 1, 0)
        X_new['annual_inc:28,555-37,440'] = np.where((X['annual_inc'] > 28555) & (X['annual_inc'] <= 37440), 1, 0)
        X_new['annual_inc:37,440-61,137'] = np.where((X['annual_inc'] > 37440) & (X['annual_inc'] <= 61137), 1, 0)
        X_new['annual_inc:61,137-81,872'] = np.where((X['annual_inc'] > 61137) & (X['annual_inc'] <= 81872), 1, 0)
        X_new['annual_inc:81,872-102,606'] = np.where((X['annual_inc'] > 81872) & (X['annual_inc'] <= 102606), 1, 0)
        X_new['annual_inc:102,606-120,379'] = np.where((X['annual_inc'] > 102606) & (X['annual_inc'] <= 120379), 1, 0)
        X_new['annual_inc:120,379-150,000'] = np.where((X['annual_inc'] > 120379) & (X['annual_inc'] <= 150000), 1, 0)
        X_new['annual_inc:>150K'] = np.where((X['annual_inc'] > 150000), 1, 0)
        X_new['dti:<=1.6'] = np.where((X['dti'] <= 1.6), 1, 0)
        X_new['dti:1.6-5.599'] = np.where((X['dti'] > 1.6) & (X['dti'] <= 5.599), 1, 0)
        X_new['dti:5.599-10.397'] = np.where((X['dti'] > 5.599) & (X['dti'] <= 10.397), 1, 0)
        X_new['dti:10.397-15.196'] = np.where((X['dti'] > 10.397) & (X['dti'] <= 15.196), 1, 0)
        X_new['dti:15.196-19.195'] = np.where((X['dti'] > 15.196) & (X['dti'] <= 19.195), 1, 0)
        X_new['dti:19.195-24.794'] = np.where((X['dti'] > 19.195) & (X['dti'] <= 24.794), 1, 0)
        X_new['dti:24.794-35.191'] = np.where((X['dti'] > 24.794) & (X['dti'] <= 35.191), 1, 0)
        X_new['dti:>35.191'] = np.where((X['dti'] > 35.191), 1, 0)
        X_new['inq_last_6mths:missing'] = np.where(X['inq_last_6mths'].isnull(), 1, 0)
        X_new['inq_last_6mths:0'] = np.where((X['inq_last_6mths'] == 0), 1, 0)
        X_new['inq_last_6mths:1-2'] = np.where((X['inq_last_6mths'] >= 1) & (X['inq_last_6mths'] <= 2), 1, 0)
        X_new['inq_last_6mths:3-4'] = np.where((X['inq_last_6mths'] >= 3) & (X['inq_last_6mths'] <= 4), 1, 0)
        X_new['inq_last_6mths:>4'] = np.where((X['inq_last_6mths'] > 4), 1, 0)
        X_new['revol_util:missing'] = np.where(X['revol_util'].isnull(), 1, 0)
        X_new['revol_util:<0.1'] = np.where((X['revol_util'] <= 0.1), 1, 0)
        X_new['revol_util:0.1-0.2'] = np.where((X['revol_util'] > 0.1) & (X['revol_util'] <= 0.2), 1, 0)
        X_new['revol_util:0.2-0.3'] = np.where((X['revol_util'] > 0.2) & (X['revol_util'] <= 0.3), 1, 0)
        X_new['revol_util:0.3-0.4'] = np.where((X['revol_util'] > 0.3) & (X['revol_util'] <= 0.4), 1, 0)
        X_new['revol_util:0.4-0.5'] = np.where((X['revol_util'] > 0.4) & (X['revol_util'] <= 0.5), 1, 0)
        X_new['revol_util:0.5-0.6'] = np.where((X['revol_util'] > 0.5) & (X['revol_util'] <= 0.6), 1, 0)
        X_new['revol_util:0.6-0.7'] = np.where((X['revol_util'] > 0.6) & (X['revol_util'] <= 0.7), 1, 0)
        X_new['revol_util:0.7-0.8'] = np.where((X['revol_util'] > 0.7) & (X['revol_util'] <= 0.8), 1, 0)
        X_new['revol_util:0.8-0.9'] = np.where((X['revol_util'] > 0.8) & (X['revol_util'] <= 0.9), 1, 0)
        X_new['revol_util:0.9-1.0'] = np.where((X['revol_util'] > 0.9) & (X['revol_util'] <= 1.0), 1, 0)
        X_new['revol_util:>1.0'] = np.where((X['revol_util'] > 1.0), 1, 0)
        X_new['out_prncp:<1,286'] = np.where((X['out_prncp'] <= 1286), 1, 0)
        X_new['out_prncp:1,286-6,432'] = np.where((X['out_prncp'] > 1286) & (X['out_prncp'] <= 6432), 1, 0)
        X_new['out_prncp:6,432-9,005'] = np.where((X['out_prncp'] > 6432) & (X['out_prncp'] <= 9005), 1, 0)
        X_new['out_prncp:9,005-10,291'] = np.where((X['out_prncp'] > 9005) & (X['out_prncp'] <= 10291), 1, 0)
        X_new['out_prncp:10,291-15,437'] = np.where((X['out_prncp'] > 10291) & (X['out_prncp'] <= 15437), 1, 0)
        X_new['out_prncp:>15,437'] = np.where((X['out_prncp'] > 15437), 1, 0)
        X_new['total_pymnt:<10,000'] = np.where((X['total_pymnt'] <= 10000), 1, 0)
        X_new['total_pymnt:10,000-15,000'] = np.where((X['total_pymnt'] > 10000) & (X['total_pymnt'] <= 15000), 1, 0)
        X_new['total_pymnt:15,000-20,000'] = np.where((X['total_pymnt'] > 15000) & (X['total_pymnt'] <= 20000), 1, 0)
        X_new['total_pymnt:20,000-25,000'] = np.where((X['total_pymnt'] > 20000) & (X['total_pymnt'] <= 25000), 1, 0)
        X_new['total_pymnt:>25,000'] = np.where((X['total_pymnt'] > 25000), 1, 0)
        X_new['total_rec_int:<1,089'] = np.where((X['total_rec_int'] <= 1089), 1, 0)
        X_new['total_rec_int:1,089-2,541'] = np.where((X['total_rec_int'] > 1089) & (X['total_rec_int'] <= 2541), 1, 0)
        X_new['total_rec_int:2,541-4,719'] = np.where((X['total_rec_int'] > 2541) & (X['total_rec_int'] <= 4719), 1, 0)
        X_new['total_rec_int:4,719-7,260'] = np.where((X['total_rec_int'] > 4719) & (X['total_rec_int'] <= 7260), 1, 0)
        X_new['total_rec_int:>7,260'] = np.where((X['total_rec_int'] > 7260), 1, 0)
        X_new['total_rev_hi_lim:missing'] = np.where(X['total_rev_hi_lim'].isnull(), 1, 0)
        X_new['total_rev_hi_lim:<6,381'] = np.where((X['total_rev_hi_lim'] <= 6381), 1, 0)
        X_new['total_rev_hi_lim:6,381-19,144'] = np.where((X['total_rev_hi_lim'] > 6381) & (X['total_rev_hi_lim'] <= 19144), 1, 0)
        X_new['total_rev_hi_lim:19,144-25,525'] = np.where((X['total_rev_hi_lim'] > 19144) & (X['total_rev_hi_lim'] <= 25525), 1, 0)
        X_new['total_rev_hi_lim:25,525-35,097'] = np.where((X['total_rev_hi_lim'] > 25525) & (X['total_rev_hi_lim'] <= 35097), 1, 0)
        X_new['total_rev_hi_lim:35,097-54,241'] = np.where((X['total_rev_hi_lim'] > 35097) & (X['total_rev_hi_lim'] <= 54241), 1, 0)
        X_new['total_rev_hi_lim:54,241-79,780'] = np.where((X['total_rev_hi_lim'] > 54241) & (X['total_rev_hi_lim'] <= 79780), 1, 0)
        X_new['total_rev_hi_lim:>79,780'] = np.where((X['total_rev_hi_lim'] > 79780), 1, 0)
        X_new['mths_since_earliest_cr_line:missing'] = np.where(X['mths_since_earliest_cr_line'].isnull(), 1, 0)
        X_new['mths_since_earliest_cr_line:<125'] = np.where((X['mths_since_earliest_cr_line'] <= 125), 1, 0)
        X_new['mths_since_earliest_cr_line:125-167'] = np.where((X['mths_since_earliest_cr_line'] > 125) & (X['mths_since_earliest_cr_line'] <= 167), 1, 0)
        X_new['mths_since_earliest_cr_line:167-249'] = np.where((X['mths_since_earliest_cr_line'] > 167) & (X['mths_since_earliest_cr_line'] <= 249), 1, 0)
        X_new['mths_since_earliest_cr_line:249-331'] = np.where((X['mths_since_earliest_cr_line'] > 249) & (X['mths_since_earliest_cr_line'] <= 331), 1, 0)
        X_new['mths_since_earliest_cr_line:331-434'] = np.where((X['mths_since_earliest_cr_line'] > 331) & (X['mths_since_earliest_cr_line'] <= 434), 1, 0)
        X_new['mths_since_earliest_cr_line:>434'] = np.where((X['mths_since_earliest_cr_line'] > 434), 1, 0)
        X_new['mths_since_issue_d:<79'] = np.where((X['mths_since_issue_d'] <= 79), 1, 0)
        X_new['mths_since_issue_d:79-89'] = np.where((X['mths_since_issue_d'] > 79) & (X['mths_since_issue_d'] <= 89), 1, 0)
        X_new['mths_since_issue_d:89-100'] = np.where((X['mths_since_issue_d'] > 89) & (X['mths_since_issue_d'] <= 100), 1, 0)
        X_new['mths_since_issue_d:100-122'] = np.where((X['mths_since_issue_d'] > 100) & (X['mths_since_issue_d'] <= 122), 1, 0)
        X_new['mths_since_issue_d:>122'] = np.where((X['mths_since_issue_d'] > 122), 1, 0)
        X_new['mths_since_last_credit_pull_d:missing'] = np.where(X['mths_since_last_credit_pull_d'].isnull(), 1, 0)
        X_new['mths_since_last_credit_pull_d:<56'] = np.where((X['mths_since_last_credit_pull_d'] <= 56), 1, 0)
        X_new['mths_since_last_credit_pull_d:56-61'] = np.where((X['mths_since_last_credit_pull_d'] > 56) & (X['mths_since_last_credit_pull_d'] <= 61), 1, 0)
        X_new['mths_since_last_credit_pull_d:61-75'] = np.where((X['mths_since_last_credit_pull_d'] > 61) & (X['mths_since_last_credit_pull_d'] <= 75), 1, 0)
        X_new['mths_since_last_credit_pull_d:>75'] = np.where((X['mths_since_last_credit_pull_d'] > 75), 1, 0)
        X_new.drop(columns = ref_categories, inplace = True)
        return X_new

loan_data = pd.read_csv("loan_data_2007_2014.csv")
loan_data.dropna(thresh = loan_data.shape[0]*0.2, axis = 1, inplace = True)
loan_data.drop(columns = ['id', 'member_id', 'sub_grade', 'emp_title', 'url', 'desc', 'title',
                          'zip_code', 'next_pymnt_d', 'recoveries', 'collection_recovery_fee',
                          'total_rec_prncp', 'total_rec_late_fee'], inplace = True)

#limpieza de la columna emp_length, asignacion de NAN a 0's y conversion a numerico
loan_data['emp_length'] = loan_data['emp_length'].str.replace('\+ years', '')
loan_data['emp_length'] = loan_data['emp_length'].str.replace('< 1 year', str(0))
loan_data['emp_length'] = loan_data['emp_length'].str.replace(' years', '')
loan_data['emp_length'] = loan_data['emp_length'].str.replace(' year', '')
loan_data['emp_length'] = pd.to_numeric(loan_data['emp_length'])
loan_data['emp_length'].fillna(value = 0, inplace = True)

#eliminacion de 'months' de la columna term y conversion a numericos 
loan_data['term'] = pd.to_numeric(loan_data['term'].str.replace(' months', ''))


#funcion creada para asignar el formato de fecha datatime de python
def date_columns(df, column):
    # store current month
    today_date = pd.to_datetime('2020-08-01')
    # convert to datetime format
    df[column] = pd.to_datetime(df[column], format = "%b-%y")
    # calculate the difference in months and add to a new column
    df['mths_since_' + column] = round(pd.to_numeric((today_date - df[column]) / 
							np.timedelta64(1, 'M')))
    # make any resulting -ve values to be equal to the max date
    df['mths_since_' + column] = df['mths_since_' + column].apply(
		lambda x: df['mths_since_' + column].max() if x < 0 else x)
    # drop the original date column
    df.drop(columns = [column], inplace = True)

date_columns(loan_data, 'earliest_cr_line')
date_columns(loan_data, 'issue_d')
date_columns(loan_data, 'last_pymnt_d')
date_columns(loan_data, 'last_credit_pull_d')
# se crea en una nueva columna basada en la información anterior, esta sera nuestra variable objetivo
loan_data['good_bad'] = np.where(loan_data.loc[:, 'loan_status'].isin(['Charged Off', 'Default',
                                                                       'Late (31-120 days)',
                                                                       'Does not meet the credit policy. Status:Charged Off']),
                                 0, 1)
# se elimina la columna original
loan_data.drop(columns = ['loan_status'], inplace = True)
X = loan_data.drop('good_bad', axis = 1)
woe_transform = WoE_Binning(X)

##########


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

st.write("Tu score es", y_score[0])