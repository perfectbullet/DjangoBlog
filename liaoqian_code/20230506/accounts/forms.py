import hashlib

from flask import request
from flask_login import login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo

from models import User, db, UserProfile, UserLoginHistory
from utils import constants
from utils.validators import phone_required


class RegisterForm(FlaskForm):
    """用户注册"""
    username = StringField(label='用户名', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入用户名'
    }, validators=[DataRequired('请输入用户名'), phone_required])
    nickname = StringField(label='用户昵称', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入用户昵称'
    }, validators=[DataRequired('请输入用户昵称'),
                   Length(min=2, max=20, message='昵称长度在2-20之间')])
    password = PasswordField(label='密码', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入密码'
    }, validators=[DataRequired('请输入密码')])
    confirm_password = PasswordField(label='确认密码', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入确认密码'
    }, validators=[DataRequired('请输入确认密码'),
                   EqualTo('password', message='两次密码输入不一致')])

    def validate_username(self, field):
        """检测用户名是否已经存在"""
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('该用户名已经存在')
        return field

    def register(self):
        """自定义的用户注册函数"""
        # 1.获取表单信息
        username = self.username.data
        password = self.password.data
        nickname = self.nickname.data
        # 2.添加到db.session
        try:
            # 将密码加密存储
            password = hashlib.sha256(password.encode()).hexdigest()
            user_obj = User(username=username, password=password, nickname=nickname)
            db.session.add(user_obj)
            profile = UserProfile(username=username, user=user_obj)
            db.session.add(profile)
            db.session.commit()
            return user_obj
        except Exception as e:
            print(e)
        return None


class LoginForm(FlaskForm):
    """用户登录"""
    username = StringField(label='用户名', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入用户名'
    }, validators=[DataRequired('请输入用户名'), phone_required])
    password = PasswordField(label='密码', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入密码'
    }, validators=[DataRequired('请输入密码')])

    def validate(self, extra_validators=None):
        result = super().validate()
        username = self.username.data
        password = self.password.data
        password = hashlib.sha256(password.encode()).hexdigest()
        print('password2: ', password)
        if result:
            # TODO 验证加密后的密码是否正确
            user = User.query.filter_by(username=username, password=password).first()
            if user is None:
                result = False
                self.username.errors = ['用户名或者是密码错误']
            elif user.status == constants.UserStatus.USER_IN_ACTIVE.value:
                result = False
                self.username.errors = ['用户已被禁用']
        return result

    def do_login(self):
        """执行登录逻辑代码"""
        username = self.username.data
        password = self.password.data
        password = hashlib.sha256(password.encode()).hexdigest()
        print('password: ', password)
        try:
            # 1.查找对应用户
            # TODO 验证加密后的密码是否正确
            user = User.query.filter_by(username=username, password=password).first()
            # 2.登录用户
            # session['user_id'] = user.id
            login_user(user)
            # 3.记录日志
            ip = request.remote_addr
            ua = request.headers.get('user-agent', None)
            obj = UserLoginHistory(username=username, ip=ip, ua=ua, user=user)
            db.session.add(obj)
            db.session.commit()
            return user
        except Exception as e:
            print(e)
        return None
