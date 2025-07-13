# import all libraires
from io import BytesIO
from flask import Flask, render_template, request, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# Initialize flask and create sqlite database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:yanivc77@localhost/alchemy"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# with app.app_context():
#     result = result = db.session.execute(text('SELECT VERSION()')).fetchone()
#     db_version = result[0]

# create datatable
class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary(length=(2**32)-1)) # MEDIUMBLOB up to 16M


# Create index function for upload and return files
@app.route("/upload", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        upload = Upload(filename=file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit()
        return jsonify({"Uploaded": file.filename, "file_id": upload.id}), 200
    return "file not uploaded only post method", 401


# create download function for download files
@app.route("/download/<upload_id>")
def download(upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()
    return send_file(
        BytesIO(upload.data), download_name=upload.filename, as_attachment=True
    )


if __name__ == "__main__":
    # with app.app_context():
    #     # Create the tables
    #     db.create_all()

    app.run(debug=True, port=5000)
