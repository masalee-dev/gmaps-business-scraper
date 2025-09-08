from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="gmaps-business-scraper",
    version="0.0.1",
    author="Masalee",
    author_email="masaleedesign@gmail.com",
    description="A Python tool for scraping business data from Google Maps.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/masalee-dev/gmaps-business-scraper",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
    python_requires='>=3.7',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'gmaps-scraper=main:cli',
        ],
    },
    keywords="google maps, web scraping, business data, selenium, data extraction",
    project_urls={
        "Bug Reports": "https://github.com/masalee-dev/gmaps-business-scraper/issues",
        "Source": "https://github.com/masalee-dev/gmaps-business-scraper",
        "Documentation": "https://github.com/masalee-dev/gmaps-business-scraper#readme",
    },
)