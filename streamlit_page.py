# -*- coding: utf-8 -*-
"""
Created on Sun Feb 27 21:54:23 2022

@author: torque
"""

import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config()


inits=pd.read_pickle('df_inits.pkl')
words=pd.read_pickle('word_ratings.pkl')
words2=words[['word','ratio']]
def recode(input):
    output=round(int(input))
    return output
words2.ratio=words2.ratio.apply(recode).copy(deep=True)

st.title('Iniciativas Populares de Norma en la Constituyente')
st.subheader('Un Análisis Cuantitativo')

st.write('He analizado el texto de 2444 de las iniciativas populares de norma\npropuestas por los chilenos durante (fechas). \nel único criterio de inclusión fué que la iniciativa tuviera más de 10 apoyos.\nno se incluyen los párrafos asociados a la propuesta de articulado ni\nlos que describen al grupo que propone la idea')

buto = st.button('Explicación') 
             
if buto:
     st.write('''Lo que queremos hacer aquí es utilizar los textos
              de las iniciativas como una especie de barómetro de las preocupaciones y las aspiraciones de 
              los chilenos, o al menos de los chilenos que escribieron propuestas de iniciativa popular de norma:
              La pregunta (o más bien, una pregunta que uno puede hacerse y que parece interesante) es: 
              ¿qué están pensando las personas que se dieron el trabajo de subir una iniciativa popular
              de norma? para respondernos a esto, utilizamos Python para contar cuántas veces aparece cada palabra en 
              las iniciativas populares. Naturalmente, las palabras más comúnes son siempre más o menos las mismas 
              en cualquier idioma: en el caso del castellano, estas son palabras como "de", "con", "el", "la", "los", "las", etcétera.  ''')
              
     st.write('''Pero la cuestión de interés no es qué palabras son más comunes en castellano en general, sino
              más bien cuáles palabras son especialmente frecuentes en las iniciativas populares respecto de 
              la frecuencia que esa palabra en particular suele tener en el idioma castellano: a esto le llamaremos
              el Puntaje de la palabra y la hemos calculado como la razón entre la frecuencia (en partes por millón) de
              una cierta palabra en el texto de las iniciativas y la frecuencia que esta suele tener en el idioma. un 
              puntaje de 10, por ejemplo, significa que la palabra aparece *diez veces más* en las iniciativas que 
              en un texto castellano cualquiera. Abajo tenemos las palabras que tienen ese puntaje o más''')
              
     st.write('''Esto es una forma sistemática de hacer algo que las personas hacemos todos los días de manera natural, 
              por ejemplo si estamos hablando con alguien, y esta persona a cada rato habla de pasteles, papas fritas, 
              asados y galletas, es razonable sospechar que es por algo: ¿quizás tiene hambre? Esto es lo mismo, pero con un
              volumen más grande de texto''')
     
words=words.reset_index().drop(columns=['index','ratio_times_rae','ratio_times_init','ratio_over_rae','ratio_over_init','ratio^2*freq'])
words=words.set_index('word')


print(words.loc['pandemia'])
print(words['ratio'])
list_color = ['antiquewhite','linen','linen','linen','antiquewhite']
      
       


vava=list(['','Cuántas veces aparece en las iniciativas','Partes por millon en el cuerpo de la RAE','Partes por millon en el texto de las iniciativas','Puntaje'])
figdata=[go.Table(
    header=dict(values=vava,
                fill_color=list_color,
                align='center',
                line_width=7
                ),
    cells=dict(values=[words.index.values, words.freq, words.ppm_rae,words.ppm_init,words.ratio],
               fill_color=list_color,
               format=['',".0f",".2f",".2f",".0f"],
               height=20,
               )
    )]


fig = go.FigureWidget(data=figdata) 

fig.update_layout(
    margin=dict(l=10, r=10, t=33, b=33),
)

st.plotly_chart(fig, use_container_width=True)




#fig.show()
#words=words.reindex(list)
#print(words['word'])
#print(words.loc[519])
#print(words)
