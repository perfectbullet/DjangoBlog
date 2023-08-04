# flask-restful-login-example
[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

### 关于jwt的概念
JSON Web Token（缩写 JWT）是目前最流行的跨域认证解决方案

JWT 的原理是，服务器认证以后，生成一个 JSON 对象，发回给用户，就像下面这样。
```json
{
  "姓名": "张三",
  "角色": "管理员",
  "到期时间": "2018年7月1日0点0分"
}
```
以后，用户与服务端通信的时候，都要发回这个 JSON 对象。服务器完全只靠这个对象认定用户身份。为了防止用户篡改数据，服务器在生成这个对象的时候，会加上签名（详见后文）。
服务器就不保存任何 session 数据了，也就是说，服务器变成无状态了，从而比较容易实现扩展。
https://www.ruanyifeng.com/blog/2018/07/json_web_token-tutorial.html


### 替换 itsdangerous 为 Flask-JWT-Extended

### INSTALLATION
* Python 3 is required. There are ways to send requests to server. 
* Postman, Insomnia, cURL, httpie and curl are simple and useful tools to send requests. 
* I mostly prefer httpie and curl. Their usage can be seen below.

Pull project and install requirements to virtual environment (*[https://pypi.org/project/virtualenv/]()*). Then run.
```
$ git clone https://github.com/melihcolpan/flask-restful-login
$ cd flask-restful-login
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python -m main
```

* For requests using httpie: *[https://httpie.io/]()*
* For requests using curl: *[https://curl.haxx.se/download.html]()*

> __Example user, admin and super admin users are created in database initializer class. You can use these users to login, logout and data handlers. For register handler, use new user information, otherwise returns already exist user.__


| Test Users        | Email Address           | Password  |
| ------------- |:-------------:| -----:|
| User      | test_email@example.com | test_password |
| Admin      | admin_email@example.com      |   admin_password |
| Super Admin | sa_email@example.com      |    sa_password |

#### Register:

* HTTPIE Request:
```sh
http POST :5000/v1/auth/register username=example_username password=example_password email=example@example.com
```
* Curl Request:
```sh
curl -H "Content-Type: application/json" --data '{"username":"example_name","password":"example_password", "email":"example@example.com"}' http://localhost:5000/v1/auth/register
```

#### Login:
* HTTPIE Request:
```sh
http POST :5000/v1/auth/login email=example@example.com password=example_password
```
* Curl Request:
```sh
curl -H "Content-Type: application/json" --data '{"email":"example@example.com", "password":"example_password"}' http://localhost:5000/v1/auth/login
```

> Response: Got access token and refresh token!


#### Logout:
* HTTPIE Request:
```sh
http POST :5000/v1/auth/logout Authorization:"Bearer ACCESS_TOKEN" refresh_token=REFRESH_TOKEN
```
* Curl Request:
```sh
curl -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN" --data '{"refresh_token":"REFRESH_TOKEN"}' http://localhost:5000/v1/auth/logout
```

#### Reset Password:
* HTTPIE Request:
```sh
http POST :5000/v1/auth/password_reset Authorization:"Bearer ACCESS_TOKEN" old_pass=<OLD-PASSWORD> new_pass=<NEW-PASSWORD>
```
* Curl Request:
```sh
curl -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN" --data '{"old_pass":"OLD-PASSWORD", "new_pass":"NEW-PASSWORD"}' http://localhost:5000/v1/auth/password_reset
```


>__There are some example routes in UserHandlers file. These handlers mostly return only text. To use them:__


#### Example routes that require authentication
Route addresses according to user privileges 
| User Type        | Route Address           |
| ------------- |:-------------:|
| User      | /data_user |
| Admin      | /data_admin      |
| Super Admin | /data_super_admin      |

* HTTPIE Request:
```sh
http GET :5000/<ROUTE-ADDRESS> Authorization:"Bearer ACCESS_TOKEN"
```
* Curl Request:
```sh
curl -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN" http://localhost:5000/<ROUTE-ADDRESS>
```

#### Super admin requiring authentication extra example handler, list users
This handler searches username, email or creation dates (range) in users table and returns information these users to super admin.
* HTTPIE Request:
```sh
http GET :5000/users Authorization:"Bearer ACCESS_TOKEN" usernames==test_username,admin_username emails==test_email@example.com,admin_email@example.com start_date==01.01.1990 end_date==01.01.2050
```
* Curl Request:
```sh
curl -X GET 'localhost:5000/users?usernames=test_username,admin_username&emails=test_email@example.com,admin_email@example.com&start_date=01.01.1990&end_date=01.01.2050' -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN" 
```

License
----

MIT


**Free Software, Hell Yeah!**