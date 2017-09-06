
import mechanize
import BeautifulSoup

br = mechanize.Browser()
br.open("http://www.example.com/gestione")
#response = br.response()
#response.geturl()
#br.select_form('login_form')
br.select_form(nr=0)

br.form['email'] = 'xxxxxxxxxxxxxxxxxxxxxxx'
br.form['passwd'] = 'yyyyyyyyyyyyyyyy'
br.submit()

br.find_link(text='Clienti')
req = br.click_link(text='Clienti')
br.open(req)
print br.response().read()

r = br.open("http://www.somewebsite.com")
br.find_link(text='Click this link')
req = br.click_link(text='Click this link')
br.open(req)
print br.response().read()

for link in br.links():
    print link.text, link.url


request = br.click_link(link)
response = br.follow_link(link)
response.geturl()

br.find_link(url_regex='viewcustomer')
br.links(url_regex='viewcustomer')  # elenco clienti prima pagina


