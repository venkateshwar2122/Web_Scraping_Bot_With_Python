import requests
from bs4 import BeautifulSoup
import time
import csv
import send_mail
from datetime import date

urls = ["https://finance.yahoo.com/quote/AMZN?p=AMZN&.tsrc=fin-srch", "https://finance.yahoo.com/quote/GOOGL?p=GOOGL&.tsrc=fin-srch", "https://finance.yahoo.com/quote/MSFT?p=MSFT&.tsrc=fin-srch","https://eodhd.com/financial-summary/AMZN.US"]
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}

today = str(date.today()) + ".csv"
csv_file = open(today, "w")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Stock Name', 'Current Price', 'Previous Close', 'Open', 'Bid', 'Ask', 'Day Range', '52 Week Range', 'Volume', 'Avg. Volume'])

for url in urls:
    try:
        stock = []
        html_page = requests.get(url, headers=headers)
        soup = BeautifulSoup(html_page.content, 'lxml')

        header_info = soup.find_all("div", id="quote-header-info")[0]
        stock_title = header_info.find("h1").get_text()
    # print(stock_title)
        current_price = header_info.find("div", class_="My(6px) Pos(r) smartphone_Mt(6px) W(100%)").find("fin-streamer").get_text()
        stock.append(stock_title)
        stock.append(current_price)

        
        table_info = soup.find_all("div", class_="D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($seperatorColor)")[0].find_all("tr")
    # print(table_info[0].find_all("td")[0].get_text())
        for i in range(0,8):
            value = table_info[i].find_all("td")[1].get_text()
            stock.append(value)
        
        csv_writer.writerow(stock)
        time.sleep(5)
    except:
        continue
    


csv_file.close()
send_mail.send(filename = today)

