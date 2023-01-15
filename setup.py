from setuptools import setup

setup(
    name="walking_ani",
    version="0.0.1",
    packages=["walking_ani"],
    entry_points={
        "console_scripts": [
            "walking_ani = walking_ani.__main__:main"
        ]
    },
    install_requires=["pygame"]
)