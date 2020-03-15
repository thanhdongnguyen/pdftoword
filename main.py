# -*- coding: utf-8 -*-
from docx import Document

import PyPDF2
import os 
import re


def check_enviroment():
    pass

def parse_input():
    import argparse
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "-i",
        required=True,
        help="Path Of File PDF"
    )
    parser.add_argument(
        "-o",
        required=True,
        help="Path Will Save File Docx"
    )
    args = parser.parse_args()
    file_pdf = args.i 
    save_path = args.o 

    extension, status = check_extension(file_pdf, "pdf")
    if extension == False:
        return extension, status
    extension, status = check_extension(save_path, "docx")
    if extension == False:
        return extension, status
    content, status = read_file_pdf(file_pdf)
    if status == False:
        print(content)
    is_save, status = save(content, save_path)
    return is_save, status


def check_permission(path, chmod: int):
    permissions = oct(os.stat(path).st_mode)[-3:]
    user_permission = permissions[2] 
    if int(user_permission) == chmod:
        return "this file: {} not permission read".format(path), False
    return "", True

def check_extension(path, extension):
    extension = re.search("\.{}$".format(extension), path) 
    if extension is None:
        return "file extension is not support", False
    return "", True

def read_file_pdf(path: str):
    if not os.path.exists(path) or not os.path.isfile(path):
        return "file not valid or path not exist", False 
    user_permission, status = check_permission(path, 3) 
    if status == False:
        return user_permission, status
    
    open_file = open(path, "rb")
    content = PyPDF2.PdfFileReader(open_file)
    pages = content.getNumPages()
    if pages == 0:
        return "this file: {} have page is 0".format(path), False
    
    return content, True
    

def save(content, path: str):
    '''
    user_permission, status = check_permission(path, 5)
    if status == False:
        return user_permission, status
    '''
    docx = Document()
    pages = content.getNumPages()
    for i in range(pages):
        docx.add_paragraph(content.getPage(i).extractText().encode("utf8"))

    docx.save(path)
    return "Success", True

if __name__ == "__main__":
    exec, status = parse_input()
    print(exec)
    exit()
