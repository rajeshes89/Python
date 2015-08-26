import requests
import urllib3
import re
#out = requests.get("https://www.quora.com/How-can-I-learn-programming-3")
#value = out.text
#upvoteCounts = re.findall("\d+ upvotes",value)
#print(upvoteCounts)

#page =urllib2.urlopen("https://www.quora.com/How-can-I-learn-programming-3")
#data = page.read()

http = urllib3.PoolManager()
out = http.request('GET',"http://www.quora.com/How-can-I-learn-programming-3")
value1 = out.data
value2 = value1.decode('UTF-8')
#upvoteCounts = re.findall("\<[\s\S]+\>\d+ upvotes",value2)
#upvoteCounts = re.findall("\>(\d+ upvotes)[\s\S]+href=(\"[\s\S]+\") ",value2)
upvoteCounts = re.findall(">(\d+ upvotes)</a></span><span class=\"\w+\"> \&bull; </span><span id=\"[\s\S]+\"><a class=\".*\" href=\"([\s\S]+)\" action_mousedown",value2)
print(upvoteCounts)
#re.findall(">(\d+ upvotes)</a></span><span class=\"\w+\"> \&bull; </span><span id=\"[\s\S]+\"><a class=\".*\" href=\"([\s\S]+)\" action_mousedown=\"\w+\" id=\"[\s\S]+\">[Updated|Written]",out)
