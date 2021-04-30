import os
import sys
from setuptools import setup

VERSION = '1.3'

if sys.argv[-1] == 'publish':
    if os.system("pip freeze | grep wheel"):
        print("wheel not installed.\nUse `pip install wheel`.\nExiting.")
        sys.exit()
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    print("You probably want to also tag the version now:")
    print("  git tag -a {0} -m 'version {0}'".format(VERSION))
    print("  git push --tags")
    sys.exit()

setup(
    name="mkdocs_markdown_graphviz",
    version=VERSION,
    py_modules=["mkdocs_markdown_graphviz"],
    install_requires=['Markdown>=2.3.1'],
    author="Rodrigo SCHWENCKE",
    author_email="dev.hopper@lyceeperier.fr",
    description="Render Graphviz graphs as inline SVGs and PNGs in Mkdocs with Markdown (python3 version)",
    long_description_content_type="text/markdown",
    long_description="""This is just a continuation of the great job of :

* Cesare Morel [cesaremorel/markdown-inline-graphviz](https://github.com/cesaremorel/markdown-inline-graphviz), and before him,
* Steffen Prince in [sprin/markdown-inline-graphviz](https://github.com/sprin/markdown-inline-graphviz), 
* Initially inspired by Jawher Moussa [jawher/markdown-dot](https://github.com/jawher/markdown-dot)
    
in order to get it work with pip3 and mkdocs.

If you use python 2, please use the original extension instead.""",
    license="MIT",
    url="https://github.com/rodrigoschwencke/mkdocs-markdown-graphviz",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Documentation',
        'Topic :: Text Processing',
        'License :: OSI Approved :: MIT License',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
