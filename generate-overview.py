import os
import math
from PIL import Image, ImageOps
import logging



def main():
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)


    values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    path = './02_data_resize_all_remove_duplicate_and_new_images'

    for value in values:
        generate(path, value, 15)



def concat_images(image_paths, size, shape=None):
    # Open images and resize them
    width, height = size
    images = map(Image.open, image_paths)

    images = [ImageOps.expand(image, border=10,fill='white')
              for image in images]
    
    images = [ImageOps.fit(image, size, Image.Resampling.NEAREST) 
              for image in images]
    
    # Create canvas for the final image with total size
    shape = shape if shape else (1, len(images))
    image_size = (int(width * shape[1]), int(height * shape[0]))
    image = Image.new('RGB', image_size, color='white')
    
    # Paste images into final image
    for row in range(shape[0]):
        for col in range(shape[1]):            
            offset = width * col, height * row
            idx = row * shape[1] + col
            try:
                image.paste(images[idx], offset)
            except:
                pass
    
    return image


def generate(path, prefix, cols):
    logging.info("Generating summary image of all '%s*.jpg' images in %s..." % (prefix, path))
    # Get list of image paths
    image_paths = [os.path.join(path, f) 
                for f in os.listdir(path) if (f.startswith(prefix) and f.endswith('.jpg'))]
    image_paths.sort()

    logging.debug("Found %d images." % len(image_paths))

    rows = math.ceil(float(len(image_paths)) / cols)

    logging.debug("Generating grid of %d x %d images" % (cols, rows))


    # Create and save image grid
    image = concat_images(image_paths, (int(800/cols), int(800/cols)), (rows, cols))
    image.save("./html_output/digital-" + prefix + ".jpg", 'JPEG')


if __name__ == "__main__":
     main()
