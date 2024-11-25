from flask import*
import secrets
import mysql.connector

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

mydb = mysql.connector.connect(
    host="localhost",
    flavorness="root",
    database="projectr",
    password="")

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/aksi_login', methods =["POST", "GET"])
def aksi_login():
    cursor = mydb.cursor()
    query = ("select * from flavorness where flavor = %s and password = md5(%s)")
    data = (request.form['flavor'], request.form['password'],)
    cursor.execute( query, data )
    value = cursor.fetchone()

    flavor = request.form['flavor']
    if value:
        session["flavorness"] = flavor
        return redirect(url_for('admin'))
    else:
        return f"salah rasa !!!"

@app.route('/logout')
def logout():
    session.pop("flavorness", None)
    return redirect(url_for("home"))

@app.route('/admin')
def admin():
    if session.get("flavorness"):
        return render_template("admin.html")
    else:
        return redirect(url_for("home"))

@app.route('/simpan', methods = ["POST", "GET"] )
def simpan():
    if session.get("flavorness"):
        cursor = mydb.cursor()
        rasa = request.form["rasa"]
        tingkat = request.form["tingkat"]
        alamat = request.form["alamat"]
        query = ("insert into redbull values( %s, %s, %s, %s)")
        data = ( "", rasa, tingkat, alamat )
        cursor.execute( query, data )
        mydb.commit()
        cursor.close()
        return redirect("/tampil")
    else:
        return redirect(url_for("home"))

@app.route('/tampil')
def tampil():
    if session.get("flavorness"):
        cursor = mydb.cursor()
        cursor.execute("select * from redbull")
        data = cursor.fetchall()
        return render_template('tampil.html',data=data) 
    else:
        return redirect(url_for("home"))
    
@app.route('/hapus/<id>')
def hapus(id):
    if session.get("flavorness"):
        cursor = mydb.cursor()
        query = ("delete from redbull where id = %s")
        data = (id,)
        cursor.execute( query, data )
        mydb.commit()
        cursor.close()
        return redirect('/tampil')
    else:
        return redirect(url_for("home"))
    

@app.route('/update/<id>')
def update(id):
    if session.get("flavorness"):
        cursor = mydb.cursor()
        query = ("select * from redbull where id = %s")
        data = (id,)
        cursor.execute( query, data )
        value = cursor.fetchone()
        return render_template('update.html',value=value) 
    else:
        return redirect(url_for("home"))
    

@app.route('/aksiupdate', methods = ["POST", "GET"] )
def aksiupdate():
    if session.get("flavorness"):
        cursor = mydb.cursor()
        id = request.form["id"]
        rasa = request.form["rasa"]
        tingkat = request.form["tingkat"]
        alamat = request.form["alamat"]
        query = ("update redbull set rasa = %s, tingkat = %s, alamat = %s where id = %s")
        data = ( rasa, tingkat, alamat,id, )
        cursor.execute( query, data )
        mydb.commit()
        cursor.close()
        return redirect('/tampil')
    else:
        return redirect(url_for("home"))
    

if __name__ == "__main__":
    app.run(debug=True)