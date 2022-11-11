import streamlit as st
from server.pre_process import getWoeTransform
from server.get_score import get_score

@st.cache
def load_data():
    woe_transform = getWoeTransform()
    return woe_transform

woe_transform = load_data()

st.write("""
# Credit Scorecard
Conoce tu score crediticio!


Esta aplicación está destinada a las personas que desean calcular su score crediticio y evaluar su pocisión frente a las entidades bancarias antes de realizar un préstamo.

""")

# st.write("[Reporte](https://deepnote.com/@tae-2022-2/Trabajo-2-2d8bceee-9d6f-499d-a2bd-fd29b704bf2c)")
# st.write("[Video](https://www.youtube.com/watch?v=F9fa0imsUdk)")

url_reporte = 'https://deepnote.com/@tae-2022-2/Trabajo-2-2d8bceee-9d6f-499d-a2bd-fd29b704bf2c'


st.markdown(f'''
<a href={url_reporte}><button style="background-color:GreenYellow;">Reporte técnico</button></a>
''',
unsafe_allow_html=True)

url_video= '[Video](https://www.youtube.com/watch?v=F9fa0imsUdk)'
st.markdown(link, unsafe_allow_html=True)

term = st.radio('Selecciona el término del préstamo (cuotas)', [36, 60])
int_rate = st.number_input('Digita la tasa de interés del préstamo (%)', min_value=0, max_value=30)
grade = st.selectbox(
    '¿Cual es la clasificación del crédito?',
     ['A', 'B', 'C', 'D', 'E', 'F', 'G'])
emp_length = st.slider('¿Cuantos años has trabajado?', min_value=0, max_value=10)
home_ownership = st.selectbox(
    '¿Cual es tu estado de propiedad de vivienda?',
     ['MORTGAGE', 'OWN', 'RENT', 'NONE', 'OTHER'])
annual_inc = st.number_input('¿Cuáles son tus ingresos anuales?', min_value=0, max_value=5000000)
verification_status = st.selectbox(
    '¿Tus ingresos o los de tu co-deudor han sido verificados?',
     ['Verified', 'Not Verified', 'Source Verified'])
purpose = st.selectbox(
    '¿Cual es el propósito del préstamo?',
     ['car', 'credit_card', 'debt_consolidation', 'educational', 
     'home_improvement', 'house', 'major_purchase', 'medical', 
     'moving', 'other', 'renewable_energy', 'small_business', 'vacation', 'wedding'])
dti = st.number_input('Digita el dti (relación deuda-ingreso)', min_value=0, max_value=40)
inq_last_6mths = st.slider('Selecciona el número de consultas en los últimos 6 meses', min_value=0, max_value=20)
revol_util = st.number_input('Digita la cantidad del crédito utilizado respecto al credito rotatorio', min_value=0, max_value=400)
total_acc = st.slider('Selecciona el numero de líneas actuales en el expediente crediticio', min_value=1, max_value=100)
out_prncp = st.number_input('Digita el capital restante para el préstamo total', min_value=0, max_value=50000)
total_pymnt = st.number_input('Digita los pagos realizados hasta la fecha por el préstamo total', value=30000, min_value=0, max_value=100000)
total_rec_int = st.number_input('Digita los intereses pagados hasta la fecha', value=30000, min_value=0, max_value=50000)
last_pymnt_amnt = st.number_input('Digita el importe del último pago total realizado', value=30000, min_value=0, max_value=50000)
tot_cur_bal = st.number_input('Digita el saldo actual total de todas las cuentas', value=2000000, min_value=0, max_value=5000000)
total_rev_hi_lim = st.number_input('Digita el límite de crédito/crédito superior renovable total', value=32000, min_value=0, max_value=2000000)
mths_since_earliest_cr_line = st.number_input('Digita el número de meses desde que abriste la primera línea de crédito', value=79, min_value=0, max_value=1000)
mths_since_issue_d = st.number_input('Digita el el número de meses desde el momento en que se financió el préstamo', value=79, min_value=0, max_value=500)
mths_since_last_pymnt_d = st.number_input('Digita el número de meses desde que realizaste el último pago', value=79, min_value=0, max_value=500)
mths_since_last_credit_pull_d = st.number_input('Digita el número de meses desde que la entidad prestamista sacó crédito para tu préstamo', value=79, min_value=0, max_value=500)

#grade
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
elif grade == 'G': grade_G = 1

#home ownership
home_ownership_MORTGAGE = 0
home_ownership_NONE = 0
home_ownership_OTHER = 0
home_ownership_OWN = 0
home_ownership_RENT = 0

if home_ownership == 'MORTGAGE': home_ownership_MORTGAGE = 1
elif home_ownership == 'NONE': home_ownership_NONE = 1
elif home_ownership == 'OTHER': home_ownership_OTHER = 1
elif home_ownership == 'OWN': home_ownership_OWN = 1
elif home_ownership == 'RENT': home_ownership_RENT = 1

#verification
verification_status_Not_Verified = 0
verification_status_Source_Verified = 0
verification_status_Verified = 0

if verification_status == 'Not Verified': verification_status_Not_Verified = 1
elif verification_status == 'Source Verified': verification_status_Source_Verified = 1
elif verification_status == 'Verified': verification_status_Verified = 1

#purpose
purpose_car= 0
purpose_credit_card= 0
purpose_debt_consolidation= 0
purpose_educational= 0
purpose_home_improvement= 0
purpose_house= 0
purpose_major_purchase= 0
purpose_medical= 0
purpose_moving= 0
purpose_other= 0
purpose_renewable_energy= 0
purpose_small_business= 0
purpose_vacation= 0
purpose_wedding= 0

if purpose == 'car': purpose_car = 1
elif purpose == 'credit_card': purpose_credit_card = 1
elif purpose == 'debt_consolidation': purpose_debt_consolidation = 1
elif purpose == 'educational': purpose_educational = 1
elif purpose == 'home_improvement': purpose_home_improvement = 1
elif purpose == 'house': purpose_house = 1
elif purpose == 'major_purchase': purpose_major_purchase = 1
elif purpose == 'medical': purpose_medical = 1
elif purpose == 'moving': purpose_moving = 1
elif purpose == 'other': purpose_other = 1
elif purpose == 'renewable_energy': purpose_renewable_energy = 1
elif purpose == 'small_business': purpose_small_business = 1
elif purpose == 'vacation': purpose_vacation = 1
elif purpose == 'wedding': purpose_wedding = 1

  
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

calcular = st.sidebar.button('Calcular Score!')

if (calcular):
    st.sidebar.write('# Resultados')
    st.sidebar.write("## Tu score es ", score)

    if (score > 549.36):
        score_info = '## Felicidades! Tu Score es mayor que el promedio!'
        st.balloons()

    elif (score < 549.36):
        score_info = '## Oh no! Tu Score es menor que el promedio :('
        st.snow()

    st.sidebar.write(score_info)

    st.sidebar.write("""
    El score promedio de la población es 549.36
    El mínimo score que puedes obtener es 300, y el máximo es 850.
    """)
