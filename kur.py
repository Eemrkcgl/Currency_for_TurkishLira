from bs4 import BeautifulSoup
import requests
from datetime import datetime,date
import json
import os
import time

class Kur():
    def __init__(self, dolara, dolars, altina, altins):
        self.dolara=dolara
        self.dolars=dolars
        self.altina=altina
        self.altins=altins

    def getDolar(self):
        url = "https://bigpara.hurriyet.com.tr/doviz/dolar/"
        response = requests.get(url)

        html_codes = response.content

        soup = BeautifulSoup(html_codes, "html.parser")

        alis = soup.find("span", class_="value dw").string
        alis = alis.replace(",", ".")

        satis = soup.find("span", class_="value up").string

        satis = satis.replace(",", ".")

        self.dolara=float(alis)
        self.dolars=float(satis)


    def getAltin(self):
        url = "https://bigpara.hurriyet.com.tr/altin/"
        response = requests.get(url)

        html_codes = response.content

        soup = BeautifulSoup(html_codes, "html.parser")

        alis = soup.find("span", class_="box bFirst").get_text()

        satis = soup.find_all("span", class_="box")[1].get_text()


        alis = float(alis[10:].replace(",", "."))

        satis = list(soup.find_all("span", class_="box"))[1]
        satis = satis.get_text()[11:-1]
        satis = float(satis.replace(",", "."))

        self.altina = alis
        self.altins = satis



class fileManagment(Kur):

    def __init__(self,year,month,day,dolara,dolars,altina,altins):
        super().__init__(dolara,dolars,altina,altins)
        self.year=year
        self.month=month
        self.day=day


    def newInit(self):
        self.year=input("Yıl: ")
        self.month=input("Ay: ")
        self.day=input("Gün: ")

    def writeDaily(self):
        Kur.getDolar(self)
        Kur.getAltin(self)

        today=date.today()

        hour = datetime.now()

        current_time = hour.strftime("%H:%M:%S")

        dict={
            "Dolar Alis":self.dolara,
            "Dolar Satis":self.dolars,
            "Altin Alis":self.altina,
            "Altin Satis":self.altins,
            "Tarih":str(today),
            "Saat":str(current_time)
        }

        if os.path.exists('gecmis.json'):

            with open("gecmis.json","r+") as json_file:
                data=json.load(json_file)
                data.get("a").append(dict)
                json_file.seek(0)
                json.dump(data,json_file)

                print("Kayıt tamamlandı.")

        else:
            with open("gecmis.json","w") as json_file:
                dict2={"a":[dict]}
                json.dump(dict2, json_file)

                print("Kayıt tamamlandı.")


    def pastCurrency(self):

        fileManagment.newInit(self)

        counter = 0
        with open("gecmis.json", "r") as json_file:
            data=json.load(json_file)

            for each in data.get("a"):
                if str(each["Tarih"]) == self.year + "-" + self.month + "-" + self.day:
                    counter += 1
                    print(
                        "Dolar Alış: {}\tDolar Satış: {}\nAltın Alış: \tAltın Satış: {}\nTarih: {}\nSaat: {}\n\n".
                            format(
                            each["Dolar Alis"], each["Dolar Satis"], each["Altin Alis"], each["Altin Satis"],each["Tarih"], each["Saat"]
                        )
                    )
        if counter != 0:
            print("{} kayıt bulundu".format(counter))
        else:
            print("Belirtilen tarihte herhangi bir kayıt bulunamadı.")


#json_object = [json.loads(line) for line in json_file]
#r_json_object=list(map(lambda x: re.sub('\'','\"',x),json_object))



class convertCurrency(Kur):

    def __init__(self,dolara,dolars,altina,altins):
        super().__init__(dolara,dolars,altina,altins)

    def tr2dolar(self,amounttr):
        Kur.getDolar(self)
        return amounttr/self.dolara
    def dolar2tr(self,amountdolar):
        Kur.getDolar(self)
        return self.dolars*amountdolar


    def tr2altin(self,amounttr):
        Kur.getAltin(self)
        return amounttr/self.altina
    def altin2tr(self,amountgram):
        Kur.getAltin(self)
        return self.altins*amountgram



class showCurrency(Kur):
    def __init__(self,dolara,dolars,altina,altins):
        super().__init__(dolara,dolars,altina,altins)


    def showDolar(self):
        Kur.getDolar(self)
        print("Alış: {}\tSatış: {}\n".format(self.dolara, self.dolars))


    def showAltin(self):
        Kur.getAltin(self)
        print("Alış: {}\tSatış: {}\n".format(self.altina, self.altins))



#User Interface
main = Kur(None, None, None, None)
sub1_file = fileManagment(None, None, None, None, None, None, None)
sub2_convert = convertCurrency(None, None, None, None)
sub3_show = showCurrency(None, None, None, None)
sub1_file.writeDaily()
#sub1_file.pastCurrency()
while True:
    print("Menu\n"
          "1-Dolar Kuru\n"
          "2-Altın Kuru\n"
          "3-Tarih Sorgu\n"
          "4-Çevirici\n"
          "5-Kayıt Al\n"
          "Çıkmak için bir harfe basınız\n")
    menu = input("Yapılacak işlemi seçiniz: ")
    print("\n\n\n\n\n")
    try:
        menu = int(menu)
        if menu == 1:
            sub3_show.showDolar()
        elif menu == 2:
            sub3_show.showAltin()
        elif menu == 3:
            sub1_file.pastCurrency()
        elif menu == 4:
            while True:
                print("Çevirme neyden neye olacak: \n"
                      "1-Tr-Dolar\n"
                      "2-Dolar-Tr\n"
                      "3-Tr-Altin\n"
                      "4-Altin-Tr\n\n")
                choice=int(input("Yapılacak İşlemi Seçiniz: \n\n\n\n"))
                if choice == 1:
                    amount = float(input("Tr Miktarı: \n"))
                    print("Dolar karşılığı: {} Dolar\n\n".format(sub2_convert.tr2dolar(amount)))
                    break
                elif choice == 2:
                    amount = float(input("Dolar Miktarı: \n"))
                    print("TL karşılığı: {} Türk Lirası\n\n".format(sub2_convert.dolar2tr(amount)))
                    break
                elif choice == 3:
                    amount = float(input("Tr Miktarı: \n"))
                    print("Altın Gram karşılığı: {} gram\n\n".format(sub2_convert.tr2altin(amount)))
                    break
                elif choice == 4:
                    amount = float(input("Gram Miktarı: \n"))
                    print("TL karşılığı: {} Türk Lirası\n\n".format(sub2_convert.altin2tr(amount)))
                    break
                else:
                    print("Bilinmeyen komut tekrar deneyin...\n\n\n")

        elif menu == 5:
            sub1_file.writeDaily()
        else:
            print("Bilinmeyen komut.\n\n\n\n\n\n\n")
    except ValueError:
        print("Çıkış yapılıyor...")
        time.sleep(1)
        break
            
            



