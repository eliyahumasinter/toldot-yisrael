from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from urllib.request import urlopen
from bs4 import BeautifulSoup
import wikipedia as wk
from search import searchterms
import sqlite3
import re
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey123'
bootstrap = Bootstrap(app)


@app.route("/")
@app.route("/home")
def home():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    text = "SELECT link, name FROM videos WHERE count==1 LIMIT 12"
    cur.execute(text)
    row = cur.fetchall()
    return render_template("home.html", videos=row)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/search", methods=['POST'])
def search():
    search = request.form['search']

    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    text = "SELECT * FROM videos WHERE name LIKE '%" + search + "%' LIMIT 10"
    cur.execute(text)
    row = cur.fetchall()
    return render_template("results.html", results=row, query=search)


@app.route('/searchterm', methods=['POST'])
def searchterm():
    searchterm = request.form['searchterm']
    numbers = [18, 24, 35, 65, 66, 81, 99]
    x = searchterms(searchterm, numbers)
    KEYS = list(x.keys())
    string = ''
    for i in KEYS:
        string += str(i)
        if KEYS[-1] != i:
            string += ","
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    text = "SELECT link FROM videos WHERE ID IN (" + string + ")"
    print(text)
    cur.execute(text)
    row = cur.fetchall()
    final_dic = {}
    count = 0
    for i in row:
        final_dic[i] = x[numbers[count]]
        count += 1

    return render_template("searchterms.html", final_dic=final_dic, search=searchterm)


@app.route("/person/<person>")
def person(person):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    text = "SELECT about FROM videos WHERE name = '" + person + "'"
    cur.execute(text)
    row = cur.fetchall()
    link = row[0][0]
    return render_template("person.html", person=person, about=link, webinfo=webinfo(link))


@app.route("/information/<information>")
def information(information):
    link = None
    try:
        link = wk.page(wk.search(information)[0]).url
        x = wk.page(wk.search(information)[0]).content[:1500] + "..."
    except:
        x = None
    try:
        img = wk.page(wk.search(information)[0]).images[0]
    except:
        img = None
    return render_template("information.html", query=information, info=x, img=img, url=link)


def webinfo(link):
    if link == "None":
        return None
    source = urlopen(link).read()
    soup = BeautifulSoup(source, 'lxml')
    soup
    paras = []
    for paragraph in soup.find_all('p'):
        paras.append(str(paragraph.text))
    heads = []
    for head in soup.find_all('span', attrs={'mw-headline'}):
        heads.append(str(head.text))
    text = [val for pair in zip(paras, heads) for val in pair]
    text = text[1:]
    text = ' '.join(text)
    text = re.sub(r"\[.*?\]+", '', text)
    text = text.replace('\n', '')[:-11]
    return text


if __name__ == '__main__':
    app.run(port=1234, debug=True, host="0.0.0.0")
