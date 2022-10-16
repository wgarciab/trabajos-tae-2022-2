import streamlit as st
from server.pre_process import getWoeTransform
from server.get_score import get_score

@st.cache
def load_data():
    woe_transform = getWoeTransform()
    return woe_transform

woe_transform = load_data()

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

score = get_score(dic, woe_transform)

st.write("Tu score es", score)