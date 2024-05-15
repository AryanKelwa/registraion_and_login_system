from flask import Flask,render_template,request,flash,redirect,session
from flask_sqlalchemy import SQLAlchemy
from os import path
import os

app=Flask(__name__)

############ database configuration #############
DB_NAME='mysql.db'
app.config['SECRET_KEY']=os.urandom(20)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # Corrected key name

db=SQLAlchemy(app)


########### home page #####################
@app.route('/home')
def home():
    users=User.query.all()
    if 'user_id' in session:        
        print("User id",session['user_id'])
        return render_template('home.htm',users=users)
    else:      
        return redirect('/')
    
    


#################  login    ####################
@app.route('/',methods=['GET',"POST"])
def login():
    
    if 'user_id' in session:
        print("user_id")
        return redirect('/home')
    
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        
        if not user:
            flash('user doesn\'t exists',category='error')
            print('user not found')
        else:
            if password == user.password:
                print("*************  login succesfull *****************")
                session['user_id']=user.id
                return redirect('/home')
            else:
                flash('wrong password',category='error')
                return redirect('/')
                
                
        
    return render_template('login.htm')




################# log out ##########################
@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')




################## register a new user ###########################

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        password=request.form.get('password')
        
        user=User.query.filter_by(email=email).first()
        
        if user:
            flash('email already exists',category='error')
            print('user already exists')
            return redirect('/register')
        else:
            user=User(name=name,email=email,password=password)
            db.session.add(user)
            db.session.commit()
            session['user_id']=user.id
            
        return redirect('/home')
    return render_template('register.htm')



##################### database #################
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(100),unique=True)
    password=db.Column(db.String(100),nullable=True)
    
def create_database(app):
    with app.app_context():
        if not path.exists('website/'+DB_NAME):
            db.create_all()




################### main function ########################3
if __name__ == '__main__':
    create_database(app)
    app.run(debug=True)