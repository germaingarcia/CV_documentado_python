#!/usr/bin/env python
# coding: utf-8
from pathlib import Path
from PyPDF2 import PdfMerger, PdfReader
from putNumber import putNumberPages
import os

def mergeFiles(df_Index,dfs_dict,path_Files,pdf_output_dir):
	merger = PdfMerger()
	Number_of_Pages = 1
	for index, row in df_Index.iterrows():
		pageNumber = []
		#if(row['Pagina']!='DatosPersonales'):
		for i,r in dfs_dict[row['Pagina']].iterrows():
			file_name = '' if r['LinkDocumento'].strip()=='nan' else r['LinkDocumento'].strip()
			if file_name != '':
				merger.append(PdfReader(str(path_Files /file_name),"rb"))
				pageNumber.append(str(Number_of_Pages))
				Number_of_Pages+=(len(PdfReader(str(path_Files /file_name),"rb").pages))
			else:
				pageNumber.append('')
		dfs_dict[row['Pagina']]['PageNumber'] = pageNumber
	merger.write(str(pdf_output_dir / f"temp.pdf"))
	merger.close()
	putNumberPages(str(pdf_output_dir / f"temp.pdf"),str(pdf_output_dir / f"CV_Combinado.pdf"))
	#os.remove(str(pdf_output_dir / f"temp.pdf"))

