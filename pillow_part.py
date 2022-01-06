def pic2text(imagename):
    from PIL import Image

    im = Image.open(f'images/{imagename}.png')
    pixels = im.load()
    _WIDTH = 100
    _HEIGHT = 100
    resized_img = im.resize((_WIDTH, _HEIGHT), Image.ANTIALIAS)
    pixels = resized_img.load()
    x, y = resized_img.size
    values = []
    for i in range(x):
        for j in range(y):
            c = pixels[i, j]
            if c[0] <= 100 and c[1] <= 100 and c[2] <= 100:
                values.append((i, j))
    return values
