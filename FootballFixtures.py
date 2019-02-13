from selenium import webdriver
from pynput.keyboard import Key, Controller
import time, datetime

url = 'https://www.bbc.co.uk/sport/football/teams/hibernian/scores-fixtures'
driver = webdriver.Chrome()
driver.get(url)

#Empty list soon to be populated with details of upcoming football fixtures
Matches = []

#Variables for switching between months in the season
XPATH = '//*[@id="sp-timeline-future-dates"]/li[1]'
xpDigit = 0
counter = 1

#Today's date for ensuring that games in the second half of the season are placed in the correct calendar year
#Also used as the date for games that are happening on the day of the script being executed
Today = datetime.datetime.now()


#Hibs fixtures
#While not in June:
while (driver.find_element_by_xpath(XPATH).text[0:3] != "JUN"):

    time.sleep(5) #Have a wee rest to make sure the page loads fixtures each month
    #Find matches in this month and add their details to the Matches list
    MatchesThisMonth = driver.find_elements_by_class_name('qa-match-block')

    #Pick out details of each match
    for i in range(len(MatchesThisMonth)):
        Match = MatchesThisMonth[i]
        try:
            Date = Match.find_element_by_class_name('gel-pica-bold').text
        except:
            Date = Today.strftime("%A %d %B %Y")
            try:
                print(driver.find_element_by_xpath('//*[@id="sp-timeline-current-dates"]/li[3]').text)
                xpDigit = 2
                XPATH = '//*[@id="sp-timeline-current-dates"]/li[' + str(xpDigit) + ']'
            except:
                print("Today is the first match of this month.")
                xpDigit = 1
                XPATH = '//*[@id="sp-timeline-current-dates"]/li[' + str(xpDigit) + ']'
                      
        Competition = Match.find_element_by_class_name('sp-c-match-list-heading').text

        try:
            HomeTeam = Match.find_element_by_class_name('sp-c-fixture__team--time-home').text
            AwayTeam = Match.find_element_by_class_name('sp-c-fixture__team--time-away').text
        except:
            #Handles matches that have already kicked off / been played
            HomeTeam = Match.find_element_by_class_name('sp-c-fixture__team--home').text[:-2]
            AwayTeam = Match.find_element_by_class_name('sp-c-fixture__team--away').text[:-2]
        
        try:
            KickOff = Match.find_element_by_class_name('sp-c-fixture__block--time').text
        except:
            #If match has already been played / is in progress, just set it to the current hour
            KickOff = str(Today.strftime("%H") + ':00')

        Matches.append(Competition + "," + HomeTeam + "," + AwayTeam + "," + Date + "," + KickOff)

    if(driver.find_element_by_xpath(XPATH).text[0:5] != "TODAY"):
        #Next Month coming up
        XPATH = '//*[@id="sp-timeline-future-dates"]/li[' + str(counter) + ']'
        driver.find_element_by_xpath(XPATH).click()
        counter = counter + 1
    else:
        XPATH = '//*[@id="sp-timeline-current-dates"]/li[' + str(xpDigit + 1) + ']'
        driver.find_element_by_xpath(XPATH).click()

    
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
        try:
            Date = Match.find_element_by_class_name('gel-pica-bold').text
        except:
            Date = Today.strftime("%A %d %B %Y")
            try:
                print(driver.find_element_by_xpath('//*[@id="sp-timeline-current-dates"]/li[3]').text)
                xpDigit = 2
                XPATH = '//*[@id="sp-timeline-current-dates"]/li[' + str(xpDigit) + ']'
            except:
                print("Today is the first match of this month.")
                xpDigit = 1
                XPATH = '//*[@id="sp-timeline-current-dates"]/li[' + str(xpDigit) + ']'
                      
        Competition = Match.find_element_by_class_name('sp-c-match-list-heading').text

        try:
            HomeTeam = Match.find_element_by_class_name('sp-c-fixture__team--time-home').text
            AwayTeam = Match.find_element_by_class_name('sp-c-fixture__team--time-away').text
        except:
            #Handles matches that have already kicked off / been played
            HomeTeam = Match.find_element_by_class_name('sp-c-fixture__team--home').text[:-2]
            AwayTeam = Match.find_element_by_class_name('sp-c-fixture__team--away').text[:-2]
        
        try:
            KickOff = Match.find_element_by_class_name('sp-c-fixture__block--time').text
        except:
            #If match has already been played / is in progress, just set it to the current hour
            KickOff = str(Today.strftime("%H") + ':00')

        Matches.append(Competition + "," + HomeTeam + "," + AwayTeam + "," + Date + "," + KickOff)

    if(driver.find_element_by_xpath(XPATH).text[0:5] != "TODAY"):
        #Next Month coming up
        XPATH = '//*[@id="sp-timeline-future-dates"]/li[' + str(counter) + ']'
        driver.find_element_by_xpath(XPATH).click()
        counter = counter + 1
    else:
        XPATH = '//*[@id="sp-timeline-current-dates"]/li[' + str(xpDigit + 1) + ']'
        driver.find_element_by_xpath(XPATH).click()

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
keyboard.release(Key.enter)


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
    keyboard.release(Key.enter)
    time.sleep(2)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(2)
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)
    time.sleep(2)
    keyboard.type(Competition)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)


#Quit Calendar app - time for Python bye-bye!
with keyboard.pressed(Key.cmd):
    keyboard.press('q')
