## Как собирать 

```
./venv/Scripts/activate
pip install -r ./requirements.txt
pyinstaller --paths .\venv\Lib\site-packages\ --onefile .\image-compression.py
```

## Как пользоваться

1. Положить в корень или в папку input картинки.
2. Запустить прогу.
3. Подождать.
4. Забрать картинки из папки output.