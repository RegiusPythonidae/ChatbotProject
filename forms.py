from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, DateField, RadioField, SelectField, TextAreaField, \
    SelectMultipleField
from wtforms.validators import DataRequired, length, EqualTo


class RegisterForm(FlaskForm):
    username = StringField("შეიყვანეთ სახელი", validators=[DataRequired(), length(min=8, max=64)])

    password = PasswordField("შეიყვანეთ პაროლი", validators=[length(min=8, max=64, message="პაროლი არის მოკლე")])
    repeat_password = PasswordField("გაიმეორეთ პაროლი",
                                    validators=[EqualTo("password", message="პაროლები არ ემთხვევა")])

    birthday = DateField("დაბადების თარიღი")
    country = SelectField("აირჩიეთ ქვეყანა", choices=["აირჩიეთ ქვეყანა", "Georgia", "USA", "Germany"])
    gender = RadioField("მონიშნეთ სქესი", choices=["კაცი", "ქალი"])
    about_me = TextAreaField("თქვენს შესახებ")

    submit = SubmitField("რეგისტრაცია")


class LoginForm(FlaskForm):
    username = StringField("შეიყვანეთ სახელი", validators=[DataRequired(), length(min=8, max=64)])

    password = PasswordField("შეიყვანეთ პაროლი", validators=[length(min=8, max=64, message="პაროლი არის მოკლე")])
    submit = SubmitField("ავტორიზაცია")

class MessageForm(FlaskForm):
    message = StringField("შეიყვანეთ მესიჯი")
    submit = SubmitField("გაგზავნა")
