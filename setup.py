from distutils.core import setup

setup(
    name="uberduck_discord_example",
    version="0.1dev",
    packages=["uberduck_discord_example"],
    license="MIT",
    long_description="placeholder",
    install_requires=[
        "aiohttp>=3.7.4",
        "nextcord @ git+https://github.com/nextcord/nextcord.git@master#egg=nextcord[voice]",
        "PyNaCl==1.4.0",
        "requests",
    ],
)

