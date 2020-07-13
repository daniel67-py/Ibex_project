#!/usr/bin/python3
#-*- coding: Utf-8 -*-
import re
import os
import sys
import csv
import sqlite3
from jinja2 import *
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *

####################################################################################################
### Valknut - GSS & SQLite3 manager
### developped by Meyer Daniel for Python 3, July 2020
### this is version 0.1.001
####################################################################################################

####################################################################################################
### Valknut_gss class
####################################################################################################
class Valknut_gss:
    def __init__(self):
        ### definition of some variables ###
        self.file = None
        self.feedback = 0
        self.out_file = "auto_gen.html"
        self.use_template = "templates/root_page.html"
        ### definition of some values to include in the page ###
        self.project_title = "knut_page"
        self.project_header = "knut_header"
        self.project_footer = "knut_footer"

    ### this class start the convertion of the markdown file ###
    ### all begins from here when using this program... ###        
    def generate(self):
        ### first trying to read the specified template ###
        try:
            with open(self.use_template, 'r') as model:
                static_page = model.read()
        except:
            print("the specified template is not present...")
        ### opening the markdown file ###
        with open(self.file, 'r') as source:
            contain = source.read()
        ### analysing the document ###
        print("searching for h6 to h1 titles")
        contain = self.per_lines(contain, "######", "<h6>", "</h6> \n")
        contain = self.per_lines(contain, "#####", "<h5>", "</h5> \n")
        contain = self.per_lines(contain, "####", "<h4>", "</h4> \n")
        contain = self.per_lines(contain, "###", "<h3>", "</h3> \n")
        contain = self.per_lines(contain, "##", "<h2>", "</h2> \n")
        contain = self.per_lines(contain, "#", "<h1>", "</h1> \n")
        print("searching for separators")
        contain = self.per_lines(contain, "------", "<hr />", "\n ")
        print("searching for code examples")
        contain = self.per_coding_example(contain, "    ", " <pre><code>\n    ", " </code></pre>\n")
        print("searching for paragraphs")
        contain = self.per_lines(contain, "  ", "<p>\n", " </p>\n")
        print("searching for lists")
        contain = self.per_list(contain, "+", "<ol>", "</ol>\n")
        contain = self.per_list(contain, "-", "<ul>", "</ul>\n")
        print("searching for triple splat bold and italic quote")
        contain = self.per_emphasis(contain, "***", "<b><i>", "</i></b>")
        print("searching for double splat bold quote")
        contain = self.per_emphasis(contain, "**", "<b>", "</b>")
        print("searching for single splat italic quote")
        contain = self.per_emphasis(contain, "*", "<i>", "</i>")
        print("searching for strikethrough quote")
        contain = self.per_emphasis(contain, "~~", "<s>", "</s>")
        print("searching for underlines")
        contain = self.per_emphasis(contain, "__", "<u>", "</u>")
        print("searching for pictures")
        contain = self.per_images(contain)
        print("searching for urls")
        contain = self.per_links(contain)
        print("searching for emails adresses")
        contain = self.per_mails(contain)
        print("indexing the document's titles")
        contain = self.indexer(contain)
        print("extracting the links to intern chapters")
        doc_chapter = self.chapter(contain)
        print("saving the output result into .html")
        ### and there comes the output, if feedback = 0, it gives a html ###
        ### other case, it return directly the result ###
        if self.feedback == 0:         
            with open(self.out_file, 'w') as output_file:
                templ = Template(static_page)
                output_file.write(
                    templ.render(
                        page_title = self.project_title,
                        page_summary = doc_chapter,
                        page_header = self.project_header,
                        page_contains = contain,
                        page_footer = self.project_footer,
                        ))
        elif self.feedback != 0:
            templ = Template(static_page)
            output_file = templ.render(page_title, page_contains = contain)
            return output_file
        ### tell the user that the job is done ###
        print("job done !")

    ####################################################    
    ### here begins the real analyse and parsing job ###
    ####################################################

    ### this function analyse lines per lines the whole markdown file ###
    ### and puts quote for titles or separators ###
    def per_lines(self, sequence, symbol_to_modify, replace_open_parse, replace_ending_parse):
        analyse = sequence.splitlines()
        mark_code = 0
        mark_cite = 0
        new_output = ""

        for y in analyse:
            if "<pre><code>" in y:
                mark_code = 1
            elif "</code></pre>" in y:
                mark_code = 0

            if y.startswith(symbol_to_modify) == True and mark_code == 0:
                y = y.replace(symbol_to_modify, replace_open_parse)
                y += replace_ending_parse
                new_output += y
            else:
                new_output += y
            new_output += "\n"

        return new_output

    ### this function analyse lines per lines the whole markdown file ###
    ### and search if there is coding exemples ###
    def per_coding_example(self, sequence, number_of_spaces, opening_parse, closing_parse):
        mark_coding = 0

        analyse = sequence.splitlines()
        new_output = ""

        for x in analyse:
            if x.startswith(number_of_spaces) and mark_coding == 0:
                x = x.replace(number_of_spaces, opening_parse)
                new_output += x
                mark_coding = 1
            elif x.startswith(number_of_spaces) and mark_coding == 1:
                new_output += x
            elif mark_coding == 1 and x == "":
                mark_coding = 0
                x = x.replace("", closing_parse)
                new_output += x
            else:
                new_output += x
            new_output += "\n"

        return new_output

    ### this function analyse lines per lines the whole markdown file ###
    ### and search if there is some unordered  or ordered lists ###
    def per_list(self, sequence, begins, opening_parse, closing_parse):
        mark_list = 0
        old_mark_level = 0
        new_mark_level = 0

        analyse = sequence.splitlines()
        new_output = ""

        for w in analyse:
            extract = w.split(" ")
            try:
                new_mark_level = extract[0].count(begins)
            except:
                new_mark_level = 0

            diff_back = [
                new_mark_level == old_mark_level - 1,
                new_mark_level == old_mark_level - 2,
                new_mark_level == old_mark_level - 3,
                new_mark_level == old_mark_level - 4,
                new_mark_level == old_mark_level - 5,
                new_mark_level == old_mark_level - 6,
                new_mark_level == old_mark_level - 7,
                new_mark_level == old_mark_level - 8,
                new_mark_level == old_mark_level - 9,
                new_mark_level == old_mark_level - 10,
                new_mark_level == old_mark_level - 11,
                new_mark_level == old_mark_level - 12,
                new_mark_level == old_mark_level - 13,
                new_mark_level == old_mark_level - 14,
                new_mark_level == old_mark_level - 15,
                new_mark_level == old_mark_level - 16,
                ]
            
            if new_mark_level == 0 and mark_list == 1:
                mark_list = 0
                w = closing_parse * old_mark_level
                new_output += w
            
            elif new_mark_level == old_mark_level + 1:
                old_mark_level = new_mark_level
                if w.startswith(begins) == True and mark_list == 0:
                    w = w.replace(begins * new_mark_level, opening_parse + "<li>")
                    new_output += w 
                    mark_list = 1
                elif w.startswith(begins) == True and mark_list == 1:
                    w = w.replace(begins * new_mark_level, opening_parse + "<li>")
                    new_output += w 
                    
            elif any(diff_back) == True:
                old_mark_level = old_mark_level - new_mark_level
                if w.startswith(begins) == True and mark_list == 1:
                    w = w.replace(begins * new_mark_level, "</li>\n" * old_mark_level + closing_parse * old_mark_level + "<li>")
                    new_output += w 
                old_mark_level = new_mark_level
                
            elif new_mark_level == old_mark_level and new_mark_level > 0 and mark_list == 1:
                if w.startswith(begins) == True:
                    w = w.replace(begins * new_mark_level, "</li><li>")
                    new_output += w 
                
            else:
                new_output += w
                
            new_output += "\n"
            
        return new_output

    ### this function analyse lines per lines the whole markdown file ###
    ### and parse bold or italic symbols ###
    def per_emphasis(self, sequence, symbol_to_modify, replace_open_parse, replace_ending_parse):
        mark_emphasis = 0
        mark_code = 0

        analyse = sequence.split(" ")
        new_output = ""
                
        for z in analyse:
            if "<pre><code>" in z:
                mark_code = 1
            elif "</code></pre>" in z:
                mark_code = 0

            if z.startswith(symbol_to_modify) == True and mark_emphasis == 0 and mark_code == 0:
                if z.endswith(symbol_to_modify) == True:
                    z = z.split(symbol_to_modify)
                    z[0] = replace_open_parse
                    z[-1] = replace_ending_parse
                    new_output += "".join(z) + " "
                elif z.endswith(symbol_to_modify + ".") == True:
                    z = z.split(symbol_to_modify)
                    z[0] = replace_open_parse
                    z[-1] = replace_ending_parse
                    new_output += "".join(z) + ". "
                elif z.endswith(symbol_to_modify + "?") == True:
                    z = z.split(symbol_to_modify)
                    z[0] = replace_open_parse
                    z[-1] = replace_ending_parse
                    new_output += "".join(z) + "? "
                elif z.endswith(symbol_to_modify + "!") == True:
                    z = z.split(symbol_to_modify)
                    z[0] = replace_open_parse
                    z[-1] = replace_ending_parse
                    new_output += "".join(z) + "! "
                elif z.endswith(symbol_to_modify + "\n") == True:
                    z = z.split(symbol_to_modify)
                    z[0] = replace_open_parse
                    z[-1] = replace_ending_parse
                    new_output += "".join(z) + "\n"
                else:    
                    z = z.replace(symbol_to_modify, replace_open_parse)
                    mark_emphasis = 1
                    new_output += z + " "
                    
            elif symbol_to_modify in z and mark_emphasis == 0 and mark_code == 0:
                z = z.replace(symbol_to_modify, replace_open_parse)
                new_output += z + " "
                mark_emphasis = 1
                
            elif symbol_to_modify in z and mark_emphasis == 1 and mark_code == 0:
                z = z.replace(symbol_to_modify, replace_ending_parse)
                new_output += z + " "
                mark_emphasis = 0
                
            elif z.endswith(symbol_to_modify) == True and mark_emphasis == 1 and mark_code == 0:
                z = z.replace(symbol_to_modify, replace_ending_parse)
                new_output += z + " "
                mark_emphasis = 0
                
            else:
                new_output += z + " "

        return new_output

    ### this function analyse lines per lines the whole markdown file ###
    ### and parse images ###
    def per_images(self, sequence):
        mark_code = 0

        expression_img = r"\!\[(?P<text>.+)\]\((?P<url>.+)\)"
        
        analyse = sequence.splitlines()
        new_output = ""

        for z in analyse:
            if "<pre><code>" in z:
                mark_code = 1
            elif "</code></pre>" in z:
                mark_code = 0

            extract_img = re.search(expression_img, z)
            if extract_img is not None and mark_code == 0:
                lnk = f"""<figure><center><img src='{extract_img.group('url')}' alt='{extract_img.group('text')}' /></center></figure>\n"""
                to_replace = f"![{extract_img.group('text')}]({extract_img.group('url')})"
                print(to_replace)
                z = z.replace(to_replace, lnk)
                new_output += z
            else:
                new_output += z + " "
            new_output += "\n"

        return new_output

    ### this function analyse lines per lines the whole markdown file ###
    ### and parse url ###
    def per_links(self, sequence):
        mark_code = 0

        expression_url = r"\[(?P<text>.+)\]\((?P<url>.+)\)"
        
        analyse = sequence.splitlines()
        new_output = ""

        for z in analyse:
            if "<pre><code>" in z:
                mark_code = 1
            elif "</code></pre>" in z:
                mark_code = 0

            extract_lnk = re.search(expression_url, z)
            if extract_lnk is not None and mark_code == 0:
                lnk = f"""<a href = '{extract_lnk.group("url")}'>{extract_lnk.group("text")}</a>"""
                to_replace = f"[{extract_lnk.group('text')}]({extract_lnk.group('url')})"
                z = z.replace(to_replace, lnk)
                new_output += z
            else:
                new_output += z + " "
            new_output += "\n"

        return new_output

    ### this function analyse lines per lines the whole markdown file ###
    ### and parse emails adresses ###
    def per_mails(self, sequence):
        mark_code = 0

        expression_mail = r"\[(?P<mail_add>.+\@.+)\]"
        
        analyse = sequence.splitlines()
        new_output = ""

        for z in analyse:
            if "<pre><code>" in z:
                mark_code = 1
            elif "</code></pre>" in z:
                mark_code = 0

            extract_mail = re.search(expression_mail, z)
            if extract_mail is not None and mark_code == 0:
                lnk = f"""<a href = "mailto:{extract_mail.group("mail_add")}">{extract_mail.group("mail_add")}</a>"""
                to_replace = f"[{extract_mail.group('mail_add')}]"
                z = z.replace(to_replace, lnk)
                new_output += z
            else:
                new_output += z + " "
            new_output += "\n"

        return new_output

    ### this function do an indexation of the document and add a div='x' to <hx> quotes ###
    ### but only in the 'body'. incase of absence of any sections, it still working ###
    def indexer(self, sequence):
        analyse = sequence.splitlines()
        mark_section = 0
        counter = 0
        new_output = ""
        expression_check = r"<h(?P<number>\d)>"

        section_begins = ['<head>', '<header>', '<foot>', '<footer>']
        section_ends = ['</head>', '</header>', '</foot>', '</footer>']
        
        for x in analyse:
            
            for y in section_begins:
                if y in x:
                    mark_section = 1
            for z in section_ends:
                if z in x:
                    mark_section = 0

            extract = re.search(expression_check, x)
            if extract is not None and mark_section == 0:
                opening_symbol = f"<h{extract.group('number')}>"
                z = x.split(opening_symbol)
                new_open_symbol = opening_symbol.replace(">", f" id='{counter}'>")
                z[0] = new_open_symbol
                new_output += "".join(z)
                counter += 1
            else:
                new_output += x
                
            new_output += "\n"
            
        return new_output

    ### this function extract the chapters of the body section ###
    ### it returns it in the <nav> section of the basic template ###
    def chapter(self, sequence):
        analyse = sequence.splitlines()
        dict_chapter = []
        new_dict_chapter = []

        for x in analyse:
            expression = r"<h(\d) id='(\d+)'>(?P<chapter>.*)</h(\d)>"
            try:
                extract = re.search(expression, x)
                dict_chapter.append(extract.group("chapter"))
            except:
                None

        for y in range(0, len(dict_chapter)):
            includer = f"<a href='#{y}'>{dict_chapter[y]}</a><br>"
            new_dict_chapter.append(includer)

        return new_dict_chapter

####################################################################################################
### survivaltool_gss tkinter interface
####################################################################################################
class Valknut_gss_interface(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Valknut GSS interface for Python 3.x")
        self.resizable(height = False, width = False)
        self.use_font_title = ""
        self.use_font_rests = ""

        lbl_source = Label(self, text = "Source file  : ")
        lbl_source.grid(row = 1, column = 1)
        lbl_out_fl = Label(self, text = "Destination  : ")
        lbl_out_fl.grid(row = 2, column = 1)
        lbl_use_tp = Label(self, text = "Use template : ")
        lbl_use_tp.grid(row = 3, column = 1)
        lbl_title = Label(self, text = "Project title : ")
        lbl_title.grid(row = 4, column = 1)
        lbl_header = Label(self, text = "Project header : ")
        lbl_header.grid(row = 5, column = 1)
        lbl_footer = Label(self, text = "Project footer : ")
        lbl_footer.grid(row = 6, column = 1)

        self.source_entry = Entry(self, width = 20)
        self.source_entry.grid(row = 1, column = 2)
        self.out_file_entry = Entry(self, width = 20)
        self.out_file_entry.grid(row = 2, column = 2)
        self.out_file_entry.insert(1, "auto_gen.html")
        self.use_tp_entry = Entry(self, width = 20)
        self.use_tp_entry.grid(row = 3, column = 2)
        self.use_tp_entry.insert(1, "templates/root_page.html")
        self.title_entry = Entry(self, width = 20)
        self.title_entry.grid(row = 4, column = 2)
        self.title_entry.insert(1, "Valknut Page")
        self.header_entry = Entry(self, width = 20)
        self.header_entry.grid(row = 5, column = 2)
        self.header_entry.insert(1, "Generated by Valknut")
        self.footer_entry = Entry(self, width = 20)
        self.footer_entry.grid(row = 6, column = 2)
        self.footer_entry.insert(1, "Program under license")

        self.source_button = Button(self, text = "open", command = lambda x = "source" : self.open_file(x))
        self.source_button.grid(row = 1, column = 3)
        self.out_file_button = Button(self, text = "open", command = lambda x = "destination" : self.open_file(x))
        self.out_file_button.grid(row = 2, column = 3)
        self.use_tp_button = Button(self, text = "open", command = lambda x = "template" : self.open_file(x))
        self.use_tp_button.grid(row = 3, column = 3)
        self.title_button = Button(self, text = "clean", command = lambda x = "title" : self.cleaner(x))
        self.title_button.grid(row = 4, column = 3)
        self.header_button = Button(self, text = "clean", command = lambda x = "header" : self.cleaner(x))
        self.header_button.grid(row = 5, column = 3)
        self.footer_button = Button(self, text = "clean", command = lambda x = "footer" : self.cleaner(x))
        self.footer_button.grid(row = 6, column = 3)

        self.generation_button = Button(self, text = "Generate !", command = self.generating)
        self.generation_button.grid(row = 20, column = 1, columnspan = 2)
        self.byebye_button = Button(self, text = "Exit...", command = self.quit)
        self.byebye_button.grid(row = 20, column = 2, columnspan = 2)
        
        self.mainloop()
        try:
            self.destroy()
        except TclError:
            sys.exit()

    def open_file(self, selection):
        source = askopenfilename(filetypes = [("markdown", ".md"), ("text", ".txt"), ("html", ".html")])
        if selection == "source":
            self.source_entry.delete(0, 10000)
            self.source_entry.insert(0, source)
        elif selection == "destination":
            self.out_file_entry.delete(0, 10000)
            self.out_file_entry.insert(0, source)
        elif selection == "template":
            self.use_tp_entry.delete(0, 10000)
            self.use_tp_entry.insert(0, source)

    def cleaner(self, selection):
        if selection == "title":
            self.title_entry.delete(0, 10000)
        elif selection == "header":
            self.header_entry.delete(0, 10000)
        elif selection == "footer":
            self.footer_entry.delete(0, 10000)

    def generating(self):
        srv = Valknut_gss()
        srv.file = self.source_entry.get()
        srv.feedback = 0
        srv.out_file = self.out_file_entry.get()
        srv.use_template = self.use_tp_entry.get()
        srv.project_title = self.title_entry.get()
        srv.project_header = self.header_entry.get()
        srv.project_footer = self.footer_entry.get()
        try:
            srv.generate()
            showinfo("okay !", "the job is done !")
        except:
            showwarning("no no no...", "cannot do the job, something is missing somewhere !")
        
####################################################################################################
### Valknut - GSS & SQLite3 manager
### developped by Meyer Daniel for Python 3, July 2020
### this is version 0.1.001
####################################################################################################

####################################################################################################
### New database creation class
####################################################################################################
class Valknut_New():
    ################################################################################################
    ### initialization function for a new database
    ################################################################################################
    def __init__(self, database):
        ### presentation ###
        print("### Valknut - SQLite3 manager ###")
        ### file to create ###
        self.database = database
        ### creation of the new databse ###
        if os.path.exists(self.database) == False and os.path.isfile(self.database) == False:
            connexion = sqlite3.connect(self.database)
            connexion.close()
            ### try to access ###
            if os.path.exists(self.database) == True and os.path.isfile(self.database) == True:
                print("...verification if access path to file is ok...",
                      os.path.exists(self.database))
                print("...verification if path is a valid file...",
                      os.path.isfile(self.database))
                print("...ACCESS DATA OK - NEW DATABASE READY TO OPERATE...")
            else:
                print("!!! ERROR WHILE CREATION OF THE NEW DATABASE !!!")
        else:
            print("!!! THIS DATABASE ALREADY EXIST !!!")
            
####################################################################################################
### Database manager class
####################################################################################################
class Valknut():
    ################################################################################################
    ### initialization function
    ################################################################################################
    def __init__(self, database):
        ### framework variables ###
        self.debug_sqlite_instruction = False  ### True for showing sqlite instructions will running
        self.displaying_line = True            ### True for printing at screen
        ### presentation ###
        print("### Valknut - SQLite3 manager ###")
        ### file to analyse ###
        self.database = database
        ### verification if file exist and if access path is ok ###
        if os.path.exists(self.database) == True and os.path.isfile(self.database) == True:
            print("...verification if access path to file is ok...",
                  os.path.exists(self.database))
            print("...verification if path is a valid file...",
                  os.path.isfile(self.database))
            print("...ACCESS DATAS OK !...")
        else: 
            print("!!! ERROR : FILE DOES NOT EXIST !!!")
            self.database = None

    ################################################################################################
    ### entry modification in a table
    ################################################################################################
    def modification_values(self, table, column_to_modify, new_value, reference_column, reference_value):
        """permit to change an entry in table"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the SQL instruction ###
            instruction = (f"UPDATE {table} SET {column_to_modify} = '{new_value}' WHERE {reference_column} = '{reference_value}'")
            self.debug_sqlite(instruction)
            ### try to execute the instruction ###
            try:
                c.execute(instruction)
                mark = True
            except:
                print("Impossible to modifie the value, something does not match !")
                mark = False
            ### commiting and closing ###
            connexion.commit()
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### add an entry to specific table
    ################################################################################################
    def add_values(self, table, *elements):
        """permit to add an entry to a specific table"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the SQL instruction ###
            instruction = (f"""INSERT INTO {table} VALUES {str(elements)}""")
            self.debug_sqlite(instruction)
            ### try to execute the instruction ###
            try:
                c.execute(instruction)
                mark = True
            except:
                print("Impossible to add the values, something does not match !")
                mark = False
            ### commiting and closing ###
            connexion.commit()
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### add an entry to specific increased table
    ################################################################################################
    def add_increased_values(self, table, *elements):
        """permit to add an entry to a specific increased table"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### counting the number of entry in the table ###
            instruction_1 = f"""SELECT COUNT(*) FROM {table}"""
            c.execute(instruction_1)
            nb_id = c.fetchone()
            nb_id = str(nb_id[0])
            elements = (nb_id, ) + elements
            ### concatenation of the SQL instruction ###
            instruction_2 = (f"""INSERT INTO {table} VALUES {str(elements)}""")
            self.debug_sqlite(instruction_2)
            ### try to execute the instruction ###
            try:
                c.execute(instruction_2)
                mark = True
            except:
                print("Impossible to add the values, something does not match !")
                mark = False
            ### commiting and closing ###
            connexion.commit()
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### creating a new table with specific columns
    ################################################################################################
    def new_table(self, table, *columns):
        """permit to create a new table with specific columns"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the SQL instruction ###
            instruction = (f"CREATE TABLE {table} {str(columns)}")
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                c.execute(instruction)
                mark = True
                print("New table create")
            except:
                print("Impossible to add a new table to database")
                mark = False
            ### commiting and closing ###
            connexion.commit()
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### copy a table to a new one
    ################################################################################################
    def copy_table(self, source_table, destination_table):
        """permit to copy a table to a new table"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the SQL instruction ###
            instruction = (f"CREATE TABLE {destination_table} AS SELECT * FROM {source_table}")
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                c.execute(instruction)
                mark = True
                print("Table has been copied")
            except:
                print("Impossible to copy this table")
                mark = False
            ### commiting and closing ###
            connexion.commit()
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### copy specific columns from a table to a new one
    ################################################################################################
    def copy_control_table(self, source_table, destination_table, *columns):
        """permit to copy a table to a new table only with specified columns"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the SQL instruction ###
            instruction = f"CREATE TABLE {destination_table} AS SELECT "
            for x in range(0, len(columns)):
                instruction += columns[x]
                if x != len(columns) - 1:
                    instruction += ", "
                else:
                    instruction += " "
            instruction += f"FROM {source_table}"
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                c.execute(instruction)
                mark = True
                print("Table has been copied")
            except:
                print("Impossible to copy this table")
                mark = False
            ### commiting and closing ###
            connexion.commit()
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### redo a specific table with only specific columns
    ################################################################################################
    def redo_table(self, source_table, *columns):
        """permit to redo a table only with specified column"""
        mark = None
        destination_table = source_table
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the SQL instruction ###
            instruction = f"CREATE TABLE survival_temporary_table AS SELECT "
            for x in range(0, len(columns)):
                instruction += columns[x]
                if x != len(columns) - 1:
                    instruction += ", "
                else:
                    instruction += " "
            instruction += f"FROM {source_table}"
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                c.execute(instruction)
                print("Table has been copied to valknut_temporary_table.")
                ### then delete the source table
                try :
                    print("Deleting old version of the table")
                    self.delete_table(source_table)
                    print("Restitution of the new version of the table")
                    self.copy_table('valknut_temporary_table', destination_table)
                    print("Deleting temporary exchange table")
                    self.delete_table('valknut_temporary_table')
                    mark = True
                except:
                    print("Something gone wrong while trying to redo the specified table")
                    mark = False
            except:
                print("Impossible to copy this table")
                mark = False
            ### commiting and closing ###
            connexion.commit()
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### add a new column in specific table
    ################################################################################################
    def add_column(self, table, column):
        """permit to add a new column in specific table"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the SQL instruction ###
            instruction = (f"ALTER TABLE {table} ADD {column}")
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                c.execute(instruction)
                mark = True
                print("New column created")
            except:
                print("Impossible to add a new column to this table")
                mark = False
            ### commiting and closing ###
            connexion.commit()
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### delete a table with its entry from database
    ################################################################################################
    def delete_table(self, table):
        """permit to delete a table from database"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the SQL instruction ###
            instruction = (f"""DROP TABLE {table}""")
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                c.execute(instruction)
                print(f"The table {table} has been deleted !")
                mark = True
            except:
                print("Impossible to delete the table, she does not exist")
                mark = False
            ### commiting and closing ###
            connexion.commit()
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### purge a table 
    ################################################################################################
    def purge_table(self, table):
        """permit to purge a table"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the SQL instruction ###
            instruction = (f"""DELETE FROM '{table}'""")
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                c.execute(instruction)
                print(f"The table {table} has been purged !")
                mark = True
            except:
                print("Impossible to purge the table, she does not exist")
                mark = False
            ### commiting and closing ###
            connexion.commit()
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### delete an entry
    ################################################################################################
    def delete_entry(self, table, column, value):
        """permit to delete an entry from a specific table"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the SQL instruction ###
            instruction = (f"DELETE FROM {table} WHERE {column} = '{value}'")
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                c.execute(instruction)
                print(f"The value {value} from the column {column} has been deleted !")
                mark = True
            except:
                print("Impossible to delete the entry, she does not exist")
                mark = False
            ### commiting and closing ###
            connexion.commit()
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### searching an entry in a specific table
    ################################################################################################
    def search_value(self, table, column, value):
        """permit to search an entry in a specific table"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to the database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the instruction ###
            if type(value) == str:
                instruction = (f"SELECT * FROM {table} WHERE {column} = '{value}'")
            elif type(value) == int or type(valeur) == float:
                instruction = (f"SELECT * FROM {table} WHERE {column} = {value}")
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                mark = []
                for x in c.execute(instruction):
                    self.displaying_return(x)
                    mark.append(x)
            except:
                print("One or many specified values are not good")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            if self.displaying_line == False:
                return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### searching an entry who starts with what's specified 
    ################################################################################################
    def search_start_like_value(self, table, column, value):
        """permit to search an entry who starts with the specified value"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to the database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the instruction ###
            instruction = (f"SELECT * FROM {table} WHERE {column} LIKE '{value}%'")
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                mark = []
                for x in c.execute(instruction):
                    self.displaying_return(x)
                    mark.append(x)
            except:
                print("One or many specified values are not good")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            if self.displaying_line == False:
                return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### searching an entry who ends with what's specified 
    ################################################################################################
    def search_end_like_value(self, table, column, value):
        """permit to search an entry who ends with the specified value"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to the database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the instruction ###
            instruction = (f"SELECT * FROM {table} WHERE {column} LIKE '%{value}'")
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                mark = []
                for x in c.execute(instruction):
                    self.displaying_return(x)
                    mark.append(x)
            except:
                print("One or many specified values are not good")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            if self.displaying_line == False:
                return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### searching an entry who contain what's specified 
    ################################################################################################
    def search_seems_like_value(self, table, column, value):
        """permit to search an entry who contain the specified value"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to the database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the instruction ###
            instruction = (f"SELECT * FROM {table} WHERE {column} LIKE '%{value}%'")
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                mark = []
                for x in c.execute(instruction):
                    self.displaying_return(x)
                    mark.append(x)
            except:
                print("One or many specified values are not good")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            if self.displaying_line == False:
                return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### searching entries between an interval in a specific table
    ################################################################################################
    def between_value(self, table, column, interval_1, interval_2):
        """permit to search entries between an interval in a specific table"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to the database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the instruction ###
            instruction = (f"""SELECT * FROM {table} WHERE {column} BETWEEN '{interval_1}' AND '{interval_2}'""")
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                mark = []
                for x in c.execute(instruction):
                    self.displaying_return(x)
                    mark.append(x)
            except:
                print("One or many specified values are not good")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            if self.displaying_line == False:
                return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### searching entries not between an interval in a specific table
    ################################################################################################
    def not_between_value(self, table, column, interval_1, interval_2):
        """permit to search entries between an interval in a specific table"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to the database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the instruction ###
            instruction = (f"""SELECT * FROM {table} WHERE {column} NOT BETWEEN '{interval_1}' AND '{interval_2}'""")
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                mark = []
                for x in c.execute(instruction):
                    self.displaying_return(x)
                    mark.append(x)
            except:
                print("One or many specified values are not good")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            if self.displaying_line == False:
                return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### sorting the entries in a specific table
    ################################################################################################
    def sort_value(self, table, sens, *column):
        """permit to sort the entries in a specific table"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to the database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of the instruction by analyse of *arg column ###
            if sens == 0: ### in ascendence ###
                instruction = (f"SELECT * FROM {table} ORDER BY ")
                for x in range (0, len(column)):
                    instruction += column[x]
                    if x != len(column) - 1:
                        instruction += " ,"
                    else:
                        instruction += " "
                instruction += "ASC"
            elif sens == 1: ### in descendence ###
                instruction = (f"SELECT * FROM {table} ORDER BY ")
                for x in range (0, len(column)):
                    instruction += column[x]
                    if x != len(column) - 1:
                        instruction += " ,"
                    else:
                        instruction += " "
                instruction += "DESC"
            ### incase of too much trouble ###
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                mark = []
                for x in c.execute(instruction):
                    self.displaying_return(x)
                    mark.append(x)
            except:
                print("One or many specified values are not good")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            if self.displaying_line == False:
                return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### return each table's name and column's name
    ################################################################################################
    def return_structure(self):
        """return database's structure via dictionnary"""
        mark = {}
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            ### c : analyse the tables, d : analyse column's name ###
            connexion = sqlite3.connect(self.database)
            connexion.row_factory = sqlite3.Row
            c = connexion.cursor()
            d = connexion.cursor()
            ### another cursor to analyse the table's entry ###
            connexion2 = sqlite3.connect(self.database)
            e = connexion2.cursor()
            ### concatenation of the first instruction ###
            instruction_1 = """SELECT name FROM sqlite_master WHERE type = 'table' """
            self.debug_sqlite(instruction_1)
            ### analyse table's name of the database with c ###
            c.execute(instruction_1)
            for x in iter(c.fetchall()):
                ### concatenation of the second instruction ###
                instruction_2 = f"SELECT * FROM {x[0]}"
                self.debug_sqlite(instruction_2)
                ### analyse column's name of each tables with d ###
                d.execute(instruction_2)
                mark[x[0]] = d.fetchone().keys()
            ### closing ###
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return None

    ################################################################################################
    ### display the integrality of the database
    ################################################################################################
    def show_all(self):
        """display the integrality of the database"""
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            ### c : analyse the tables, d : analyse column's name ###
            connexion = sqlite3.connect(self.database)
            connexion.row_factory = sqlite3.Row
            c = connexion.cursor()
            d = connexion.cursor()
            ### another cursor to analyse the table's entry ###
            connexion2 = sqlite3.connect(self.database)
            e = connexion2.cursor()
            ### display the contains ###
            print("\n...OK... The database contains :")
            print(self.database)
            print("  |")
            ### concatenation of the first instruction ###
            instruction_1 = """SELECT name FROM sqlite_master WHERE type = 'table' """
            self.debug_sqlite(instruction_1)
            ### analyse table's name of the database with c ###
            c.execute(instruction_1)
            for x in iter(c.fetchall()):
                ### concatenation of the second instruction ###
                instruction_2 = f"SELECT * FROM {x[0]}"
                self.debug_sqlite(instruction_2)
                ### analyse column's name of each tables with d ###
                d.execute(instruction_2)
                ### display the tree ###
                print("  + -",x[0])
                try:
                    print("  |       \ _ _ _ _ _", d.fetchone().keys())
                except:
                    print("  | ")
                ### concatenation of the third instruction ###
                instruction_3 = f"SELECT * FROM {x[0]}"
                self.debug_sqlite(instruction_3)
                ### analyse of the table contains with e ###
                for y in e.execute(instruction_3):
                    ligne = ""
                    ### concatenation of datas in one line ###
                    for z in range(0, len(y)):
                        ligne = ligne + str(y[z]) + " - "
                    ### display the data ###
                    print("  |\t\t\t", ligne)
            ### closing ###
            connexion.close()
            ### and final line of the tree display ###
            print("  | \n  |_ END OF DATAS !\n")
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return None
            
    ################################################################################################
    ### display the structure of the database
    ################################################################################################
    def show_structure(self):
        """display database's structure"""
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            ### c : analyse the tables, d : analyse column's name
            connexion = sqlite3.connect(self.database)
            connexion.row_factory = sqlite3.Row
            c = connexion.cursor()
            d = connexion.cursor()
            ### display the contains ###
            print("\n...OK... This is database's tree :")
            print(self.database)
            print("  |")
            ### analyse the name of the table with c ###
            c.execute("""SELECT name FROM sqlite_master WHERE type = 'table' """)
            for x in iter(c.fetchall()):
                ### analyse column's name with d ###
                d.execute(f"SELECT * FROM {x[0]}")
                ### display the tree ###
                print("  + -",x[0])
                try:
                    print("  |       \ _ _ _ _ _", d.fetchone().keys())
                except:
                    print("  | ")
            ### closing ###                 
            connexion.close()
            ### and final line of the tree display ###
            print("  | \n  |_ END OF DATAS !\n")
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return None

    ################################################################################################
    ### do the sum of a column
    ################################################################################################
    def column_sum(self, table, column):
        """return the sum of a specific column and return it as integer or float"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of instruction ###
            instruction = f"""SELECT SUM({column}) FROM {table}"""
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                c.execute(instruction)
                out = c.fetchone()
                mark = out[0]
            except:
                print("Impossible to do the sum of this column.")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark
            
    ################################################################################################
    ### do the total of a column
    ################################################################################################
    def column_total(self, table, column):
        """return the total of a specific column and return an float"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of instruction ###
            instruction = f"""SELECT TOTAL({column}) FROM {table}"""
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                c.execute(instruction)
                out = c.fetchone()
                mark = out[0]
            except:
                print("Impossible to do the total of this column")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### find the minimal value of a table
    ################################################################################################
    def data_minimal(self, table, column):
        """find and return the minimal value in a specific column of a specific table"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of instruction ###
            instruction = f"""SELECT MIN({column}) FROM {table}"""
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                c.execute(instruction)
                out = c.fetchone()
                mark = out[0]
            except:
                print("Impossible to find the minimal value, something is not right")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### find the maximal value of a table
    ################################################################################################
    def data_maximal(self, table, column):
        """find and return the maximal value in a specific column of a specific table"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of instruction ###
            instruction = f"""SELECT MAX({column}) FROM {table}"""
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                c.execute(instruction)
                out = c.fetchone()
                mark = out[0]
            except:
                print("Impossible to find the maximal value, something is not right")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### do the average of a group of values
    ################################################################################################
    def data_average(self, table, column):
        """do the average of a group of non-null values"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of instruction ###
            instruction = f"""SELECT AVG({column}) FROM {table}"""
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                c.execute(instruction)
                out = c.fetchone()
                mark = out[0]
            except:
                print("Impossible to do the average, something is not right")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### do an innerjoin between two tables, will return only those who are present in both tables
    ################################################################################################
    def data_crosscheck(self, table_1, table_2, column_t1, column_t2):
        """do an innerjoin between two tables, return only those who are present in both tables"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of instruction ###
            instruction = f"""SELECT * FROM {table_1} INNER JOIN {table_2} WHERE {table_1}.{column_t1} = {table_2}.{column_t2}"""
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                mark = []
                c.execute(instruction)
                for x in iter(c.fetchall()):
                    self.displaying_return(x)
                    mark += [x]
            except:
                print("Impossible to do the crosscheck, something is not right")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            if self.displaying_line == False:
                return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### do an union between two tables, will return the integrity of both tables without doubles
    ################################################################################################
    def data_union(self, table_1, table_2):
        """do an union between two tables, will return the intergrity of both tables without doubles"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### concatenation of instruction ###
            instruction = f"""SELECT * FROM {table_1} UNION SELECT * FROM {table_2}"""
            self.debug_sqlite(instruction)
            ### execution of the instruction ###
            try:
                mark = []
                c.execute(instruction)
                for x in iter(c.fetchall()):
                    self.displaying_return(x)
                    mark += [x]
            except:
                print("Impossible to do the crosscheck, something is not right")
                mark = False
            ### closing ###
            connexion.close()
            ### return result of the function ###
            if self.displaying_line == False:
                return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################       
    ### output database's structure to a txt file
    ################################################################################################
    def edit_structure_txt(self, nom_fichier_sortie = "analyse_valknut.txt"):
        """output database's structure to a txt file"""
        ### if database is a valid file ###
        if self.database != None:
            ### create and open a new text file ###
            fichier_texte = open(nom_fichier_sortie, "w")
            ### connection to database ###
            ### c : analyse the tables, d : analyse the column's name ###
            connexion = sqlite3.connect(self.database)
            connexion.row_factory = sqlite3.Row
            c = connexion.cursor()
            d = connexion.cursor()
            ### concatenation of the lines for file header ###
            ligne_entete_01 = "\n...OK... This is the tree :"
            ligne_entete_02 = self.database
            ligne_entete_03 = "  |"
            ### write the header to file ###
            fichier_texte.write(ligne_entete_01 + "\n")
            fichier_texte.write(ligne_entete_02 + "\n")
            fichier_texte.write(ligne_entete_03 + "\n")
            ### concatenation of the first instruction ###
            instruction_1 = """SELECT name FROM sqlite_master WHERE type = 'table' """
            self.debug_sqlite(instruction_1)
            ### analyse the tables in the database with c ###
            c.execute(instruction_1)
            for x in iter(c.fetchall()):
                ### concatenation of the second instruction ###
                instruction_2 = f"SELECT * FROM {x[0]}"
                self.debug_sqlite(instruction_2)
                ### analyse the column's name with d ###
                d.execute(instruction_2)
                ### concatenation for output ###
                ligne_A = "  + -" + str(x[0])
                try:
                    ligne_B = "  |       \ _ _ _ _ _" + str(d.fetchone().keys())
                except:
                    ligne_B = "  | "
                ### write the lines into the file ###
                fichier_texte.write(ligne_A + "\n")
                fichier_texte.write(ligne_B + "\n")
            ### definition of the final line ###
            ligne_fin = "  | \n  |_ END OF DATAS !\n"
            fichier_texte.write(ligne_fin + "\n")
            ### closing database and text file ###
            connexion.close()
            fichier_texte.close()
            ### if job is done return True ###
            return True
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            ### if job is not done return False ###
            return False

    ################################################################################################
    ### output a specific table to CSV
    ################################################################################################
    def edit_contains_csv(self, table, nom_fichier_sortie = "analyse_valknut.csv"):
        """output the contain of a specific table to a csv spreadsheet"""
        mark = None
        ### if database is a valid file ###
        if self.database != None:
            ### create and open a new csv file ###
            fichier_csv = open(nom_fichier_sortie, "w", newline = "")
            ecriture = csv.writer(fichier_csv)
            ### first connection to database ###
            connexion = sqlite3.connect(self.database)
            c = connexion.cursor()
            ### second connection to database to put out column's name ###
            connexion2 = sqlite3.connect(self.database)
            connexion2.row_factory = sqlite3.Row
            d = connexion2.cursor()
            try:
                ### concatenation of the first instruction ###
                instruction_1 = (f"SELECT * FROM {table}")
                self.debug_sqlite(instruction_1)
                ### analuse column's name ###
                d.execute(instruction_1)
                colonnes = d.fetchone()
                ### write the column's name into the file ###
                ecriture.writerow(colonnes.keys())
                ### concatenation of the second instruction ###
                instruction_2 = (f"SELECT * FROM {table}")
                self.debug_sqlite(instruction_2)
                ### analyse the contain of the table and output to file ###
                for x in c.execute(instruction_2):
                    ecriture.writerow(x)
                ### closing database and csv file ###
                fichier_csv.close()
                connexion.close()
                connexion2.close()
                mark = True
            except:
                ### in case of impossibility to check the table ###
                print("This table does not exist")
                mark = False
            ### return if job done or not ###
            return mark
        ### if database is not valid ###
        else:
            print("Action not allowed because no database is defined.")
            return mark

    ################################################################################################
    ### debugging function : will display the SQL instructions while running
    ################################################################################################
    def debug_sqlite(self, instruction):
        if self.debug_sqlite_instruction == True:
            print(instruction)

    ################################################################################################
    ### general displaying function : will print at screen if displaying_line = True
    ################################################################################################
    def displaying_return(self, display_this):
        if self.displaying_line == True:
            print(display_this)

####################################################################################################
### finally, when running the program like an executable, return the gss_interface
####################################################################################################
if __name__ == "__main__":
    runner = Valknut_gss_interface()
    runner
