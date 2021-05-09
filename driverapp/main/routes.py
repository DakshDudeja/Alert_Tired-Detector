from flask import *
 
import cv2
import time
from keras.preprocessing import image
from keras.models import load_model

main = Blueprint('main',__name__)

@main.route('/')
def index():
    return render_template('index.html')

model = load_model('./Driver_Data.h5')

@main.route('/check')
def check():
    img_path = ("./photoup.jpg")
    img = image.load_img(img_path, target_size=(150, 150))
    x = image.img_to_array(img).astype("int32")
    x = x.reshape((1,) + x.shape)
    res=model.predict_classes(x)
    if res==0:
        res="<center> <h1>Alert</h1> </center>"
    elif res==1:
        res="<center> <h1>Non-Vigilant</h1> </center>"
    else:
        res="<center> <h1>Tired</h1> </center>"
    return res

@main.route('/click')
def click():
    time.sleep(2)
    cap=cv2.VideoCapture(0)
    result = True
    while result:
        ret,frame = cap.read()
        time.sleep(2)
        cv2.imwrite("./photo.jpg",frame)
        result = False
    cap.release()
    cv2.destroyAllWindows()
    img_path = ("./photo.jpg")
    img = image.load_img(img_path, target_size=(150, 150))
    x = image.img_to_array(img).astype("int32")
    x = x.reshape((1,) + x.shape)
    res=model.predict_classes(x)
    if res==0:
        res="<center> <h1>Alert</h1> </center>"
    elif res==1:
        res="<center> <h1>Non-Vigilant</h1> </center>"
    else:
        res="<center> <h1>Tired</h1> </center>"
    return res

@main.route('/upload')
def upload():
    return render_template('upload.html')

@main.route('/up', methods=['POST'])
def up():
    if request.method == "POST":
        if request.files:
            img = request.files["photo"]
            img.save("./photoup.jpg")
    return redirect(url_for('main.check'))
