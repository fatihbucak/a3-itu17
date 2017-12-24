
#####################################################################
### Assignment skeleton
### You can alter the below code to make your own dynamic website.
### The landing page for assignment 3 should be at /
#####################################################################

from bottle import route, run, default_app, debug, request, static_file
from csv import reader

contents = []
input_file = open("a2_input.csv","r")
for row in reader(input_file):
    contents = contents + [row]
def htmlify(title,text):
    page = """
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8" />
            <title>%s</title>
            <link rel="stylesheet" href="/static/custom.css"/>
        </head>
        <body>
            <div id="main">
                <a id="logo" href="/"><img src="static/home.png" alt="Time Travel"/></a>
                <h1 id="title">Movies About Time Travel</h1>
                %s
            </div>
        </body>
    </html>
    """ % (title, text)
    return page

def sort_html_code():
    form = '''
    <form id="form" action="/sort_search" method="POST">
        <table>
            <tr>
                <td class="odd">
                    <span>Search</span></br>
                    <input type="text" name="search" value="%s" placeholder = "Movie"/>
                </td>
            
                <td class="even">
                    <div>
                        <input type="radio" name="desc_or_asc" value="descending" %s/>Descending order<br/>
                        <input type="radio" name="desc_or_asc" value="ascending" %s/>Ascending order<br/>
                    </div>
                </td>
            
                <td class="odd">
                    <div>
                        <span>Sort by</span></br>
                        <select name="column_no">
                            <option value="1" %s>Year</option>
                            <option value="2" %s>IMDb</option>
                            <option value="3" %s>Duration</option>
                        </select>
                    </div>
                </td>
            
                <td class="even">
                    <span>Filter</span></br>
                    
                    <input type="checkbox" name="filter_no" value="1" %s/>Year
                    <select name="year_filter_type">
                        <option value="0" %s>&gt;</option>
                        <option value="1" %s>&lt;</option>
                    </select>
                    <input class="numbers" type="number" name="year_filter_text" value="%s"/><br/>
                    
                    <input type="checkbox" name="filter_no" value="2" %s/>IMDb
                    <select name="imdb_filter_type">
                        <option value="0" %s>&gt;</option>
                        <option value="1" %s>&lt;</option>
                    </select>
                    <input class="numbers" type="number" name="imdb_filter_text" value="%s"/><br/>
                    
                    <input type="checkbox" name="filter_no" value="3" %s/>Duration
                    <select name="duration_filter_type">
                        <option value="0" %s>&gt;</option>
                        <option value="1" %s>&lt;</option>
                    </select>
                    <input class="numbers" type="number" name="duration_filter_text" value="%s"/><br/>
                </td>
            
                <td class="odd">
                    <input type="submit" value="Search and Sort"/><br/>
                </td>
            </tr>
        </table>
    </form>
    '''
    return form


def sort_search(list, desc_or_asc, column_no, search, filter_no, year_filter_type, imdb_filter_type, duration_filter_type, year_filter_text,imdb_filter_text, duration_filter_text):

    ordered_list = []

    for row in list:
        if search.lower() in str(row[0]).lower():
            ordered_list += [row]

    
    if "1" in filter_no:
        temporary_list = ordered_list
        ordered_list = []
        if year_filter_type == "0":
            for row in temporary_list:
                if int(row[1]) > int(year_filter_text):
                    ordered_list += [row]
        elif year_filter_type == "1":
            for row in temporary_list:
                if int(row[1]) < int(year_filter_text):
                    ordered_list += [row]

    
    if "2" in filter_no:
        temporary_list = ordered_list
        ordered_list = []
        if imdb_filter_type == "0":
            for row in temporary_list:
                if float(row[2]) > float(imdb_filter_text):
                    ordered_list += [row]
        elif imdb_filter_type == "1":
            for row in temporary_list:
                if float(row[2]) < float(imdb_filter_text):
                    ordered_list += [row]
                    
    if "3" in filter_no:
        temporary_list = ordered_list
        ordered_list = []
        if duration_filter_type == "0":
            for row in temporary_list:
                if int(row[3]) > int(duration_filter_text):
                    ordered_list += [row]
        elif duration_filter_type == "1":
            for row in temporary_list:
                if int(row[3]) < int(duration_filter_text):
                    ordered_list += [row]
    
    if desc_or_asc == "ascending":
        while True:
            all_is_well = True
            for row in range(len(ordered_list)-1):
                if float(ordered_list[row][column_no])>float(ordered_list[row+1][column_no]):
                    temporary = ordered_list[row]
                    ordered_list[row] = ordered_list[row+1]
                    ordered_list[row+1] = temporary
                    all_is_well = False
            if all_is_well:
                break
    elif desc_or_asc == "descending":
        while True:
            all_is_well = True
            for row in range(len(ordered_list)-1):
                if float(ordered_list[row][column_no])<float(ordered_list[row+1][column_no]):
                    temporary = ordered_list[row]
                    ordered_list[row] = ordered_list[row+1]
                    ordered_list[row+1] = temporary
                    all_is_well = False
            if all_is_well:
                break
    return ordered_list

def get_table_html_code(list):
    if len(list) == 0:
        return "<h4>Not Found!\nPlease try again</h4>"
    table_code = '''
    <tr class="tr_list">
        <th class="list_th">Movies</th>
        <th class="list_th">Year</th>
        <th class="list_th">IMDb</th>
        <th class="list_th">Duration</th>
    </tr>
    '''
    for rows in range(len(list)):
        row = ""
        for column in range(len(list[rows])):
            row += "<td class=\"list_td\">%s</td>\n" % str(list[rows][column])
        table_code += "<tr class=\"tr_list\">\n%s\n</tr>\n" % row
    return '''<table id="list_table" >\n%s\n</table>''' % table_code

def index():
    return htmlify("Time Travel Movies",
                   sort_html_code() % ("","checked","","selected","","","","selected","","2000","","selected","","7","","selected","","90") + get_table_html_code(contents))

def order_page():
    desc_or_asc = request.POST['desc_or_asc']
    column_no = request.POST['column_no']
    search = request.POST['search']
    filter_no = request.POST.getall('filter_no')
    year_filter_type = request.POST['year_filter_type']
    imdb_filter_type = request.POST['imdb_filter_type']
    duration_filter_type = request.POST['duration_filter_type']
    year_filter_text = request.POST['year_filter_text']
    imdb_filter_text = request.POST['imdb_filter_text']
    duration_filter_text = request.POST['duration_filter_text']
    
    
    if desc_or_asc == "descending":
        desc="checked"
        asce=""
    elif desc_or_asc == "ascending": 
        desc=""
        asce="checked"

    col1=""
    col2=""
    col3=""

    if column_no == "1":
        col1="selected"

    elif column_no == "2":
        col2="selected"

    elif column_no == "3":
        col3="selected"
        
    if "1" in filter_no:
        check1 = "checked"
    else:
        check1 = ""

    if "2" in filter_no:
        check2 = "checked"
    else:
        check2 = ""

    if "3" in filter_no:
        check3 = "checked"
    else:
        check3 = ""

    yft0 = ""
    yft1 = ""
    if year_filter_type == "0":
        yft0 = "selected"
    elif year_filter_type == "1":
        yft1 = "selected"
        
    ift0 = ""
    ift1 = ""
    if imdb_filter_type == "0":
        ift0 = "selected"
    elif imdb_filter_type == "1":
        ift1 = "selected"


    dft0 = ""
    dft1 = ""
    if duration_filter_type == "0":
        dft0 = "selected"
    elif duration_filter_type == "1":
        dft1 = "selected"
        
    sort_html = sort_html_code() % (search,desc,asce,col1,col2,col3,check1,yft0,yft1,year_filter_text,check2,ift0,ift1,imdb_filter_text,check3,dft0,dft1,duration_filter_text)

    return htmlify("Time Travel Movies",
                   sort_html + get_table_html_code(sort_search(contents, desc_or_asc, int(column_no),search, filter_no, year_filter_type, imdb_filter_type, duration_filter_type, year_filter_text,imdb_filter_text, duration_filter_text)))


def server_static(path):
    return static_file(path, root='.')


route('/', 'GET', index)
route('/sort_search', 'POST', order_page)
route('/static/<path>', 'GET', server_static)

#####################################################################
### Don't alter the below code.
### It allows this website to be hosted on Heroku
### OR run on your computer.
#####################################################################

# This line makes bottle give nicer error messages
debug(True)
# This line is necessary for running on Heroku
app = default_app()
# The below code is necessary for running this bottle app standalone on your computer.
if __name__ == "__main__":
  run()

