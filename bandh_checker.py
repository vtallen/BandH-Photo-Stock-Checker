'''
TODO
- Add documentation to this spaghetti monster so that when I look back at it I don't question my sanity



'''
from selenium import webdriver
import smtplib
import time
import datetime
import json
from os import path

urls = {}

conf = {
    "gmail_email": None,
    "send_to_email": None,
    "app_password": None,
    "request_interval": None,
    "binary_location": None,
}

def initialize():
    global conf
    global urls

    # Load the configuration, create it if it does not exist
    if path.isfile("conf.json"):
        conf_file = open("conf.json", "r")
        conf = json.load(conf_file)
        conf_file.close()
    else:
        conf_file = open("conf.json", "w")
        gmail_address = input("What is your gmail address? :: ")
        conf["gmail_email"] = gmail_address

        send_to_email = input("What email address should notifications be sent to? :: ")
        conf["send_to_email"] = send_to_email

        app_password = input("What is your gmail app password? :: ")
        conf["app_password"] = app_password

        request_interval = int(input("How often should the program check stock? (seconds) :: "))
        conf["request_interval"] = request_interval

        binary = input("Where is your chrome binary located? :: ")
        conf["binary_location"] = binary

        json.dump(conf, conf_file, indent=5)
        conf_file.close()

    # Load the URLs.json file, create it if it does not exist
    gathering_urls = True
    if path.isfile("urls.json"):
        urls_file = open("urls.json", "r")
        urls = json.load(urls_file)
        urls_file.close()
    else:
        print("urls.json not found")
        while gathering_urls:
            input_url = input("B&H Photo Product URL :: ")
            urls[input_url] = "no_email_sent"
            add_again = input("Add another URL? (Y/N) :: ")
            if add_again.lower() == "n":
                gathering_urls = False

        urls_file = open("urls.json", "w")
        json.dump(urls, urls_file, indent=len(urls.keys()) + 1)
        urls_file.close()


def log(message):
    log_file = open("log.txt", "a")
    log_file.write(message + "\n")
    log_file.close()


def is_in_stock(url):
    global conf

    # service = Service(driver_path)
    options = webdriver.ChromeOptions()
    options.binary_location = conf.get("binary_location")  # Path to Brave Browser (this is the default)

    driver = webdriver.Chrome(options=options)

    # From here its Selenium as usual, example:
    driver.get(url)

    stock_status = driver.find_element('xpath', '//*[@data-selenium="stockStatus"]')
    item_title = driver.find_element('xpath', '//*[@data-selenium="productTitle"]')
    item_title = item_title.text
    stock_status = stock_status.text
    driver.close()

    log_message = str(datetime.datetime.now()) + " " + item_title + " : Stock Status : " + stock_status
    print(log_message)
    log(log_message)

    if stock_status == "Temporarily Out of Stock" or stock_status == "Back-Ordered":
        return item_title, False
    elif stock_status == "In Stock":
        return item_title, True
    else:
        raise ValueError("is_in_stock returned an unknown stock status")


def send_email(message):
    global conf
    log_message = str(datetime.datetime.now()) + " EMAIL SENT"
    print(log_message)
    log(log_message)
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(conf.get("gmail_email"), conf.get("app_password"))

    # sending the mail
    s.sendmail(conf.get("gmail_email"), conf.get("send_to_email"), message)

    # terminating the session
    s.quit()


def main():
    running = True
    while running:
        for url in urls.keys():
            title, in_stock = is_in_stock(url)
            if in_stock == True and urls.get(url) != "in_stock":
                urls[url] = "in_stock"

                subject = "B&H Photo Item Is In Stock"

                text = f"""
                B&H Photo Item : {title}
                Is in stock
                
                Buy it at {url}
                """

                message = 'Subject: {}\n\n{}'.format(subject, text)

                send_email(message)

                # Dump the urls dictionary to reflect that the email has been sent
                urls_file = open("urls.json", "w")
                json.dump(urls, urls_file, indent=len(urls.keys()) + 1)
                urls_file.close()
            elif in_stock == False and urls.get(url) == "in_stock":
                urls[url] = "out_of_stock"

                subject = "B&H Photo Item Out Of Stock"

                text = f"""
                                B&H Photo Item : {title}
                                Has changed stock status
                                
                                See it at {url}
                                """

                message = 'Subject: {}\n\n{}'.format(subject, text)

                send_email(message)

                # Dump the urls dictionary to reflect that the email has been sent
                urls_file = open("urls.json", "w")
                json.dump(urls, urls_file, indent=len(urls.keys()) + 1)
                urls_file.close()

        time.sleep(conf.get("request_interval"))


if __name__ == '__main__':
    initialize()
    main()
