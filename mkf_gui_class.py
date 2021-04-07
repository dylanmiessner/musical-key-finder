##################################################################
# this file is where the Musical Key Finder's GUI is located.
# wrapped as a class, this should be easily imported and ran,
# which should improve trouble shooting and modularity.
#
#   Author: Dylan Miessner
##################################################################

#imports
from appJar import gui
import crepe_model as cm
import random

# setting the gui up as a class which can be easily used and managed
class mkf_gui:
    # class variables
    browsed = False
    filename = ''
    test_iterator = 0
    test_score = 0
    test_answer = 0
    # begin by creating a list, 1-13, for each possible scale including chromatic
    test_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    mkf = gui("Musical Key Finder", "1000x800")

    # the default constructor for when the class is called, in order to create the mkf gui
    def __init__(self):
        self.draw_background()
        self.draw_labels()
        self.draw_images()
        self.draw_buttons()
        self.mkf.go()

    # this function simply handles drawing the background
    def draw_background(self):
        self.mkf.setBg("light blue")
        self.mkf.setFont(18)

    # this function only draws labels, for use in the constructor
    def draw_labels(self):
        self.mkf.addLabel("title", "Musical Key Finder")
        self.mkf.setLabelBg("title", "white")
        self.mkf.setLabelFg("title", "blue")

    # draw the buttons, used by the constructor
    def draw_buttons(self):
        # all buttons used in the user interface
        self.mkf.addButtons(["Play Audio", "Record Again", "Analyze Again", "Main Menu"], self.press)
        self.mkf.addButtons(['Most Recent Recording', 'From File'], self.press)
        self.mkf.addButtons(['Record Temporary', 'Record Permanent'], self.press)
        self.mkf.addButtons(["Record", "Analyze", "Test Mode", "Quit"], self.press)
        self.organize_buttons()
        self.mkf.hideButton("Main Menu")
        self.mkf.hideButton("Record Again")
        self.mkf.hideButton("Record Permanent")
        self.mkf.hideButton("Record Temporary")
        self.mkf.hideButton("Play Audio")
        self.mkf.hideButton("Analyze Again")
        self.mkf.hideButton("Most Recent Recording")
        self.mkf.hideButton("From File")

    def organize_buttons(self):
        # the main menu's buttons
        self.mkf.moveButton('Record', row=2, column=0, colspan=0, rowspan=0, sticky='EW')
        self.mkf.moveButton('Analyze', row=3, column=0, colspan=0, rowspan=0, sticky='EW')
        self.mkf.moveButton('Test Mode', row=4, column=0, colspan=0, rowspan=0, sticky='EW')
        self.mkf.moveButton('Quit', row=5, column=0, colspan=0, rowspan=0, sticky='EW')

        # record sub menu's buttons
        self.mkf.moveButton('Record Temporary', row=2, column=0, colspan=0, rowspan=0, sticky='EW')
        self.mkf.moveButton('Record Permanent', row=3, column=0, colspan=0, rowspan=0, sticky='EW')
        self.mkf.moveButton('Play Audio', row=2, column=0, colspan=0, rowspan=0, sticky='EW')
        self.mkf.moveButton('Record Again', row=3, column=0, colspan=0, rowspan=0, sticky='EW')
        self.mkf.moveButton('Main Menu', row=5, column=0, colspan=0, rowspan=0, sticky='EW')

        # analyze sub menu's buttons
        self.mkf.moveButton('Most Recent Recording', row=2, column=0, colspan=0, rowspan=0, sticky='EW')
        self.mkf.moveButton('From File', row=3, column=0, colspan=0, rowspan=0, sticky='EW')
        self.mkf.moveButton('Analyze Again', row=3, column=0, colspan=0, rowspan=0, sticky='EW')
        self.mkf.moveButton('Main Menu', row=5, column=0, colspan=0, rowspan=0, sticky='EW')

    # draw the initial image, used by the constructor
    def draw_images(self):
        # creates the initial image 
        self.mkf.clearImageCache()
        self.mkf.addImage("image", "./images/treble_clef.png")

    ###################################################################
    # this press function handles all button presses that occur within the GUI
    ###################################################################
    def press(self, button):
        if button == "Quit": # exit the program, the X in top right also functions
            self.mkf.stop()

        elif button == "Test Mode": # launch the testing functionality, handled in a separate file
            self.test_style()
            self.setup_test()
            self.play_scale()
            
        elif button == "Record": # record a 10 second audio bite to analyze
            self.record_style()
            
        elif button == "Analyze": # call the analyze style functionality which brings up a new set of menu options
            self.analyze_style()

        elif button == "Play Audio": # plays the audio back when a file has been recorded or browsed for
            if self.browsed == False: # this line of code determines if the user browsed for a file
                cm.play_audio('./wav_recordings/output.wav')
            else:
                cm.play_audio(self.filename) # If the user browsed for a file, play the file they browsed for

        elif button == "Main Menu": # returns to the main screen
            self.main_menu()

        elif button == 'Most Recent Recording': # uses the most recently recorded audio sample
            self.analyze_functionality('./wav_recordings/output.wav')

        elif button == 'From File': # allows the user to browse for a file
            self.filename = self.browse_files()
            self.browsed = True
            self.analyze_functionality(self.filename)

        elif button == "Analyze Again": # resets the analyze functionality
            self.analyze_again()

        elif button == "Record Again": # if we want to record another time
            self.record_again()

        elif button == "Record Temporary": # temporary recording dialog box
            self.record_functionality('./wav_recordings/output.wav')

        elif button == "Record Permanent": # open a saving dialog box, otherwise continue as normal
            filename = self.save_file()
            self.record_functionality(filename)

    ############################################################################
    # these blocks of code handle functionality within the GUI, like analyzing
    # and recording audio
    ############################################################################

    # this function handles all the graphical requirements of the recording functionality
    def record_functionality(self, filename):
        self.mkf.setLabel("title", "Recording...")
        self.style_change()
        self.mkf.infoBox("Recording", "Hit \"OK\" to return to start recording")
        cm.record_audio(filename)
        self.mkf.infoBox("Finished Recording", "Finished Recording.")
        self.mkf.showButton("Play Audio")
        self.mkf.showButton("Record Again")
        self.mkf.showButton("Main Menu")

    # this function handles all the graphical requirements of the analysis functionality
    def analyze_functionality(self, filename):
        # set up the style for pre-analysis
        self.mkf.setLabel("title", "Analysis in progress, please wait a moment...")
        self.style_change()
        self.mkf.infoBox("Analyizing", "Hit \"OK\"  to begin analysis.")

        # go to the crepe_model.py file to use the analyze_audio() function
        key = cm.analyze_audio(filename)
        self.mkf.infoBox("Analysis Complete", "Analysis completed. Hit \"OK\" to view.")

        # rebuild the GUI to allow for user interaction

        # this logic changes the image based on if we browswed or not. 
        if not self.browsed:
            self.mkf.reloadImage("image", "./recording_analysis/output.activation.png")
        else:
            filename_only = filename.split("/")
            filename_raw = filename_only[5]
            filename_cleaned = filename_raw.split(".")
            self.mkf.reloadImage("image", "./recording_analysis/" + filename_cleaned[0] + ".activation.png")

        self.mkf.setLabel("title", "Your sample is in the key of " + key)
        self.mkf.hideButton("Most Recent Recording")
        self.mkf.hideButton("From File")
        self.mkf.showButton("Play Audio")
        self.mkf.showButton("Analyze Again")
        self.mkf.showButton("Main Menu")

    # Reset the program back to it's default state, bring us back to analyze
    def analyze_again(self):
        self.reset_browse()
        self.analyze_style()

    def record_again(self):
        self.reset_browse()
        self.record_style()

    # this function is used to browse for and return filenames
    def browse_files(self):
        return self.mkf.openBox("Audio File", "./recordings", 
                    fileTypes=[('sound files', '*.wav'), ('sound files', '*.mp3')])

    def save_file(self):
        return self.mkf.saveBox(title="Save Audio File", fileName="output.wav", dirName="./recordings",
                        fileExt=".wav", fileTypes=[('audio', '*.wav')])
    
    #######################################################################
    # these blocks of code handle all GUI transformations and style changes
    #######################################################################

    # analysis style
    def analyze_style(self): # set the GUI up to analyze
        self.style_change()
        self.mkf.showButton('Most Recent Recording')
        self.mkf.showButton('From File')
        self.mkf.showButton('Main Menu')

    def record_style(self): # sets up the GUI to record
        self.style_change()
        self.mkf.showButton('Record Temporary')
        self.mkf.showButton('Record Permanent')
        self.mkf.showButton('Main Menu')

    # sets the GUI to be a clean state to prevent any overlapping of buttons
    def style_change(self):
        self.mkf.hideButton("Most Recent Recording")
        self.mkf.hideButton("Record Again")
        self.mkf.hideButton("Record Permanent")
        self.mkf.hideButton("Record Temporary")
        self.mkf.hideButton("Analyze Again")
        self.mkf.hideButton("Main Menu")
        self.mkf.hideButton("Play Audio")
        self.mkf.hideButton("From File")
        self.mkf.hideButton("Record")
        self.mkf.hideButton("Analyze")
        self.mkf.hideButton("Quit")
        self.mkf.hideButton("Test Mode")

    # resets all browsing information
    def reset_browse(self):
        self.browsed = False
        self.filename = ''

    # this function sets the GUI to be ready for testing mode
    def test_style(self):
        self.style_change()
        self.mkf.hideImage("image")
        self.mkf.setLabel("title", "Testing Mode: Question 1 of 13")
        self.mkf.addButton("Replay Audio", self.play_scale)
        self.mkf.addButtons(["A", "A#"], self.get_test_answer)
        self.mkf.addButtons(["B", "B#/C"], self.get_test_answer)
        self.mkf.addButtons(["C", "C#"], self.get_test_answer)
        self.mkf.addButtons(["D", "D#"], self.get_test_answer)
        self.mkf.addButtons(["E", "E#/F"], self.get_test_answer)
        self.mkf.addButtons(["F", "F#"], self.get_test_answer)
        self.mkf.addButtons(["G", "G#"], self.get_test_answer)
        self.mkf.addButton("Chromatic", self.get_test_answer)

    # return to main menu from anything
    # this also resets all choices that have been made
    def main_menu(self):
        self.reset_browse()

        self.mkf.setImage("image", "./images/treble_clef.png")
        self.mkf.setLabel("title", "Musical Key Finder")
        self.mkf.showImage("image")
        self.style_change()
        self.mkf.showButton("Record")
        self.mkf.showButton("Analyze")
        self.mkf.showButton("Test Mode")
        self.mkf.showButton("Quit")

    ##############################################################
    # These blocks of code handle all of the testing portions of 
    # Musical Key Finder, such as updating the GUI and ensuring
    # it functions as we would expect through the audio logic.
    ##############################################################

    # returns a number based on the button that they hit
    def get_test_answer(self, button):

        # create a bytes like input for each answer
        if button == "A":
            self.test_answer = 1
        elif button == "B":
            self.test_answer = 2
        elif button == "C":
            self.test_answer = 3
        elif button == "D":
            self.test_answer = 4
        elif button == "E":
            self.test_answer = 5
        elif button == "F":
            self.test_answer = 6
        elif button == "G":
            self.test_answer = 7
        elif button == "A#":
            self.test_answer = 8
        elif button == "B#/C":
            self.test_answer = 3
        elif button == "C#":
            self.test_answer = 9
        elif button == "D#":
            self.test_answer = 10
        elif button == "E#/F":
            self.test_answer = 6
        elif button == "F#":
            self.test_answer = 11
        elif button == "G#":
            self.test_answer = 12
        elif button == "Chromatic":
            self.test_answer = 13

        if self.test_answer == self.test_list[self.test_iterator]:
            self.test_score += 1

        self.test_iterator += 1
        self.test_results()

    def test_results(self):
        # the next task is to handle the GUI modification so that 13 options are drawn on the screen
        # and the image is hidden
        if self.test_iterator >= 13:
            self.mkf.removeButton("A")
            self.mkf.removeButton("B")
            self.mkf.removeButton("C")
            self.mkf.removeButton("D")
            self.mkf.removeButton("E")
            self.mkf.removeButton("F")
            self.mkf.removeButton("G")
            self.mkf.removeButton("A#")
            self.mkf.removeButton("B#/C")
            self.mkf.removeButton("C#")
            self.mkf.removeButton("D#")
            self.mkf.removeButton("E#/F")
            self.mkf.removeButton("F#")
            self.mkf.removeButton("G#")
            self.mkf.removeButton("Chromatic")
            self.mkf.removeButton("Replay Audio")
            self.mkf.showButton("Main Menu")

            if self.test_score >= 9:
                self.mkf.setLabel("title", "Your score was " + str(self.test_score) + " out of 13! Excellent work!")
            else:
                self.mkf.setLabel("title", "Your score was " + str(self.test_score) + " out of 13.  Keep practicing!")
        else:
            self.mkf.setLabel("title", "Testing Mode: Question " + str(self.test_iterator + 1) + " of 13")
            self.play_scale()


    # choose the scale to play
    def play_scale(self):
        scale = self.test_list[self.test_iterator]
        if scale == 1:
            cm.play_audio("./scales/a_scale.wav")

        elif scale == 2:
            cm.play_audio("./scales/b_scale.wav")

        elif scale == 3:
            cm.play_audio("./scales/c_scale.wav")

        elif scale == 4:
            cm.play_audio("./scales/d_scale.wav")

        elif scale == 5:
            cm.play_audio("./scales/e_scale.wav")

        elif scale == 6:
            cm.play_audio("./scales/f_scale.wav")

        elif scale == 7:
            cm.play_audio("./scales/g_scale.wav")

        elif scale == 8:
            cm.play_audio("./scales/a#_scale.wav")

        elif scale == 9:
            cm.play_audio("./scales/c#_scale.wav")

        elif scale == 10:
            cm.play_audio("./scales/d#_scale.wav")

        elif scale == 11:
            cm.play_audio("./scales/f#_scale.wav")

        elif scale == 12:
            cm.play_audio("./scales/g#_scale.wav")

        elif scale == 13:
            cm.play_audio("./scales/chromatic_scale.wav")

    # this function sets all the variables back to their default's and shuffles the list so the test is not the same each time
    def setup_test(self):
        self.test_answer = 0
        self.test_iterator = 0
        self.test_score = 0
        random.shuffle(self.test_list)