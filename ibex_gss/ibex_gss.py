#!/usr/bin/python3
#-*- coding: Utf-8 -*-

### no imports, uses only the python's build-in functions ###

page_header_style = """
<!DOCTYPE html>
<html>
<body>
"""

page_footer_style = """
</body>
</html>
"""

### this function analyse lines per lines the whole markdown file ###
### and puts quote for titles or separators ###
def per_lines(sequence, symbol_to_modify, replace_open_parse, replace_ending_parse):
    analyse = sequence.splitlines()
    new_output = ""

    for y in analyse:
        if y.startswith(symbol_to_modify) == True:
            y = y.replace(symbol_to_modify, replace_open_parse)
            y += replace_ending_parse
            new_output += y
        else:
            new_output += y
        new_output += "\n"

    return new_output

### this function analyse lines per lines the whole markdown file ###
### and search if there is coding exemples ###
def per_coding_example(sequence, number_of_spaces, opening_parse, closing_parse):
    mark_coding = 0

    analyse = sequence.splitlines()
    new_output = ""

    for x in analyse:
        if number_of_spaces in x and mark_coding == 0:
            x = x.replace(number_of_spaces, opening_parse)
            new_output += x
            mark_coding = 1
        elif number_of_spaces in x and mark_coding == 1:
            new_output += x
        elif mark_coding == 1 and x == "":
            mark_coding = 0
            x = x.replace("", closing_parse)
            new_output += x
        else:
            new_output += x
        new_output += "\n"

    return new_output

### this function analyse lines per lines the whole markdonw file ###
### and search if there is some unordered lists ###
def per_list(sequence, begins, opening_parse, closing_parse):
    mark_list = 0

    analyse = sequence.splitlines()
    new_output = ""

    for w in analyse:
        if w.startswith(begins) == True and mark_list == 0:
            w = w.replace(begins, opening_parse + "<li>")
            new_output += w + "</li>"
            mark_list = 1
        elif w.startswith(begins) == True and mark_list == 1:
            w = w.replace(begins, "<li>")
            new_output += w + "</li>"
        elif mark_list == 1 and w == "":
            mark_list = 0
            w = w.replace("", closing_parse)
            new_output += w
        else:
            new_output += w
        new_output += "\n"

    return new_output

### this function analyse lines per lines the whole markdown file ###
### and parse bold or italic symbols ###
def per_emphasis(sequence, symbol_to_modify, replace_open_parse, replace_ending_parse):
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
### and parse url or images symbols ###
def per_links(sequence, symbol_to_modify, replace_parse):
    mark_links = 0
    mark_code = 0

    analyse = sequence.split(" ")
    new_output = ""
            
    for z in analyse:
        if "<pre><code>" in z:
            mark_code = 1
        elif "</code></pre>" in z:
            mark_code = 0

        if symbol_to_modify in z and mark_code == 0:
            z = z.replace(symbol_to_modify, replace_parse)
            new_output += z
        else:
            new_output += z + " "

    return new_output

### this function start the convertion of the markdown file ###
### all beggins from here... ###
def ibex_gss(file, feedback = 0, out_file = 'ibex_gss.html'):
    with open(file, 'r') as source:
        contain = source.read()

    print("searching for h6 to h1 titles")
    contain = per_lines(contain, "######", " <h6>", " </h6>\n")
    contain = per_lines(contain, "#####", " <h5>", " </h5>\n")
    contain = per_lines(contain, "####", " <h4>", " </h4>\n")
    contain = per_lines(contain, "###", " <h3>", " </h3>\n")
    contain = per_lines(contain, "##", " <h2>", " </h2>\n")
    contain = per_lines(contain, "#", " <h1>", " </h1>\n")
    print("searching for separators")
    contain = per_lines(contain, "------", "<hr />", "\n ")
    print("searching for code examples")
    contain = per_coding_example(contain, "    ", " <pre><code>\n    ", " </code></pre>\n")
    print("searching for lists")
    contain = per_list(contain, "+ ", "<ol>", "</ol>")
    contain = per_list(contain, "- ", "<ul>", "</ul>")
    print("searching for double splat bold quote")
    contain = per_emphasis(contain, "**", "<b>", "</b>")
    print("searching for single splat italic quote")
    contain = per_emphasis(contain, "*", "<i>", "</i>")
    print("searching for urls")
    contain = per_links(contain, "[+url]", "<a href = '")
    contain = per_links(contain, "[url+]", "'>lien</a>")
    print("searching for images")
    contain = per_links(contain, "[+img]", "<figure><center><img src='")
    contain = per_links(contain, "[img+]", "'></center></figure>")
    print("saving the output result into ibex_gss.html")

    if feedback == 0:
        with open(out_file, 'w') as output_file:
            output_file.write(page_header_style)
            output_file.write(contain)
            output_file.write(page_footer_style)
    elif feedback != 0:
        output_file = page_header_style + contain + page_footer_style
        return output_file

    print("job done !")
        
