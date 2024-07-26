from PIL import Image, ImageFilter


def temp_save(im, suffix):
    """Temporarily save an image in tmp directory."""
    f_out = f"tmp/tmp{suffix}.jpg"
    im.save(f_out)


if __name__ == "__main__":
    f_name = "cat.jpg"
    im = Image.open(f_name)

    # apply some transformation, then save image
    temp_save(im, "orig")

    filters = [
        ("contour", ImageFilter.CONTOUR),
        ("detail", ImageFilter.DETAIL),
        ("edge_enhance", ImageFilter.EDGE_ENHANCE),
        ("edge_enhance_more", ImageFilter.EDGE_ENHANCE_MORE),
        ("emboss", ImageFilter.EMBOSS),
        ("find_edges", ImageFilter.FIND_EDGES),
        ("sharpen", ImageFilter.SHARPEN),
        ("smooth", ImageFilter.SMOOTH),
        ("smooth_more", ImageFilter.SMOOTH_MORE),
    ]

    for n, f in filters:
        tmp_im = im.filter(f)
        temp_save(tmp_im, n)
