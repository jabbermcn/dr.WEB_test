import os
import shutil
import subprocess
import urllib.request
import zipfile
import ssl

# Установка переменных
zlib_url = 'https://github.com/madler/zlib/archive/master.zip'
zlib_dir = 'zlib-master'
build_dir = 'zlib_build'
install_dir = 'zlib_install'

# Скачивание и распаковка исходного кода
print('Скачивание и распаковка исходного кода...')

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Download the file using urlopen and a custom Request object
req = urllib.request.Request(zlib_url)
response = urllib.request.urlopen(req, context=ssl_context)
with open('zlib.zip', 'wb') as file:
    file.write(response.read())

# Extract the downloaded file
with zipfile.ZipFile('zlib.zip', 'r') as zip_ref:
    zip_ref.extractall()

# Переход в директорию с исходным кодом
os.chdir(zlib_dir)

# Сборка проекта с помощью MS Visual Studio и Makefile
print('Сборка проекта...')
if os.name == 'nt':
    subprocess.run(['msbuild', 'contrib\\vstudio\\vc14\\zlibvc.sln', '/p:Configuration=Release'])
else:
    subprocess.run(['make', 'distclean'])
    os.chmod('./configure', 0o755)  # Grant execution permissions to the configure script
    subprocess.run(['./configure'])
    subprocess.run(['make'])

# Создание директории для установки
if not os.path.exists(install_dir):
    os.makedirs(install_dir)

# Копирование файлов в директорию установки
print('Копирование файлов в директорию установки...')
if os.name == 'nt':
    shutil.copy(os.path.join(zlib_dir, 'contrib', 'vstudio', 'vc14', 'Win32', 'Release', 'zlibwapi.lib'), install_dir)
    shutil.copy(os.path.join(zlib_dir, 'contrib', 'vstudio', 'vc14', 'x64', 'Release', 'zlibwapi.lib'), install_dir)
    shutil.copy(os.path.join(zlib_dir, 'contrib', 'vstudio', 'vc14', 'Win32', 'Release', 'zlibwapi.dll'), install_dir)
    shutil.copy(os.path.join(zlib_dir, 'contrib', 'vstudio', 'vc14', 'x64', 'Release', 'zlibwapi.dll'), install_dir)
else:
    shutil.copy('libz.a', install_dir)
    # shutil.copy(os.path.join(zlib_dir, 'libz.so'), install_dir)

# Очистка директории сборки
print('Очистка директории сборки...')
if os.path.exists(build_dir):
    shutil.rmtree(build_dir)
os.mkdir(build_dir)

# Копирование файлов в директорию сборки
print('Копирование файлов в директорию сборки...')
if os.name == 'nt':
    shutil.copy(os.path.join(install_dir, 'zlibwapi.lib'), build_dir)
    shutil.copy(os.path.join(install_dir, 'zlibwapi.dll'), build_dir)
else:
    shutil.copy('libz.a', build_dir)
    # shutil.copy(os.path.join(install_dir, 'libz.so'), build_dir)

os.chdir('..')  # Вернуться в исходную директорию

# Очистка
print('Очистка...')
if os.path.exists(os.path.abspath(install_dir)):
    shutil.rmtree(os.path.abspath(install_dir))
os.remove('zlib.zip')

print('Успешно завершено!')
