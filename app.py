from flask import Flask, request, jsonify, make_response
import pymysql

# Membuat server flask
app = Flask(__name__)

mydb = pymysql.connect(
    host="localhost",
    user="root",
    passwd="",
    database="gudang3"
)

@app.route('/')
@app.route('/index')
def index():
    return "<h1>KELAS PRAK CLOUD COMP</h1>"
    
@app.route('/get_data_toko', methods=['GET'])
def get_data_toko():
    query = "SELECT * FROM toko WHERE 1=1"
    values = ()
    
    id_toko = request.args.get("id_toko")
    nama_toko = request.args.get("nama_toko")
    jumlah_cabang = request.args.get("jumlah_cabang")


    if id_toko:
        query += " AND id_toko=%s "
        values += (id_toko,)
        
    if nama_toko:
        query += " AND nama_toko LIKE %s "
        values += ("%"+nama_toko+"%", )
    
    if jumlah_cabang:
        query += " AND jumlah_cabang=%s "
        values += (jumlah_cabang,)
        
    mycursor = mydb.cursor()
    mycursor.execute(query, values)
    data = mycursor.fetchall()

    row_headers = [x[0] for x in mycursor.description]
    json_data = []
    for result in data:
        json_data.append(dict(zip(row_headers, result)))

    return make_response(jsonify(json_data),200)

@app.route('/insert_data_toko', methods=['POST'])
def insert_data_toko():
    hasil = {"status": "gagal insert data toko"}

    try:
        data = request.json

        id_toko = data["id_toko"]
        nama_toko = data["nama_toko"]
        deskripsi_toko = data["deskripsi_toko"]
        alamat_toko = data["alamat_toko"]
        jumlah_cabang = data["jumlah_cabang"]
        nama_pemilik = data["nama_pemilik"]


        query = "INSERT INTO toko(id_toko, nama_toko, deskripsi_toko, alamat_toko, jumlah_cabang, nama_pemilik) VALUES(%s,%s,%s,%s,%s,%s)"
        values = (id_toko, nama_toko, deskripsi_toko, alamat_toko, jumlah_cabang, nama_pemilik, )

        mycursor = mydb.cursor()
        mycursor.execute(query, values)
        mydb.commit()
        hasil = {"status": "berhasil insert data toko"}
    except Exception as e:
        print("Error: " + str(e))

    return jsonify(hasil)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)
