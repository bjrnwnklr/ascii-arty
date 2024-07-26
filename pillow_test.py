from PIL import Image, ImageOps


def temp_save(im, suffix):
    """Temporarily save an image in tmp directory."""
    f_out = f"tmp/tmp{suffix}.jpg"
    im.save(f_out)


if __name__ == "__main__":
    f_name = "cat.jpg"
    im = Image.open(f_name)

    # apply some transformation, then save image
    temp_save(im, "orig")
