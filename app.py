from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response, Response, send_file
from flask_sqlalchemy import SQLAlchemy, query
from sqlalchemy import text
from datetime import datetime, timedelta
from models import db, surat_masuk, surat_keluar, user
from werkzeug.security import check_password_hash, generate_password_hash
from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(
    user='root1', password='123', server='localhost', database='db_arsip')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'odeopideiffff'

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
global COOKIE_TIME_OUT
COOKIE_TIME_OUT = 60*5

db.init_app(app)


@app.route('/')
def home():
    if 'email' in session:
        username_session = session['email']
        user_rs = user.query.filter_by(email=username_session).first()
        return render_template('index.html')
    else:
        return redirect('/login')


@app.route('/surat_masuk')
def sm():
    datas = surat_masuk.query.all()
    return render_template('surat_masuk.html', datas=datas)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        flash("Data berhasil ditambahkan")
        asal_surat = request.form['asal_surat']
        no_surat = request.form['no_surat']
        kode_wilayah = request.form['kode_wilayah']
        tanggal_surat = request.form['tanggal_surat']
        tanggal_diterima = request.form['tanggal_diterima']
        perihal = request.form['perihal']
        keterangan = request.form['keterangan']
        file = request.form['file']

        data_baru = surat_masuk(asal_surat=asal_surat, no_surat=no_surat, kode_wilayah=kode_wilayah, tanggal_surat=tanggal_surat,
                                tanggal_diterima=tanggal_diterima, perihal=perihal, keterangan=keterangan, file=file)

        db.session.add(data_baru)
        db.session.commit()
        return redirect(url_for('sm'))

    return render_template('surat_masuk.html')


@app.route('/edit/<int:data_id>', methods=['GET', 'POST'])
def edit(data_id):
    data = surat_masuk.query.get(data_id)

    if request.method == 'POST':
        data.asal_surat = request.form['asal_surat']
        data.no_surat = request.form['no_surat']
        data.kode_wilayah = request.form['kode_wilayah']
        data.tanggal_surat = request.form['tanggal_surat']
        data.tanggal_diterima = request.form['tanggal_diterima']
        data.perihal = request.form['perihal']
        data.keterangan = request.form['keterangan']
        data.file = request.form['file']

        db.session.commit()
        flash("Data berhasil diedit")
        return redirect(url_for('sm'))
    else:
        print("error")
    return render_template('edit.html', data=data)


@app.route('/delete/<int:data_id>', methods=['GET', 'POST'])
def delete(data_id):
    delete_data = surat_masuk.query.get(data_id)
    if delete_data:
        data = surat_masuk.query.get_or_404(data_id)

        db.session.delete(data)
        db.session.commit()

        total_data = surat_masuk.query.count()

        sql_statement = text(
            f"ALTER TABLE surat_masuk AUTO_INCREMENT = {total_data + 1}; ")
        db.session.execute(sql_statement)
        db.session.commit()
        flash("Data berhasil di hapus")
    return redirect(url_for('sm'))


@app.route('/surat_keluar')
def sk():
    listSk = surat_keluar.query.all()
    return render_template('surat_keluar.html', listSk=listSk)


@app.route('/addsk', methods=['GET', 'POST'])
def add_sk():
    if request.method == 'POST':
        no_surat = request.form['no_surat']
        tanggal_dibuat = request.form['tanggal_dibuat']
        jenis_surat = request.form['jenis_surat']
        asal_instansi = request.form['asal_instansi']
        ditujukan = request.form['ditujukan']
        perihal = request.form['perihal']
        file = request.form['file']

        listBaru = surat_keluar(no_surat=no_surat, tanggal_dibuat=tanggal_dibuat, jenis_surat=jenis_surat,
                                asal_instansi=asal_instansi, ditujukan=ditujukan, perihal=perihal, file=file)

        db.session.add(listBaru)
        db.session.commit()
        return redirect(url_for('sk'))
    return render_template('')


@app.route('/edit_sk/<int:id>', methods=['GET', 'POST'])
def edit_sk(id):
    list = surat_keluar.query.get(id)

    if request.method == 'POST':
        list.no_surat = request.form['no_surat']
        list.tanggal_dibuat = request.form['tanggal_dibuat']
        list.jenis_surat = request.form['jenis_surat']
        list.asal_instansi = request.form['asal_instansi']
        list.ditujukan = request.form['ditujukan']
        list.perihal = request.form['perihal']
        list.file = request.form['file']

        db.session.commit()
        return redirect(url_for('sk'))
    else:
        print('error')
    return render_template('edit_sk.html', list=list)


@app.route('/delete_sk/<int:id>', methods=['GET', 'POST'])
def delete_sk(id):
    delete_data = surat_keluar.query.get(id)
    if delete_data:
        data = surat_keluar.query.get_or_404(id)

        db.session.delete(data)
        db.session.commit()

        total_data = surat_keluar.query.count()

        sql_statement = text(
            f"ALTER TABLE surat_keluar AUTO_INCREMENT = {total_data + 1}; ")
        db.session.execute(sql_statement)
        db.session.commit()
        flash("Data berhasil di hapus")
    return redirect(url_for('sk'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')


@app.route('/submit', methods=['POST', 'GET'])
def login_submit():
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    _remember = request.form.getlist('inputRemember')

    if 'email' in request.cookies:
        username = request.cookies.get('email')
        password = request.cookies.get('pwd')
        row = user.query.filter_by(email=username).first()
        if row and check_password_hash(row.password_hash, password):
            session['email'] = row.email
            return redirect('/')
        else:
            return redirect('/login')
    elif _email and _password:
        row = user.query.filter_by(email=_email).first()
        if row:
            if check_password_hash(row.password, _password):
                session['email'] = row.email
                if _remember:
                    resp = make_response(redirect('/'))
                    resp.set_cookie('email', _email, max_age=COOKIE_TIME_OUT)
                    resp.set_cookie('pwd', _password, max_age=COOKIE_TIME_OUT)
                    resp.set_cookie('rem', 'checked', max_age=COOKIE_TIME_OUT)
                    return resp
                return redirect('/')
            else:
                flash('password anda salah')
                return redirect('/login')
        else:
            flash('username atau password anda salah')
            return redirect('/login')
    else:
        flash('username atau password anda salah')
        return redirect('/login')


@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email', None)
    return redirect('/login')


@app.route('/profil')
def profile():
    User = user.query.all()
    return render_template('profile.html', User=User)


@app.route('/edit3/<int:id>', methods=['POST', 'GET'])
def edit3(id):
    ul = user.query.get(id)

    if request.method == 'POST':
        ul.foto = request.form['foto']
        ul.username = request.form['username']
        ul.password = request.form['password']
        ul.email = request.form['email']
        ul.jabatan = request.form['jabatan']

        db.session.commit()
        return redirect(url_for('profile'))
    else:
        print('error')
    return render_template('edit_profil.html', ul=ul)


@app.route('/download/<int:id>', methods=['POST', 'GET'])
def download(id):
    file = surat_masuk.query.get(id)
    if file:
        response = Response(file.file, content_type='application/pdf')
        response.headers['Content-Disposition'] = f'inline; filename={file.file}.pdf'
        return response
    else:
        return 'Data tidak ditemukan', 404
    
@app.route('/download1/<int:id>', methods=['POST', 'GET'])
def download1(id):
    file = surat_keluar.query.get(id)
    if file:
        response = Response(file.file, content_type='application/pdf')
        response.headers['Content-Disposition'] = f'inline; filename={file.file}.pdf'
        return response
    else:
        return 'Data tidak ditemukan', 404


@app.route('/generate_pdf', methods=['POST', 'GET'])
def generate_pdf():
    data = surat_masuk.query.all()

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    

    elements = []
   
    table_data = [['NO', 'Asal Surat', 'No Surat', 'Kode Wolayah', 'Tanggal Surat',
                   'Tanggal Diterima', 'Perihal', 'Keterangan']]  # Ganti dengan header kolom yang sesuai
    for item in data:
        table_data.append([item.id, item.asal_surat, item.no_surat, item.kode_wilayah, item.tanggal_surat,
                          item.tanggal_diterima, item.perihal, item.keterangan])  # Ganti dengan nama kolom yang sesuai
        
    

    table = Table(table_data)
    table.setStyle(TableStyle([
        # Warna latar belakang header
        ('BACKGROUND', (0, 0), (-1, 0), (0.7, 0.7, 0.7)),
        ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),  # Warna teks header
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Pusatkan teks dalam sel
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Font teks header
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Jarak antara header dan isi
        # Warna latar belakang isi tabel
        ('BACKGROUND', (0, 1), (-1, -1), (0.9, 0.9, 0.9)),
        # Tambahkan garis pada sel tabel
        ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),  # Jarak sisi kiri sel
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements = [table]

    # Membuat dokumen PDF
    doc.build(elements)

    # Reset posisi buffer ke awal
    buffer.seek(0)

    # Kirimkan respons HTTP dengan tipe konten PDF
    return Response(buffer.read(), mimetype='application/pdf', headers={'Content-Disposition': 'inline; filename=export.pdf'})

@app.route('/generate_pdf1', methods=['POST', 'GET'])
def generate_pdf1():
    data = surat_keluar.query.all()

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    

    elements = []
   
    table_data = [['No', 'No. Surat', 'Tanggal dibuat', 'Jenis surat', 'Asal instansi',
                   'Bagian', 'Perihal', 'file']]  # Ganti dengan header kolom yang sesuai
    for item in data:
        table_data.append([item.id, item.no_surat, item.tanggal_dibuat, item.jenis_surat, item.asal_instansi,
                          item.ditujukan, item.perihal, item.file])  # Ganti dengan nama kolom yang sesuai
        
    

    table = Table(table_data)
    table.setStyle(TableStyle([
        # Warna latar belakang header
        ('BACKGROUND', (0, 0), (-1, 0), (0.7, 0.7, 0.7)),
        ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),  # Warna teks header
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Pusatkan teks dalam sel
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Font teks header
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Jarak antara header dan isi
        # Warna latar belakang isi tabel
        ('BACKGROUND', (0, 1), (-1, -1), (0.9, 0.9, 0.9)),
        # Tambahkan garis pada sel tabel
        ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),  # Jarak sisi kiri sel
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements = [table]

    # Membuat dokumen PDF
    doc.build(elements)

    # Reset posisi buffer ke awal
    buffer.seek(0)

    # Kirimkan respons HTTP dengan tipe konten PDF
    return Response(buffer.read(), mimetype='application/pdf', headers={'Content-Disposition': 'inline; filename=export.pdf'})

if __name__ == '__main__':
    app.run(debug=True, port=3040)
