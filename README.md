# Ascii Arty

A simple project to convert photos into ASCII art, inspired by [Robert Heaton's Programming Projects for Advanced Beginners #1: ASCII art](https://robertheaton.com/2018/06/12/programming-projects-for-advanced-beginners-ascii-art/)

# High level steps

1. read in image and print height and width in pixels
    - resize image to screen size
2. load image data into 2d array
3. Convert RGB tuples into single brightness numbers
4. Convert brightness numbers to ASCII characters
5. Print ASCII version of image
    - print 2-3 horizontal characters as chars are higher than wide

## Improvements

-   Multiple brightness conversion algorithms
    -   average, min_max, luminosity (0.21 R + 0.72 G + 0.07 B)
    -   [More detail on StackOverflow](https://stackoverflow.com/questions/596216/formula-to-determine-perceived-brightness-of-rgb-color)
-   Invert dark to light
-   Print in color

## ASCII characters by brightness

```
`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$
```

## Example image

Kitty photo by [Loan]("https://unsplash.com/@l_oan?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash") on [Unsplash](https://unsplash.com/photos/silver-tabby-kitten-on-floor-7AIDE8PrvA0?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash")

[Cat photo](https://unsplash.com/photos/brown-and-white-tabby-cat-mBRfYA0dYYE?utm_content=creditShareLink&utm_medium=referral&utm_source=unsplash) by Lloyd Henneman on Unsplash

# Documentation - Pillow

[Pillow](https://pillow.readthedocs.io/en/stable/)

### Key methods / concepts

-   Read an image

```python
from PIL import Image
im = Image.open("name.jpg")
```

Print image information

```python
print(im.format, im.size, im.mode)
# print RGB information

```

-   Get image pixel values

Returns the image pixels as a flattened list

```python
pixels = im.getdata(band=None|0)
list(pixels) # turn to ordinary list for printing

# get values of a specific pixel
pixel = im.getpixel(xy: tuple[int, int])
```

-   Resize an image

```python
im.resize()
# resize relative to a given size
from PIL import Image, ImageOps
size = (100, 150)
ImageOps.contain(im, size).save("new file") # fits to smallest dimension = (100, 100)
ImageOps.cover(im, size).save("new file") # fits to largest dimension = (150, 150)
ImageOps.fit(im, size).save("new file") # fits to exact dimension = (100, 150)
ImageOps.pad(im, size).save("new file") # pads the image to smallest dimension and pads the remaining pixels = (100, 150)
```
