# PyRKG (Mario Kart 7 support)
This is a command line input viewer for Mario Kart Wii and Mario Kart 7 ghost files. It allows the user to save a video of the inputs of any Time Trial ghost, which can then be overlayed with a recording of said ghost.

This is a fork of AtishaRibeiro's PyRKG that adds support for [Mario Kart 7's DAT ghost files](https://wiki.tockdom.com/wiki/User:B_squo#DAT_.28File_Format.29_.28Mario_Kart_7.27s_Ghost_Format.29). Part of this fork uses code from [luckytyphlosion's fork](https://github.com/luckytyphlosion/PyRKG/commit/4840fd54ec30926cae26f7c9a790edabf65dad6c) as well.

Clone or download this repository to any folder you want, then follow the instructions below to install the dependencies and execute the script.

## Table of Contents
1. [Prerequisites](#Prerequisites)
2. [Running PyRKG](#Running-PyRKG)
3. [Making your own layouts](#Making-your-own-layouts)
4. [Making your own components](#Making-your-own-components)

### Prerequisites
- Have Python installed, download [here](https://www.python.org/downloads/)
- Have the `Pillow` library installed, after installing Python run `pip install Pillow`
- If you have errors executing the `pip` command, you may not have it installed in your computer. In that case, [install the command](https://www.liquidweb.com/kb/install-pip-windows/) and try again.
- Download `FFMPEG` from [here](https://github.com/BtbN/FFmpeg-Builds/releases) and place the `ffmpeg.exe` in the same folder as `main.py`

### Running PyRKG
The main command is `python main.py -l <layout> -g <ghost_file>` where:
-  `<layout>` is the name of the layout you want to use (the name of the folder in `layouts`). The layout for Mario Kart 7 is called `mk7`.
- `<ghost_file>` is the path to the ghost file you want to make a video of.

For example, to generate a video of the inputs from a Mario Kart 7 ghost, you would need to execute the following command:
```
python main.py -l mk7 -g your_ghost.dat
```

This will generate a video in the same folder as `main.py`, called `video.mov`. There are a few video settings you can specify, these can be found in `src/CONFIG.py`:

- `VIDEO_FRAME_RATE`: the video frame rate
- `VIDEO_EXTENSION`: the video file format
- `TRANSPARENT`: whether the video should have a transparent background

For Mario Kart 7 ghosts, you also have three additional options you can toggle on/off by setting them to either **True** or **False**. These are:

- `SHOW_FIRST_PERSON_ENABLED_TEXT`: Shows a piece of text stating if the ghost is driving in first person view at any given moment.
- `SHOW_JOYSTICK_VALUES`: Shows the raw values of the stick.
- `JOYSTICK_RANGE_7_7`: If enabled, the range of values used for the stick will be between (-7, 7), rather than (0, 14). Note that the option `SHOW_JOYSTICK_VALUES` must be enabled in order for this to work.

### Making your own Layouts
Layouts reside in the `layouts` folder. To make a new layout simply create a folder there.
*Make sure to check the layouts already present in this repo to get an idea of what it should look like!*

In order to see what the layout looks like while you're editing, run `python main.py -l <layout> -t`.
This will make live updates of the `config.json` file.

The only file that is absolutely necessary is the `config.json` file which looks like this:
```json
{
	"width": "int",
	"height": "int",
	"bg_color": ["int", "int", "int"]
	"components": [
		"..."
	]
}
```
Within the `components` list you can add different components which visualise the ghost's inputs.
There are several default components which can be found in `src/Component.py`
Components should be specified as follows:
```json
{
	"name": "str",
	"input_type": "str"
	"info": {
		"..."
	}
}
```
- `name` is the class name of the component
- `input_type` is one of 5 types:
	- `a_btn`: the A button (accelerator)
	- `b_btn`: the B button (drift)
	- `l_btn`: the L button (shroom)
	- `analog`: the directional inputs (analog stick)
	- `trick`: trick type (d-pad)
- `info` is a dictionary containing all the data that will be passed on to the component itself. What goes in here depends on the component.

### Making your own components
If the default components don't do exactly what you want them to, you can make your own components for your layout. Simply create a `Component.py` file in your layout folder and import the base `Component` class
```py
from src.Component import Component
```
You can add as many components as you want in this file but they should all look something like this:
```py
class MyComponent(Component):
	# this list specifies what inputs your component supports
	supported_input_types = ["a_btn", "b_btn", "l_btn", "analog", "trick"]

	# this info dict is the same as the one in the config.json file!
	def  init_component(self, info: dict):
		...
		
	# let your component change depending on current_input
	def  process_input_and_draw(self, current_input):
		...
```
Let's say I don't like how the default text component uses the `[0,14]` range for the directional inputs and would rather have it use the `[-7, 7]` range. This could be done like this:
```py
class MyAnalogText(Component):

    supported_input_types = ["analog"]
    # info_format is not actually used anywhere, but it gives an idea of what the info dict should contain
    info_format = {
        "position": list, # [x, y]
        "font": str, # font file name
        "size": int # font size
    }

    def init_component(self, info: dict):
        self.info = info
        self.position = tuple(info["position"])
        self.canvas.load_font(self.info["font"], self.info["size"])

    def process_input_and_draw(self, current_input):
        new_input = (current_input[0] - 7, current_input[1] - 7)	
        text = f"{str(new_input )}"
        self.canvas.draw_text(text, **self.info)
```


