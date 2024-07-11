import queue
from flask import Flask, render_template, request, Response, jsonify,flash,url_for,redirect
from flask_login import UserMixin, LoginManager, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
import threading
import librosa
import json
import time
import math
import torch
import os
import io
from .MER_model import RCNN,DynamicPCALayer
from flask_sqlalchemy import SQLAlchemy
from google.cloud import storage
db = SQLAlchemy()
def Processor_Creation():
    app = Flask(__name__)
    app.config['Password'] = 'UserPassword'
    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    #db storage for account data
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '19980706'
    db.init_app(app)

    #GCS
    bucket_name = 'music-visualisation-app'
    storage_client = storage.Client()
    try:
        bucket = storage_client.get_bucket(bucket_name)
        print(f"Bucket {bucket_name} exists.")
    except Exception as e:
        print(f"Bucket {bucket_name} does not exist. Creating new bucket.")
        bucket = storage_client.create_bucket(bucket_name)
        print(f"Bucket {bucket_name} created.")


    from .user_class import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


    long_term_store = []
    clients = []
    outputting = []
    processing_event = threading.Event()  # 创建一个事件对象
    simulator = threading.Event()
    stop_event = threading.Event()
    lock = threading.Lock()
    model = RCNN()
    model_path = 'Back_Stage/best_model.pth'
    pca_paths = ['Back_Stage/pca1.pkl', 'Back_Stage/pca2.pkl', 'Back_Stage/pca3.pkl']
    model.load_model(model_path, pca_paths)
    model.eval()

    @app.route('/')
    def index():
        return render_template('start.html')

    @app.route('/main')
    @login_required
    def main():
        return render_template('C_index.html', user=current_user)


    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/login', methods=['POST'])
    def login_post():
        USER_email = request.form['user_email']
        USER_password = request.form['user_password']
        # print(USER_email,USER_password)
        USER = User.query.filter_by(user_email=USER_email).first()

        if not USER or not check_password_hash(USER.user_password, USER_password):
            flash('Please check your e-mail address or password.')
            return redirect(url_for('login'))

        login_user(USER)
        return redirect(url_for('main'))

    @app.route('/signup')
    def signup():
        return render_template('signup.html')

    @app.route('/signup', methods=['POST'])
    def signup_post():
        USER_email = request.form.get('user_email')
        USER_password = request.form.get('user_password')
        USER_name = request.form.get('user_name')

        USER = User.query.filter_by(user_email=USER_email).first()

        if USER:
            flash('Email address already exists')
            return redirect(url_for('signup'))

        NEW_USER = User(user_email=USER_email, user_name=USER_name,
                        user_password=generate_password_hash(USER_password, method='pbkdf2:sha256'),
                        user_age=25,user_gender='X')

        # upload the new user information
        db.session.add(NEW_USER)
        db.session.commit()

        login_user(NEW_USER)
        return redirect(url_for('filling'))

    @app.route('/filling')
    @login_required
    def filling():
        return render_template('filling.html', user=current_user)

    @app.route('/filling', methods=['POST'])
    @login_required
    def filling_post():

        current_user.user_age = request.form.get('user_age')
        current_user.user_gender = request.form.get('user_gender')
        db.session.commit()
        return redirect(url_for('main'))

    def send_to_clients(data):
        dead_clients = []
        for client in clients:
            try:
                client.put(data)
            except Exception as e:  # 如果发送失败，假设客户端已断开
                dead_clients.append(client)
        for client in dead_clients:
            clients.remove(client)

    @app.route('/register_client')
    @login_required
    def register_client():
        def gen():
            q = queue.Queue()
            clients.append(q)
            P_time = 0
            try:
                while True:
                    try:
                        data = q.get(timeout=10)  # 设置超时以避免长时间阻塞
                        D_time = time.time() - P_time
                        if D_time < 0.1:
                            time.sleep(0.1-D_time)
                        yield data
                        P_time = time.time()
                    except queue.Empty:
                        # 如果超时没有数据，发送一个保持连接的心跳信号
                        # 注意: 心跳信号的内容需要符合客户端处理逻辑
                        yield 'data: {}\n\n'  # 发送空数据包来保持连接
            except GeneratorExit:
                # 当客户端断开连接时，清理操作
                clients.remove(q)

        return Response(gen(), mimetype='text/event-stream')

    def process_data(user_email):
        pitch_record = np.zeros(128)
        pitch_mag = np.zeros(128)
        pitch_id = np.zeros(128)
        time_record = 0.00001
        middle = [250, 250]
        X_recording = []
        Y_recording = []
        heart_beat = time.time()
        ID = 1
        a = 0
        pitch_active = np.zeros(128)
        note_pic = []
        angle = np.linspace(0, 2 * math.pi, 360)
        radius = np.linspace(0, 250, 128)

        while True:
            if stop_event.is_set():
                T = time.time()
                print(T)  # 确保这个打印语句可以执行
                print("Stop event is set. Performing cleanup and exiting.")

                X = torch.stack(X_recording, dim=0)
                Y = torch.stack(Y_recording, dim=0)
                blob_path_X = f"{user_email}/{T}/X.pt"
                blob_path_Y = f"{user_email}/{T}/Y.pt"
                X_steam = io.BytesIO()
                Y_steam = io.BytesIO()
                torch.save(X, X_steam)
                X_steam.seek(0)
                torch.save(Y, Y_steam)
                Y_steam.seek(0)
                blob_X = bucket.blob(blob_path_X)
                blob_Y = bucket.blob(blob_path_Y)
                blob_X.upload_from_file(X_steam)
                blob_Y.upload_from_file(Y_steam)
                print("uploaded")  # 确保这个打印语句可以执行

                stop_event.clear()
                processing_event.clear()
                return {"status": "Stopped"}, 200

            with lock:
                l = len(long_term_store)
                print("working", l)
                print(f"Stop event status inside lock: {stop_event.is_set()}")

            if l >= 220500:
                heart_beat = time.time()
                with lock:
                    short_term_store = long_term_store[:220500]
                    del long_term_store[:220500]
                    print("cut", len(long_term_store))
                    print(f"Stop event status after cutting: {stop_event.is_set()}")

                pitches, magnitudes = librosa.piptrack(y=np.array(short_term_store), sr=44100, hop_length=441,
                                                       threshold=0.1)
                pitch_times = librosa.times_like(pitches, sr=44100, hop_length=441)

                S = librosa.feature.melspectrogram(y=np.array(short_term_store), sr=44100, n_mels=24, hop_length=441)
                S_dB = librosa.power_to_db(S, ref=np.max)
                zcr = librosa.feature.zero_crossing_rate(np.array(short_term_store), hop_length=441)
                mfccs = librosa.feature.mfcc(y=np.array(short_term_store), sr=44100, n_mfcc=24, hop_length=441)
                F = np.vstack((S_dB, zcr, mfccs))
                F = [F]
                F = torch.tensor(np.stack(F, axis=0))
                F = F.reshape(1, F.shape[0], F.shape[1], F.shape[2])
                F = [F[:, :, :, i * 50:i * 50 + 50] for i in range(10)]
                F = torch.tensor(np.stack(F, axis=2))
                X_recording.append(F)
                Y = model(F.float())[0, :, :]
                Y_recording.append(Y)
                print(Y)

                Yc = Y[0, :]

                for j in range(pitches.shape[1]):
                    start_time = time.time()
                    current_time = pitch_times[j] + time_record

                    for i in range(pitches.shape[0]):
                        if stop_event.is_set():
                            print("Stop event is set during pitch processing. Performing cleanup and exiting.")
                            T = time.time()
                            print(T)  # 确保这个打印语句可以执行

                            X = torch.stack(X_recording, dim=0)
                            Y = torch.stack(Y_recording, dim=0)
                            blob_path_X = f"{user_email}/{T}/X.pt"
                            blob_path_Y = f"{user_email}/{T}/Y.pt"
                            X_steam = io.BytesIO()
                            Y_steam = io.BytesIO()
                            torch.save(X, X_steam)
                            X_steam.seek(0)
                            torch.save(Y, Y_steam)
                            Y_steam.seek(0)
                            blob_X = bucket.blob(blob_path_X)
                            blob_Y = bucket.blob(blob_path_Y)
                            blob_X.upload_from_file(X_steam)
                            blob_Y.upload_from_file(Y_steam)
                            print("uploaded")  # 确保这个打印语句可以执行

                            stop_event.clear()
                            processing_event.clear()
                            return {"status": "Stopped"}, 200

                        if magnitudes[i, j] > 0:
                            midi_note = int(librosa.hz_to_midi(pitches[i, j]))
                            pitch_active[midi_note] = 1
                            if pitch_mag[midi_note] < magnitudes[i, j]:
                                pitch_mag[midi_note] = magnitudes[i, j]

                    # 更新所有音符圆的信息
                    if j % (pitches.shape[1] // 100) == 0:  # per 0.1s
                        for p in range(128):
                            if pitch_active[p] == 0 and pitch_record[p] != 0:  # 需要消除的圆（已结束的音）
                                note_pic = [item for item in note_pic if item["id"] != pitch_id[p]]
                                pitch_id[p] = 0
                                pitch_record[p] = 0

                        for element in note_pic:
                            element["size"] += 1
                            element["opacity"] -= 0.05
                            if element["opacity"] < 0:
                                element["opacity"] = 0
                        for p in range(128):
                            if pitch_active[p] != 0 and pitch_record[p] == 0 and current_time - pitch_record[p] > 0.05:
                                # 新产生的圆（新出现的音）
                                if a < 360:
                                    angle_N = angle[a]
                                    a += 1
                                else:
                                    a -= 360
                                    angle_N = angle[a]
                                    a += 1
                                radius_N = radius[p]
                                x = middle[0] + radius_N * math.cos(angle_N)
                                y = middle[1] + radius_N * math.sin(angle_N)
                                s = 0
                                if (Yc[0] < 0) & (Yc[1] < 0):  # sad
                                    s = 0
                                elif (Yc[0] < 0) & (Yc[1] > 0):  # relaxed
                                    s = 1
                                elif (Yc[0] > 0) & (Yc[1] < 0):  # tense
                                    s = 2
                                elif (Yc[0] > 0) & (Yc[1] > 0):  # excited
                                    s = 3
                                Emotion = "sad" if s == 0 else "relaxed" if s == 1 else "tense" if s == 2 else "excited"

                                Hue_Base = [0, 90, 180, 270]
                                Saturation_Base = [45, 50, 55, 60]
                                Lightness_Base = [45, 50, 55, 60]

                                Base = [Hue_Base[s], Saturation_Base[s], Lightness_Base[s]]

                                Control_Range = [10, 30, 30]

                                Coff = [0.9, 0.9, 0.9]

                                Hue = min(360, Base[0] + int((p % 16) * Control_Range[0]) * Coff[0])
                                Saturation = (Base[1] + (min(pitch_mag[p], 50) / 50) * Control_Range[1]) * Coff[1]
                                Lightness = (Base[2] + (min(pitch_mag[p], 50) / 50) * Control_Range[2]) * Coff[2]
                                color = (
                                    f"hsl({Hue},"
                                    f"{Saturation}%,"
                                    f"{Lightness}%)")
                                size = min(pitch_mag[p] / 100, 20)  # 初始圆的尺寸
                                note_pic.append({
                                    "id": ID,
                                    "pitch": p,
                                    "x": x,
                                    "y": y,
                                    "size": size,
                                    "color": color,
                                    "opacity": 1,
                                    "emotion": Emotion,
                                    "arousal": Yc[0].float().item(),
                                    "valence": Yc[1].float().item()
                                })
                                pitch_id[p] = ID
                                pitch_record[p] = current_time
                                ID += 1

                        json_data = json.dumps(note_pic)
                        send_to_clients(f"data: {json_data}\n\n")
                        pitch_active = np.zeros(128)
                        pitch_mag = np.zeros(128)
                        d_time = time.time() - start_time
                        if d_time < 0.1:
                            time.sleep(0.1 - d_time)
                time_record += pitch_times[-1]
            else:
                time.sleep(0.5)  # 等待更多数据到达
                T = time.time()
                print(T)
                print(f"Stop event status in else: {stop_event.is_set()}")
                if T - heart_beat > 20:
                    X = torch.stack(X_recording, dim=0)
                    Y = torch.stack(Y_recording, dim=0)
                    blob_path_X = f"{user_email}/{T}/X.pt"
                    blob_path_Y = f"{user_email}/{T}/Y.pt"
                    X_steam = io.BytesIO()
                    Y_steam = io.BytesIO()
                    torch.save(X, X_steam)
                    X_steam.seek(0)
                    torch.save(Y, Y_steam)
                    Y_steam.seek(0)
                    blob_X = bucket.blob(blob_path_X)
                    blob_Y = bucket.blob(blob_path_Y)
                    blob_X.upload_from_file(X_steam)
                    blob_Y.upload_from_file(Y_steam)
                    print("uploaded")
                    return {"status": "Stopped"}, 200



    def Simulator():
        ssr = 44100

        for t in range(len(audio) // ssr):  # 检查 notes_midi 是否为空
            if stop_event.is_set():
                stop_event.clear()
                simulator.clear()
                return {"status": "Stopped"}, 200
            start_time = time.time()
            data = audio[t * ssr:t * ssr + ssr].tolist()
            with lock:
                long_term_store.extend(data)
            D_time = time.time() - start_time
            if D_time < 1:
                time.sleep(1 - D_time)

    @app.route('/start', methods=['GET', 'POST'])
    @login_required
    def send_Msg():
        if request.method == 'POST':
            if not processing_event.is_set():
                processing_event.set()  # 标记处理事件为已设置
                user_email = current_user.user_email
                threading.Thread(target=process_data,args=(user_email,)).start()
            if not simulator.is_set():
                simulator.set()
                threading.Thread(target=Simulator).start()
            print("Started")

            return render_template('C_index.html', user=current_user)

    @app.route('/stop',methods =['POST'])
    @login_required
    def stop():
        long_term_store.clear()
        stop_event.set()
        processing_event.set()
        print("Stop event set")  # 添加打印以确认事件被设置
        return render_template('C_index.html', user=current_user)

    @app.route('/upload', methods=['POST'])
    @login_required
    def upload_file():
        global audio, sr, file_path
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            filename =file.filename
            #file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            #file.save(file_path)
            file_content=file.read()
            audio, sr = librosa.load(io.BytesIO(file_content), sr=44100)
            print(audio.shape)
            flash('File successfully uploaded')

            return render_template('C_index.html', user=current_user)


    return app
