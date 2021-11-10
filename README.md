# Board

A simple drawing board made with python and opencv. This project is incomplete, if someone wants to contribute, then feel free to fork this repo, clone the repo to your local machine, make changes and then make a Pull Request. Any help would be appreciated.

If you want to use it, download the code as a zip file and then unzip it, or you can use git to clone it in your local machine.

`$ git clone git@github.com:Ritam727/Board.git`

`$ cd Board/`

To install the requirements, run the following command(make sure you have python3 and pip installed on your machine):

`$ pip install -r requrements.txt`

Then run the program with:

`$ python main.py`

Change the R, G and B values to tweak the colour of the brush, the colour you are currently using is visible in the top left corner of the drawing screen. Press 'e' to change to erase mode and 'esc' to quit. Press 's' to save the current frame to a folder named `savedImages` in the directory in which the program is currently located. Press 'z' to undo(at most 10 undos allowed).

Controls shifted to new window, resizing feature added, though its incomplete. Note that in the current version only increasing height and width of window works as expected, but on reducing them, the image is also resized(any help regarding this would be appreciated).
