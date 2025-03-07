from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
import numpy, random, csv, json, os, openpyxl
from openpyxl import Workbook


expInfo = {'Subject_ID': ' ', 'Session_Number':' '} ###Change to subject id
expInfo['dateStr'] = data.getDateStr()

########present a dialogue to change params
dlg = gui.DlgFromDict(expInfo, title='Cocaine Study Stroop Test Tutorial', fixed=['dateStr'])
if dlg.OK:
    toFile('lastParams.pickle', expInfo) #save params to file for next time
else:
    core.quit() #the user hit cancel, so exit

#########Definition of Global Clock --> Used to keep track of the time words/fixation crosses appear and disappear, and GLOBAL time the first button was clicked
globalClock = core.Clock()


############make a csv file to store the data
fileName = expInfo['Subject_ID'] + '_' + expInfo['Session_Number'] + '_CocaineStroopTest_IC_Tutorial' + expInfo['dateStr']
dataFile = open('data/' + fileName + '.csv', 'w') # a simple text file with comma seperated values
dataFile.write('sequence,thisN,thisRepN,word,wordtype,number_on_screen,correctAnswer,key_pressed,correct,time_button_pressed_relative, buttonClickedList, time_word_shown_global, time_button_pressed_global, time_word_gone_global, time_cross_shown_global, time_cross_gone_global \n')
#time_fixation_cross_appeared,time_fixation_cross_stopped,duration_fixation_cross,time_word_appeared,time_word_stopped,duration_word --> Will not use these because these are frame based

#############import main.xlsx
mainlist = data.importConditions('main.xlsx')

#############get pre-seq prior from mainlist (needs to be pre because personal words will be inserted later once personal word number is determined to either be set or random)
preseq_1_2_ic = mainlist[0]
preseq_2_2_ic = mainlist[1]
preseq_3_2_ic = mainlist[2]


####################################################################################################
'''
Step 1. Load personal_words_randomization.xlsx.
    - if personal_word_randomization is "none", then proceed
Step 2. Load list_of_twelve_personal_words.xlsx twice into a 2d list. list[0] contains the list random


Everything below this line is no longer necessary because randomization only occurs once per participant, the number of times the personalized words appear in
a frame is fixed, personal word slots are fixed, and the list of 12 words must be randomized, then inserted into slots, then 12 words are randomized again, and
then inserted into remaining slots.
'''
###################################################################################################

############
def personal_word_inserter(preseq):
    preseqlist = data.importConditions(preseq["blocks"])
    for i in range(0,len(preseqlist)):
        if preseqlist[i]["word"] == None:
            #preseqlist[i] = personal_words.pop(0)
            newitem = personal_words.pop(0)
            preseqlist[i]["word"] = newitem["personal_words_order"]
            preseqlist[i]["type"] = newitem["type"]
            preseqlist[i]["number"] = newitem["number"]
            preseqlist[i]["answer"] = newitem["answer"]
    #if preseq["personal_word_number"] == "random":  ##--> Not necessary right now
        #personal_word_number_randomizer(preseqlist)  ##--> Not necessary right now
    return preseqlist 

###################################################################################################

seq_1_2_ic = data.TrialHandler(trialList=personal_word_inserter(preseq_1_2_ic),nReps=1,method='sequential',originPath=None)
seq_2_2_ic = data.TrialHandler(trialList=personal_word_inserter(preseq_2_2_ic),nReps=1,method='sequential',originPath=None)
seq_3_2_ic = data.TrialHandler(trialList=personal_word_inserter(preseq_3_2_ic),nReps=1,method='sequential',originPath=None)


#win = visual.Window(fullscr=True,allowGUI=True, checkTiming=True)
win = visual.Window([800,800])
#event.globalKeys.add(key=quitKey, func=forceQuit)
welcome_message = visual.TextStim(win, pos=[0,0], text='Welcome to the Stroop Test (Tutorial)! Press t to continue.')
fixation_cross = visual.TextStim(win, text="+", height=1)
instruction_1_text = 'In this task you will count the number of words you see on the screen' + '\n' + 'Then press the button as fast as you can to indicate the number of words you counted.' + '\n' + 'Let\'s practice! Press BUTTON 1 (index finger) now'
instruction_2_text = 'In this task you will count the number of words you see on the screen' + '\n' + 'Then press the button as fast as you can to indicate the number of words you counted.' + '\n' + 'Let\'s practice! Press BUTTON 2 (middle finger) now'
instruction_3_text = 'In this task you will count the number of words you see on the screen' + '\n' + 'Then press the button as fast as you can to indicate the number of words you counted.' + '\n' + 'Let\'s practice! Press BUTTON 3 (ring finger) now'
instruction_4_text = 'In this task you will count the number of words you see on the screen' + '\n' + 'Then press the button as fast as you can to indicate the number of words you counted.' + '\n' + 'Let\'s practice! Press BUTTON 4 (small finger/pinky) now'
start_screen_text = 'Great! Now let\'s start'
get_ready_text = 'Get Ready'

instruction_1_message = visual.TextStim(win, pos=[0,0], text=instruction_1_text)
instruction_2_message = visual.TextStim(win, pos=[0,0], text=instruction_2_text)
instruction_3_message = visual.TextStim(win, pos=[0,0], text=instruction_3_text)
instruction_4_message = visual.TextStim(win, pos=[0,0], text=instruction_4_text)

start_screen_message = visual.TextStim(win, pos=[0,0], text=start_screen_text)
get_ready_message = visual.TextStim(win, pos=[0,0], text=get_ready_text)
blank_infinite = visual.TextStim(win, pos=[0,0], text="")
goodbye_message = visual.TextStim(win, pos=[0,0], text="Thanks for participating!")

redo_infinite_secondtrial = visual.TextStim(win, pos=[0,0], text="You will now proceed to the second trial of the task")
redo_infinite_thirdtrial = visual.TextStim(win, pos=[0,0], text="You will now proceed to the third and last trial of the task")


#Definition of Repeating Words Function
def newWordText(increment):
    counter = int(increment["number"])
    newText = ""
    while counter > 0:
        newText += increment["word"] + "\n"
        counter -= 1
    return newText
  
#Definition of Trial Clock --> Will reset everytime a new word is shown in order to get relative time the first button was clicked
trialClock = core.Clock()


#Definition of Loop Function
def Loop(first_seq, first_seqname):
    
    #Percentage Threshold Reached (will be determined later)
    threshold_reached = None
    
    ####Main Loop###############################################################################################################################
    new_img = visual.TextStim(win, pos=[0,0], height=0.2)
    
    ##Total size of sequence
    sequence_size = 0
    
    #Correct Counter - Will be used to determine how many correct responses were made by the participant per loop
    correctCounter = 0
    
    #Desired Correct Percentage
    desiredCorrectPercentage = 80
    
    for thisIncrement in first_seq:
        
        sequence_size += 1
        
        ##Quit Button During Code
        quitbutton = event.getKeys(keyList=['q'])
        if len(quitbutton) > 0:
            for a in quitbutton:
                if a == 'q':
                    core.quit()
        
        
        buttonsClickedList = []
        displaytext = newWordText(thisIncrement)
        
        ##Setting important variables for this specific word
        new_img.text = displaytext
        word = thisIncrement["word"]
        wordtype = thisIncrement["type"]
        number_on_screen = thisIncrement["number"]
        correctAnswer = thisIncrement["answer"]
        thisN = first_seq.thisN
        thisRepN = first_seq.thisRepN

        key_pressed = None
        correct = None
        sequence = first_seqname
        time_button_pressed_relative = None
        
        time_word_shown_global = None
        time_button_pressed_global = None
        time_word_gone_global = None
        time_cross_shown_global = None
        time_cross_gone_global = None
        
        time_button_pressed_global_bool = True ##Exists to make sure that the global time for only the first button press is recorded, not all the others
        
        ##Reset trialClock Right before image is shown for 2 seconds
        trialClock.reset()

        ##The 2 seconds (120 frames) where the image is shown
        time_word_shown_global = str(globalClock.getTime())
        for x in range(120):
            
            ##Quit Button During Code
            quitbutton = event.getKeys(keyList=['q'])
            if len(quitbutton) > 0:
                for a in quitbutton:
                    if a == 'q':
                        core.quit()
            
            #new_img.text = displaytext 
            new_img.draw() 
            win.flip() 
            allKeys = event.getKeys(keyList=['2','3','4','5'], timeStamped=True) 
            if len(allKeys) > 0: 
                time_button_pressed_relative = str(trialClock.getTime()) 
                allKeys[0][1] = time_button_pressed_relative  
                buttonsClickedList.append(allKeys[0]) 
                
                if time_button_pressed_global_bool == True:
                    time_button_pressed_global = str(globalClock.getTime())
                    time_button_pressed_global_bool = False
        
        time_word_gone_global = str(globalClock.getTime())
        trialClock.reset() 
                
        if len(buttonsClickedList) > 0:
            key_pressed = buttonsClickedList[0][0]
            time_button_pressed_relative = buttonsClickedList[0][1]
        if key_pressed == None:
            correct = None
        elif int(key_pressed) == int(correctAnswer):
            correct = True
            correctCounter += 1
        else:
            correct = False
        
        #json_buttonsClickedList = json.dumps(buttonsClickedList)
        flat = '; '.join([':: '.join(sublist) for sublist in buttonsClickedList])
        
        #Write data to csv file up to time_word_gone_global
        dataFile.write(f"{sequence},{thisN},{thisRepN},{word},{wordtype},{number_on_screen},{correctAnswer},{key_pressed},{correct},{time_button_pressed_relative},{flat},{time_word_shown_global},{time_button_pressed_global},{time_word_gone_global},")
        
        ##300 ms fixation cross
        time_cross_shown_global = str(globalClock.getTime())
        for x in range(18):
            
            ##Quit Button During Code
            quitbutton = event.getKeys(keyList=['q'])
            if len(quitbutton) > 0:
                for a in quitbutton:
                    if a == 'q':
                        core.quit()
            
            fixation_cross.draw()
            win.flip()
            #Remember to record appearance of fixation cross ##Actually, maybe not...
        time_cross_gone_global = str(globalClock.getTime())
        
        #Write data to csv for time_cross_shown_global and time_cross_gone_global
        dataFile.write(f"{time_cross_shown_global},{time_cross_gone_global}\n")
    
    #Calculate the percentage of responses that were correct, and whether threshold was reached
    calculatedCorrectPercentage = 100 * (correctCounter / sequence_size)
    if calculatedCorrectPercentage >= desiredCorrectPercentage:
        threshold_reached = True
    else:
        threshold_reached = False
    
    ##Add a new line to csv file that tells you total images in sequence, how many correct, percentage correct, desired percentage threshold, and whether it passed or failed, 
    total_amount = 'total_amount:'
    amount_correct = 'amount_correct:'
    percent_correct = 'percent_correct:'
    desired_percent = 'desired_precent'
    reached_threshold = 'reached_threshold:'
    space = ''
    dataFile.write(f"{total_amount},{sequence_size},{space},{amount_correct},{correctCounter},{space},{percent_correct},{calculatedCorrectPercentage},{space},{desired_percent},{desiredCorrectPercentage},{space},{reached_threshold},{threshold_reached}\n\n")
    
    
    ##10 second pause before proceeding #####################################################################################################
    for x in range(600):
        fixation_cross.draw()
        win.flip()
        ##Quit Button During Code
        quitbutton = event.getKeys(keyList=['q'])
        if len(quitbutton) > 0:
            for a in quitbutton:
                if a == 'q':
                    core.quit()
        #Remember to record appearance of fixation cross ##Actually, maybe not...
     
    return threshold_reached
    
#1. Display Welcome Screen, infinite until "t" is pressed. Also create press_t eventKeys object
welcome_message.draw()
win.flip()
press_t = event.waitKeys(keyList="t", timeStamped=True)

#2. Display initial 300ms (18 frames) Cross Fixation
for x in range(18):
    fixation_cross.draw()
    win.flip()
    ##Quit Button During Code
    quitbutton = event.getKeys(keyList=['q'])
    if len(quitbutton) > 0:
        for a in quitbutton:
            if a == 'q':
                core.quit()
    
#3. Instruction 1
instruction_1_message.draw()
win.flip()
press_2 = event.waitKeys(keyList=["2",'q'], timeStamped=True)
if press_2[0][0] == 'q':
    core.quit()

#4. Instruction 2
instruction_2_message.draw()
win.flip()
press_3 = event.waitKeys(keyList=["3",'q'], timeStamped=True)
if press_3[0][0] == 'q':
    core.quit()

#5. Instruction 3
instruction_3_message.draw()
win.flip()
press_4 = event.waitKeys(keyList=["4", 'q'],timeStamped=True)
if press_4[0][0] == 'q':
    core.quit()

#6. Instruction 4
instruction_4_message.draw()
win.flip()
press_5 = event.waitKeys(keyList=["5", 'q'], timeStamped=True)
if press_5[0][0] == 'q':
    core.quit()

#7. Display start screen for 5 seconds (300 frames)
for x in range(300):
    
    ##Quit Button During Code
    quitbutton = event.getKeys(keyList=['q'])
    if len(quitbutton) > 0:
        for a in quitbutton:
            if a == 'q':
                core.quit()
    
    start_screen_message.draw()
    win.flip()
    
#8. Display get_ready screen for 10 seconds (600 frames)
for x in range(600):
    
    ##Quit Button During Code
    quitbutton = event.getKeys(keyList=['q'])
    if len(quitbutton) > 0:
        for a in quitbutton:
            if a == 'q':
                core.quit()
    
    get_ready_message.draw()
    win.flip()

#9. Display 300ms (18 frames) Cross Fixation Prior to Loop 1
for x in range(18):
    
    ##Quit Button During Code
    quitbutton = event.getKeys(keyList=['q'])
    if len(quitbutton) > 0:
        for a in quitbutton:
            if a == 'q':
                core.quit()
    
    fixation_cross.draw()
    win.flip()

#10 Loop 1

answer_1 = Loop(seq_3_2_ic, "seq_3_2_ic")

#11 Check if Loop 1 resulted in the threshold being reached
if answer_1 == True:
    #Display Goodbye Screen (for 20 seconds)
    for x in range(1200):
        
        ##Quit Button During Code
        quitbutton = event.getKeys(keyList=['q'])
        if len(quitbutton) > 0:
            for a in quitbutton:
                if a == 'q':
                    core.quit()
        
        goodbye_message.draw()
        win.flip()

    #End
    dataFile.close()
    print("Run completed")
    core.quit()

#12 Display Redo Infinite for Second Trial after Loop 1 (press b to continue)
redo_infinite_secondtrial.draw()
win.flip()
press_b = event.waitKeys(keyList=["b", 'q'], timeStamped=True)
if press_b[0][0] == 'q':
    core.quit()

#13 Display Get Ready (press t to continue)
get_ready_message.draw()
win.flip()
press_t_2 = event.waitKeys(keyList=["t", 'q'], timeStamped=True)
if press_t_2[0][0] == 'q':
    core.quit()

#14. Display 300ms (18 frames) Cross Fixation Prior to Loop 2
for x in range(18):
    
    ##Quit Button During Code
    quitbutton = event.getKeys(keyList=['q'])
    if len(quitbutton) > 0:
        for a in quitbutton:
            if a == 'q':
                core.quit()
    
    fixation_cross.draw()
    win.flip()
 
#15. Loop 2

answer_2 = Loop(seq_1_2_ic, "seq_1_2_ic")

#16 Check if Loop 2 resulted in the threshold being reached
if answer_2 == True:
    #Display Goodbye Screen (for 20 seconds)
    for x in range(1200):
        
        ##Quit Button During Code
        quitbutton = event.getKeys(keyList=['q'])
        if len(quitbutton) > 0:
            for a in quitbutton:
                if a == 'q':
                    core.quit()
        
        goodbye_message.draw()
        win.flip()

    #End
    dataFile.close()
    print("Run completed")
    core.quit()


#17 Display Redo Infinite for Third Trial after Loop 2 (press b to continue)
redo_infinite_thirdtrial.draw()
win.flip()
press_b_2 = event.waitKeys(keyList=["b", 'q'], timeStamped=True)
if press_b_2[0][0] == 'q':
    core.quit()

#18 Display Get Ready (press t to continue)
get_ready_message.draw()
win.flip()
press_t_3 = event.waitKeys(keyList=["t", 'q'], timeStamped=True)
if press_t_3[0][0] == 'q':
    core.quit()

#19. Display 300ms (18 frames) Cross Fixation Prior to Loop 3
for x in range(18):
    
    ##Quit Button During Code
    quitbutton = event.getKeys(keyList=['q'])
    if len(quitbutton) > 0:
        for a in quitbutton:
            if a == 'q':
                core.quit()
    
    fixation_cross.draw()
    win.flip()
    
#20 Loop 3

answer_3 = Loop(seq_2_2_ic, "seq_2_2_ic")


#21 Display Goodbye Screen (for 20 seconds)
for x in range(1200):
    
    ##Quit Button During Code
    quitbutton = event.getKeys(keyList=['q'])
    if len(quitbutton) > 0:
        for a in quitbutton:
            if a == 'q':
                core.quit()
    
    goodbye_message.draw()
    win.flip()

#20. End
dataFile.close()
print("Run completed")

































'''
image | duration | button press duration |

welcome_screen = 

for increment in sequence:
    run the fixation for certain amount of frames
    run increment for certain amount of frames
        display correct number of words on screen
        record key presses and other data
        record the frame at which buttons was pressed, convert that to milliseconds, and record
        
after increment in sequence, then implement planned pauses according to frames

'''


#the seqx_x need to have the number and answers blank for the personal words in case you want those words to appear a certain amount randomly
'''
Not necessary anymore
#get personal_word_order value from mainlist to determine if word order is set or random
random_or_set_order = mainlist[9]["personal_word_number"]
'''

'''
Not necessary anymore
#Do this if random_or_set_order is set to random. Will randomize the personal words dict list prior to insertion
if random_or_set_order == "random":
    l = len(personal_words)
    newlist = l * [0]
    
    for x in range(0,len(newlist)):
        rand_integer = random.randrange(0,l)
        newlist[x] = personal_words[rand_integer]
        personal_words.pop(rand_integer)
        l -= 1
        
    personal_words = newlist
'''

'''
Not necessary anymore
def personal_word_number_randomizer(preseqlist):
    for i in range(0,len(preseqlist)):
        if preseqlist[i]["type"] == "personal":
            randnumber = random.randrange(1,5)
            preseqlist[i]["number"] = randnumber
            preseqlist[i]["answer"] = f"{randnumber+1}"
'''

