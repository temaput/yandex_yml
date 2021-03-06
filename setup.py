import setuptools

setuptools.setup(
    name="yandex-yml",
    version="0.1.0",
    url="https://github.com/temaput/yandex_yml",

    author="Artem Putilov",
    author_email="putilkin@gmail.com",

    description="Package for working with yandex market yml prices",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
