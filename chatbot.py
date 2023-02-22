import os
import time
import gspread
import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from oauth2client.service_account import ServiceAccountCredentials

creds = ServiceAccountCredentials.from_json_keyfile_name('config\service_account.json', ['https://www.googleapis.com/auth/spreadsheets'])
client = gspread.authorize(creds)

options = webdriver.ChromeOptions() 
options.add_argument("user-data-dir=/profile")
options.add_argument('--profile-directory=chatbot')
options.add_argument('disable-notifications')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://web.whatsapp.com/")
esperar = WebDriverWait(driver, 600)
esperar.until(EC.presence_of_element_located((By.XPATH, '//span[@title="fixado"]')))
driver.find_element(By.XPATH, '//span[@title="fixado"]').click()
while auxiliar == 0:
    esperar.until(EC.presence_of_element_located((By.XPATH, '//span[@data-testid="icon-unread-count"]')))
    unread_mark = driver.find_element(By.XPATH, '//span[@data-testid="icon-unread-count"]')
    if unread_mark:
        unread_mark.click()
        time.sleep(1)
        contato = driver.find_element(By.XPATH, '//span[@data-testid="conversation-info-header-chat-title"]').text
        sheet = client.open_by_key("1hucsZFHb2lIjJ3vQae_hxy6SP6J9dUrE2368cD_4v3w")
        worksheet = sheet.get_worksheet(0)
        contatoExiste = worksheet.find(contato)
        if contatoExiste:
            status = worksheet.cell(contatoExiste.row, 6).value
            if status == 'FECHADO':
                worksheet.update_cell(contatoExiste.row, 6, 'ABERTO')
                worksheet.update_cell(contatoExiste.row, 3, str(datetime.datetime.today().strftime('%H:%M:%S')))
                worksheet.update_cell(contatoExiste.row, 5, str(datetime.datetime.today().strftime('%H:%M:%S')))
                with open(os.getcwd() + '/config/messages/1.txt', 'r', encoding='utf-8') as f:
                    worksheet.update_cell(contatoExiste.row, 4, '1')
                    mensagem = f.read()
            else:
                worksheet.update_cell(contatoExiste.row, 3, str(datetime.datetime.today().strftime('%H:%M:%S')))
                worksheet.update_cell(contatoExiste.row, 5, str(datetime.datetime.today().strftime('%H:%M:%S')))
                elementos = driver.find_elements(By.XPATH, "//div[@class='_21Ahp']")
                comprimento = len(elementos)
                resposta = driver.find_element(By.XPATH, f'(//div[@class="_21Ahp"])[{comprimento}]')
                ultima_mensagem = resposta.text
                ultima_resposta = worksheet.cell(contatoExiste.row, 4).value # ultima resposta do robo
                if ultima_resposta == '1':
                    if ultima_mensagem == '1':
                        with open(os.getcwd() + '/config/messages/1.1.txt', 'r', encoding='utf-8') as f:
                            worksheet.update_cell(contatoExiste.row, 4, '1.1')
                            mensagem = f.read()
                    elif ultima_mensagem == '2':
                        worksheet.update_cell(contatoExiste.row, 6, 'FECHADO')
                        with open(os.getcwd() + '/config/messages/1.2.txt', 'r', encoding='utf-8') as f:
                            worksheet.update_cell(contatoExiste.row, 4, '1.2')
                            mensagem = f.read()
                    else:
                        mensagem = "Desculpe, estou com dificuldades para entender o que você está dizendo. Pode tentar novamente. Lembre-se, digite somente o número da opção."
                elif ultima_resposta == '1.1':
                    with open(os.getcwd() + '/config/messages/2.txt', 'r', encoding='utf-8') as f:
                        worksheet.update_cell(contatoExiste.row, 4, '2')
                        mensagem = f.read()
                elif ultima_resposta == '2':
                    with open(os.getcwd() + '/config/messages/3.txt', 'r', encoding='utf-8') as f:
                        worksheet.update_cell(contatoExiste.row, 4, '3')
                        mensagem = f.read()
                elif ultima_resposta == '3':
                    with open(os.getcwd() + '/config/messages/4.txt', 'r', encoding='utf-8') as f:
                        worksheet.update_cell(contatoExiste.row, 4, '4')
                        mensagem = f.read()
                elif ultima_resposta == '4':
                    with open(os.getcwd() + '/config/messages/5.txt', 'r', encoding='utf-8') as f:
                        worksheet.update_cell(contatoExiste.row, 4, '5')
                        mensagem = f.read()
                else:
                    with open(os.getcwd() + '/config/messages/6.txt', 'r', encoding='utf-8') as f:
                        worksheet.update_cell(contatoExiste.row, 4, '6')
                        mensagem = f.read()
        else:
            vazio = worksheet.acell('G4').value
            worksheet.update_cell(str(vazio), 1, str(contato))
            worksheet.update_cell(str(vazio), 3, str(datetime.datetime.today().strftime('%H:%M:%S')))
            worksheet.update_cell(str(vazio), 5, str(datetime.datetime.today().strftime('%H:%M:%S')))
            worksheet.update_cell(str(vazio), 6, "ABERTO")
            with open(os.getcwd() + '/config/messages/1.txt', 'r', encoding='utf-8') as f:
                worksheet.update_cell(str(vazio), 4, '1')
                mensagem = f.read()
        esperar.until(EC.presence_of_element_located((By.XPATH, '//div[@title="Mensagem"]')))
        message_field = driver.find_element(By.XPATH, '//div[@title="Mensagem"]')
        message_field.click()
        message_field.send_keys(mensagem)
        message_field.send_keys(Keys.ENTER)
        driver.find_element(By.XPATH, '//span[@title="fixado"]').click()
        auxiliar = 1
    else:
        time.sleep(5)