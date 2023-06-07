import io
import re
from setuptools import setup


def read(path):
    with io.open(path, mode="r", encoding="utf-8") as fd:
        content = fd.read()
    # Convert Markdown links to reStructuredText links
    return re.sub(r"\[([^]]+)]\(([^)]+)\)", r"`\1 <\2>`_", content)


setup(
    name='huanxiangjiLib',
    version='0.1.0',
    author='VeronicaAlexia',
    author_email='Elaina-Alex@proton.me',
    packages=['huanxiangjiLib'],
    url='https://github.com/VeronicaAlexia/huanxiangji-api-python',
    license='MIT',
    description='this is a huanxiangjiLib api, you can use it to get huanxiangji book info',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    keywords=['huanxiangjiLib'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    install_requires=["rich", "Scrapy", "requests"],
)