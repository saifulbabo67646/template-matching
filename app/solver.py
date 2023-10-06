# This is how easy it is to solve TikTok captchas

import cv2
import base64
import numpy as np


class PuzzleSolver:
    def __init__(self, base64puzzle, base64piece):
        self.puzzle = base64puzzle
        self.piece = base64piece

    def get_position(self):
        puzzle = self.__background_preprocessing()
        piece = self.__piece_preprocessing()
        #will remove later
        # output_dir = "./output_images/"
        # # Save the processed images to the output directory
        # cv2.imwrite(output_dir + "background.png", puzzle)
        # cv2.imwrite(output_dir + "template.png", piece)
        web_puzzle_width = 250
        web_puzzle_height = 149

        provided_puzzle_width = 310
        provided_puzzle_height = 155

        width_scaling_factor = web_puzzle_width / provided_puzzle_width
        height_scaling_factor = web_puzzle_height / provided_puzzle_height

        matched = cv2.matchTemplate(
          puzzle, 
          piece, 
          cv2.TM_CCOEFF_NORMED
        )
        return matched
        # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(matched)
        # adjusted_x_position = int(max_loc[0] * width_scaling_factor)
        # print(adjusted_x_position)
        # return max_loc[0]

    def __background_preprocessing(self):
        img = self.__img_to_grayscale(self.piece)
        background = self.__sobel_operator(img)
        return background

    def __piece_preprocessing(self):
        img = self.__img_to_grayscale(self.puzzle)
        template = self.__sobel_operator(img)
        return template

    def __sobel_operator(self, img):
        scale = 1
        delta = 0
        ddepth = cv2.CV_16S

        img = cv2.GaussianBlur(img, (3, 3), 0)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        grad_x = cv2.Sobel(
            gray,
            ddepth,
            1,
            0,
            ksize=3,
            scale=scale,
            delta=delta,
            borderType=cv2.BORDER_DEFAULT,
        )
        grad_y = cv2.Sobel(
            gray,
            ddepth,
            0,
            1,
            ksize=3,
            scale=scale,
            delta=delta,
            borderType=cv2.BORDER_DEFAULT,
        )
        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)
        grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

        return grad

    def __img_to_grayscale(self, img):
        return cv2.imdecode(
          self.__string_to_image(img),
          cv2.IMREAD_COLOR
        )

    def __string_to_image(self, base64_string):

        return np.frombuffer(
          base64.b64decode(base64_string),
          dtype="uint8"
        )


# def run():
#     puzzle_filename = "./full14.png"
#     piece_filename = "./piece14.png"
    
#     # Read puzzle and piece images
#     with open(puzzle_filename, "rb") as f:
#         puzzle_img_data = f.read()
    
#     with open(piece_filename, "rb") as f:
#         piece_img_data = f.read()
    
#     # Encode images to base64
#     base64_puzzle = base64.b64encode(puzzle_img_data).decode("utf-8")
#     base64_piece = base64.b64encode(piece_img_data).decode("utf-8")
#     # print(base64_puzzle)
    
#     solver = PuzzleSolver(base64_puzzle, base64_piece)
#     max_loc = solver.get_position()

#     print(max_loc)

# run()
