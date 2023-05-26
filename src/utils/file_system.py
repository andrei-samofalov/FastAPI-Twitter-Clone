import hashlib
from contextlib import suppress
from pathlib import Path

import aiofiles
from fastapi import UploadFile

from utils.settings import MEDIA_ROOT


async def prepare_media_dir() -> None:
    """Создает директорию картинок, если ее нет, для загрузки"""
    Path(MEDIA_ROOT).mkdir(mode=0o777, parents=False, exist_ok=True)


async def get_filename(path: Path) -> Path:
    """Добавляет к имени файла цифру, если уже есть с таким именем"""
    counter = 0
    dir = path.resolve().parent
    file = path.stem
    extension = path.suffix
    if path.exists():
        while Path(str(dir), f"{file} ({counter}){extension}").is_file():
            counter += 1
        return Path(str(dir), f"{file} ({counter}){extension}")
    return path


async def write_file(file: UploadFile) -> str:
    """Записывает файл в директорию картинок."""
    with suppress(OSError):
        await prepare_media_dir()
        path = Path(MEDIA_ROOT, file.filename)
        filename = await get_filename(path)
        contents = file.file.read()
        async with aiofiles.open(filename, mode="wb") as f:
            await f.write(contents)

        return f"/images/{filename.stem}{filename.suffix}"


async def files_hash_is_equal(file1, file2) -> bool:
    """Сравнивает хэш двух файлов, возвращает результат сравнения."""
    async with aiofiles.open(file1, 'rb') as f1, aiofiles.open(
        file2, 'rb'
    ) as f2:
        hash1 = hashlib.sha256(await f1.read()).hexdigest()
        hash2 = hashlib.sha256(await f2.read()).hexdigest()

    return hash1 == hash2
