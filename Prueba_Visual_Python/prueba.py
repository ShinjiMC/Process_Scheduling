import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from matplotlib.transforms import Bbox
from datetime import datetime, timedelta
import pandas as pd



def convert(date):
    return datetime.strptime(date,"%d-%m-%Y")


datos=pd.read_excel('./Planificacion.xlsx')

if datos['Inicio'].dtypes=='datetime64[ns]':
    datos['DT inicio']=datos['Inicio']
    datos['Inicio']=datos['Inicio'].dt.strftime('%d/%m/%Y')
else:
    datos['DT inicio']=datos['Inicio'].apply(convert)
    
if datos['Fin'].dtypes=='datetime64[ns]':
    datos['DT fin']=datos['Fin']
    datos['Fin']=datos['Fin'].dt.strftime('%d/%m/%Y')
else:
    datos['DT fin']=datos['Fin'].apply(convert)
    
datos['DT duracion']=datos['DT fin']-datos['DT inicio']
datos['Color']=datos['Color'].replace(np.nan,'blue')

#datos['Avance']=datos['Avance'].replace(np.nan,0)
datos['Avance'] = datos['Avance'].replace('%', '', regex=True).astype(float) / 100


datos.reset_index(inplace=True)

# datos['DT duracion avance']=datos['DT duracion']*datos['Avance']
# Convertir los valores timedelta64 a días (o la unidad que prefieras)
datos['DT duracion'] = datos['DT duracion'] / np.timedelta64(1, 'D')

# Realizar la multiplicación con 'Avance'
datos['DT duracion avance'] = datos['DT duracion'] * datos['Avance']



hitos=datos[datos['DT duracion']==timedelta()]
nrows=datos.shape[0]
datos_tabla=datos[['Tarea','Inicio','Fin','DT duracion']]
duracion_total=datos['DT fin'].max()-datos['DT inicio'].min()
 


 
 
fig, ax=plt.subplots(1,1,figsize=(duracion_total.days/10,nrows*0.3),constrained_layout=True,sharex=False)
ax.invert_yaxis()
ax.barh(datos['index'],
        datos['DT duracion'],
        left=datos['DT inicio'],
        label=datos['Tarea'],
        color=datos['Color'],
        height=0.35,
        alpha=0.5)
ax.barh(datos['index'],
        datos['DT duracion avance'],
        left=datos['DT inicio'],
        label=datos['Tarea'],
        color=datos['Color'],
        height=0.15,
        alpha=1)
ax.scatter(hitos['DT inicio'],
           hitos['index'],
           marker='D',
           color=hitos['Color'],)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
# for d, l, r in zip(datos['DT fin'], datos['index'],datos['Avance']):
#     ax.annotate('{}%'.format(round(r*100),2),
#                 xy=(d,l),
#                xytext=(-3, np.sign(l)*3),
#                textcoords='offset points',
#                horizontalalignment='left')

for d, l, r in zip(datos['DT fin'], datos['index'],datos['Avance']):
    if not np.isnan(r):
        ax.annotate('{}%'.format(round(r*100), 2),
                    xy=(d, l),
                    xytext=(-3, np.sign(l)*3),
                    textcoords='offset points',
                    horizontalalignment='left')
    else:
        ax.annotate('N/A',
                    xy=(d, l),
                    xytext=(-3, np.sign(l)*3),
                    textcoords='offset points',
                    horizontalalignment='left')


table=ax.table(cellText=datos_tabla.to_numpy(),
              loc='left',
              colLabels=['Tarea','Inicio','Fin','Duracion'],
              colWidths=[0.02,0.02,0.02,0.03],
              bbox=(-0.6,0,0.6,(nrows+1)/nrows))
ax.margins(y=0.005)
table.auto_set_font_size(False)
table.set_fontsize(9)
ax.grid(True)
ax.yaxis.set_ticklabels([])
plt.savefig('Planificacion 1.pdf',bbox_inches='tight')

plt.show()