import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import random
import string

img = cv.imread("./pict/img8.png", cv.IMREAD_COLOR)
img_grey = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
cv.imshow('img', img_grey)
cv.waitKey(0)

fig = plt.figure(figsize=(10, 7))
row_fig = 1
column_fig = 1

fig.add_subplot(row_fig, column_fig, 1)
plt.imshow(img_grey)
plt.axis('on')
plt.title("RGB")

plt.show()
def segmentasiKarakter(img_plate_gray):
 
    # konversi dari grayscale ke BW
    (thresh, img_plate_bw) = cv.threshold(img_plate_gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    # hasil dari konversi BW tidak terlalu mulus, 
    # ada bagian-bagian kecil yang tidak diinginkan yang mungkin bisa mengganggu
    # maka hilangkan area yang tidak diinginkan dengan operasi opening

    # buat kernel dengan bentuk cross dan ukuran 3x3
    kernel = cv.getStructuringElement(cv.MORPH_CROSS, (3,3))

    cv.imshow("sebelum open", img_plate_bw)
    cv.waitKey(0)

    # lakukan operasi opening dengan kernel di atas
    # img_plate_bw = cv.morphologyEx(img_plate_bw, cv.MORPH_OPEN, kernel) # apply morph open

    # cv.imshow("sesudah open", img_plate_bw)
    # cv.waitKey(0)

    # Segmentasi karakter menggunakan contours
    # dapatkan kontur dari plat nomor
    contours_plate, hierarchy = cv.findContours(img_plate_bw, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) 

    # index contour yang berisi kandidat karakter
    index_chars_candidate = [] #index

    # index counter dari setiap contour di contours_plate
    index_counter_contour_plate = 0 #idx

    # duplikat dan ubah citra plat dari gray dan bw ke rgb untuk menampilkan kotak karakter
    img_plate_rgb = cv.cvtColor(img_plate_gray,cv.COLOR_GRAY2BGR)
    # cv.imshow('dsadsa',img_plate_rgb)


    img_plate_bw_rgb = cv.cvtColor(img_plate_bw, cv.COLOR_GRAY2RGB)
    # cv.imshow('plate_bw_segment',img_plate_bw_rgb)
    # cv.imshow('contur',contours_plate)
    # cv.waitKey(0)
    print(contours_plate)

    # Mencari kandidat karakter
    for contour_plate in contours_plate:

        # dapatkan lokasi x, y, nilai width, height dari setiap kontur plat
        x_char,y_char,w_char,h_char = cv.boundingRect(contour_plate)
        
        # Dapatkan kandidat karakter jika:
        #   tinggi kontur dalam rentang 40 - 60 piksel
        #   dan lebarnya lebih dari atau sama dengan 10 piksel 
        if h_char >= 40 and h_char <= 90 and w_char >=5:

            # dapatkan index kandidat karakternya
            index_chars_candidate.append(index_counter_contour_plate)

            # gambar kotak untuk menandai kandidat karakter
            cv.rectangle(img_plate_rgb,(x_char,y_char),(x_char+w_char,y_char+h_char),(0,255,0),5)
            cv.rectangle(img_plate_bw_rgb,(x_char,y_char),(x_char+w_char,y_char+h_char),(0,255,0),5)

        index_counter_contour_plate += 1

    # tampilkan kandidat karakter
    cv.imshow('Kandidat Karakter',img_plate_rgb)
    cv.waitKey(0)

    if index_chars_candidate == []:

        # tampilkan peringatan apabila tidak ada kandidat karakter
        print('Karakter tidak tersegmentasi')
    else:

        # Mendapatkan yang benar-benar karakter
        #   terkadang area lain yang bukan karakter ikut terpilih menjadi kandidat karakter
        #   untuk menghilangkannya bisa dicek apakah sebaris dengan karakter plat nomor atau tidak
        #
        # Caranya dengan Scoring:
        #   Bagian karakter plat nomor akan selalu sebaris, 
        #       memiliki nilai y yang hampir sama atau tidak terlalu besar perbedaannya.
        #       Maka bandingkan nilai y dari setiap kandidat satu dengan kandidat lainnya. 
        #   Jika perbedaannya tidak lebih dari 11 piksel maka tambahkan score 1 point ke kandidat tersebut.
        #       Kandidat yang benar-benar sebuah karakter akan memiliki nilai score yang sama dan tertinggi

        # Scoring

        # untuk menyimpan skor setiap karakter pada kandidat
        score_chars_candidate = np.zeros(len(index_chars_candidate))

        # untuk counter index karakter
        counter_index_chars_candidate = 0

        # bandingkan lokasi y setiap kandidat satu dengan kandidat lainnya
        for chars_candidateA in index_chars_candidate:
            
            # dapatkan nilai y dari kandidat A
            xA,yA,wA,hA = cv.boundingRect(contours_plate[chars_candidateA])
            for chars_candidateB in index_chars_candidate:

                # jika kandidat yang dibandikan sama maka lewati
                if chars_candidateA == chars_candidateB:
                    continue
                else:
                    # dapatkan nilai y dari kandidat B
                    xB,yB,wB,hB = cv.boundingRect(contours_plate[chars_candidateB])

                    # cari selisih nilai y kandidat A dan kandidat B
                    y_difference = abs(yA - yB)
                    # print(y_difference)

                    # jika perbedaannya kurang dari 50 piksel
                    if y_difference < 5000:
                        
                        # tambahkan nilai score pada kandidat tersebut
                        score_chars_candidate[counter_index_chars_candidate] = score_chars_candidate[counter_index_chars_candidate] + 1 
            # lanjut ke kandidat lain
            counter_index_chars_candidate += 1

        print(score_chars_candidate)

        # untuk menyimpan karakter
        index_chars = []

        # counter karakter
        chars_counter = 0

        # dapatkan karakter, yaitu yang memiliki score tertinggi
        for score in score_chars_candidate:
            if score == max(score_chars_candidate):

                # simpan yang benar-benar karakter
                index_chars.append(index_chars_candidate[chars_counter])
            chars_counter += 1

        # Sampai disini sudah didapatkan karakternya
        #   sayangnya karena ini menggunakan contours, 
        #   urutan karakter masih berdasarkan letak sumbu y, dari atas ke bawah,
        #   misal yang harusnya Z 1234 AB hasilnya malah 1 3Z24 BA.
        #   Hal ini akan menjadi masalah ketika nanti proses klasifikasi karakter.
        #   Maka mari disusun berdasarkan sumbu x, dari kiri ke kanan.

        # duplikat dan ubah ke rgb untuk menampilkan urutan karakter yang belum terurut
        img_plate_rgb2 = cv.cvtColor(img_plate_gray, cv.COLOR_GRAY2BGR)

        # tampilkan urutan karakter yang belum terurut
        for char in index_chars:
            x, y, w, h = cv.boundingRect(contours_plate[char])
            cv.rectangle(img_plate_rgb2,(x,y),(x+w,y+h),(0,255,0),5)
            cv.putText(img_plate_rgb2, str(index_chars.index(char)),(x, y + h + 50), cv.FONT_ITALIC, 2.0, (0,0,255), 3)
        
        # tampilkan karakter yang belum terurut
        # cv.imshow('Karakter Belum Terurut', img_plate_rgb2)

        # Mulai mengurutkan

        # untuk menyimpan koordinat x setiap karakter
        x_coors = []

        for char in index_chars:
            # dapatkan nilai x
            x, y, w, h = cv.boundingRect(contours_plate[char])

            # dapatkan nilai sumbu x
            x_coors.append(x)

        # urutkan sumbu x dari terkecil ke terbesar
        x_coors = sorted(x_coors)

        # untuk menyimpan karakter
        index_chars_sorted = []

        # urutkan karakternya berdasarkan koordinat x yang sudah diurutkan
        for x_coor in x_coors:
            for char in index_chars:

                # dapatkan nilai koordinat x karakter
                x, y, w, h = cv.boundingRect(contours_plate[char])

                # jika koordinat x terurut sama dengan koordinat x pada karakter
                if x_coors[x_coors.index(x_coor)] == x:

                    # masukkan karakternya ke var baru agar mengurut dari kiri ke kanan
                    index_chars_sorted.append(char)

        # duplikat dan ubah ke rgb untuk menampilkan yang benar-benar karakter
        img_plate_rgb3 = cv.cvtColor(img_plate_gray, cv.COLOR_GRAY2BGR)

        # Gambar kotak untuk menandai karakter yang terurut dan tambahkan teks urutannya
        for char_sorted in index_chars_sorted:

            # dapatkan nilai x, y, w, h dari karakter terurut
            x,y,w,h = cv.boundingRect(contours_plate[char_sorted])

            # gambar kotak yang menandai karakter terurut
            cv.rectangle(img_plate_rgb3,(x,y),(x+w,y+h),(0,255,0),5)

            # tambahkan teks urutan karakternya
            cv.putText(img_plate_rgb3, str(index_chars_sorted.index(char_sorted)),(x, y + h + 50), cv.FONT_ITALIC, 2.0, (0,0,255), 3)
        
        # tampilkan hasil pengurutan
        cv.imshow('Karakter Terurut', img_plate_rgb3)

        # ==== Cek Segmentasi Karakter START ====
        # Bisa di comment/uncomment

        fig3 = plt.figure(figsize=(10, 7))
        row_fig = 2
        column_fig = 2
        
        fig3.add_subplot(row_fig, column_fig, 1)
        plt.imshow(img_plate_bw_rgb)
        plt.axis('on')
        plt.title("Kandidat Karakter BW")
        
        fig3.add_subplot(row_fig, column_fig, 2)
        plt.imshow(cv.cvtColor(img_plate_rgb, cv.COLOR_BGR2RGB))
        plt.axis('on')
        plt.title("Kandidat Karakter")
        
        fig3.add_subplot(row_fig, column_fig, 3)
        plt.imshow(cv.cvtColor(img_plate_rgb2, cv.COLOR_BGR2RGB))
        plt.axis('on')
        plt.title("Karakter Belum Terurut")
        
        fig3.add_subplot(row_fig, column_fig, 4)
        plt.imshow(cv.cvtColor(img_plate_rgb3, cv.COLOR_BGR2RGB))
        plt.axis('on')
        plt.title("Karakter Terurut")
        
        plt.show()

        # KALSIFIKASI KARAKTER
        # untuk mengklasifikasi karakter, saya menggunakan tutorial:
        # https://www.tensorflow.org/tutorials/images/classification
        # hasil klasifikasi akan tersimpan di var plate_number

        # tinggi dan lebar citra untuk test
        img_height = 40 
        img_width = 40

        # klas karakter
        class_names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        # load model yang sudah terlatih
        # model = keras.models.load_model('./my_model_new')
        # print("adasdaw /n")
        # print(model)
        # print("adasdaw /n")

        # untuk menyimpan string karakter
        num_plate = []
        name = 0
        for char_sorted in index_chars_sorted:
            x,y,w,h = cv.boundingRect(contours_plate[char_sorted])
            name = str(index_chars_sorted.index(char_sorted))
            print(str(index_chars_sorted.index(char_sorted)))

            # potong citra karakter
            char_crop = cv.cvtColor(img_plate_bw[y:y+h,x:x+w], cv.COLOR_GRAY2BGR)

            # resize citra karakternya
            char_crop = cv.resize(char_crop, (img_width, img_height))
            # name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
            cv.imwrite('./dataset2_40/8/8_'+ name +'.png',char_crop)

        # Gabungkan string pada list
        plate_number = ''
        for a in num_plate:
            plate_number += a

        # Hasil deteksi dan pembacaan
        # cv.putText(img_show_plate, plate_number,(x_plate, y_plate + h_plate + 50), cv.FONT_ITALIC, 2.0, (0,255,0), 3)
        # cv.imshow(plate_number, img_show_plate)

        print("\n"+plate_number)
    
    return 


segmentasiKarakter(img_grey)