# Stroop_Test_IC_Standardization
This repository contains the Stroop Test Program for establishing the participant's baseline ability to respond to stimuli. It uses words of numbers that are either incongruent or congruent.

Purpose
The Stroop Task is a widely used cognitive task designed to assess selective attention, cognitive flexibility, and processing speed. In this task, participants are required to respond to the number of words while ignoring conflicting information (e.g., the word's semantic meaning), making it useful for evaluating response accuracy and reaction time (RT) under conditions of cognitive interference.
The Stroop Task Training program will be administered on a study laptop and is designed to ensure participants have an adequate understanding of the task prior to completing the Cocaine Stroop Task during the MRI scan. This training phase is essential to avoid scheduling and resource losses related to participants being unable to complete the task in the scanner due to inability to comprehend the task, thus must be done before the MRI scan is scheduled.
The training task records the participant’s accuracy and RT in response to congruent versus incongruent word-number stimuli. Participants will be asked to press buttons 1 through 4 on the keyboard to indicate how many times a word appears on the screen, regardless of what the word says. For example:
•	Congruent trial: the word “THREE” displayed three times.
•	Incongruent trial: the word “FOUR” displayed three times.
The contrast between responses to incongruent versus congruent trials forms the basis for evaluating task comprehension.
Training Location and Timing
This training will take place in a designated office or TMS lab space using a study laptop, prior to the participant undergoing the Cocaine Stroop Task in the MRI scanner.
Accuracy Requirement and Training Protocol
To proceed to the scanner-based Cocaine Stroop Task, participants must achieve a predetermined accuracy threshold for the incongruent vs. congruent contrast. Participants are allowed up to three attempts to meet this criterion. The training procedure is as follows:
1.	First Attempt: The participant completes the Stroop Task training module.
2.	If accuracy threshold is met, no further attempts are needed.
If the accuracy threshold is not met, the study staff member will pause to review the task with the participant, asking them to explain the instructions in their own words to identify any misunderstandings. 
3.	Clarification: If misunderstandings are identified, the staff member will clarify the instructions before the participant proceeds to the next attempt.
4.	Second Attempt: The participant retakes the task after clarification.
o	If accuracy criterion is met, no further attempts are needed.
5.	Third Attempt (if needed): A final opportunity is provided under staff supervision.
o	If the participant fails to meet the criterion after three attempts, a study PI must be notified.
Follow-Up and Eligibility Decisions
Participants who do not meet the training accuracy criterion after three attempts may still be eligible to complete other parts of the MRI study, but will not proceed to the Cocaine Stroop Task in the scanner without PI approval. This process helps ensure that MRI scan slots are used efficiently and that all collected task data are valid.

Scope
This SOP applies specifically to Protocol #8483. 

Procedures
Requirements – Only follow if using a laptop that does not have the Stroop Task pre-installed 
1.	Laptop (must use Windows 10 or most recent OS, CANNOT use Mac)
2.	The following File Structure inside the computer:
a.	Documents
i.	CoStim
1.	Cocaine_Stroop_Task
2.	Stroop_Task_Training
3.	Python 3.10, or most recent version
4.	PsychoPy v2.4 modern (Python 3.10), or most recent version (https://www.psychopy.org/download.html)
5.	Cocaine Stroop Task Program (https://github.com/vano31/Stroop_Task_Training)
a.	Click Code > Download Zip on the link above to download the zip file if not done so already
b.	Unzip folder, and rename unzipped folder to “Stroop_Task_Training-TEMPLATE”
c.	Move “Stroop_Test_Training-TEMPLATE” to inside Documents > CoStim > Stroop_Task_Training

Session 1
1.	On the laptop meant for the Stroop Test, navigate to Settings > Display > Advanced Display > Choose a Refresh Rate.
2.	Ensure that the Refresh Rate is set to 60 Hz (TASK WILL FAIL IF THIS IS NOT SET).
3.	Navigate to Documents > CoStim > Stroop_Task_Training.
4.	Copy the Folder named “Stroop_Task_Training-TEMPLATE” and paste it in the current folder you are in.
5.	Rename the copied folder to “Stroop_Task_Training_Subject_[INSERT SUBJECT ID NUMBER HERE]”. Enter this folder.
6.	Open PsychoPy. On type right corner of Window, click “Show Coder” Icon (the icon is a striped circle with a white sheet and a red “>” symbol on its bottom right corner). This will open the Coder Window.
7.	If a black window pops up, minimize it.
8.	On top left corner of Coder Window, click “Open” Icon (the icon is an open folder).
9.	In the Open File Window, Navigate to Documents > CoStim > Stroop_Task_Training > Stroop_Task_Training_Subject_[SUBJECT ID]. Within this folder, click the file named “Stroop_Task_Training.py” and press Open.
10.	Code will appear in the Coder Window. DO NOT EDIT CODE IN THE CODER WINDOW- typing code will not be necessary for any part of the task.
11.	On the top of the Coder Window’s Tool Bar, look for the icon that looks like a slider between the words “Pilot” and “Run”. Ensure that the slider is set to “Run.” The “Run” Icon (represented by a play button) should be GREEN. (If “Run” Icon is Orange, the slider is set to “Pilot” and should be changed).
12.	Press the GREEN “Run” Icon. A small window named “Cocaine Study Stroop Task Training” should appear.
13.	Inside the Cocaine Study Stroop Task Training Window, type the Subject_ID (should be same ID the folder was named after), the Session Number (Should be 1), and the Desired Percentage Correct (in integers, ie 90). Press OK.
14.	The task will take up the screen. Follow the onscreen instructions.
15.	Whenever the screen is blank, press “b” to move on.
16.	Whenever the screen says “Get Ready,” press “t” to move on.
17.	To quickly close the program, press “q.” This will completely terminate the program and save everything up until the most recent action. Once this is done, the task must be completed all over again.

Session 2 (if needed)
1.	Follow Steps 1-3 in the Session 1 instructions.
2.	Open the Folder named “Stroop_Task_Training_Subject_[SUBJECT ID].”
3.	Follow Steps 6-13 in Session 1 instructions.
4.	Inside the Cocaine Study Stroop Task Tutorial Window, type the Subject_ID (should be same ID the folder was named after), the Session Number (Should be 2), and the Desired Percentage Correct (in integers, ie 90). Press OK.
5.	Follow Steps 14-17 in Session 1 instructions.

Retrieving Data
1.	To retrieve data for a specific participant, navigate to Documents > CoStim > Stroop_Task_Training > Stroop_Task_Training_Subject_[SUBJECT ID] > data. Enter the “data” folder.
2.	Excel Sheets named “[SUBJECT ID]_[SESSION NUMBER]_[DESIRED PERCENTAGE CORRECT]_Stroop_Task_Training[DATE OF SESSION]” will contain information regarding participant responses to words in show on screen. The bottom of the file should provide information regarding whether or not the participant reached the Desired Percentage Correct. If this percentage is reached in Session 1, subsequent sessions are not necessary.

Sources
1.	https://github.com/vano31/Stroop_Task_Training
2.	https://www.psychopy.org/download.html



