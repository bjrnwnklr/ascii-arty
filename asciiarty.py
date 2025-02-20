from PIL import Image, ImageOps
import argparse
import pathlib
import sys

ASCII_brightness = '`^",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'

# sRGB luminance(Y) values
rY = 0.212655
gY = 0.715158
bY = 0.072187


def inv_gam_sRGB(ic: int):
    """Convert a 256 RGB value into a normalized (0.0-1.0) RGB value with
    inverse gamma applied."""
    c = ic / 255.0
    if c <= 0.04045:
        return c / 12.92
    else:
        return pow(((c + 0.055) / 1.055), 2.4)


def gam_sRGB(v):
    if v <= 0.0031308:
        v *= 12.92
    else:
        v = 1.055 * pow(v, 1.0 / 2.4) - 0.055
        # the + 0.5 might not be required, try results
    # return int(v * 255 + 0.5)
    return int(v * 255)


def luminance(px):
    """Convert RGB tuple value into luminance, according to a very complicated formula
    from https://stackoverflow.com/a/13558570."""
    return gam_sRGB(
        rY * inv_gam_sRGB(px[0]) + gY * inv_gam_sRGB(px[1]) + bY * inv_gam_sRGB(px[2])
    )


def brightness_avg(px):
    """Convert RGB tuple pixel into brightness, using
    average of RGB values."""
    return sum(px) / 3


def brightness_lightness(px):
    """Convert RGB tuple pixel into brightness, using
    lightness - the average of the min and max RGB values."""
    return (max(px) + min(px)) / 2


f_brightness = {
    "average": brightness_avg,
    "lightness": brightness_lightness,
    "luminance": luminance,
}


def brightness_to_ascii(px_bright):
    """Convert a brightness pixel value (0-255) into an ASCII character"""
    conversion_factor = 256 / len(ASCII_brightness)
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
    # TODO: add an --invert parameter to invert the colors of the image
    invert = False
    # TODO: add an --adjust switch and threshold (0-255) and factor (0-1) parameters
    # To adjust any pixels darker than threshold by factor
    adjust = True
    factor = 0.6
    threshold = 100

    # TODO: add option to select brightness calculation by keyword, e.g. "average"
    # brightness_calc = "average"
    # brightness_calc = "lightness"
    brightness_calc = "luminance"
    brightness_function = f_brightness[brightness_calc]

    args = parser.parse_args()

    # check if image exists, exit if not
    im_name = args.image
    path = pathlib.Path(im_name)
    if not path.exists():
        print(f"File does not exist: {im_name}")
        sys.exit(-1)

    # print image information
    im = Image.open(im_name)
    print(im.format, im.size, im.mode)

    # if --invert, invert the image
    if invert:
        im = ImageOps.invert(im)

    # resize image to default size
    # fit to smallest dimension
    im = ImageOps.contain(im, size)
    print(f"Resized image: {im.size}")

    # convert image to 2d pixel data
    pixels = im.getdata()
    print(f"Image converted to pixels: {len(list(pixels))}")

    # convert pixel tuples into brightness numbers
    pixels_brightness = [brightness_function(pxl) for pxl in pixels]
    print(f"Converted pixels to brightness: {len(pixels_brightness)}")

    # if --adjust selected, apply adjustment to each pixel
    if adjust:
        pixels_brightness = [
            factor * pxl if pxl < threshold else pxl for pxl in pixels_brightness
        ]

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
