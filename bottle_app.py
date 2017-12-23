
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
            %s
        </body>
    </html>
    """ % (title,text)
    return page

def sort_html_code():
    form = '''
    <form action="/sort" method="POST">
        <table>
            <tr>
                <td>
                    <div>
                        <input type="radio" name="desc_or_asc" value="descending" %s/>Descending<br/>
                        <input type="radio" name="desc_or_asc" value="ascending" %s/>Ascending<br/>
                    </div>
                </td>
                <td>
                    <div>
                        <span>sort by</span></br>
                        <select name="column_no">
                            <option value="1" %s>Year</option>
                            <option value="2" %s>IMDb</option>
                            <option value="3" %s>Duration</option>
                        </select>
                    </div>
                </td>
                <td>
                    <input type="text" name="search" value="%s"/>
                </td>
                <td>
                
                    <span>search in</span></br>
                    <input type="checkbox" name="search_type" value="0">Year<br>
                    <input type="checkbox" name="search_type" value="1">IMDb (greater than)<br>
                    <input type="checkbox" name="search_type" value="2">Duration
                </td>
                    
                <td>
                    <input type="submit" value="Search and Sort"/><br/>
                </td>
            </tr>
        </table>
    </form>
    '''
    return form

def comment_form_html_code(content):
    form = '''
    <form action="/save_comment/%s" method="POST">
        <input type="text" name="comment_text" value=""/><br/>
        <input type="submit" value="Save"/>
    </form>
    ''' % content
    return form

def comment_button(movie_name):
    code= '''<form action="/comments/%s" method="POST">
        <input type="submit" value="Comment"/>
    </form>
    ''' % movie_name
    return code
def sort(list, desc_or_asc, column_no, search):

    ordered_list = []

    for row in list:
        if search.lower() in str(row).lower():
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
        return "<h1>Not Found!\nPlease try again</h1>"
    table_code = '''
    <tr>
        <th>Movies About Time Travel</th>
        <th>Year</th>
        <th>IMDb</th>
        <th>Duration</th>
        <th>Comment</th>
    </tr>
    '''
    for rows in range(len(list)):
        row = ""
        for column in range(len(list[rows])):
            row += "<td>%s</td>\n" % str(list[rows][column])
        row += "<td>%s</td>\n" % comment_button(list[rows][0])
        table_code += "<tr>\n%s\n</tr>\n" % row
    return "<table>\n%s\n</table>" % table_code

def index():
    return htmlify("Time Travel Movies",
                   sort_html_code() % ("checked","","selected","","","")+get_table_html_code(contents))

def order_page():
    desc_or_asc = request.POST['desc_or_asc']
    column_no = request.POST['column_no']
    search = request.POST['search']
    sort_html = sort_html_code() % ("%s","%s","%s","%s","%s",search)
    if desc_or_asc == "descending":
        sort_html = sort_html % ("checked","","%s","%s","%s")
    elif desc_or_asc == "ascending": 
        sort_html = sort_html % ("","checked","%s","%s","%s")

    if column_no == "1":
        sort_html = sort_html % ("selected","","")
    elif column_no == "2":
        sort_html = sort_html % ("","selected","")
    elif column_no == "3":
        sort_html = sort_html % ("","","selected")

    return htmlify("Time Travel Movies",
                   sort_html+get_table_html_code(sort(contents, desc_or_asc, int(column_no),search)))

def comment_page(movie_name):
    return htmlify("Comment",
                   comment_form_html_code(movie_name))

def show_comments():
    comments = []
    comments_file = open("comments.txt","r")
    for row in reader(comments_file):
        comments = comments + [row]
    return str(comments)
    

def save_comment(content):
    comment_text = request.POST['comment_text']
    comments_file = open('comments.txt','w')
    comments_file.write(comment_text+ " " + content)
    comments_file.close()
    return htmlify("Comment",
                   "kaydedildi: " + comment_text+ " " + content)



def server_static(path):
    return static_file(path, root='.')


route('/', 'GET', index)
route('/sort', 'POST', order_page)
route('/comments/<movie_name>', 'POST', comment_page)
route('/save_comment/<content>', 'POST', save_comment)
route('/comments', 'GET', show_comments)
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

