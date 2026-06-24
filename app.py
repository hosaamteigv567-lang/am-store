import os
import uuid
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# تحديد مكان مخزن الصور
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# التأكد التام أن مجلد الرفع موجود على الجهاز لعدم حدوث أخطاء
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 1. الصفحة الرئيسية للمتجر (تفتح صفحة fox store النظيفة)
@app.route('/')
def index():
    return render_template('index.html')

# 2. صفحة معرض الصور والمنتجات المنفصلة مع ميزة القفل السري
@app.route('/gallery')
def gallery():
    # التشييك الذكي على الكلمة السرية في الرابط
    admin_mode = request.args.get('secret') == 'marwan123'
    
    # قراءة كل الصور اللي اتسجلت جوه فولدر المخزن
    try:
        images = os.listdir(app.config['UPLOAD_FOLDER'])
    except Exception:
        images = []
        
    return render_template('gallery.html', images=images, admin_mode=admin_mode)

# 3. استقبال المنتجات المرفوعة وحفظها بأسماء مشفرة
@app.route('/upload', methods=['POST'])
def upload_images():
    uploaded_files = request.files.getlist('product_images[]')
    for file in uploaded_files:
        if file and file.filename != '':
            file_extension = os.path.splitext(file.filename)[1]
            random_name = uuid.uuid4().hex  
            new_filename = random_name + file_extension
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
            
    # بعد الرفع بنجاح، يرجعك تلقائي لصفحة معرض الصور
    return redirect(url_for('gallery'))

if __name__ == '__main__':
    app.run(debug=True)