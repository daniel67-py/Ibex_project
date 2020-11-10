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
from wsgiref.simple_server import make_server

####################################################################################################
### Valknut - Micro Server, GSS & SQLite3 manager
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
        self.project_index = []

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
        #print("searching for code examples")
        contain = self.per_coding_example(contain, "    ", " <pre><code>\n    ", " </code></pre>\n")
        #print("searching for h6 to h1 titles")
        contain = self.per_lines(contain, "######", "<h6>", "</h6> \n")
        contain = self.per_lines(contain, "#####", "<h5>", "</h5> \n")
        contain = self.per_lines(contain, "####", "<h4>", "</h4> \n")
        contain = self.per_lines(contain, "###", "<h3>", "</h3> \n")
        contain = self.per_lines(contain, "##", "<h2>", "</h2> \n")
        contain = self.per_lines(contain, "#", "<h1>", "</h1> \n")
        #print("searching for separators")
        contain = self.per_lines(contain, "------", "<hr />", "\n ")
        #print("searching for paragraphs")
        contain = self.per_lines(contain, "  ", "<p>\n", " </p>\n")
        #print("searching for lists")
        contain = self.per_list(contain, "+", "<ol>", "</ol>\n")
        contain = self.per_list(contain, "-", "<ul>", "</ul>\n")
        #print("searching for triple splat bold and italic quote")
        contain = self.per_emphasis(contain, "***", "<b><i>", "</i></b>")
        #print("searching for double splat bold quote")
        contain = self.per_emphasis(contain, "**", "<b>", "</b>")
        #print("searching for single splat italic quote")
        contain = self.per_emphasis(contain, "*", "<i>", "</i>")
        #print("searching for strikethrough quote")
        contain = self.per_emphasis(contain, "~~", "<s>", "</s>")
        #print("searching for underlines")
        contain = self.per_emphasis(contain, "__", "<u>", "</u>")
        #print("searching for pictures")
        contain = self.per_images(contain)
        #print("searching for urls")
        contain = self.per_links(contain)
        #print("searching for emails adresses")
        contain = self.per_mails(contain)
        #print("indexing the document's titles")
        contain = self.indexer(contain)
        #print("extracting the links to intern chapters")
        doc_chapter = self.chapter(contain)
        #print("saving the output result into .html")
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
                        page_index = self.project_index,
                        ))
        elif self.feedback != 0:
            templ = Template(static_page)
            output_file = templ.render(page_title = self.project_title,
                                       page_summary = doc_chapter,
                                       page_header = self.project_header,
                                       page_contains = contain,
                                       page_footer = self.project_footer,
                                       page_index = self.project_index,
                                       )
            return output_file
        ### tell the user that the job is done ###
        print("job done !")

    ### this function returns directly a template without processing ###
    def direct(self, template):
        with open(template, 'r') as model:
            page = model.read()
            
        templ = Template(page)
        output_file = templ.render()
        return output_file

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
            elif y.endswith(symbol_to_modify) == True and mark_code == 0:
                y = y.replace(symbol_to_modify, replace_ending_parse)
                y = replace_open_parse + y
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
### Valknut_gss tkinter interface
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
        elif selection == "source":
            self.source_entry.delete(0, 10000)
        elif selection == "destination":
            self.out_file_entry.delete(0, 10000)

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
            self.cleaner("source")
            self.cleaner("destination")
        except:
            showwarning("no no no...", "cannot do the job, something is missing somewhere !")
