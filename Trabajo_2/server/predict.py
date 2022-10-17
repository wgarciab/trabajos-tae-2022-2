import dill
import pandas as pd

#server
def prediccion_riesgo(dic):
    modelo= dill.load(open("/work/model2.pkl", "rb"))
    data=pd.DataFrame(data=dic,index=[0])
    prediccion=modelo.predict_proba(data)
    return prediccion[0][1]