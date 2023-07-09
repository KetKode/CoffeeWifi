from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, SelectField
from wtforms.validators import DataRequired, URL
import csv
from datetime import datetime, time

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_url = StringField('Google Maps Link', validators=[DataRequired(), URL()])
    open_time = TimeField('When does it open?', validators=[DataRequired()])
    closing_time = TimeField('When does it close?', validators=[DataRequired()])
    coffee_rating = SelectField('How good is the coffee?', choices=["☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"],
                                validators=[DataRequired()])
    wifi_rating = SelectField('How good is the wifi?', choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪",
                                                                "💪💪💪💪💪"], validators=[DataRequired()])
    sockets_available = SelectField('How many sockets are there available?', choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌",
                                                                                      "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"],
                                    validators=[DataRequired()])
    submit = SubmitField('Submit', render_kw={'class': 'btn btn-warning btn-lg'})


# all Flask routes below


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_row = ','.join([
            form.cafe.data,
            form.location_url.data,
            form.open_time.data.strftime('%H:%M'),
            form.closing_time.data.strftime('%H:%M'),
            form.coffee_rating.data,
            form.wifi_rating.data,
            form.sockets_available.data
        ])
        with open("cafe-data.csv", newline='', encoding="utf8", mode="a") as file:
            file.write('\n' + str(new_row))
            return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
