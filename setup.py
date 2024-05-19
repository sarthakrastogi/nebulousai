from setuptools import setup, find_packages

setup(
    name="nebulousai",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "litellm==1.34.0",
        "wikipedia==1.4.0",
        "duckduckgo_search==6.1.0",
        
    ]
)