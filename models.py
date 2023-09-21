from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypty = Bcrypt()

class surat_masuk(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    asal_surat = db.Column(db.String(25), nullable=False)
    no_surat = db.Column(db.String(25), nullable=False)
    kode_wilayah = db.Column(db.Integer, nullable=False)
    tanggal_surat = db.Column(db.Date, nullable=False)
    tanggal_diterima = db.Column(db.Date, nullable=False)
    perihal = db.Column(db.String(50), nullable=False)
    keterangan = db.Column(db.Enum('pelayanan publik','sub bagian perencanaan', 'bendahara', 'sub bagian ketertiban','sub bagian pemerintah'))
    file = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<surat_masuk {self.title}>"
    
    
class surat_keluar(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    no_surat = db.Column(db.String(25), nullable = False)
    tanggal_dibuat = db.Column(db.Date(), nullable=False)
    jenis_surat = db.Column(db.Enum('surat pernyataan', 'surat ahli waris', 'surat keterangan tidak mampu', 'surat keterangan pernikahan'))
    asal_instansi = db.Column(db.String(30), nullable=False)
    ditujukan = db.Column(db.String(100), nullable=False)
    perihal= db.Column(db.String(100), nullable=False)
    file =db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<surat_keluar>{self.title}"
    
class user(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False )
    username = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(25), nullable=False)
    jabatan = db.Column(db.String(25), nullable=False)
    foto = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<user>'.format(self.username)
    

        

 
