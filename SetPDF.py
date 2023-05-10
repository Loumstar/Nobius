# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 12:41:22 2020

@author: pbjohnso

This script turns a set of JSON files into a .tex and compiled PDF form. It is
experimental in two senses:
    - Not all JSON content converts properly to LaTeX
    - Not all valid .tex files compile successfully with Python PDFLaTeX

With further development it could be incorporated into the Sheet Generator, but
is currently separate.

To use this script, in the 'Sheet Generator' folder, type 'python SetPDF 3' or
replace '3' with another integrer 0<i<100. This will compile the set in folder
't02' within the folder nominated at the last line of this code [needs to be
turned into a variable]
"""

import json
import os
import sys
import re
import argparse
import tempfile
import shutil
import subprocess
from subprocess import PIPE
from PyPDF2 import PdfFileMerger, PdfFileReader

def load_json_file(filepath):
    # Copied from Pierre/Louis
    with open(filepath, 'r') as f:
        try:
            json_dictionary = json.load(f)
        except json.JSONDecodeError as e:
            print(validation.get_path_string([os.path.basename(filepath)]))
            sys.tracebacklimit = 0
            raise e

    return json_dictionary

def html_to_tex(input):
    # The JSON includes HTML that needs removing or replacing
    replacements = [
        (r'<ol.*?>(.*?)<\/ol>', r'\\begin{enumerate}[(i)]\1\\end{enumerate}'),
        (r'<ul.*?>(.*?)<\/ul>', r'\\begin{itemize}\1\\end{itemize}'),
        (r'\\begin{array}(.*?)\\end{array}', r'$\\begin{array}\1\\end{array}$'),
        (r'<li>', r'\\item '), # Note \n will ruin a list so should be used to replace <br> only after a list is replaced.
        (r"<br>", r'\n'),
        (r'<p>', r'\\\\ '), #affects \item <p>
        (r'</p>', r'\\\\ '),
        (r'<i>(.*?)</i>', r'\\emph{\1}'),
        (r'&amp;', r'&'),
        (r'%', r'\\%'), #Replace HTML % with LaTeX \%
        (r'&nbsp;', r'~'),
        #(r'_', r'\textunderscore'), #Sometimes useful, sometimes not
        (r'<(.*?)>', r' '), #Remove HTML tags if not parsed
        (r'&lt;', r'<'), #Replace HTML > and < symbols after removing tags
        (r'&gt;', r'>') #Replace HTML > and < symbols after removing tags

    ]

    # Apply replaces to str
    for pattern, repl in replacements:
        input = re.sub(pattern, repl, input)
    output=input
    return output

def clean_algorithm(input,PDF_values):
    # The JSON includes algorithmic variables that need replacing

    for i in PDF_values:
        input=re.sub('\$'+i[0]+'(?!D|2)',str(i[1]),input)
        # Note requirement that expression is not followed by 'D'
        # Otherwise e.g. $TAD would be recognised as $TA.
    output=input
    return output

'''
Generate a PDF file from TeX, this uses a command (pdflatex) part of the TeX distribution
 - output dir: pdflatex generates a lot of unwanted files, we output everything to temp, and copy the pdf over afterwards
 - interaction: batchmode will essentially supress all the errors (not very nice for debugging)

We have to move to the directory the tex_path is, so that images can be rendered properly
'''
def generate_pdf_output(tex_path, pdf_path):
    print(f"[PDF] Getting reading to generate {os.path.basename(pdf_path)}")

    # Check if pdflatex is installed
    if shutil.which("pdflatex") is None:
        print("\033[91m[ERROR] pdflatex is not an executable on this system (check PATH and install)\033[0m")
        return

    # Jump to the same directory as tex_path
    initDir = os.getcwd()
    os.chdir(os.path.split(tex_path)[0])

    # Open a temp directory
    with tempfile.TemporaryDirectory() as td:
        # Setup command to pdflatex
        args = ["pdflatex",
                f"-output-directory={td}",
                "-jobname=temp_pdf",
                "-interaction=batchmode",
                os.path.basename(tex_path)]

        # Send command
        fp = subprocess.run(args, timeout=15, stdout=PIPE, stderr=PIPE)

        # If all went well, we can copy the pdf file over
        temp_pdf_path = os.path.join(td, 'temp_pdf.pdf')
        if os.path.isfile(temp_pdf_path):
            shutil.move(temp_pdf_path, pdf_path)
            print(f"\033[92m[PDF] Success! Created {os.path.basename(pdf_path)} \033[0m")

        # Error handling
        else:
            print("\033[91m[ERROR] Something went wrong with running pdflatex\033[0m")
            temp_log_path = os.path.join(td, "temp_pdf.log")
            if os.path.isfile(temp_log_path):
                print("\033[96m[PDF] Log available, print? [Y/N]: \033[0m", end='')
                if str(input()).lower() == "y":
                    with open(temp_log_path, 'r') as file:
                        for line in file.readlines():
                            print('\033[93m'+line.rstrip()+'\033[0m')
            else:
                print("\tLog file wasn't even created, printing CompletedProcess object")
                print(fp)

    # Jump back to the initial directory
    os.chdir(initDir)

def generate_tex_output(sheetDir, no_pdf, pages_acc=None, tmp_merge_folder=None):
    # Templates should be in same place relative to sheet generating scripts
    header_file=os.path.abspath('templates/header.tex') # LaTeX header

    # Load sheetInfo
    sheetInfo=load_json_file(os.path.join(sheetDir ,'SheetInfo.json'))
    print('[TEX] Generating outputs for '+str(len(sheetInfo['questions']))+' questions in Set '+ os.path.basename(sheetDir) +' "'+sheetInfo['name']+'"...')

    # Create the media folder if it doesn't already exist
    os.makedirs(os.path.join(sheetDir, 'media'), exist_ok=True)

    # Both output files
    outputfile_tex = os.path.join(sheetDir, 'media', sheetInfo['name']+'.tex')
    if tmp_merge_folder:
        # When batch rendering, we send the pdf to a separate temporary dir, to be merged later. We shouldn't render them to their respecive 'media' folders as they have modified page numbers
        outputfile_pdf = os.path.join(tmp_merge_folder, sheetInfo['name']+'.pdf')
    else:
        outputfile_pdf = os.path.join(sheetDir, 'media', sheetInfo['name']+'.pdf')

    with open(outputfile_tex, 'w') as f: #output tex file
        # Header of LaTeX file
        with open(header_file, 'r') as header:
            for line in header: # Copy all lines from the header
                f.write(line)

        # If in batchmode, set the correct page number
        if pages_acc:
            f.write("\setcounter{page}{"+str(pages_acc+1)+"}")

        # This is the first page of batchmode
        if pages_acc == 0:
            f.write("\maketitle")
            f.write("\pagebreak")

        f.write('\\ETrule')
        f.write('\\setcounter{section}{'+ str(sheetInfo["number"]-1) +'}')
        f.write('\\section{'+sheetInfo['name']+'}')
        f.write('\\ETrule Note: this sheet was automatically generated from online Problem Sets. Not all content translates to the offline version, please visit the online version, accessible via BB, for full content.')

        for question in  range(0,len(sheetInfo['questions'])):
            #print('Q'+str(question+1))
            content=load_json_file(os.path.join(sheetDir, sheetInfo['questions'][question]+'.json'))

            f.write('')
            f.write('\\ETrule')
            f.write(r'\subsection{')
            f.write(content["title"])
            f.write('}\n')

            #Master statement
            new_master=html_to_tex(content["master_statement"]) # Clean HTML
            if 'algorithm' in content.keys(): #Clean algorithmic variables
                new_master=clean_algorithm(new_master,content['PDF_values'])
            f.write(new_master)

            if 'media' in content.keys():   # If there is media
                f.write(r'\begin{center}')
                for pic in content['media']:# Loop over all media
                    # Insert graphics
                    if pic[-3:] in ['jpg','png','pdf']:  # Only accept these file types
                        f.write('\\includegraphics[clip=true,height=0.5\\textwidth]{'+pic+'}\\\\')
                f.write(r'\end{center}')
            nparts=len(content['parts']);       # Initialise number of parts
            if nparts>1:    # For multiple parts
                f.write(r'\begin{enumerate}[(a)]')  # Generate part names (a), (b) etc.)
            for i in range(0,nparts):           # Loop over all parts
                if nparts>1:
                    f.write('\\item ')              # Add label (a) etc.
                #Enter content with HTML removed
                new_content=html_to_tex(content['parts'][i]['statement']) # Clean HTML
                if 'algorithm' in content.keys(): #Clean algorithmic variables
                    new_content=clean_algorithm(new_content,content['PDF_values'])
                f.write(new_content)
                # Any content encoded especially for LaTeX
                if 'latex_only' in content['parts'][i].keys():
                    f.write(content['parts'][i]['latex_only'])
                #Any extra content in the response areas
                if 'response' in content['parts'][i].keys():
                    if 'Non Permuting Multiple Choice' in content['parts'][i]['response']['mode'] or 'Non Permuting Multiple Selection' in content['parts'][i]['response']['mode']:
                        f.write('\\begin{itemize}')
                        for choice in content['parts'][i]['response']['choices']:
                            # The usual clean and sheen routine ...
                            new_content=html_to_tex(re.sub('<p>', '', choice)) # Clean HTML
                            # Additional catch for any <p> after \item
                            if 'algorithm' in content.keys(): #Clean algorithmic variables
                                new_content=clean_algorithm(new_content,content['PDF_values'])
                            f.write('\\item '+new_content)
                        f.write('\\end{itemize}')

            if nparts>1:
                f.write('\\end{enumerate}')         # Close labels

        # Footer of LaTeX file
        f.write('\\ETrule\\end{document}')

    print(f"[TEX] Sheet tex compiled and saved to {sheetInfo['name']}.tex")

    if not no_pdf: generate_pdf_output(outputfile_tex, outputfile_pdf)

    return outputfile_pdf

parser = argparse.ArgumentParser(description="Problem Set PDF compiler based on JSON files")
parser.add_argument("--sheet-path", "-s", help="Path to the Sheet folder (if the -batch flag is set, this is interpreted as a directory containing multiple sheet folders)", required=True)
parser.add_argument("--no-pdf", help="Set this flag to disable converting the rendered .tex file into a PDF", action="store_true")
parser.add_argument("--batch-mode", "-b", help="Set this flag to render multiple sheets at once", action="store_true")
args = parser.parse_args()

# Just render out one sheet
if not args.batch_mode:
    print(f"[INIT] Starting SetPDF with sheet {os.path.basename(args.sheet_path)} (pdf_write={bool(args.no_pdf)}) (batchmode=False)")
    generate_tex_output(args.sheet_path, args.no_pdf)

# Batch mode
elif not args.no_pdf:
    print(f"[INIT] Starting SetPDF with sheets in {os.path.basename(args.sheet_path)} (pdf_write={bool(args.no_pdf)}) (batchmode=True)")

    # Get all directories inside the sheets path given
    sheets = [i for i in os.listdir(args.sheet_path) if os.path.isfile(os.path.join(args.sheet_path, i, "SheetInfo.json"))]

    print(f"[INIT] Going to render the following sheets in a temporary directory before merging.")
    print(f"└───{os.path.basename(args.sheet_path)}", end='')
    print('\n    ├─── ' + '\n    ├─── '.join(sheets[:-1]), end='')
    print(f'\n    └─── {sheets[-1]}\n')

    with tempfile.TemporaryDirectory() as tmp_merge_folder:
        print(f"[DEBUG] Temp dir is in {tmp_merge_folder}")
        # Render out each of the individual sheets, recording where their PDFs were placed
        rendered_pdfs = []
        pages_acc = 0
        for sheet in sheets:
            new_pdf = generate_tex_output(os.path.join(args.sheet_path, sheet), args.no_pdf, pages_acc, tmp_merge_folder)
            pages_acc += PdfFileReader(new_pdf).numPages # add however many pages we just rendered
            rendered_pdfs.append(new_pdf)

        # Merge all PDFs into one file
        print(f"[PDF Merge] Merging {len(rendered_pdfs)} rendered PDFs")
        mergedFile = PdfFileMerger()

        for pdf in rendered_pdfs:
            mergedFile.append(PdfFileReader(pdf, 'rb'))

    mergedFile.write(os.path.join(args.sheet_path, "MergedSheets.pdf"))
    print(f"\033[92m[PDF Merge] Merged all rendered PDFs Successfully! ({len(sheets)} accross {pages_acc} pages)\033[0m")

else:
    print(f"[ERROR] Both Batchmode and No_PDF were set - currently batchmode merging requires individual pdfs to be created")
    print("[ERROR] Render .tex files for each sheet instead (no merging or pdf) (Y/N)? ", end='')
    if str(input()).lower() == 'y':
        # Get all directories inside the sheets path given
        sheets = [i for i in os.listdir(args.sheet_path) if os.path.isfile(os.path.join(args.sheet_path, i, "SheetInfo.json"))]

        print(f"[INIT] Going to render the following sheets to their respective 'media' folder.")
        print(f"└───{os.path.basename(args.sheet_path)}", end='')
        print('\n    ├─── ' + '\n    ├─── '.join(sheets[:-1]), end='')
        print(f'\n    └─── {sheets[-1]}\n')

        # Render out each of the individual sheets
        for sheet in sheets:
            generate_tex_output(os.path.join(args.sheet_path, sheet), args.no_pdf)
