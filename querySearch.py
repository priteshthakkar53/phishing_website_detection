
from googlesearch import search

query = "paypal"

for j in search(query, tld="co.in", num=20, stop=1, pause=2):
	print(j)
