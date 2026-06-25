import os
import uuid
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# تأمين مسار المجلد بشكل صحيح
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# إنشاء المجلد تلقائياً لو مش موجود عشان نمنع أي تعليق
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ADMIN_PASSWORD = "Marwan_Secret_2026"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gallery')
def gallery():
    try:
        images = os.listdir(app.config['UPLOAD_FOLDER'])
    except Exception:
        images = []
    return render_template('gallery.html', images=images)

@app.route('/upload', methods=['POST'])
def upload_images():
    password = request.form.get('password')
    
    if password != ADMIN_PASSWORD:
        return "❌ خطأ: الباسورد غلط.", 403

    uploaded_files = request.files.getlist('product_images[]')
    
    for file in uploaded_files:
        if file and file.filename != '':
            file_extension = os.path.splitext(file.filename)[1]
            random_name = uuid.uuid4().hex
            new_filename = random_name + file_extension
            
            # حفظ الصورة بالمسار الجديد المضمون
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
            
    # إعادة توجيه لصفحة المعرض عشان الصور تظهر فوراً
    return redirect(url_for('gallery'))

if __name__ == '__main__':
    # تشغيل السيرفر بدون ما يعلق في الخلفية
    app.run(debug=True, use_reloader=False)