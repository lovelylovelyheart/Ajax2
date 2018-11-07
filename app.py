from flask import Flask,request,render_template,make_response
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
import json
import pickle


# json.dumps()
# json.loads()



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:123456@localhost:3306/Ajax"

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
db = SQLAlchemy(app)

class Admins(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    loginName = db.Column(db.String(30))
    upsd = db.Column(db.String(20))
    uname = db.Column(db.String(20))

    def to_dict(self):
        dic = {
            'id':self.id,
            'loginName':self.loginName,
            'upsd':self.upsd,
            'uname':self.uname
        }
        return dic




db.create_all()



@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/allusers',methods=['GET',"POST"])
def allUsers():
    if request.method == 'GET':
        if not request.args:
            return render_template('allusers.html')
        else:
            ls = list()
            users = Admins.query.all()
            for user in users:
                ls.append(user.to_dict())
            print(ls)
            return json.dumps(ls)
    else:
        id = request.form['uid']
        user = Admins.query.filter_by(id=id).first()
        try:
            db.session.delete(user)
            db.session.commit()
            dic = {
                'status':1,
                'msg':'删除成功'
            }
            return json.dumps(dic)
        except Exception as e:
            print(e)
            dic = {
                'status': 0,
                'msg': '删除失败,请联系管理员'
            }
            return json.dumps(dic)







if __name__ == '__main__':
    app.run()
