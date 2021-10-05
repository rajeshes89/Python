
import requests
from bs4 import BeautifulSoup

#user = input("Enter github user :: \n")
user = "rajeshes89"
url = "https://github.com/{0}".format(user)
print(url)
r = requests.get(url)
soup = BeautifulSoup(r.content,'html.parser')

profile_image = soup.find('img',{'alt' : 'Avatar'})['src'] #taken from inspect element
print(profile_image)