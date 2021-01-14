import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()


if __name__ == "__main__":
    import yfantasy_api

    setuptools.setup(
        name='yfantasy-api',
        version=yfantasy_api.__version__,
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
