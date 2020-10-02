import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='yahoo-api-hkyplyr',
    version='0.0.2',
    author='Travis Paquette',
    author_email='tpaqu15@gmail.com',
    description='Python app to access the Yahoo! Fantasy APIs',
    long_description=long_description,
    long_description_content_Type='text/markdown',
    url='https://github.com/hkyplyr/yahoo-api',
    packages=setuptools.find_packages(),
    classifiers=[],
    python_requires='>=3.6',
)
