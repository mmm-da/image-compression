from PIL import Image
from pathlib import Path
from tqdm import tqdm
from os import stat

#размер в килобайтах
max_file_size = 500

quality_step = 2

input_paths = [
    Path('./'),
    Path('./input')
]

output_path = Path('./output')

supported_formats = [
    '.png',
    '.jpg',
    '.jpeg',
    '.gif',
    '.webp',
    '.ico',
    '.bmp'
]

def get_all_images(path:Path):
    images = []
    for child in path.iterdir():
        if child.is_file():
            if child.suffix in supported_formats:
               images.append(child) 
    return images

def convert_to_jpg(input:Path,output:Path,quality:int):
    image = Image.open(input)
    image = image.convert('RGB')
    image.save(output,quality=quality)

def check_file_size(path:Path):
    return stat(path).st_size//1024

def compress_to_size(input:Path,size:int):
    quality = 100
    need_compression = True

    while need_compression and quality>5:
        output = str(output_path)+'/'+input.stem+'.jpg'
        convert_to_jpg(
            input,
            output,
            quality
        )
        if check_file_size(output) <= size:
            need_compression = False
        else:
            quality -= quality_step
            Path(output).unlink()
        
        if quality < 40:
            tqdm.write(' ⚠️ ВНИМАНИЕ! ⚠️ ВНИМАНИЕ! ⚠️ Файл {} сжался с сильной потерей качества! Лучше обработать руками.'.format(input))

if __name__ == "__main__":
    images = []
    
    print('[🔎] Ищем картинки ...')
    
    for path in input_paths:
        try:
            images += get_all_images(path)
        except FileNotFoundError as error:
            tqdm.write('[⚠️] Папка {} не найдена'.format(path))

    images_count = len(images)

    if images_count > 0:
        tqdm.write('[✔️] Найдено {} шт'.format(len(images)))

        tqdm.write('[⏳] Начинаем сжимать до {} Кб'.format(max_file_size))

        output_path.mkdir(exist_ok=True)

        for image in tqdm(images):
            compress_to_size(image,max_file_size)

        tqdm.write('[✔️] Готово! Результат в папке output.')
        input()
    else:
        tqdm.write('[❌] Не найдены изображения. Перенесите файлы в эту папку или папку input')
        input()
