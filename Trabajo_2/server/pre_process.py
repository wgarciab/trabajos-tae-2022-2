import pandas as pd
import numpy as np
from server.WoE_Binning import WoE_Binning

def getWoeTransform():
    # LOCAL
    # loan_data = pd.read_csv("loan_data_2007_2014.csv")
    # loan_data = pd.read_csv("head_loan_data.csv")

    # REMOTO
    loan_data = pd.read_csv("Trabajo_2/head_loan_data.csv")

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

    return woe_transform