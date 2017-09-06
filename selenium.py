
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Firefox()
driver.get("http://www.example.com/gestione")

driver.find_element_by_name("email").send_keys('xxxxxxxxxxx')
driver.find_element_by_name("passwd").send_keys('yyyyyyyyy')
driver.find_element_by_name("submitLogin").click()

# vai manualmente alla pagina clienti nr 0
driver.get("http://www.example.com/gestione/index.php?controller=AdminCustomers&token=xxxxxxxxxxxxxxxxxxxxxxx")

# vai alla pagina clienti nr 2
driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[1]/form/table/tbody/tr[1]/td/span[1]/input[1]").click()

txt = driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[1]/form/table/tbody/tr[2]/td/table/tbody/tr[1]/td[4]").text

# prepara le variabili
xp = "/html/body/div[2]/div/div[2]/div[1]/form/table/tbody/tr[2]/td/table/tbody/"
#xp + "tr[x]" + "/td[y]"
tab = [] # elenco link per cliente
for z in range(1,50):
	for x in range(1,51):
		row = []
		for y in [2,4,5,6]:
			row.append(driver.find_element_by_xpath(xp + "tr["+str(x)+"]" + "/td["+str(y)+"]").text)
		row.append(driver.find_element_by_xpath(xp + "tr["+str(x)+"]" + "/td[13]/a[2]").get_attribute("href"))
		tab.append(row)
	if z==1:
		driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[1]/form/table/tbody/tr[1]/td/span[1]/input[1]").click()
	driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[1]/form/table/tbody/tr[1]/td/span[1]/input[3]").click()
# elenco prodotti per cliente
prod_customer = {}
for r in range(len(tab)):
	driver.get(tab[r][4])
	try:
		x = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div[3]/div[19]/table').text
		prod_customer[tab[r][0]] = x
	except Exception as e:
		print e
		continue

	#prod_customer[tab[r][0]] = driver.find_element_by_xpath('//*[@id="container-customer"]/div[19]/table').text

try:
        webdriver.find_element_by_xpath(xpath)
except NoSuchElementException:
        return False
return True


if len(driver.find_elements_by_xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div[3]/div[19]/table')) > 0:
    print "Element exists"
	driver.find_element_by_xpath('//*[@id="container-customer"]/div[19]/table/tbody/tr[1]/td[2]')
driver.find_element_by_xpath('//*[@id="container-customer"]/div[19]/table/tbody/tr[1]/td[1]')




driver.quit()
