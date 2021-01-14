import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='yfantasy-api-hkyplyr',
    version='0.0.5',
    author='Travis Paquette',
    author_email='tpaqu15@gmail.com',
    description='Python package to access the Yahoo! Fantasy APIs',
    long_description=long_description,
    long_description_content_Type='text/markdown',
    url='https://github.com/hkyplyr/yfantasy-api',
    packages=setuptools.find_packages(),
    classifiers=[],
    python_requires='>=3.6',
)
