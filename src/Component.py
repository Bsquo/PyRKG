from math import floor

class Component:

    supported_input_types = ["a_btn", "b_btn", "x_btn", "y_btn", "l_btn", "r_btn", "1st_person_enabled", "analog"]

    def __init__(self, canvas, input_type: str):
        self.canvas = canvas
        if input_type is not None and input_type not in self.supported_input_types:
            raise Exception(f'"{input_type}" is not supported by {self.__class__.__name__}')
        else:
            self.input_type = input_type

    def init_component(self, info: dict):
        pass

    def process_input_and_draw(self, current_input, show_joystick_values, show_first_person_enabled_text, joystick_range_7_7):
        pass


class Categorical_C(Component):

    supported_input_types = ["a_btn", "b_btn", "x_btn", "y_btn", "l_btn", "r_btn", "1st_person_enabled", "analog"]
    info_format = {
        "categories": {
            str: { # string representing category
                "position": [int, int], # [x, y]
                "image": str # image file name
            }
        }
    }

    def init_component(self, info: dict):
        self.categories = info["categories"]
        for category in self.categories.values():
            self.canvas.load_image(category["image"])

    def process_input_and_draw(self, current_input, show_joystick_values, show_first_person_enabled_text, joystick_range_7_7):
        cur_info = self.categories[current_input]
        # Avoid rendering the "1st Person Enabled" image if the setting for it is toggled off.
        if self.input_type != "1st_person_enabled" or self.input_type == "1st_person_enabled" and show_first_person_enabled_text:
            self.canvas.draw_image(cur_info["image"], cur_info["position"])


class Tuple_C(Component):

    supported_input_types = ["analog"]
    info_format = {
        "image": str, # image file name
        "position": list, # [x, y]
        "pos_range": list # [x, y] x and y specify how far the image can move from its position in the x and y range respectively
    }

    def init_component(self, info: dict):
        self.image = info["image"]
        self.pos_range = tuple(info["pos_range"])
        self.position = tuple(info["position"])
        
        self.canvas.load_image(self.image)

    def process_input_and_draw(self, current_input, show_joystick_values, show_first_person_enabled_text, joystick_range_7_7):
        delta_pos = (floor((current_input[1] - 7) * self.pos_range[0] / 7), floor((7 - current_input[0]) * self.pos_range[1] / 7))
        cur_position = (self.position[0] + delta_pos[0], self.position[1] + delta_pos[1])
        self.canvas.draw_image(self.image, cur_position)


class Text_C(Component):

    supported_input_types = ["a_btn", "b_btn", "x_btn", "y_btn", "l_btn", "r_btn", "1st_person_enabled", "analog"]
    info_format = {
        "position": list, # [x, y]
        "font": str, # font file name
        "size": int, # font size
        
        # The following are all optional, they are all directly taken from Pillow's text function 
        # https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html#PIL.ImageDraw.ImageDraw.text

        "fill": [int, int, int], # text colour
        "spacing": int, # if multiline text, the number of pixels between the lines
        "align": str, # if multiline text, "left", "center" or "right"
        "direction": str, # if multiline text, "rtl" (right to left), "ltr" (left to right) or "ttb" (top to bottom)
        "stroke_width": int, # text stroke width, also known as text border
        "stroke_fill": [int, int, int] # text stroke colour
    }

    def init_component(self, info: dict):
        self.info = info
        self.position = tuple(info["position"])
        self.canvas.load_font(self.info["font"], self.info["size"])

    # Reduced the function to only display text for the joystick (the raw horizontal and vertical values)
    def process_input_and_draw(self, current_input, show_joystick_values, show_first_person_enabled_text, joystick_range_7_7):
        if self.input_type == "analog":
            # Render the joystick raw values ranging from (-7,7)
            if joystick_range_7_7:
                # Taken from the original PyRKG README
                new_input = (current_input[0] - 7, current_input[1] - 7)	
                text = f"{str(new_input )}"
            # Render the joystick raw values ranging from (0,14)
            else:
                text = f"{str(current_input)}"

        if show_joystick_values:
            self.canvas.draw_text(text, **self.info)


class StaticImage_C(Component):

    info_format = {
        "image": str, # image file name
        "position": list # [x, y]
    }

    def init_component(self, info: dict):
        self.image = info["image"]
        self.position = tuple(info["position"])
        self.canvas.load_image(self.image)

    def process_input_and_draw(self, current_input, show_joystick_values, show_first_person_enabled_text, joystick_range_7_7):
        self.canvas.draw_image(self.image, self.position)
