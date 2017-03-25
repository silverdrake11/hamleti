import os

import cv2
import tesserocr


FIRST_PAGE = 5
RIGHT_DIRPATH = 'right'
LEFT_DIRPATH = 'left'
OUT_DIRPATH = 'output'


def write_clean_image(in_filepath, out_filepath):
    '''
    Applies denoising to the image so that specs, etc. do not show up in the
    thresholded image.
    '''

    img = cv2.imread(in_filepath, 0) # Read in as grayscale
  
    # Third argument controls blur... higher is more blurry
    img = cv2.fastNlMeansDenoising(img, None, 23, 7 ,21)

    # Last argument is what you want to adjust
    img = cv2.adaptiveThreshold(
        img, 
        255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 
        11, 
        5
    )

    cv2.imwrite(out_filepath, img)


def get_text(filepath):
    return tesserocr.file_to_text(filepath, lang='sqi')


right_pages = sorted(os.listdir(RIGHT_DIRPATH))
left_pages = sorted(os.listdir(LEFT_DIRPATH))

pages = []
for idx, (right_filename, left_filename) in enumerate(zip(right_pages, left_pages), start=FIRST_PAGE):

    in_right_filepath = os.path.join(RIGHT_DIRPATH, right_filename)
    in_left_filepath = os.path.join(LEFT_DIRPATH, left_filename)

    page_num = idx * 2 - FIRST_PAGE
    out_right_filepath = os.path.join(OUT_DIRPATH, 'page' + str(page_num).zfill(3) + '.jpg')
    out_left_filepath = os.path.join(OUT_DIRPATH, 'page' + str(page_num+1).zfill(3) + '.jpg')

    write_clean_image(in_right_filepath, out_right_filepath)
    right_page_text = get_text(out_right_filepath)
    print(right_page_text)

    write_clean_image(in_left_filepath, out_left_filepath)
    left_page_text = get_text(out_left_filepath)
    print(left_page_text)

    pages.append(right_page_text)
    pages.append(left_page_text)


# Write text from all pages to file
with open('hamleti.txt', 'w') as f:
    for page_num, page in enumerate(pages, start=FIRST_PAGE):
        f.write(page)
        f.write(str(page_num))
        f.write('\n\n\n')



