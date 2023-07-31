import requests
from bs4 import BeautifulSoup
import smtplib
import time
def send_email(product_name, current_price, product_link, receiver_email):
    sender_email = 'harini23604@gmail.com'
    sender_password = 'redacted'
    subject = f'Myntra Price Drop Alert: {product_name}'
    body = f'Price dropped to {current_price}\n\n{product_link}'
    message = f'Subject: {subject}\n\n{body}'
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message)
        print('Email sent successfully!')
    except Exception as e:
        print('Error sending email:', str(e))
    finally:
        server.quit()
      
def track_myntra_price(product_link, desired_price, receiver_email):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
    page = requests.get(product_link, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    product_name = soup.find('h1', {'class': 'pdp-title'}).text.strip()
    current_price = float(soup.find('span', {'class': 'pdp-price'}).text.strip()[1:].replace(',', ''))
    if current_price <= desired_price:
        send_email(product_name, current_price, product_link, receiver_email)
    else:
        print('Price is still higher than the desired price.')

if __name__ == "__main__":
    product_link = input("Enter the Myntra product link: ")
    desired_price = float(input("Enter your desired price: "))
    receiver_email = input("Enter your email address: ")
    
    while True:
        track_myntra_price(product_link, desired_price, receiver_email)
        time.sleep(86400)  

