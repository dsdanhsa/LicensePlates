import base64
import glob
import hashlib
import json
import os
import calendar
from random import random
from datetime import date
import datetime as dt #import date and time
import time
import cv2
import pytesseract as pytesseract
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.datetime_safe import date
from django.views import View
import pymysql
from cryptography.fernet import Fernet
from django.shortcuts import HttpResponse

conn = pymysql.connect(host='localhost', user='root', password='', db='nhandienbiensoxe')
a = conn.cursor()

# Create your views here.

class Login(View):
    def get(self, request):
        request.session['username'] = ''
        request.session['password'] = ''
        return render(request, "public/login.html")
    def post(self, request):
        username = request.POST['taikhoan']
        password = request.POST['matkhau']
        sql = '' \
              'SELECT * FROM ' \
              'tbl_taikhoan INNER JOIN tbl_quyen ' \
              'ON tbl_quyen.iMa_Quyen = tbl_taikhoan.maquyen INNER JOIN tbl_nhanvien ON tbl_nhanvien.manv = tbl_taikhoan.FK_manv' \
              ' WHERE taikhoan = "' + str(username) + '" AND matkhau = "' + str(password) + '"'
        a.execute(sql)
        data = a.fetchone()
        if data != None:
            request.session['username'] = username
            request.session['password'] = password
            request.session['user'] = data[6]
            return HttpResponseRedirect("/Trangchu/")
        else:
            return HttpResponseRedirect("/")


class WelcomeClass(View):
    def get(self, request):
        if request.session['username'] != "":
            return render(request, "public/index.html")
        else:
            return HttpResponseRedirect("/")

class DetectCamera(View):
    def get(self, request):
        # conn = pymysql.connect(host='localhost', user='root', password='', db='dkxt')
        # a = conn.cursor()
        # sql = "SELECT * FROM tbl_sinhvien"
        # #Thực thi câu lệnh truy vấn (Execute Query).
        # a.execute(sql)
        # data = a.fetchall()
        # return HttpResponse(data)
         return render(request, "public/DetectCamera.html")

class chonbienso(View):
    def get(self, request):
        return render(request, "public/chonbienso.html")

def postFriend(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
        today = date.today()
        # dd/mm/YY
        d1 = today.strftime("%Y-%m-%d %H:%M:%S")

        #request_getdata = json.loads(request.POST.get('link_anh', None))
        #save_file(request_getdata)

        # return JsonResponse({"thongbao": "thanhcong", 'data' : request_getdata})
        #
        #return  HttpResponse(text)
        sql = "SELECT id_user, tenbien, thoigian_guixe, thoigian_nhanxe FROM tbl_user"
        #Thực thi câu lệnh truy vấn (Execute Query).
        a.execute(sql)
        records = a.fetchall()
        return JsonResponse({"thongbao": "thanhcong", 'data': records})

        id = ""
        # for row in request_getdata:
        #    id += random_id(15, "AWLCSLZOW120213", row['link_anh'])
        #    insert = "INSERT INTO `tbl_hinhanh` VALUES ("+id+",'" + row['link_anh']+ "',"+ str(count) +")"
        #     # a.execute(insert)
        #     # a.commit()
        # dulieu = JsonResponse({"data": request_getdata, 'thongbao' : 'thanhcong'})


    return JsonResponse({"thongbao": "thatbai", 'data' : ''})

def random_id(length, string, alpha):
    id = ''
    for i in range(0, length, 2):
        id += random.choice(string)
        id += random.choice(alpha)
    return id

def save_file(request_getdata):
    for row in request_getdata:
        imgdata = base64.b64decode(str(row['link_anh']))
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d_%m_%Y")
        path = 'static/public/img/'+dt_string+'_User_1'

        filename = path + "/" + str(row['id']+1 ) + '.jpg'
        if not os.path.exists(path):
            id_user = dt_string + '_User_1'
            insert = "INSERT INTO `tbl_user`(`id_user`,`biensoxe`) VALUES('"+str(id_user)+"','"+ str(id_user)+"')"
            a.execute(insert)
            conn.commit()
            os.mkdir(path)
        else:
            newest = max(glob.iglob('static/public/img/' + now.strftime("%d_%m_%Y") + '_User_*'),key=os.path.getctime)

            if(newest.replace("\\", "/") == path and len(glob.glob(newest.replace("\\", "/")+"/*.jpg")) < 6):
                filename = path + "/" + str(row['id'] + 1) + '.jpg'
            else:
                if(len(glob.glob(newest.replace("\\", "/")+"/*.jpg")) >= 6):
                    i = str(int(newest.replace("\\", "/").split("_")[4]) + 1)
                    path = 'static/public/img/' + dt_string + '_User_'+ i
                    os.mkdir(path)
                    filename = path + "/" + str(row['id'] + 1) + '.jpg'
                    id_user = newest.replace("\\", "/").split("/")[3]
                    insert = "INSERT INTO `tbl_user`(`id_user`,`biensoxe`) VALUES('" + str(id_user) + "','" + str(
                        id_user) + "')"
                    a.execute(insert)
                    conn.commit()
                else:
                    path = newest.replace("\\", "/")
                    filename = path + "/" + str(row['id'] + 1) + '.jpg'


        # if os.path.exists(filename):
        #     os.remove(filename)

        with open(filename, 'wb') as f:
            f.write(imgdata)
            text = detext(f.name)
            return HttpResponse(text)
            # id += random_id(15, "AWLCSLZOW120213", row['link_anh'])
            # insert = "INSERT INTO `tbl_hinhanh` VALUES ("+id+",'" + row['link_anh']+ "',"+ str(count) +")"
            # a.execute(insert)
            # a.commit()
            f.close()


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def ajax_test(request):
    if is_ajax(request=request):
        message = "This is ajax"
    else:
        message = "Not ajax"
    return HttpResponse(message)

def nhandienHinhAnh(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
        request_getdata = json.loads(request.POST.get('link_anh', None))
        imgdata = base64.b64decode(request_getdata)
        path = 'static/public/img/HinhAnhNhanDien'
        filename = path + "/HinhAnhNhanDien.jpg"
        if not os.path.exists(path):
            os.mkdir(path)
        with open(filename, 'wb') as f:
            f.write(imgdata)
            f.close()

        bienso = detext(filename)
        return JsonResponse({"thongbao": "thanhcong", 'data': bienso})

def detext(anh):
    ## LOAD THU VIEN VA MODUL CAN THIET


    # ----------------------DOC HINH ANH - TACH HINH ANH NHAN DIEN--------------------
    img = cv2.imread(anh)
    #cv2.imshow('HINH ANH GOC', img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    contours, h = cv2.findContours(thresh, 1, 2)
    largest_rectangle = [0, 0]
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4:
            area = cv2.contourArea(cnt)
            if area > largest_rectangle[0]:
                largest_rectangle = [cv2.contourArea(cnt), cnt, approx]
    x, y, w, h = cv2.boundingRect(largest_rectangle[1])

    image = img[y:y + h, x:x + w]
    cv2.drawContours(img, [largest_rectangle[1]], 0, (0, 255, 0), 8)

    cropped = img[y:y + h, x:x + w]
    #cv2.imshow('DANH DAU DOI TUONG', img)

    cv2.drawContours(img, [largest_rectangle[1]], 0, (255, 255, 255), 18)

    # --------------------- DOC HINH ANH CHUYEN THANH FILE TEXT-----------------------------
    pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    #cv2.imshow('CROP', thresh)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening

    configr = ('-l eng --oem 1 --psm 6-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghjklmnopqrstuvwxyz0123456789')
    data = pytesseract.image_to_string(invert, lang='eng', config=configr)
    return data

class TaiKhoan(View):
    def get(self, request):
        sql = "SELECT * FROM tbl_nhanvien " \
              "INNER JOIN tbl_taikhoan ON tbl_taikhoan.FK_manv = tbl_nhanvien.manv " \
              "INNER JOIN tbl_quyen ON tbl_quyen.iMa_Quyen = tbl_taikhoan.maquyen" \

        #Thực thi câu lệnh truy vấn (Execute Query).
        a.execute(sql)
        data = a.fetchall()
        a.execute("SELECT * FROM tbl_nhanvien")
        listnv = a.fetchall()
        arr = {'nhanvien' : data, 'list_nv':listnv}
        return render(request, "public/taikhoan.html", arr)
    def post(self, request):
        if request.POST['themtaikhoan'] :
            manv = request.POST['nhanvien']
            taikhoan = request.POST['taikhoan']
            matkhau = request.POST['matkhau']
            quyen = request.POST['quyen']
            sql = "INSERT INTO tbl_taikhoan(taikhoan, maquyen, matkhau, FK_manv) " \
                  "VALUES ('"+taikhoan+"',"+quyen+",'"+matkhau+"',"+manv+")"
            a.execute(sql)
            conn.commit()

        if request.POST['themnhanvien'] == 'themnhanvien':
            tennv = request.POST['tennhanvien']
            ngaysinh = request.POST['ngaysinh']
            gioitinh = request.POST['gioitinh']
            diachi = request.POST['diachi']
            sodienthoai = request.POST['sodienthoai']
            sql = "INSERT INTO tbl_nhanvien(tennv, ngaysinh, gioitinh, diachi, sodienthoai) " \
                  "VALUES ('" + tennv + "','" + ngaysinh + "','" + gioitinh + "','"+diachi+"','"+sodienthoai+"')"
            a.execute(sql)
            conn.commit()
            return HttpResponseRedirect("/Taikhoan/")
        pass

#Quản lý giá xe

class GiaXe(View):
    def get(self, request):
        sql = "SELECT * FROM tbl_time  ORDER BY id_time DESC"
        a.execute(sql)
        tbl_time = a.fetchall()

        sql = "SELECT * FROM tbl_loaixe ORDER BY ma_loai DESC"
        a.execute(sql)
        tbl_loaixe = a.fetchall()

        sql = "SELECT tbl_loaixe.loai, tbl_time.name_time, tbl_giaxe.giatien, tbl_giaxe.loai_ve, tbl_time.time_bd, tbl_time.time_kt " \
              "FROM tbl_giaxe " \
              "INNER JOIN tbl_time ON tbl_time.id_time = tbl_giaxe.PK_matime " \
              "INNER JOIN tbl_loaixe ON tbl_loaixe.ma_loai = tbl_giaxe.PK_maloai ORDER BY tbl_giaxe.PK_maloai DESC"
        a.execute(sql)
        tbl_giaxe = a.fetchall()

        arr = {
            'tbl_time':tbl_time,
            'tbl_loaixe':tbl_loaixe,
            'tbl_giaxe':tbl_giaxe,
        }
        return render(request, 'public/quanlyxe.html', arr)

def save_loaixe(request):
    tenloaixe = request.POST['tenloaixe']
    sql = "INSERT INTO tbl_loaixe(loai) " \
          "VALUES ('" + tenloaixe + "')"
    if tenloaixe != "":
        a.execute(sql)
        conn.commit()
    return HttpResponseRedirect("/Giaxe/")

def xoa_loaixe(request):
   pass

def save_time(request):
    name_time = request.POST['name_time']
    time_bd = request.POST['time_bd']
    time_kt = request.POST['time_kt']
    sql = "INSERT INTO tbl_time(name_time, time_bd, time_kt) " \
          "VALUES ('" + name_time + "','" + time_bd + "','" + time_kt + "')"
    a.execute(sql)
    conn.commit()
    return HttpResponseRedirect("/Giaxe/")

def save_giaxe(request):
    thoigian_loaixe = request.POST['thoigian_loaixe']
    thoigian_giaxe = request.POST['thoigian_giaxe']
    giatienxe = request.POST['giatienxe']
    loaive = request.POST['loaive']
    sql = "INSERT INTO tbl_giaxe(PK_maloai, PK_matime, giatien, loai_ve) " \
          "VALUES ('" + thoigian_loaixe + "','" + thoigian_giaxe + "','" + giatienxe + "','" + loaive + "')"
    a.execute(sql)
    conn.commit()
    return HttpResponseRedirect("/Giaxe/")

#Nhận diện biển số
class NhanDienBienSo(View):
    def get(self, request):
        cv2.destroyAllWindows()
        sql = "SELECT tbl_giaxe.PKma_giaxe, tbl_loaixe.loai, tbl_time.name_time, tbl_giaxe.giatien, tbl_giaxe.loai_ve, tbl_time.time_bd, tbl_time.time_kt " \
              "FROM tbl_giaxe " \
              "INNER JOIN tbl_time ON tbl_time.id_time = tbl_giaxe.PK_matime " \
              "INNER JOIN tbl_loaixe ON tbl_loaixe.ma_loai = tbl_giaxe.PK_maloai ORDER BY tbl_giaxe.PK_maloai DESC"
        a.execute(sql)
        tbl_giaxe = a.fetchall()

        sql = "SELECT  tbl_loaixe.loai, tbl_guixe.bienso_vao, tbl_guixe.ngaygui, tbl_guixe.tg_bg_gui, tbl_guixe.tg_kt_gui, " \
              "tbl_time.name_time, tbl_time.time_bd, tbl_time.time_kt, " \
              "tbl_giaxe.giatien, tbl_giaxe.loai_ve, tbl_guixe.trangthai, tbl_guixe.tongtien, tbl_guixe.ghichu, tbl_guixe.ma_guixe  " \
              "FROM tbl_guixe " \
              "INNER JOIN tbl_giaxe ON tbl_giaxe.PKma_giaxe = tbl_guixe.FK_giaxe  " \
              "INNER JOIN tbl_time ON tbl_time.id_time = tbl_giaxe.PK_matime " \
              "INNER JOIN tbl_loaixe ON tbl_loaixe.ma_loai = tbl_giaxe.PK_maloai ORDER BY tbl_guixe.ma_guixe DESC"
        a.execute(sql)
        tbl_guixe = a.fetchall()
        arr = {
            'tbl_giaxe': tbl_giaxe,
            'tbl_guixe': tbl_guixe,
        }

        return render(request, 'public/nhandienbienso.html', arr)

    def post(self, request):
        if request.POST['luuthongtin']:
            time_now = calendar.timegm(time.gmtime())
            # dd/mm/YY
            dt_string = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            giaxe = (int)(request.POST['thongtingiaxe'])
            bienso = (str)(request.POST['bienso'])
            sql = "INSERT INTO tbl_guixe(bienso_vao, ngaygui, tg_bg_gui, FK_giaxe) " \
                  "VALUES ('" + bienso + "','" + dt_string + "'," + (str)(time_now)+ "," + (str)(giaxe)  + ")"
            a.execute(sql)
            conn.commit()
            return HttpResponseRedirect("/nhandienbienso/")
        pass

#Bật camera

def BatCameRa(request):
    cap = cv2.VideoCapture(0)  # truyền vào camera

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return HttpResponseRedirect('/nhandienbienso')

    while True:
        success, frame = cap.read()
        if not success:
            break

        # Save the frame as an image
        path, dirs, files = next(os.walk("static/public/img/Camera"))
        file_count = len(files) + 1
        cv2.imwrite(f"static/public/img/Camera/photo{file_count}.jpg", frame)

        # Displaying the current date and time on the frame
        current_datetime = dt.datetime.now()
        date = str(current_datetime)
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) - 20
        cv2.putText(frame, date, (0, h), cv2.FONT_ITALIC, 1, (255, 255, 255), 1)

        cv2.imshow('vid', frame)

        if cv2.waitKey(40) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return HttpResponseRedirect('/nhandienbienso')

def TraXe(request):
    maxe = request.POST['traxe']
    sql = "SELECT tbl_giaxe.giatien  " \
          "FROM tbl_guixe " \
          "INNER JOIN tbl_giaxe ON tbl_giaxe.PKma_giaxe = tbl_guixe.FK_giaxe  " \
          " WHERE tbl_guixe.ma_guixe = "+ (str)(maxe)
    a.execute(sql)
    giaxe = a.fetchone()
    time_now = calendar.timegm(time.gmtime())
    sql = "UPDATE tbl_guixe SET trangthai = 'Đã trả xe', tg_kt_gui = "+(str)(time_now) + ", tongtien = " + (str)(giaxe[0]) +" WHERE ma_guixe = " + (str)(maxe)
    a.execute(sql)
    conn.commit()
    return HttpResponseRedirect("/nhandienbienso/")

def nhandienAnh(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
        request_getdata = json.loads(request.POST.get('link_anh', None))
        imgdata = base64.b64decode(request_getdata)
        path = 'static/public/img/HinhAnhNhanDien'
        path1, dirs, files = next(os.walk("static/public/img/HinhAnhNhanDien"))
        file_count = len(files) + 1
        filename = path + "/photo%d.jpg" % file_count
        if not os.path.exists(path):
            os.mkdir(path)
        with open(filename, 'wb') as f:
            f.write(imgdata)
            f.close()
        bienso = detext(filename).replace('\n', ' ').replace('\r', '')
        sql = "SELECT ma_guixe FROM tbl_guixe WHERE bienso_vao = '"+bienso+"' AND bienso_ra = '' AND trangthai = 'Đang gửi xe'"
        a.execute(sql)
        ma = a.fetchone()


        if ma == None:
            giaxe = request.POST.get('giaxe', None)
            time_now = calendar.timegm(time.gmtime())
            # dd/mm/YY
            dt_string = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            sql = "INSERT INTO tbl_guixe(bienso_vao, ngaygui, tg_bg_gui, FK_giaxe) " \
                  "VALUES ('" + bienso + "','" + dt_string + "'," + (str)(time_now) + "," + (str)(giaxe) + ")"
            a.execute(sql)
            conn.commit()
        else:
            maxe = ma[0]
            sql = "SELECT tbl_giaxe.giatien  " \
                  "FROM tbl_guixe " \
                  "INNER JOIN tbl_giaxe ON tbl_giaxe.PKma_giaxe = tbl_guixe.FK_giaxe  " \
                  " WHERE tbl_guixe.ma_guixe = " + (str)(maxe)
            a.execute(sql)
            giaxe = a.fetchone()
            sql = "SELECT tbl_guixe.FK_giaxe  " \
                  "FROM tbl_guixe " \
                  "INNER JOIN tbl_giaxe ON tbl_giaxe.PKma_giaxe = tbl_guixe.FK_giaxe  " \
                  " WHERE tbl_guixe.ma_guixe = " + (str)(maxe)
            a.execute(sql)
            ma_gia = a.fetchone()
            if ma_gia == 6 or ma_gia == 3:
                giaxe = 0
            time_now = calendar.timegm(time.gmtime())
            sql = "UPDATE tbl_guixe SET trangthai = 'Đã trả xe', tg_kt_gui = " + (str)(time_now) + ", tongtien = " + (
                str)(giaxe[0]) + " WHERE ma_guixe = " + (str)(maxe)
            a.execute(sql)
            conn.commit()

        return JsonResponse({"thongbao": "thanhcong", 'data': bienso})

class dangkyxethang(View):
    def get(self, request):
        sql = "SELECT tbl_giaxe.PKma_giaxe, tbl_loaixe.loai, tbl_time.name_time, tbl_giaxe.giatien, tbl_giaxe.loai_ve, tbl_time.time_bd, tbl_time.time_kt " \
              "FROM tbl_giaxe " \
              "INNER JOIN tbl_time ON tbl_time.id_time = tbl_giaxe.PK_matime " \
              "INNER JOIN tbl_loaixe ON tbl_loaixe.ma_loai = tbl_giaxe.PK_maloai ORDER BY tbl_giaxe.PK_maloai DESC"
        a.execute(sql)
        tbl_giaxe = a.fetchall()
        sql = "SELECT * FROM tbl_khach"
        a.execute(sql)
        tbl_khach = a.fetchall()
        arr = {
            'tbl_giaxe': tbl_giaxe,
            'tbl_khach': tbl_khach,
        }
        return render(request, 'public/dangkyxethang.html', arr)
    def post(self, request):
        if request.POST['themkhachhang']:
            hoten = request.POST['tenkh']
            ngaysinh = request.POST['ngaysinh']
            gioitinh = request.POST['gioitinh']
            diachi = request.POST['diachi']
            sodienthoai = request.POST['sodienthoai']
            biensoxe = request.POST['biensoxe']
            cmnd = request.POST['cmnd']
            thongtingiaxe = request.POST['thongtingiaxe']
            sql = "INSERT INTO tbl_khach(hoten, ngaysinh, gioitinh, diachi,cmnd, sdt) " \
                  "VALUES ('" + hoten + "','" + ngaysinh + "','" + gioitinh + "','" + diachi + "','" + cmnd + "','"+ sodienthoai +"')"
            a.execute(sql)
            conn.commit()
            time_now = calendar.timegm(time.gmtime())
            # dd/mm/YY
            dt_string = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            giaxe = (int)(request.POST['thongtingiaxe'])
            bienso = (str)(biensoxe)
            sql = "INSERT INTO tbl_guixe(bienso_vao, ngaygui, tg_bg_gui, FK_giaxe) " \
                  "VALUES ('" + bienso + "','" + dt_string + "'," + (str)(time_now) + "," + (str)(giaxe) + ")"
            a.execute(sql)
            conn.commit()
            return HttpResponseRedirect("/dangkyxethang/")

