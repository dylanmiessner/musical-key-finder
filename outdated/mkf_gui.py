# importing appjar, the wrapper for tkinter which is used to create simple GUIs in python
from appJar import gui

# the basis for where most logic will be performed as far as machine learning goes
import crepe_model as cm

# browsing variables needed many places in the program
# these variables are essential, as they prevent us from utilizing the wrong file for our analysis
browsed = False
filename = ''

# this function handles button presses
def press(button):
    global filename # these variables are utilized to track whether or not a user has browsed for a file before
    global browsed  # the filename has been reset or not. 

    if button == "Quit": # exit the program, the X in top right also functions
        mkf.stop()

    elif button == "Record": # record a 10 second audio bite to analyze
        record_functionality()

    elif button == "Analyze": # call the analyze style functionality which brings up a new set of menu options
        analyze_style()

    elif button == "Play Audio": # plays the audio back when a file has been recorded or browsed for
        if browsed == False: # this line of code determines if the user browsed for a file
            cm.play_audio('./wav_recordings/output.wav')
        else:
            cm.play_audio(filename) # If the user browsed for a file, play the file they browsed for

    elif button == "Main Menu": # returns to the main screen
        main_menu()

    elif button == 'Most Recent Recording': # uses the most recently recorded audio sample
        analyze_functionality('./wav_recordings/output.wav')

    elif button == 'From File': # allows the user to browse for a file
        filename = browse_files()
        browsed = True
        analyze_functionality(filename)

    elif button == "Analyze Again": # resets the analyze functionality
        analyze_again()


# this function handles all the graphical requirements of the recording functionality
def record_functionality():
    mkf.setLabel("title", "Recording...")
    style_change()
    mkf.infoBox("Recording", "Hit \"OK\" to return to start recording")
    cm.record_audio()
    mkf.infoBox("Finished Recording", "Finished Recording.")
    mkf.showButton("Play Audio")
    mkf.showButton("Main Menu")
    

# this function handles all the graphical requirements of the analysis functionality
def analyze_functionality(filename):
    # set up the style for pre-analysis
    mkf.setLabel("title", "Analysis in progress, please wait a moment...")
    style_change()
    mkf.infoBox("Analyizing", "Hit \"OK\"  to begin analysis.")

    # go to the crepe_model.py file to use the analyze_audio() function
    cm.analyze_audio(filename)
    mkf.infoBox("Analysis Complete", "Analysis completed. Hit \"OK\" to view.")

    # rebuild the GUI to allow for user interaction
    mkf.reloadImage("image", "./recording_analysis/output.activation.png")
    mkf.setLabel("title", "Frequency Analysis")
    mkf.hideButton("Most Recent Recording")
    mkf.hideButton("From File")
    mkf.showButton("Play Audio")
    mkf.showButton("Analyze Again")
    mkf.showButton("Main Menu")

# Reset the program back to it's default state, bring us back to analyze
def analyze_again():
    reset_browse()
    analyze_style()

# analysis style
def analyze_style(): # set the GUI up to analyze
    style_change()
    mkf.showButton('Most Recent Recording')
    mkf.showButton('From File')

# sets the GUI to be a clean state to prevent any overlapping of buttons
def style_change():
    mkf.hideButton("Most Recent Recording")
    mkf.hideButton("Analyze Again")
    mkf.hideButton("Main Menu")
    mkf.hideButton("Play Audio")
    mkf.hideButton("From File")
    mkf.hideButton("Record")
    mkf.hideButton("Analyze")
    mkf.hideButton("Quit")

# resets all browsing information
def reset_browse():
    global browsed
    global filename
    browsed = False
    filename = ''

# return to main menu from anything
# this also resets all choices that have been made
def main_menu():
    reset_browse()

    mkf.setImage("image", "treble_clef.png")
    mkf.setLabel("title", "Musical Key Finder")
    style_change()
    mkf.showButton("Record")
    mkf.showButton("Analyze")
    mkf.showButton("Quit")


# this function is used to browse for and return filenames
def browse_files():
    return mkf.openBox("Audio File", "./wav_recordings", fileTypes=[('sound files', '*.wav'), ('sound files', '*.mp3')])

# creating the bare bones of the GUI and the main menu
mkf = gui("Musical Key Finder", "1000x800")

mkf.setBg("light blue")
mkf.setFont(18)

# mkf.showSplash("Musical Key Finder", fill='light blue', stripe='white', fg='blue', font=60)

# creates the initial label widget
mkf.addLabel("title", "Musical Key Finder")
mkf.setLabelBg("title", "white")
mkf.setLabelFg("title", "blue")

# creates the initial image 
mkf.clearImageCache()
mkf.addImage("image", "treble_clef.png")

mkf.addButtons(["Play Audio", "Analyze Again", "Main Menu"], press)
mkf.addButtons(['Most Recent Recording', 'From File'], press)
mkf.addButtons(["Record", "Analyze", "Quit"], press)
mkf.hideButton("Main Menu")
mkf.hideButton("Play Audio")
mkf.hideButton("Analyze Again")
mkf.hideButton("Most Recent Recording")
mkf.hideButton("From File")

# launch the program
mkf.go()