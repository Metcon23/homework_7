from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='1.0',
    description='HomeWork_7',
    author='Taras Tkachyk',
    author_email='jungltmg@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'clean-folder = clean_folder.clean:main'
        ]
    },
)
