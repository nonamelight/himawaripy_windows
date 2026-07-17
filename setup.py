from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="himawaripy",
    version="2.2.0",
    url="https://github.com/nonamelight/himawaripy_windows#",
    author="gandalp",
    author_email="nonamelight1@naver.com",
    license="MIT",
    description="himawaripy is a Python 3 script that fetches near-realtime (10 minutes delayed) picture of Earth "
                "as its taken by Himawari 8 (ひまわり8号) and sets it as your desktop background.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["appdirs", "pillow", "python-dateutil", "pystray", "schedule"],
    packages=find_packages(),
    entry_points={"console_scripts": ["himawaripy=himawaripy.__main__:main"]},
)
