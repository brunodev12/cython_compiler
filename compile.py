import os
from setuptools import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

def get_python_files_in_folders(root_folder, exclude_files=None):
    python_files = []
    exclude_files = exclude_files or []

    for foldername, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith('.py') and filename not in exclude_files:
                python_files.append(os.path.join(foldername, filename))

    return python_files

root_folder = "."
exclude_files = ['compile.py', 'test.py', 'main.py']     #All files that you do not want to be compiled
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
    name='project_name',
    cmdclass={'build_ext': build_ext},
    ext_modules=cythonize(extensions, compiler_directives={'language_level': "3"}),
)
