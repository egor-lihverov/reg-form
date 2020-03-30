from flask import Flask, render_template
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import PasswordField, TextAreaField, SubmitField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

from data import db_session
from data import users

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    age = StringField('Возраст', validators=[DataRequired()])
    speciality = StringField('Профессия', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
   # about = TextAreaField("Немного о себе")
    submit = SubmitField('Войти')


def main():
    db_session.global_init("db/users.sqlite")

    @app.route('/register', methods=['GET', 'POST'])
    def reqister():
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают")
            session = db_session.create_session()
            if session.query(users.User).filter(users.User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Такой пользователь уже есть")
            user = users.User()
            user.surname = form.surname.data
            user.name = form.name.data
            user.age = form.age.data
            user.speciality = form.speciality.data
            user.address = form.address.data
            user.email = form.email.data
            user.hashed_password = form.password.data
            #user = users.User(
            #    name=form.name.data,
            #    email=form.email.data)
            #  #  surname=form.surname.data,
              #  age=int(form.age.data),
               # position=form.position.data,
              #  address=form.address.data)
            user.set_password(form.password.data)
            session.add(user)
            session.commit()
            return redirect('/login')
        return render_template('register.html', title='Регистрация', form=form)
    app.run()


if __name__ == '__main__':
    main()
