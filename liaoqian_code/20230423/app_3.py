from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    # 1.简单数据类型的渲染
    age = 40
    money = 65.89
    name = '张三'
    # 2.用户信息 dict
    user_info = {
        'username': '张三',
        'nickname': '三哥',
        'address.city': '广州',
        'address.area': '天河'
    }
    # 3.元组和列表
    tuple_city = ('北京', '上海', '广州', '深圳')
    list_city = ('北京', '上海', '广州', '深圳')

    # 4.复杂的数据结构
    list_user = [
        {
            'username': '张三',
            'address': {
                'city': '广州'
            }
        },
        {
            'username': '李四',
            'address': {
                'city': '北京'
            }
        }
    ]
    return render_template('index_3.html',
                           age=age,
                           money=money,
                           name=name,
                           user_info=user_info,
                           tuple_city=tuple_city,
                           list_city=list_city,
                           list_user=list_user)


@app.route('/tag')
def tag():
    """模板标签的使用"""
    var = 1
    a = 2
    # list_user = [
    #     {'username': '张三', 'age': 32, 'address': '北京'},
    #     {'username': '李四', 'age': 22}
    # ]
    list_user = []
    return render_template('tag.html',
                           var=var,
                           a=a,
                           list_user=list_user)
