from flask import Flask
from flask import render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import request
import folium
import json
import os


'''
    Initialising libraries
'''

################################################################################################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///User_Data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
session = []
wr_ses = []
'''
    Initialising app
'''

################################################################################################


def maker_map(data):
    def party_color(feature):
        return {
            "fillColor": feature['properties']['fill'],
            "fillOpacity": feature['properties']['fill-opacity'],
            "opacity": 0.8
        }

    def popup_html(feature):
        html = '<h5>{}</h5>'.format(feature['properties']['name'])
        html += '<b>{}</b>'.format(feature['properties']['inf'])

        return html

    m = folium.Map(
        location=[55.74759843942743, 48.742733001708984],
        # tiles='Mapbox Bright',
        zoom_start=14
    )
    # data = open("kek.geojson", 'r').read()
    print(data)
    lol = json.loads(data)

    data = lol
    for mo in data['features']:
        gj = folium.GeoJson(
            data=mo,
            style_function=party_color,
            control=False,
            highlight_function=lambda x: {
                "fillOpacity": 0.2,
                "opacity": 1
            },
            smooth_factor=0)

        folium.Popup(popup_html(mo)).add_to(gj)
        gj.add_to(m)

    folium.LayerControl().add_to(m)

    m.save(os.path.join('results', 'inno.html'))


################################################################################################

def user_add_session(name):
    session.append(name)


def user_remove_session(name):
    for i in session:
        if i == name:
            session.remove(i)

'''
    Adding and removing users functions
'''

################################################################################################

class SiteUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    spec_parameter = db.Column(db.Integer, unique=False, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    surname = db.Column(db.String(80), unique=False, nullable=False)
    js = db.Column(db.String(80), unique=False, nullable=True)

    def __repr__(self):
        return '<SiteUser {} {} {} {} {} {}>'.format(
            self.id, self.email, self.password, self.spec_parameter, self.name, self.surname, self.js)


'''
    Class that makes data base of users
'''

################################################################################################
@app.route('/login', methods=['GET', 'POST'])
def login():
    if len(wr_ses) == 0 or wr_ses[-1] == 0:
        if request.method == 'GET':
            return render_template('login.html', kek=0)

        elif request.method == 'POST':
            try:
                if request.form['reg'] != 0:
                    return redirect('http://127.0.0.1:8080/registration')
            except:
                try:
                    str_1 = str(SiteUser.query.filter_by(email=request.form['email']).first()).split()
                    print(str_1[2])
                    user_add_session(str_1[2])
                    wr_ses.append(0)
                    if request.form['password'] == str_1[3]:
                        return redirect('http://127.0.0.1:8080/success')
                    else:
                        wr_ses.append(1)
                        return redirect('http://127.0.0.1:8080/login')
                except:
                    wr_ses.append(1)
                    return redirect('http://127.0.0.1:8080/login')
            wr_ses.append(0)
        wr_ses.append(0)

    elif wr_ses[-1] == 1:
        if request.method == 'GET':
            return render_template('login.html', kek=1)

        elif request.method == 'POST':
            try:
                if request.form['reg'] != 0:
                    return redirect('http://127.0.0.1:8080/registration')
            except:
                try:
                    str_1 = str(SiteUser.query.filter_by(email=request.form['email']).first()).split()
                    print(str_1[2])
                    user_add_session(str_1[2])
                    wr_ses.append(0)
                    if request.form['password'] == str_1[3]:
                        return redirect('http://127.0.0.1:8080/success')
                    else:
                        wr_ses.append(1)
                        return redirect('http://127.0.0.1:8080/login')
                except:
                    wr_ses.append(1)
                    return redirect('http://127.0.0.1:8080/login')
            wr_ses.append(0)
        wr_ses.append(0)

'''
    Login page
'''


################################################################################################
@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html')

    elif request.method == 'POST':
        try:
            if request.form['log'] != 0:
                return redirect('http://127.0.0.1:8080/login')
        except:
            try:
                new_user = SiteUser(email=str(request.form['email']), password=str(request.form['password']),
                                    spec_parameter='1', name=str(request.form['name']), surname=str(request.form['surname']), js='')
                wr_ses.append(0)
                user_add_session(str(request.form['email']))
                db.create_all()
                db.session.add(new_user)
                db.session.commit()
                return redirect('http://127.0.0.1:8080/success')

            except:
                return render_template('registration.html', kek=1)


'''
    Registration page
'''

################################################################################################
@app.route('/success', methods=['POST', 'GET'])
def success():
    '''это не работает '''
    if request.method == 'GET':
        if len(session) != 0:
            return render_template('success.html', title='Success', username=session[-1], session=session)
        else:
            wr_ses.append(1)
            return redirect('http://127.0.0.1:8080/login')
    elif request.method == 'POST':
        try:
            if request.form['logout'] != 0:
                user_remove_session(session[-1])
                wr_ses.append(0)
                return redirect('http://127.0.0.1:8080/login')

        except:
            a = str(request.form['head'])
            b = str(request.form['text'])
            if a != '':
                maker_map(b)
                my_file = open('{}'.format(a), 'w')
                my_file.write(b)
                my_file.close()

            """"
            Тут вот он просто сохраняет файл
            """
            return redirect('http://127.0.0.1:8080/success')



'''
    Registration page
'''
################################################################################################


@app.route('/main_page', methods=['GET'])
def main_page():
    return open("templates/main_page.html", "r").read()


@app.route('/inno', methods=['GET'])
def inno():
    return open("results/inno.html", "r").read()

################################################################################################
if '__main__' == __name__:
    app.run(port=8080, host='127.0.0.1')

'''
    Running site
'''
