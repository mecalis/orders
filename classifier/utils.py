from __future__ import print_function
import joblib
from .hog import HOG
import glob
import cv2
import numpy as np

#imports facebookhoz
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import os
import wget
import io
import requests
from PIL import Image
from datetime import datetime
from datetime import date
import matplotlib.pyplot as plt


#OCR importok
from pytesseract import Output
import pytesseract
import re
import inspect

##############
def retrieve_name(var):
    """
    Gets the name of var. Does it from the out most frame inner-wards.
    :param var: variable to get name from.
    :return: string
    """
    for fi in reversed(inspect.stack()):
        names = [var_name for var_name, var_val in fi.frame.f_locals.items() if var_val is var]
        if len(names) > 0:
            return names[0]

def load_model():
    '''
    Modell betöltése a lemezről
    :return: model
    '''
    #
    import pickle
    model = pickle.load(open("classifier\model2.sav", "rb"))

    # initialize the HOG descriptor
    hog = HOG(orientations=18, pixelsPerCell=(10, 10),
              cellsPerBlock=(1, 1), transform=True, block_norm="L2-Hys")
    return model, hog

def grab_image(a):
    '''
    Egy kép letöltése a netről link alapján és konvertáláse opencv képpé
    :param a: a kép linkje a facebookon
    :return: opencv formájú kép
    '''
    data = requests.get(a).content
    image = Image.open(io.BytesIO(data))
    image = image.convert('RGB')
    open_cv_image = np.array(image)
    # Convert RGB to BGR
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    return open_cv_image

def classify(image, model, hog):
    '''
    Egy memóriában lévő kép osztályozása, hogy az napi menü-e
    :param image: kép a memóriában
    :param model: classifier modell
    :param hog: hog leíró
    :return: 1 vagy 0
    '''
    dim = (843, 1193)
    image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    hist = hog.describe(image)
    pred = int(model.predict([hist])[0])
    pred_for_print = "napi menü" if pred == 1 else "egyéb kép"
    print("[INFO] Szerintem ez egy: {}".format(pred_for_print))

    return pred

def extract_day_roi(image, path, counter, ROI_name_list):
    '''
    Egy adott nepi müt tartalmazó képből az egyes napokhoz tartozó napi ajánlatok befoglaló méreteinek kiszedése
    :param image: szétvágandó kép
    :param path: mentés helye
    :param counter: kép számláló aktuális állása
    :param ROI_name_list: keresendő napok nevei lista formában
    :return: kibányászott szövegek és az egyes napok befoglaló dobozai
    '''
    # print(image.shape)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    options = "-l hun"
    results = pytesseract.image_to_data(rgb, config=options, output_type=Output.DICT)
    ROI = {}

    for i in range(0, len(results["text"])):
        # extract the bounding box coordinates of the text region from
        # the current result
        x = results["left"][i]
        y = results["top"][i]
        w = results["width"][i]
        h = results["height"][i]

        # extract the OCR text itself along with the confidence of the
        # text localization
        text = results["text"][i]
        conf = int(results["conf"][i].split('.')[0])
        if text in ROI_name_list:
            # print(text)
            ROI[text] = {'x': x, 'y': y, 'w': w, 'h':h}

        # filter out weak confidence text localizations
        if conf > 0.5:
            # display the confidence and text to our terminal
            # print("Confidence: {}".format(conf))
            # print("Text: {}".format(text))
            # print("")
            text_nonascii = "".join([c if ord(c) < 128 else "" for c in text]).strip()
            cv2.rectangle(rgb, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(rgb, text_nonascii, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        1.2, (0, 0, 255), 3)

    # show the output image
    save_as = os.path.join(path, str(counter) + 'OCR.jpg')
    # cv2.imwrite(save_as, rgb)
    # cv2.imshow("Image", rgb)
    # cv2.waitKey(0)

    return results, ROI

def get_images_from_facebook(only_one = True, save = False):
    '''
    A függvény felmegy a Margaréta oldalára, és letölti a napi menüket.
    :param only_one: csak a legutolsó napi menüt töltse le?
    :param save: képet mentse le a lemezre?
    :return: képek tömbben
    '''
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    chrome_options.add_argument("--headless")

    # specify the path to chromedriver.exe (download and save on your computer)
    driver = webdriver.Chrome('C:/ML/chromedriver.exe', options=chrome_options)

    # open the webpage
    driver.get("http://www.facebook.com")
    print("[INFO] Webhely felkeresve")
    button = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[title='Az összes elfogadása']"))).click()
    id = "u_0_j_Ct"

    # target username
    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

    # enter username and password
    username.clear()
    username.send_keys("mecalis@gmail.com")
    password.clear()
    password.send_keys("OKOS1984")

    # target the login button and click it
    button = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    # We are logged in!

    # wait 5 seconds to allow your new page to load
    time.sleep(4)
    images = []

    driver.get("https://www.facebook.com/Margar%C3%A9ta-Gyors%C3%A9tterem-102986047900956/photos/")
    time.sleep(3)
    print("[INFO] Login sikeres volt, album megtalálva.")
    # scroll down
    for j in range(0, 0):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    # target all the link elements on the page
    anchors = driver.find_elements_by_tag_name('a')
    # anchors = [a.get_attribute('href') for a in anchors]

    anchors_filtered = []
    for a in anchors:
        href = a.get_attribute('href')
        if str(href).startswith("https://www.facebook.com/Margar%C3%A9ta-Gyors%C3%A9tterem-102986047900956/photos") and str(href).endswith("/"):
            # print(href)
            anchors_filtered.append(a)
    # anchors_filtered = [a for a in anchors if str(a).startswith("https://www.facebook.com/Margar%C3%A9ta-Gyors%C3%A9tterem-102986047900956/photos")]

    print('[INFO] Találtam ' + str(len(anchors_filtered)) + ' linket képekhez.')

    model, hog = load_model()
    print("[INFO] Classifier betöltve.")
    # extract the [1]st image element in each link
    for a in anchors_filtered:
        # driver.get(a)  # navigate to link
        # time.sleep(2)  # wait a bit
        img = a.find_elements_by_tag_name("img")

        images.append(img[0].get_attribute("src"))  # may change in future to img[?]

    # print('I scraped ' + str(len(images)) + ' images!')

    path = os.getcwd()
    path = os.path.join(path, "FB_SCRAPED")
    # # create the directory
    # os.mkdir(path)
    ROI_name_list = ['HETFO:', 'KEDD:', 'SZERDA:', 'CSÜTÖRTÖK:', 'PENTEK:', 'SZOMBAT:']
    counter = 0
    images_from_facebook = []

    for link in images:
        # print(str(link))
        counter += 1
        image = grab_image(link)
        # plt.imshow(img)
        # plt.show()
        pred = classify(image, model, hog)

        if int(pred) == 1:
            images_from_facebook.append(image)
            if save:
                save_as = os.path.join(path, str(counter) + '.jpg')
                wget.download(link, save_as)
            # results, ROI = extract_day_roi(image, path, counter, ROI_name_list)
            if only_one:
                break
    return images_from_facebook

def get_text_from_day(v, target, image_day, ifdigit = False, print = False):
    '''
    Ételek kiszedése egy adott naphoz tartozó képrészletből
    :param v: eltolásvektorok dict
    :param target: a kívánt mező neve, pl M1_leves
    :param image_day: egy naphoz tartozó képdarab
    :param ifdigit: csal számot kérünk belőle? Bool
    :return:
    '''
    options_digits = "-l hun -c tessedit_char_whitelist=0123456789"
    options = "-l hun"
    focus = v[target]
    cropped = image_day[focus[2]:focus[3], focus[0]:focus[1]]
    if ifdigit == True:
        results = pytesseract.image_to_string(cropped, config=options_digits).strip()
    else:
        results = pytesseract.image_to_string(cropped, config=options).strip()
    if print:
        print('Eredmény: ', results)
    return results

def extract_data_from_image(image):
    '''
    2. főfüggvény. Egy adott heti menüből kiszedi az összes ételt, dict formában
    :param image: heti menü
    :return: dict
    '''
    ROI_name_list = ['HETFO:', 'KEDD:', 'SZERDA:','CSÜTÖRTÖK:','PENTEK:','SZOMBAT:']
    # cv2.imshow("Image", image)
    # cv2.waitKey(0)
    path = os.getcwd()
    path = os.path.join(path, "FB_SCRAPED")
    results, day_ROI = extract_day_roi(image, path, 1, ROI_name_list)
    # print(image.shape)
    hetfo_roi = day_ROI['HETFO:']
    kedd_roi = day_ROI['KEDD:']
    szerda_roi = day_ROI['SZERDA:']
    csütörtök_roi = day_ROI['CSÜTÖRTÖK:']
    péntek_roi = day_ROI['PÉNTEK:']
    szombat_roi = day_ROI['SZOMBAT:']

    v = {
        'fozi_ar': [0,180, 36,65],
        'fozi_nev': [0,300, 65,95],
        'feltet_ar': [0,300, 95,125],
        'feltet_nev': [0,300, 127,155],
        'M1_leves': [300,800, 40,64],
        'M1_fo': [300,800, 65,93],
        'M2_leves': [300,800, 123,152],
        'M2_fo': [300,800, 150,185],
        'date': [0 , 300 , 0,  42],
    }

    cropped_days = []
    HETFO = image[hetfo_roi['y']-10:kedd_roi['y']-10, hetfo_roi['x']-10:image.shape[1]-150]
    cropped_days.append(HETFO)
    KEDD = image[kedd_roi['y']-10:szerda_roi['y']-10, kedd_roi['x']-10:image.shape[1]-150]
    cropped_days.append(KEDD)
    SZERDA = image[szerda_roi['y']-10:csütörtök_roi['y']-10, szerda_roi['x']-10:image.shape[1]-150]
    cropped_days.append(SZERDA)
    CSÜTÖRTÖK = image[csütörtök_roi['y']-10:péntek_roi['y']-10, csütörtök_roi['x']-10:image.shape[1]-150]
    cropped_days.append(CSÜTÖRTÖK)
    PÉNTEK = image[péntek_roi['y']-10:szombat_roi['y']-10, péntek_roi['x']-10:image.shape[1]-150]
    cropped_days.append(PÉNTEK)
    SZOMBAT = image[szombat_roi['y']-10:szombat_roi['y']+200-10, szombat_roi['x']-10:image.shape[1]-150]
    cropped_days.append(SZOMBAT)

    day_data = {}

    for day in cropped_days:
        date_of_meal = get_text_from_day(v=v, target='date', image_day=day, ifdigit=True)
        fozi_ar = get_text_from_day(v = v, target = 'fozi_ar', image_day=day, ifdigit= True)
        fozi_nev = get_text_from_day(v = v, target = 'fozi_nev', image_day=day, ifdigit= False)
        feltet_ar = get_text_from_day(v = v, target = 'feltet_ar', image_day=day, ifdigit= True)
        feltet_nev = get_text_from_day(v = v, target = 'feltet_nev', image_day=day, ifdigit= False)
        M1_leves = get_text_from_day(v = v, target = 'M1_leves', image_day=day, ifdigit= False)
        M1_fo = get_text_from_day(v = v, target = 'M1_fo', image_day=day, ifdigit= False)
        M2_leves = get_text_from_day(v = v, target = 'M2_leves', image_day=day, ifdigit= False)
        M2_fo = get_text_from_day(v = v, target = 'M2_fo', image_day=day, ifdigit= False)
        M1 = f"{M1_leves} és {M1_fo}"
        M2 = f"{M2_leves} és {M2_fo}"
        name_of_day = retrieve_name(day)
        fozi_ar = int(fozi_ar) if len(fozi_ar) > 0 else fozi_ar
        feltet_ar = int(feltet_ar) if len(feltet_ar) > 0 else feltet_ar
        date_of_meal = f"{str(date.today()).split('-')[0]}-{date_of_meal[0:2]}-{date_of_meal[2:]}"

        day_data[name_of_day] = {
            'date': date_of_meal,
            'fozi_ar': fozi_ar,
            'fozi_nev': fozi_nev,
            'feltet_ar': feltet_ar,
            'feltet_nev': feltet_nev,
            'M1_leves': M1_leves,
            'M1_fo': M1_fo,
            'M1': M1,
            'M2_leves': M2_leves,
            'M2_fo': M2_fo,
            'M2': M2,
        }
    return day_data

# images = get_images_from_facebook()

# path = os.getcwd()
# path = os.path.join(path, "FB_SCRAPED")
# image_path = os.path.join(path, "1.jpg")
# image = cv2.imread(image_path)

# data = extract_data_from_image(images[0])
# print(data['HETFO'])
# print(data['KEDD'])
# print(data['SZERDA'])


# print(day_ROI)
# cv2.imshow("Image", HETFO)
# cv2.waitKey(0)
# cv2.imwrite(os.path.join(path, "1_hetfo.jpg"), HETFO)

'''
Eltolásvektorok
dátum = nap:nap + 90, 0:36
főzelék ár = 0:180, 36:65
főzelék név = 0:330, 65:95
feltét ár = 0:300, 95:125
feltét név = 0:300, 125:150
M1 leves = 300:800, 35:62
M1 főétel = 300:800, 62:90
M2 leves = 300:800, 120:150
M2 főétel = 300:800, 150:185

'''
