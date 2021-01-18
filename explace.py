# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 13:01:37 2021

@author: Batman

This scipt works for UTF-8 encoding only
"""

from pathlib import Path
import sys
import os

def fetch(p):
    """
    command to use: python script.py -f .html h2 (use your own file type and tag)
    """
    filetype = sys.argv[2]
    
    if filetype.startswith("-"): raise SystemExit("Only 1 flag allowed!")
    
    #list all required files in current direcorty tree
    paths = list(p.glob('**/*' + filetype))
    
    # 3D array for storing: path, line number, text
    text = [list(), list(), list()]
    
    # tag to find
    element = sys.argv[3]
    
    open_tag = "<" + element + ">"
    close_tag = '</' + open_tag[1:]
    
    length_open_tag = len(open_tag)
    
    for p in paths:
        with p.open() as file:
            content = file.readline()
            line = 0
            opened = False # whether tag is opened
            multiline_content = []
            
            while content != '':
                
                if opened:
                    # the opening tag was in previous line. skip the next block that finds open tag
                    close_index = content.find(close_tag)
                    
                    if close_index > -1:
                        opened = False
                        multiline_content.append(content[ : close_index])
                        
                        # update the list. the line number of the original opening tag line is already fed
                        text[0].append(str(p))
                        text[2].append(" ".join(multiline_content))
                        
                        del multiline_content[:]
                        
                    else:
                        # closing tag still not found
                        line+=1
                        content = file.readline()
                        continue
                        
                else:
                    open_index = content.find(open_tag)
                
                    # if opening tag is found
                    if open_index > -1:
                        opened  = True
                    
                        # look for closing tag.
                        close_index = content.find(close_tag)
                        
                        if close_index > -1:
                            opened = False
                            
                            # append path, line number and string data to list
                            text[0].append(str(p))
                            text[1].append(line)
                            text[2].append(content[open_index + length_open_tag : close_index])
                        
                        else: # closing tag not found on same line
                            # save content from lines
                            multiline_content.append(content[open_index + length_open_tag : ])
                            
                            # note the line number
                            text[1].append(line)
                    
                    line+=1
                    content = file.readline()
    
    # write the text list to a file
    
    with open("edit_data.txt", "w") as file:
        
        #iterate over lists inside text.
        for i in range(len(text[0])):
            file.write(text[0][i] + '\n') # path
            file.write(str(text[1][i]) + '\n') # line number
            file.write(text[2][i] + '\n') # text
            file.write('\n')

def replace(p):
    """
    command to use: python script.py -r h2 (use your own tag)
    """
    # tag to find
    try:
        element = sys.argv[2]
        
    except IndexError:
        raise SystemExit("No tag provided")
    
    open_tag = "<" + element + ">"
    close_tag = '</' + element + ">"
    length_open_tag = len(open_tag)
    
    try:
        # read the data.txt file that has the paths and changes
        with open("edit_data.txt", "r") as edit_data_reader:
            existed_in = "" # to check if changes are going to be made to same path
            path = ""
            put_cursor_at = 0 # Where to put the cursor, depending on if path is same
            lines = 0 # write lines as is until change_after_line_number reached
            
            while 1:
                exists_in = edit_data_reader.readline() # first line is path
                exists_in = exists_in.strip('\n')
                
                # if reached end of file, dont proceed
                if not exists_in:
                    break
                
                if exists_in != existed_in: # if not same path
                    # split to seperate path and file
                    tmp = exists_in.rsplit('\\', 1)
                    
                    has_dirs = True if len(tmp) == 2 else False
                    
                    # create the required directories
                    try:
                        if has_dirs:
                            path = Path.joinpath(p, "generated", tmp[0])
                            file = tmp[1]
                            
                        else:
                            path = Path.joinpath(p, "generated")
                            file = tmp[0]
                        
                        os.makedirs(path)
                        
                    except OSError:
#                        print("Directory: " + path + " couldn't be made.\n")
                        pass
                    
                    except FileExistsError:
#                        print("File already exists.\n")
                        pass
                    
                    # update previous path
                    existed_in = exists_in
                    # read from start, zero lines read
                    put_cursor_at = lines = 0
    
                # read from original file, write a copy incorporating the changes
                read_from = Path.joinpath(p, exists_in)
                write_to = Path.joinpath(path, file)
                
                with open(read_from, "r") as file_reader, open(write_to, "a") as file_writer:
                        file_reader.seek(put_cursor_at)
                        
                        # second line is line number after which exists the tag
                        change_after_line_number = int (edit_data_reader.readline())
                        
                        while lines != change_after_line_number:
                            file_writer.write(file_reader.readline())
                            lines+=1
                        
                        # cursor position at line start when it has the tag
                        cursor_at_line_start = file_reader.tell()
                        
                        data = edit_data_reader.readline() # third lines is the data to be written
                        
                        # the line with the tag
                        original_content = file_reader.readline()
                        lines+=1
                        
                        # get index of opening tag
                        open_index = original_content.find(open_tag)
                        
                        if open_index > -1:
                            # put cursor at start of the read line
                            file_reader.seek(cursor_at_line_start)
                            
                            # write till the open tag; tag inclusive
                            file_writer.write(file_reader.read(open_index + length_open_tag))
                            
                            # write the new data
                            file_writer.write(data)
                            
                            close_index = original_content.find(close_tag)
                            
                            if close_index > -1:
                                # put cursor at closing tag
                                file_reader.seek(cursor_at_line_start + close_index)
                                
                                # write remaining data of the read line
                                file_writer.write(file_reader.read(len(original_content) - close_index))
                                
                                # log the cursor position in case, next change is to same path
                                put_cursor_at = file_reader.tell()
                                
                                # check for newline
                                edit_data_cursor = edit_data_reader.tell()
                                tmp = edit_data_reader.readline()
                                tmp = tmp.strip("\n")
                                # if 1 new line exists, put cursor on next line
                                if not tmp:
                                    pass
                                else:
                                    # restore the cursor
                                    edit_data_reader.seek(edit_data_cursor)
                                    
                            else:
                                pass
                        
    except FileNotFoundError:
        print("edit_data.txt not found.\n")


if __name__ == "__main__":
    
    p = Path('.') # curernt directory

    try:
        flag = sys.argv[1]
    except IndexError:
        raise SystemExit("Flag not found!")
    
    if flag == '-f':
        fetch(p)
        
    elif flag == '-r':
        replace(Path.cwd())