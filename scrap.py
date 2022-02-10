import csv
from getpass import getpass
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome



#Created By JuanPCabana


def get_tweet_data(tweet):
    #se extrae el tweet con esta funcion
    
    #se extraen los parametros del tweet (autor, usuario)
    username = tweet.find_element_by_xpath('.//span').text
    account = tweet.find_element_by_xpath('.//span[contains(text(), "@")]').text
    text = ''
    videolink = ''
    imglink = ''
    
    #aqui se pone una condicional que hace que si el tweet no tiene fecha, no lo almacene, ya que normalmente son anuncios
    try:
        date = tweet.find_element_by_xpath('.//time').get_attribute('datetime')
    except NoSuchElementException:
        return


    #se extrae la primera parte del tweet (en respuesta a..., texto del tweet)
    replying = tweet.find_element_by_xpath('.//div[2]/div[2]/div[2]/div[1]//div[@dir="auto"]').text
    text = replying
    
    try:
        reply = tweet.find_element_by_xpath('.//div[2]/div[2]/div[2]/div[2]/div/span').text    
        text = replying + ' .. ' + reply
    except NoSuchElementException:
        sleep(0)
    
    #se extrae la segunda parte del tweet (enlaces)

    try:
        responding = tweet.find_element_by_xpath('.//link').get_attribute('href')
        text= text+' link: '+responding
    except NoSuchElementException:
        sleep(0)
    try:
        responding = tweet.find_element_by_xpath('.//div[2]/div[2]/div[2]/div[2]//video').get_attribute('src')
        videolink=' link video: '+responding
            
    except NoSuchElementException:
            sleep(0)
    try:
        responding = tweet.find_element_by_xpath('.//div[2]/div[2]/div[2]/div[2]//img').get_attribute('src')
        imglink=' link imagen: '+responding
            
    except NoSuchElementException:
        sleep(0)
    
    #se extraen la cantidad de comentarios, retweets y likes.
    
    reply_cnt = tweet.find_element_by_xpath('.//div[@data-testid="reply"]').text
    retweet_cnt = tweet.find_element_by_xpath('.//div[@data-testid="retweet"]').text
    like_cnt = tweet.find_element_by_xpath('.//div[@data-testid="like"]').text
    
    info = (username, account, text, imglink, videolink, reply_cnt, like_cnt, retweet_cnt, date)
    return info

#se crea una instancia del navegador
driver = Chrome()
sleep(2)


#se entra en twitter
driver.get('http://www.twitter.com/login')
sleep(4)
#se inicia sesion
my_username = driver.find_element_by_xpath('//input[@autocomplete="username"]')
my_username.send_keys('El_Juanchozz')
my_username.send_keys(Keys.RETURN)

my_password = 'Juan tiene 2 hermanos.'
sleep(4)
password = driver.find_element_by_xpath('//input[@name="password"]')
password.send_keys(my_password)
password.send_keys(Keys.RETURN)

print("Ingrese El Topico A Scrappear: ", end="")
search = input()

scraps = input("ingresa la cantidad de tweets a extraer: ")

#se hace la busqueda
try:
    driver.find_element_by_xpath('//a[@aria-label="Buscar y explorar"]').click()
    sleep(5)
    
    search_input = driver.find_element_by_xpath('//input[@aria-label="Búsqueda"]')
    search_input.send_keys(search)
    search_input.send_keys(Keys.RETURN)
    
except NoSuchElementException:  #esto es por si el navegador esta en pantalla completa o no
    
    search_input = driver.find_element_by_xpath('//input[@aria-label="Búsqueda"]')
    search_input.send_keys(search)
    search_input.send_keys(Keys.RETURN)

    
#nos vamos a la pestana de tweets mas recientes
driver.find_element_by_link_text('Más reciente').click()

#se obtienen todos los tweets de la pagina
data = []
card_ids = set()
last_position = driver.execute_script("return window.pageYOffset;")
scrolling = True

while len(data) < int(scraps):
    
    page_cards = driver.find_elements_by_xpath('//article[@data-testid="tweet"]')
    
    for tweet in page_cards[-15:]:
        card = get_tweet_data(tweet)
        if card:
            card_id = ' '.join(card)
            if card_id not in card_ids:
                card_ids.add(card_id)
                data.append(card)

    driver.execute_script('window,scrollTo(0, document.body.scrollHeight)')
    sleep(2)
    
print("Almacenado en base de datos...", end="")
#se guarda en un archivo csv    
with open(search+'_tweets.csv', 'w', newline='', encoding='utf-8') as f:
    header = ['username', 'account', 'text', 'comments', 'likes', 'retweets', 'date']
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data[0:int(scraps)])

driver.close()
exit()