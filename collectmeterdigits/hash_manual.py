from PIL import Image
from datetime import date
import imagehash
from collectmeterdigits.collect import save_hash_file, ziffer_data_files

def calculate_hash(image_filenames, meter, hashfunc = imagehash.average_hash):
    images = []
    print(f"Calculate hashes for {len(image_filenames)} images ..." )

    datum = date.today().strftime("%Y-%m-%d")

    for img in sorted(image_filenames):
        try:
            hash = hashfunc(Image.open(img).convert('L').resize((32,20)))
        except Exception as e:
            print('Problem: ', e, ' with ', img)
            continue
        images.append([hash, img, meter, datum])
    return images;


input_dir = "./data/labeled_20220606"
hashfilename = "./data/HistoricHashData.txt"

image_filenames = ziffer_data_files(input_dir)
hash = calculate_hash(image_filenames, "hash_manual")
save_hash_file(hash, hashfilename)


