# -- coding = utf-8 --

from selenium import webdriver

browser = webdriver.Chrome()

# info
# https://movie.douban.com/subject/26611804/ 

def subject():

	dbId = 30140571
	dbPath = "https://movie.douban.com/subject/%s/" % (dbId)
	browser.get(dbPath)
	
	# #info > span:nth-child(1) > span.attrs > a
	
	# 导演
	# //*[@id="info"]/span[1]/span[2]/a
	elem = browser.find_element_by_xpath('//*[@id="info"]/span[1]/span[2]/a[1]')
	print(elem.text)
	
	# 编辑
	# //*[@id="info"]/span[2]/span[2]/a[1]
	elem = browser.find_elements_by_xpath('//*[@id="info"]/span[2]/span[2]/a')
	for ele in elem:
		print(ele.text)

	print('\n\n主演:')
	# //*[@id="info"]/span[3]/span[2]/span[1]/a
	elem = browser.find_elements_by_xpath('//*[@id="info"]/span[3]/span[2]/span')
	for ele in elem:
		ele.style.display = 'block'
		print(ele.text)


subject()

