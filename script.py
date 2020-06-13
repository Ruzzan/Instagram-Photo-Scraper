import requests
import os
from selenium import webdriver
from getpass import getpass
import time
from conf import OUTPUTS

# logging in 
def Login():
    url = "https://instagram.com"
    reciever_url = "https://www.instagram.com/{}/".format(reciever)
    driver.get(url)
    time.sleep(1)

    USERNAME = driver.find_element_by_name("username").send_keys(username)
    PASSWORD = driver.find_element_by_name("password").send_keys(password)

    login_btn = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[4]/button')
    login_btn.click()

    time.sleep(5)
    
    print("Logged In")
    # going to instagram  to avoid save password section
    driver.get(url)
    
    # this will handle the not now in turn on notificcation or not modal
    try:
        not_now_btn = driver.find_element_by_xpath("/html/body/div[4]/div/div/div[3]/button[2]")
        not_now_btn.click()
        print('not now')
    except:
        pass

    # go to recievers profile section  and click the message the button 
    driver.get(reciever_url)

def ScrapeDetails():
    username = driver.find_elements_by_tag_name("h2")
    detail_div = driver.find_element_by_class_name("-vDIg")
    full_name = detail_div.find_element_by_tag_name("h1").text
    bio = detail_div.find_element_by_tag_name("span").text    
    followers_posts = driver.find_elements_by_class_name("Y8-fY ")

    for i in range(0, len(username)):
        print(f"Username: {username[0].text}")
    
    print(f"Full Name: {full_name}")
    print(f"Bio: {bio}")
    for data in followers_posts:
        print(data.text)

def ScrollPage():
    # Scroll test 
    SCROLL_PAUSE_TIME = 10

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(SCROLL_PAUSE_TIME)

        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            print("Images Scanned")
            break
        
        last_height = new_height

def ScrapeImage():
    images = driver.find_elements_by_class_name("FFVAD")

    images_to_download = []
    for i,image in enumerate(images):
        image_source =  image.get_attribute("src")
        images_to_download.append(image_source)

    DOWNLOAD_PATH = os.path.join(OUTPUTS, reciever)
    os.makedirs(DOWNLOAD_PATH, exist_ok=True)

    try:
        profile_pic      = driver.find_element_by_class_name("be6sR")
        profile_pic_src  = profile_pic.get_attribute("src")
    except:
        profile_pic      = driver.find_element_by_class_name("_6q-tv")
        profile_pic_src  = profile_pic.get_attribute("src")


    profile_pic_name    = os.path.join(DOWNLOAD_PATH, "pp.jpg") 

    with open(profile_pic_name, 'wb') as f:
        r = requests.get(profile_pic_src)
        f.write(r.content)

    print('Profile Picture Downloaded')

    if profile_pic.get_attribute("class") == "be6sR":
        print("It is a private account you haven't followed. Cannot Download Images.")
    else:
        print('Downloading images......')
        for index,download in enumerate(images_to_download):
            image_name = os.path.join(DOWNLOAD_PATH, f"{index+1}.jpg")
            # urllib.request.urlretrieve(download, image_name)
            r = requests.get(download)
            with open(image_name, 'wb') as f:
                f.write(r.content)
            print(f"Image-{index+1} downloaded..")
            time.sleep(2)

if __name__ == "__main__":
    print("Login to download photos of private accounts you follow.")
    login_inp = str(input("Login?\ny / n:"))
    if login_inp.lower() == "y":
        username = str(input('enter username:'))
        password = str(getpass(prompt="enter password:"))
        reciever = str(input('person2 username:'))
        # Your chromedriver path 
        PATH   = "C:\Program Files (x86)\chromedriver.exe"
        driver = webdriver.Chrome(PATH)
        Login()
        ScrapeDetails()
        ScrollPage()
        ScrapeImage()
        driver.quit()

    elif login_inp.lower() == "n":
        reciever = str(input("person-2 username:"))
        # Your chromedriver path 
        PATH   = "C:\Program Files (x86)\chromedriver.exe"
        driver = webdriver.Chrome(PATH)
        reciever_url = "https://www.instagram.com/{}/".format(reciever)
        driver.get(reciever_url)
        time.sleep(1)
        ScrapeDetails()
        ScrollPage()
        ScrapeImage()
        driver.quit()

    

    





