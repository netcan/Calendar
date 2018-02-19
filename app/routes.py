from flask import render_template, session, request, jsonify
from datetime import date
from app import app
from app.models import User
import calendar


@app.route("/")
@app.route("/index")
def index():
    if session.get('username'):
        u = User.query.filter_by(username=session['username']).first()
        return render_template("index.html", u=u)
    else:
        users = User.query.all()
        return render_template("login.html", users=users)


@app.route("/api/login", methods=['POST'])
def login():
    """
    status_code: 0表示成功，1表示失败
    """
    ret = {'status_code': 1}
    if session.get('username'):
        ret['status_code'] = 0
        return jsonify(**ret)

    username = request.form.get('username', None)
    password = request.form.get('password', None)
    if username and password:
        u = User.query.filter_by(username=username).first()
        if u and u.check_password(password):
            session['username'] = username
            ret['status_code'] = 0

    return jsonify(**ret)


@app.route("/api/logout")
def logout():
    session.pop('username', None)
    return jsonify('logout success')


@app.route("/api/cal/")
@app.route("/api/cal/<int:year>/<int:month>")
def cal(year=None, month=None):
    """
    返回当前月份的天数
    """
    today = date.today()
    if year is None or not (1 <= month <= 12):
        year = today.year
        month = today.month

    cal = calendar.Calendar(firstweekday=6)

    monthdates = cal.monthdatescalendar(year, month)
    next_monthdates = cal.monthdatescalendar(year if month + 1 <= 12 else year + 1,
                                             month + 1 if month + 1 <= 12 else 12)
    while len(monthdates) < 6:
        for w in next_monthdates:
            if w in monthdates:
                continue
            monthdates.append(w)

    days = []
    for w in monthdates:
        for d in w:
            day = {
                'day': d.day,
                'style': 'day'
            }
            if today.day == d.day and today.year == d.year and today.month == d.month:
                day['style'] = 'today'
            elif d.month != month:
                day['style'] = 'other-day'

            days.append(day)

    ret = {}
    for w in range(6):
        ret['week' + str(w)] = days[7 * w:7 * (w + 1)]

    ret["cal-title"] = calendar.month_name[month] + ' ' + str(year)
    ret["year"] = year
    ret["month"] = month

    return jsonify(**ret)
