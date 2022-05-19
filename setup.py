from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as readme:
    description = readme.read()

setup(
    name="scp",
    version="0.2.0",
    author="iaacornus",
    author_email="iaacornus.devel@gmail.com",
    description="View SCP Foundation's entry from your terminal!",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/iaacornus/scpterm",
    py_modules=[
        "main",
        "cli",
        "utils/md_init",
        "utils/database_init",
        "utils/scp_utils",
        "tui/tui",
    ],
    include_package_data=True,
    package_dir={
        "": "src",
        "img": "img",
        "program_help": "program_help"
    },
    packages=find_packages(
        where="src",
        include=[
            "utils",
            "tui"
        ]
    ),
    package_data={
        "program_help": ["program_help/wiki.md"],
        "img": ["img/scp_logo.txt"]
    },
    python_requires="<=3.10.4",
    install_requires=[
        "requests<=2.27.1",
        "rich<=12.4.1",
        "bs4<=0.0.1",
        "random_user_agent<=1.0.1",
        "html5lib<=1.1",
        "opencv-python<=4.5.5.64"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
        "Intended Audience :: End Users/Desktop",
        "Operating System :: POSIX :: ",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment "
    ],
    entry_points={
        "console_scripts" : [
            "scp=cli:program_options",
        ]
    },
)
