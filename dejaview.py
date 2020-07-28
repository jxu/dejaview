# Finds duplicate images using perceptual average hash
# https://www.hackerfactor.com/blog/?/archives/432-Looks-Like-It.html

from sys import argv
import numpy as np
from PIL import Image
from pathlib import Path
from collections import defaultdict

def img_avg_hash(img):
    # force resize to 8x8 grayscale image and flatten as array
    thumb = img.resize((8, 8)).convert('L')
    gray_arr = np.asarray(thumb).flatten()

    # compute hash by comparing to average value and packing bits
    bool_arr = (gray_arr > gray_arr.mean()).astype(np.uint64)
    hash = bool_arr.dot(1 << np.arange(64, dtype=np.uint64))
    return hash


def main():
    img_hashes = defaultdict(list)

    for path in Path(argv[1]).rglob("*"):

        try:
            img = Image.open(path)
            hash = img_avg_hash(img)
            img_hashes[hash].append(path)
            #print(path, hex(hash))

        except:
            print("Could not open", path)

    # print images with same hash
    for path_list in img_hashes.values():
        if len(path_list) > 1:
            print(' '.join(map(str, path_list)))


if __name__ == "__main__":
    main()