import itertools
import argparse
import os

def split_file(input_file, chunk_size, output_prefix='part', encoding='utf-8'):
    """Разбивает текстовый файл на части по количеству строк."""
    buffer_size = 1024 * 1024  # 1 МБ для ускорения I/O
    
    if not os.path.exists(input_file):
        print(f"Ошибка: Файл '{input_file}' не найден.")
        return
        
    if chunk_size <= 0:
        print("Ошибка: Количество строк (chunk_size) должно быть больше 0.")
        return

    print(f"Начинаю разбиение файла '{input_file}' по {chunk_size} строк...")
    
    # Открываем файл с увеличенным буфером
    with open(input_file, 'r', encoding=encoding, buffering=buffer_size) as f:
        for i in itertools.count():
            chunk_iter = itertools.islice(f, chunk_size)
            
            # Проверяем, есть ли еще строки
            try:
                first_line = next(chunk_iter)
            except StopIteration:
                break  # Файл закончился

            # Формируем имя файла с ведущими нулями для правильной сортировки
            output_file = f'{output_prefix}_{i:04d}.txt'
            
            # Записываем часть "лениво" (без загрузки в память)
            with open(output_file, 'w', encoding=encoding, buffering=buffer_size) as part_file:
                part_file.write(first_line)
                part_file.writelines(chunk_iter)
                
            print(f"Создан файл: {output_file}")
            
    print("Готово!")

if __name__ == '__main__':
    # Настройка парсера аргументов командной строки
    parser = argparse.ArgumentParser(
        description="Утилита для разбиения больших текстовых файлов на части по количеству строк."
    )
    
    # Обязательный позиционный аргумент (название файла)
    parser.add_argument(
        'input_file', 
        type=str, 
        help="Путь к входному файлу (например, data.txt или script.json)"
    )
    
    # Необязательный аргумент для количества строк (с значением по умолчанию)
    parser.add_argument(
        '-c', '--chunk-size', 
        type=int, 
        default=1500000, 
        help="Количество строк в одном файле (по умолчанию: 1500000)"
    )
    
    # Необязательный аргумент для префикса выходных файлов
    parser.add_argument(
        '-p', '--prefix', 
        type=str, 
        default='part', 
        help="Префикс для имен выходных файлов (по умолчанию: 'part')"
    )
    
    # Необязательный аргумент для кодировки
    parser.add_argument(
        '-e', '--encoding', 
        type=str, 
        default='utf-8', 
        help="Кодировка файла (по умолчанию: utf-8)"
    )

    args = parser.parse_args()
    
    # Запуск функции с переданными параметрами
    split_file(
        input_file=args.input_file, 
        chunk_size=args.chunk_size, 
        output_prefix=args.prefix,
        encoding=args.encoding
    )