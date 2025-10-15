from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="RAG Medcal Chatbot",
    version="0.1",
    author="Sudhanshu",
    packages=find_packages(),
    install_requires = requirements,
)

# d403628d89c19fb997d5339b3f2a235398ef52629e1bd23b528924beeaeaefb5