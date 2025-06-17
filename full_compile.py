import os
import shutil
from setuptools import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

SOURCE_DIR = "../Listen Events"
TARGET_DIR = "."
EXCLUDE_FILES = ['compile.py', 'test.py', 'main.py', 'readme.txt', 'full_compile.py']  # Archivos que no quieres compilar ni borrar
FOLDERS_TO_COPY = ['src', 'utils', 'data', 'database', 'services']  # Agrega aquí todas las carpetas que quieras copiar

# ---- 1. LIMPIAR CARPETAS EXISTENTES EN TARGET_DIR ----
for folder in FOLDERS_TO_COPY:
    target_path = os.path.join(TARGET_DIR, folder)
    if os.path.exists(target_path):
        shutil.rmtree(target_path)
        print(f"Eliminada carpeta antigua: {target_path}")

# ---- 2. COPIAR CARPETAS DESDE listen-events ----
for folder in FOLDERS_TO_COPY:
    source_path = os.path.join(SOURCE_DIR, folder)
    target_path = os.path.join(TARGET_DIR, folder)
    if os.path.exists(source_path):
        shutil.copytree(source_path, target_path)
        print(f"Copiada carpeta: {source_path} → {target_path}")
    else:
        print(f"ADVERTENCIA: No se encontró {source_path}, se omitirá.")

# ---- 3. BUSCAR ARCHIVOS .py PARA COMPILAR ----
def get_python_files_in_folders(root_folder, exclude_files=None):
    python_files = []
    exclude_files = exclude_files or []

    for foldername, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith('.py') and filename not in exclude_files:
                python_files.append(os.path.join(foldername, filename))

    return python_files

root_folder = "."
exclude_files = ['compile.py', 'test.py', 'main.py', 'full_compile.py']     #All files that you do not want to be compiled
python_files = get_python_files_in_folders(root_folder, exclude_files)

extensions = []

for file in python_files:
    file_list = file.split('/')
    file_without_py = file_list[2].split('.')[0]
    extensions.append(Extension(f"{file_list[1]}.{file_without_py}", [f"{file_list[1]}/{file_list[2]}"]))

#If you got the error: <Cython directive 'language_level' not set> uncomment the lines below
# for ext_module in extensions:
#     ext_module.cython_directives = {'language_level': "3"}

setup(
    name='listenEvents',
    cmdclass={'build_ext': build_ext},
    ext_modules=cythonize(extensions, compiler_directives={'language_level': "3"}),
)

# ---- 4. ELIMINAR ARCHIVOS NO .so ----
for foldername, _, filenames in os.walk(TARGET_DIR):
    for filename in filenames:
        file_path = os.path.join(foldername, filename)

        # Eliminar si NO termina en .so y NO está en la lista de exclusión
        if not filename.endswith('.so') and filename not in EXCLUDE_FILES:
            try:
                os.remove(file_path)
                print(f"Archivo eliminado: {file_path}")
            except Exception as e:
                print(f"No se pudo eliminar {file_path}: {e}")

# ---- 5. ELIMINAR CARPETAS __pycache__ ----
for foldername, dirnames, _ in os.walk(TARGET_DIR):
    for dirname in dirnames:
        if dirname == "__pycache__":
            cache_path = os.path.join(foldername, dirname)
            try:
                shutil.rmtree(cache_path)
                print(f"Carpeta __pycache__ eliminada: {cache_path}")
            except Exception as e:
                print(f"No se pudo eliminar {cache_path}: {e}")