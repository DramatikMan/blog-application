from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, URL

from core.models import User


class OpenIDForm(FlaskForm):
    openid = StringField('OpenID URL', [DataRequired(), URL()])


class CommentForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired(), Length(max=255)]
    )
    text = TextAreaField(
        'Comment',
        validators=[DataRequired()]
    )


class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField('Remember Me')

    def validate(self):

        # check if validators pass
        check_validate = super().validate()
        if not check_validate:
            return False

        # check if a user exists
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('Invalid username or password')
            return False

        # check if passwords match
        if not user.check_password(self.password.data):
            self.username.errors.append('Invalid username or password')
            return False

        return True


class RegisterForm(FlaskForm):
    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired(), Length(min=8)])
    confirm = PasswordField('Confirm Password', [
        DataRequired(),
        EqualTo('password')
    ])
    recaptcha = RecaptchaField()

    def validate(self):

        # check if validators pass
        check_validate = super().validate()
        if not check_validate:
            return False

        # check if username is taken
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('User with that name already exists.')
            return False

        return True


class PostForm(FlaskForm):
    title = StringField('Title', [DataRequired(), Length(max=255)])
    # text = TextAreaField('Content', [DataRequired()])
    text = TextAreaField('Content') # no DataRequired() or CKEditor breaks
