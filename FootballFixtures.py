from selenium import webdriver
from pynput.keyboard import Key, Controller
import time

url = 'https://www.bbc.co.uk/sport/football/teams/hibernian/scores-fixtures'
driver = webdriver.Chrome()
driver.get(url)

#Empty list soon to be populated with details of upcoming football fixtures
Matches = []

#Variables for switching between months in the season
XPATH = '//*[@id="sp-timeline-future-dates"]/li[1]'
counter = 1

######################Still need to make this today-proof#####################

#Hibs fixtures
#While not in June:
while (driver.find_element_by_xpath(XPATH).text[0:3] != "JUN"):

    time.sleep(5) #Have a wee rest to make sure the page loads fixtures each month
    #Find matches in this month and add their details to the Matches list
    MatchesThisMonth = driver.find_elements_by_class_name('qa-match-block')

    #Pick out details of each match
    for i in range(len(MatchesThisMonth)):
        Match = MatchesThisMonth[i]
        Date = Match.find_element_by_class_name('gel-pica-bold').text
        Competition = Match.find_element_by_class_name('sp-c-match-list-heading').text
        HomeTeam = Match.find_element_by_class_name('sp-c-fixture__team--time-home').text
        AwayTeam = Match.find_element_by_class_name('sp-c-fixture__team--time-away').text
        KickOff = Match.find_element_by_class_name('sp-c-fixture__block--time').text
        Matches.append(Competition + "," + HomeTeam + "," + AwayTeam + "," + Date + "," + KickOff)

    #Next Month coming up
    XPATH = '//*[@id="sp-timeline-future-dates"]/li[' + str(counter) + ']'
    driver.find_element_by_xpath(XPATH).click()
    counter = counter + 1

    
#Arsenal games now
url = 'https://www.bbc.co.uk/sport/football/teams/arsenal/scores-fixtures'
driver.get(url)

#Reset variables for switching between months in the season
XPATH = '//*[@id="sp-timeline-future-dates"]/li[1]'
counter = 1

#While not in June:
while (driver.find_element_by_xpath(XPATH).text[0:3] != "JUN"):

    time.sleep(5) #Have a wee rest to make sure the page loads fixtures each month
    #Find matches in this month and add their details to the Matches list
    MatchesThisMonth = driver.find_elements_by_class_name('qa-match-block')

    #Pick out details of each match
    for i in range(len(MatchesThisMonth)):
        Match = MatchesThisMonth[i]
        Date = Match.find_element_by_class_name('gel-pica-bold').text
        Competition = Match.find_element_by_class_name('sp-c-match-list-heading').text
        HomeTeam = Match.find_element_by_class_name('sp-c-fixture__team--time-home').text
        AwayTeam = Match.find_element_by_class_name('sp-c-fixture__team--time-away').text
        KickOff = Match.find_element_by_class_name('sp-c-fixture__block--time').text
        Matches.append(Competition + "," + HomeTeam + "," + AwayTeam + "," + Date + "," + KickOff)

    #Next Month coming up
    XPATH = '//*[@id="sp-timeline-future-dates"]/li[' + str(counter) + ']'
    driver.find_element_by_xpath(XPATH).click()
    counter = counter + 1


#Close the Chrome window
driver.close()


#Setup the keyboard for the next bit!
keyboard = Controller()

#Open calendar
with keyboard.pressed(Key.cmd):
    keyboard.press(Key.space)
    keyboard.release(Key.enter)

time.sleep(2)
keyboard.type("Calendar")
keyboard.press(Key.enter)


#Create Calender events for each match
for i in range(len(Matches)):
    time.sleep(2)
    Competition, HomeTeam, AwayTeam, Date, Time = Matches[i].split(",")

    #Create new event (shortcut)
    with keyboard.pressed(Key.cmd):
        keyboard.press('n')

    #Enter the event details    
    keyboard.type(HomeTeam + " vs " + AwayTeam + " @ " + Time + " " + Date)
    keyboard.press(Key.enter)
    time.sleep(1)
    keyboard.press(Key.enter)
    time.sleep(1)
    keyboard.press(Key.tab)
    time.sleep(1)
    keyboard.type(Competition)
    keyboard.press(Key.enter)


#Quit Calendar app - time for Python bye-bye!
with keyboard.pressed(Key.cmd):
    keyboard.press('q')
