from flask import Flask, render_template, url_for, request
import sqlite3
import os

app = Flask(__name__)
flag = 0
time = ''
#Путь текущего файла
cd = os.path.dirname(os.path.abspath(__file__))

#Главная страница
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

#Страница входа на сайт
@app.route('/reg', methods=['GET'])
def reg():
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']
        connection = sqlite3.connect(r'C:\Users\senya\register.db')
        cursor = connection.cursor()
        query1 = 'SELECT password from Registration WHERE name = "{n}"'.format(n = name)
        result = cursor.execute(query1)
        if result == None:
            return render_template('reg.html')
        else:
            #Переадрессация на страницу оптимизации сна
            return render_template('wakeup.html')
    return render_template('reg.html')

#Страница оптимизации сна
@app.route('/wakeup', methods=['POST', 'GET'])
def wakeup():
    global flag
    global time
    if request.method == "POST":
        sleep = request.form['sleep'].split(':')
        wakeup = request.form['wakeup'].split(':')
        print(sleep)
        print(wakeup)
        if sleep != [''] and wakeup != ['']:
            h = int(sleep[0])
            m = int(sleep[1])
            h_2 = int(wakeup[0])
            m_2 = int(wakeup[1])
        else:
            return render_template('wakeup.html')
        sleep_time = 0
        wake_up_time = 0


        #Класс для расчёта оптимального времени пробуждения 
        class WakeUp:
            global time
            def __init__(self, h, m, h_2, m_2):
                global flag
                if h > 23 or h_2 > 23 or m > 59 or m_2 > 59 or h == '' or m == '' or h_2 == '' or m_2 == '':
                    flag = 1
                else:
                    self.h = int(h) * 60
                    self.m = int(m)
                    self.h_2 = int(h_2) * 60
                    self.m_2 = int(m_2)

            def goodtime(self):
                global flag
                if flag == 1:
                    print('Недопустимый формат ввода')
                global sleep_time
                global wake_up_time
                sleep_time = self.h + self.m
                wake_up_time = self.h_2 + self.m_2
                if sleep_time < wake_up_time:
                    while sleep_time < wake_up_time - 105:
                        sleep_time += 105
                else:
                    sleep_time = 1439 - sleep_time
                    while sleep_time < wake_up_time - 105:
                        sleep_time += 105
                good_time = sleep_time
                total_minutes = good_time
                hours = total_minutes // 60
                minutes = total_minutes % 60
                r_minutes = str(minutes)
                if len(r_minutes) == 1:
                    r_minutes = r_minutes + '0'
                time_string = '{}:{}'.format(hours, r_minutes)
                return time_string
                sleep_time = 0
                wake_up_time = 0

        WK = WakeUp(h, m, h_2, m_2)
        time = WK.goodtime()
    return render_template('wakeup.html', time=time)

#Информационная страница
@app.route('/info')
def info():
    return render_template('info.html')

#Страница регистрации
@app.route('/registration', methods=["POST", "GET"])
def registration():
    if request.method == "POST":
        #Получение данных от пользователя
        name = request.form['name']
        password = request.form['password']
        #Подключение к базе данных
        connection = sqlite3.connect('register.db')
        cursor = connection.cursor()
        connection.commit()
        #Добавление нового пользователя
        query1 = 'INSERT INTO Registration(name, password) VALUES("{n}", "{passw}")'.format(n=name, passw=password)
        #Получение данных о всех логинах зарегистрированных на сайте
        query2 = 'SELECT name FROM Registration'
        if name not in cursor.execute(query2).fetchall():
            cursor.execute(query1)   
        connection.commit()
    #Переадрессация на страницу входа на сайт
    return render_template('registration.html')

if __name__ == '__main__':
    app.run(debug=True)

    
