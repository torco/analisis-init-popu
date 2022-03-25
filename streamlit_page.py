# -- coding: utf-8 --
"""
Created on Sun Feb 27 21:54:23 2022

@author: tomas boncompte
"""

import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import re
import random

st.set_page_config()
base="light"

inits=pd.read_pickle('df_inits.pkl')
inits2=inits
words=pd.read_pickle('word_ratings.pkl')
words2=words[['word','ratio']]
def recode(input):
    output=round(int(input))
    return output
words2.ratio=words2.ratio.apply(recode).copy(deep=True)

st.title('Iniciativas Populares de Norma en la Constituyente')

st.write('Este análisis incluye 2444 de las iniciativas populares de norma\npropuestas por los chilenos durante enero de 2022. \nel único criterio de inclusión fué que la iniciativa tuviera más de 10 apoyos. Se muestra la frecuencia absoluta de cada palabra, cuánta frecuencia tiene en el corpus de referencia de la RAE y en las iniciativas mismas, y finalmente el puntaje, que representa cuánto más frecuente la palabra es en las iniciativas. ')


     
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

a = words2["word"]

buto = st.button('Qué es el puntaje?') 
             
if buto:
     st.write('''Lo que queremos hacer aquí es utilizar los textos
              de las iniciativas como una especie de barómetro de las preocupaciones y las aspiraciones de 
              los chilenos, o al menos de los chilenos que escribieron propuestas de iniciativa popular de norma:
              La pregunta (o más bien, una pregunta que uno puede hacerse y que parece interesante) es: 
              ¿qué están pensando las personas que se dieron el trabajo de subir una iniciativa popular
              de norma? para respondernos a esto contamos cuántas veces aparece cada palabra en 
              las iniciativas populares. Naturalmente, las palabras más comúnes son siempre más o menos las mismas 
              en cualquier idioma: en el caso del castellano, estas son palabras como "de", "con", "el", "la", "los", "las", etcétera.  ''')
              
     st.write('''Pero la cuestión de interés no es qué palabras son más comunes en castellano en general, sino
              más bien cuáles palabras son especialmente frecuentes en las iniciativas populares respecto de 
              la frecuencia que esa palabra en particular suele tener en el idioma castellano: a esto le llamaremos
              el Puntaje de la palabra y la hemos calculado como la razón entre la frecuencia (en partes por millón) de
              una cierta palabra en el texto de las iniciativas y la frecuencia que esta suele tener en el idioma. un 
              puntaje de 10, por ejemplo, significa que la palabra aparece diez veces más en las iniciativas que 
              en un texto castellano cualquiera. Abajo tenemos las palabras que tienen ese puntaje o más''')
              
     st.write('''Esto es una forma sistemática de hacer algo que las personas hacemos todos los días de manera natural, 
              por ejemplo si estamos hablando con alguien, y esta persona a cada rato habla de pasteles, papas fritas, 
              asados y galletas, es razonable sospechar que es por algo: ¿quizás tiene hambre? Esto es lo mismo, pero con un
              volumen más grande de texto''')

option = st.selectbox(
     'explorar palabra:',
    a)

inits = inits.sort_values(by='F_{}'.format(option), ascending=False)
contain_values = inits[inits['cuerpo'].str.contains(option)]

nombres=contain_values['nombre']
rat = words2.loc[words2['word']==option,'ratio'].iloc[0]
print('$$$$$$$$$')
print(rat)


st.write('es {} veces más frecuente de lo normal en las iniciativas'.format(rat))

a=inits2.sort_values(by='F_{}'.format(option))

#  construye la muestra random de frases

todas_frases = []
for index, each in inits.iterrows():
    text=each[1]
    splitted = re.split("[.,:;?()]",text)
    for phrase in splitted:
        todas_frases.append(phrase)
        
print(len(todas_frases))
print(todas_frases[12])

frases=[]
for each in todas_frases:
    if option in each and 'Breve reseña sobre quién o quiénes proponen y la historia de la elaboración de la iniciativa' not in each and len(each.split(' ')) > 7 and each.split(' ')[-1] != 'que' and 'Situación Ideal' not in each:
        frases.append(each)

buto_muestra = st.button('ver una muestra del uso de la palabra') 
if buto_muestra:
    sample=random.sample(frases, 3)
    st.markdown("""
<style>
.smol {
    font-size:12px !important;
    text-align: right;
}
</style>
""", unsafe_allow_html=True)
    for each in sample:
        k='{}{}{}'.format('<b>',option,'</b>')
        write=each.replace(option,k)
        for index, init in inits.iterrows():
            if each in init['cuerpo']:
                nombre=init['nombre']
                link=init['links']
        iqtlf = nombre
        linku= '<a href="'+link+'">[ver en contexto]</a>'
        linea =  '<p class="smol">'+write+' '+linku+'</p> '
        
        st.markdown(linea, unsafe_allow_html=True)
    
st.write('y aparece en {} iniciativas diferentes'.format(len(contain_values)))
option2 = st.selectbox(
     'iniciativa:',
    nombres)


cor = ''
for index, each in a.iterrows():
    if option2 in each[0]:
        cor=each[1]

k='{}{}{}'.format('<mark class="red">**',option,'**</mark>')
print(k)

k2='{}{}{}'.format('<mark class="red"><strong>',option,'</strong></mark>')
print(k2)

times = cor.count(option)
st.write('{} aparece {} veces en la iniciativa seleccionada'.format(option, times))

st.markdown("""
<style>
.init {
    font-size:13px !important;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

newcor=''
allowable = [' ','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'á', 'é', 'í', 'ó', 'ú', 'ñ', 'Ñ', '0', '1', '2','3','4','5','6','7','8','9','.',',',':',';','?','!']
for char in cor[:]:
    if char in allowable:
        newcor=newcor+char
        print(newcor)
cor = newcor

buto2 = st.button('Ver') 
if buto2:
    cor = cor.replace(option,k2)
    cor = cor.rstrip()
    cor=cor.replace('\n',' ')
    cor=cor.replace('Propuesta de articuladoPropuesta de articulado','Propuesta de articulado')
    cor='<br><br> <strong>Problema a Solucionar</strong><br>'+cor
    cor=cor.replace('Situación Ideal:','<br><br> <strong>Situación Ideal</strong><br>  ')
    cor=cor.replace('Qué debe Contemplar la Nueva Constitución:','<br><br> <strong>Qué debe Contemplar la Nueva Constitución</strong><br>  ')
    cor=cor.replace('¿Con qué argumentos tú o tu organización respaldan esta propuesta?','<br><br> <strong>¿Con qué argumentos tú o tu organización respaldan esta propuesta?</strong><br>  ')    
    cor=cor.replace('Propuesta de articulado','<br><br> <strong>Propuesta de articulado</strong><br>  ')
    cor=cor.replace('Breve reseña sobre quién o quiénes proponen y la historia de la elaboración de la iniciativa','<br><br> <strong>Breve reseña sobre quién o quiénes proponen y la historia de la elaboración de la iniciativa</strong><br>  ')
    
    cor=cor.replace('\r\n','')
    cor=cor.replace(u'\025','')
    cor=cor.replace('\n\r','')
    cor=cor.replace('\n','')
    cor=cor.replace(u'\036','')
    
    st.write('<p class="init">'+cor+'</p> ',unsafe_allow_html=True)
    
    
    

#%% this is just debug


#newcor=''
#allowable = [' ','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'á', 'é', 'í', 'ó', 'ú', 'ñ', 'Ñ', '0', '1', '2','3','4','5','6','7','8','9','.',',',':',';','?','!','(',')','-']
#for char in cor[:]:
#    if char in allowable:
#        newcor=newcor+char
#        print(newcor)
        

#%%

#emptylist=[]
#for index, each in inits2.iterrows():
#    text=each['cuerpo']
#    if 'terceros para poder trabajar y tener' in text:
#        emptylist.append(text)
        
