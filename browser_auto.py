import os
import time as time
import numpy as np
import pyautogui
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import json

from solve_maze import solve_maze

""" Setup Browser """
start_time = time.perf_counter()
options = webdriver.ChromeOptions()
dc = DesiredCapabilities.CHROME
dc['goog:loggingPrefs'] = {'browser': 'ALL'}
options.add_argument("--start-maximized")
options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
browser = webdriver.Chrome(options=options, service_args=[f'--log-path=/log_file.txt', ],desired_capabilities=dc)

""" Visit Challenge HomePage """
step00 = browser.get("http://54.80.137.197:5000/")

""" Start Challenge """
print(" Starting Challenge . . .")
step01 = browser.find_element_by_css_selector("a[href*='intro']").click()


""" Ahoy Matey Challenge """
print(" Ahoy Matey Challenge . . .")
step02 = browser.find_element_by_css_selector('button[id="start"]').click()


""" Random Access Challenge """
print(" Random Access Challenge  . . .")
for i in range(5):
    val = i + 1
    button = 'button[id="c1submitbutton' + str(val) + '"]'
    try:
        step03 = browser.find_element_by_css_selector(button).click()
    except NoSuchElementException:
        break


""" A Video Player Challenge """
print(" A Video Player Challenge  . . .")
browser.switch_to.frame(browser.find_element_by_xpath('//iframe[starts-with(@src, "https://www.youtube.com/embed")]'))
WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Play"]'))).click()
browser.switch_to.default_content()
time.sleep(7)
pyautogui.moveTo(1005, 655, 2)
element_to_hover = browser.find_element(By.ID, 'aVideoPlayer')
hover = ActionChains(browser).move_to_element(element_to_hover)
hover.perform()
browser.switch_to.frame(browser.find_element_by_xpath('//iframe[starts-with(@src, "https://www.youtube.com/embed")]'))
WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Mute (m)"]'))).click()
browser.switch_to.default_content()
step04 = browser.find_element_by_css_selector('button[id="aVideoSubmit"]').click()

""" Crystal Maze Challenge """
print(" Crystal Maze Challenge  . . .")
maze = []
start_cell = []
table_id = browser.find_element(By.ID, 'maze')
rows = table_id.find_elements(By.TAG_NAME, "tr") # get all of the rows in the table
for row in rows:
    # Get the columns (all the column 2)
    col = row.find_elements(By.TAG_NAME, "td") #[1] #note: index start from 0, 1 is col 2
    row = []
    for cell in col:

        #print(col.text) #prints text from the element
        try:
            item = cell.get_attribute("class")
            words = item.split(" ")
            if len(words) <= 2 :
                row.append(1)
            elif words[2] == "deep-purple":
                row.append(2)
            elif words[2] == "black":
                row.append(1)
            elif words[2] == "blue-grey":
                row.append(0)
            elif words[2] == "green":
                row.append(3)
            else:
                row.append(1)
        except:
            continue

    maze.append(row)

maze_puzzle = np.array(maze)
maze_solution = solve_maze(maze_puzzle)
# print("Maze solution")
# print(maze_solution)
for step in maze_solution:
    if step == 0 :
        browser.find_element_by_xpath("//a[contains(@onclick, 'up')]").click()
    elif step == 1 :
        browser.find_element_by_xpath("//a[contains(@onclick, 'down')]").click()
    elif step == 2:
        browser.find_element_by_xpath("//a[contains(@onclick, 'left')]").click()
    elif step == 3:
        browser.find_element_by_xpath("//a[contains(@onclick, 'right')]").click()
    else:
        pass
    #time.sleep(1)

step05 = browser.find_element_by_css_selector('button[id="crystalMazeFormSubmit"]').click()


""" Focus on Map Challenge """
print(" Focus on Map Challenge  . . .")
actions = ActionChains(browser)
# actions.send_keys(Keys.TAB)
# actions.perform()
WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='map']"))).click()
#browser.find_element_by_partial_link_text("OpenLayers_Layer_Vector_").click()
#browser.find_element_by_xpath('/').click()
#starts-with(@src, "https://www.youtube.com/embed")] /*[name()="svg"]
# //*[@id="OpenLayers_Layer_Vector_25_svgRoot"]
# #OpenLayers_Layer_Vector_25_svgRoot
#image_click = browser.find_element_by_tag_name('olTileImage').click()
# actions.send_keys('i')
browser.find_element_by_xpath("//div[@id='map']").send_keys('i')
# actions.send_keys('I')

elem = browser.find_element_by_tag_name('circle')
# tag_value1 = elem.get_attribute('cx')
# tag_value2 = elem.get_attribute('cy')
# tag_value3 = elem.get_attribute('r')
element_id = elem.get_attribute('id')
# print("element found with tag value = " + str(tag_value1) + " " + str(tag_value2) + " " + str(tag_value3))
# elem = browser.find_element_by_id(element_id)
elem1 = "document.getElementById('"+str(element_id)+"').setAttribute('cy', 98.5);"
elem2 = "document.getElementById('"+str(element_id)+"').setAttribute('cx', 367);"
elem3 = "document.getElementById('"+str(element_id)+"').setAttribute('r', 6);"
browser.execute_script(elem1)
browser.execute_script(elem2)
browser.execute_script(elem3)
# print("element after with tag value = " + str(tag_value1) + " " + str(tag_value2) + " " + str(tag_value3))

step06 = browser.find_element_by_css_selector('button[id="mapsChallengeSubmit"]').click()


""" Not a Bot Challenge """
print(" Not a Bot Challenge  . . .")
entries = browser.get_log('browser')
# print(type(entries))
newDict = entries[len(entries)-1]
words = newDict['message'].split()
word = words[2].strip()
word = json.loads(word)
browser.find_element_by_id("notABotCaptchaResponse").send_keys(word)
step07 = browser.find_element_by_css_selector('button[id="notABotCaptchaSubmit"]').click()


""" Socket Gate Challenge """
print(" Socket Gate Challenge  . . .")
script = """
x = document.getElementsByClassName("yellow");
console.log(x[0].textContent);
"""
browser.execute_script(script)
entries2 = browser.get_log('browser')
# print(type(entries))
newDict2 = entries2[len(entries2)-1]
words = newDict2['message'].split()
word = words[4].strip()
message_text = word.replace("\\n", "")
message_text = message_text.strip()
# print(message_text)
script = """
var webSocket = new WebSocket('ws://54.80.137.197:5001');
webSocket.onopen = function(e) { webSocket.send('""" + str(message_text) + """');}
webSocket.onmessage = function(e) { console.log(e.data); }
webSocket.onclose = function(e) { console.log(e.data); }
"""

browser.execute_script(script)
time.sleep(1)
entries3 = browser.get_log('browser')
newDict3 = entries3[len(entries3)-1]
words = newDict3['message'].split()
word = words[2].strip()
message_text = json.loads(word)
message_text = message_text.strip()


script = "x = document.getElementById('socketGateMessage'); x.value = '"+str(message_text)+"';"
time.sleep(1)
# browser.execute_script(script)
WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, "socketGateMessage"))).click()
browser.find_element_by_id("socketGateMessage").send_keys(message_text)
time.sleep(1)

step08 = browser.find_element_by_tag_name('button').click()

print("Found the Treasure ! ")
Time_Taken = time.perf_counter() - start_time
print(str(Time_Taken) + " seconds to complete the challenge")
