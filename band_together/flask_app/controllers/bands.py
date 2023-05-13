from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.band import Band

# main dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("dashboard.html",user=User.get_by_id(data),bands=Band.get_all())

@app.route('/new/sighting')
def new():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('create_bands.html',user=User.get_by_id({"id":session['user_id']}))

@app.route('/create',methods=['POST'])
def create():
    if not Band.validate(request.form):
        return redirect('/new/sighting')  
    Band.save(request.form)
    return redirect('/dashboard')

@app.route('/edit/<id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/login')
    print(Band.select_one({"id": id}))
    return render_template('edit_Bands.html',user=User.get_by_id({"id":session['user_id']}),item=Band.select_one({"id": id}))

@app.route('/process',methods=['POST'])
def process_edit():
    if not Band.validate(request.form):
        return redirect(f'/update/{request.form["id"]}')  
        # return redirect('/new')  

    Band.update(request.form)
    return redirect('/dashboard')

@app.route('/mybands')
def mybands():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("view_bands.html",user=User.get_by_id(data),bands=Band.my_bands(data))

@app.route('/delete/<id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/login')
    Band.delete({"id": id})
    return redirect('/dashboard')

