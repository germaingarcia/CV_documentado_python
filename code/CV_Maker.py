#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
from docxtpl import DocxTemplate
from pathlib import Path
from Merge_PDF import mergeFiles

# Path and Name of templates
#paths
pdf_files_Path = Path(__file__).parent / f"pdf_files" 
pdf_output_dir = Path(__file__).parent / "OUTPUT"
pdf_output_dir.mkdir(parents=True,exist_ok=True)

word_templates_path = Path(__file__).parent / f"WordTemplates"


sheet_path_Name = 'Template_CV.xlsx'
Documento_template_Main = "CV_Template_Main.docx"

subdoc_template_base = "base_Information.docx"
dic_Templates_Information = {'Información_Personal':'Template_personalInformation.docx',
                             'Título_Año':'Template_Titulo_Anho.docx',
                             'Lista_Items':'Template_Lista_Items.docx'}


df_Indice = pd.read_excel(sheet_path_Name, sheet_name='Indice')
df_Indice.sort_values(by=['Orden'],inplace=True)

# reading and storing different dataframes
dfs_Dics ={}
for index, row in df_Indice.iterrows():
    dfs_Dics[row['Pagina']] = pd.read_excel(sheet_path_Name, sheet_name=row['Pagina'])
    dfs_Dics[row['Pagina']].sort_values(by=['Orden'],inplace=True)
    dfs_Dics[row['Pagina']]['PageNumber'] = ''
    dfs_Dics['DatosPersonales']['LinkDocumento'] = dfs_Dics['DatosPersonales']['LinkDocumento'].astype('str')

dfs_Dics['DatosPersonales']['Datos'] = dfs_Dics['DatosPersonales']['Datos'].astype('str')
Temp_Dic = dfs_Dics['DatosPersonales'].set_index('Titulo').to_dict()['Datos']
# Documento Template
doc_Template = DocxTemplate(str(word_templates_path/Documento_template_Main))

#DatosPersonales
context = {}
#context['personalitems'] = dfs_Dics['DatosPersonales'][['Titulo','Datos']].to_dict('records')
context['nombre_completo'] = Temp_Dic['Nombre'] +' '+Temp_Dic['Apellidos']
context['Presentacion'] = Temp_Dic['Presentacion']
#doc_Template.render(context)

#MerginDocument
#In Dictionary of dataframes
#out dictionary of dataframes with NumberOf pages
mergeFiles(df_Indice,dfs_Dics,pdf_files_Path,pdf_output_dir)
#Function to add content to each section
def getDict(tempRow,NameFormat):
    Complemento = '' if tempRow['PageNumber'].strip()=='' else ' (Pag. '+tempRow['PageNumber']+')'
    if NameFormat =='Información_Personal':
        return {'Titulo':tempRow['Titulo'],'Datos':tempRow['Datos']+Complemento}
    elif NameFormat =='Título_Año':
        return {'anho':tempRow['Anho'],'titulo':tempRow['Titulo']+Complemento,'lugar':tempRow['Lugar'],'descripcion':tempRow['Descripcion']}
    else:
        return {'Information': ' - '.join(str(e) for e in list(tempRow.to_dict().values())) + Complemento}

def AgregarContenido(dd_context,documento,NombrePlantilla,df_temp,NameFormat,NameItem):
    pages = []
    for idx, tempRow in df_temp.iterrows():
        page_doc = DocxTemplate(NombrePlantilla)
        data =getDict(tempRow,NameFormat)#{'anho':tempRow['Anho'],'titulo':tempRow['Titulo']+' (Pag. '+tempRow['PageNumber']+')','lugar':tempRow['Lugar'],'descripcion':tempRow['Descripcion']}
        page_doc.render(context=data)

        sd = documento.new_subdoc()
        sd.subdocx = page_doc.docx

        pages.append(sd)

    dd_context[NameItem]= pages
    #documento.render(context)
# filling personal informaiton
#AgregarContenido(context,doc_Template,str(word_templates_path/dic_Templates_Information['Información_Personal']),dfs_Dics['DatosPersonales'],'Información_Personal','personalitems')
context['personalitems'] = [getDict(tempRow,'Información_Personal') for idx, tempRow in dfs_Dics['DatosPersonales'].iterrows()]
# Adding aditional Information
pages = []
for index, row in df_Indice.iterrows():
    if(row['Titulo']!='Datos Personales'):
        page_doc = DocxTemplate(str(word_templates_path/subdoc_template_base))
        data ={'Titulo_seccion':row['Titulo']}
           
        #Aqui llenamos el contenido
        AgregarContenido(data,page_doc,str(word_templates_path/dic_Templates_Information[row['Plantilla']]),dfs_Dics[row['Pagina']].drop(columns=['Orden','LinkDocumento',]),row['Plantilla'],'items')
        page_doc.render(data)
        sd = doc_Template.new_subdoc()
        sd.subdocx = page_doc.docx
        pages.append(sd)
context["pages"] = pages
doc_Template.render(context)
doc_Template.save(str(pdf_output_dir/"CV_Template_result.docx"))



# Datos académicos

