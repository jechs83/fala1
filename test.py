from requests_html import HTMLSession
session = HTMLSession()

r = session.get('https://www.oechsle.pe/tecnologia')
r.html.render()

print( r.html.xpath("/html[1]/body[1]/main[1]/div[8]/section[2]/div[1]/div[2]/div[4]/div[1]/div[2]/div[2]/div[1]/ul[1]/li[1]/div[1]/div[2]/div[4]/div[4]/div[2]/span[1]"))