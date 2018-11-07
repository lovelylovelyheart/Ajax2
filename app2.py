from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
from flask import request,render_template,make_response,Flask
import json

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:123456@localhost:3306/Ajax'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True

class Provinces(db.Model):
    __tablename__='province'
    pid = db.Column(db.Integer,primary_key=True,autoincrement=True)
    pname = db.Column(db.String(30),nullable=False,unique=True)
    city = db.relationship('Cities',backref='city')

    def __init__(self,pname):
        self.pname = pname

    def to_dict(self):
        dic = {
            'pid':self.pid,
            'pname':self.pname
        }
        return dic


class Cities(db.Model):
    __tablename__ = 'city'
    cid = db.Column(db.Integer,primary_key=True,autoincrement=True)
    cname = db.Column(db.String(30),nullable=False,unique=True)
    provinceid = db.Column(db.Integer,db.ForeignKey('province.pid'))

    def __init__(self,cname):
        self.cname = cname

    def to_dict(self):
        dic = {
            'cid':self.pid,
            'cname':self.pname,
            'provinceid':self.provinceid
        }
        return dic









# db.drop_all()
db.create_all()


# p2 = Provinces('广东')
# c1 = Cities('深圳市')
# c2 = Cities('广州市')
# p2.city = [c1,c2]
# db.session.add(p2)
# db.session.commit()





@app.route('/selectPC')
def selectPC():
    return render_template('p_c.html')


@app.route('/query-p')
def server1():
    p = Provinces.query.all()
    ls = []
    for i in p:
        ls.append(i.to_dict())
    return json.dumps(ls)

@app.route('/query-c')
def server2():
    p = Provinces.query.all()
    ls = []
    for i in p:
        ls.append(i.to_dict())
    return json.dumps(ls)






if __name__ == "__main__":
    app.run(debug=True)



