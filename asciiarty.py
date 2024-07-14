from PIL import Image, ImageOps
import argparse
import pathlib
import sys

ASCII_brightness = '`^",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'


def brightness_avg(px):
    """Convert RGB tuple pixel into brightness, using
    average of RGB values."""
    return sum(px) / 3


def brightness_lightness(px):
    """Convert RGB tuple pixel into brightness, using
    lightness - the average of the min and max RGB values."""
    return (max(px) + min(px)) / 2


f_brightness = {"average": brightness_avg, "lightness": brightness_lightness}


def brightness_to_ascii(px_bright):
    """Convert a brightness pixel value (0-255) into an ASCII character"""
    l = len(ASCII_brightness)
    conversion_factor = 256 / l
    ascii_index = int(px_bright / conversion_factor)
    return ASCII_brightness[ascii_index]


def main():
    """The main method"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "image",
        nargs="?",
        help="the image to convert",
        default="cat.jpg",
        type=pathlib.Path,
    )
    # TODO: add option to resize by entering width and height arguments (or just one?)
    size = (120, 80)
    # TODO: add option to select brightness calculation by keyword, e.g. "average"
    # brightness_calc = "average"
    brightness_calc = "lightness"
    brightness_function = f_brightness[brightness_calc]

    args = parser.parse_args()

    # check if image exists, exit if not
    im_name = args.image
    path = pathlib.Path(im_name)
    if not path.exists():
        print(f"File does not exist: {im_name}")
        sys.exit(-1)

    # print image information
    im_orig = Image.open(im_name)
    print(im_orig.format, im_orig.size, im_orig.mode)

    # resize image to default size
    # fit to smallest dimension
    im = ImageOps.contain(im_orig, size)
    print(f"Resized image: {im.size}")

    # convert image to 2d pixel data
    pixels = im.getdata()
    print(f"Image converted to pixels: {len(list(pixels))}")

    # convert pixel tuples into brightness numbers
    pixels_brightness = [brightness_function(pxl) for pxl in pixels]
    print(f"Converted pixels to brightness: {len(pixels_brightness)}")

    # Convert brightness to ASCII character
    pixels_ascii = [brightness_to_ascii(pxl) for pxl in pixels_brightness]
    print(f"Converted brightness pixels into ASCII characters: {len(pixels_ascii)}")

    # print ascii image
    column_factor = 2
    cols, rows = im.size
    for r in range(rows):
        row = ""
        for c in range(cols):
            row += pixels_ascii[c + r * cols] * column_factor
        print(row)


if __name__ == "__main__":
    main()
