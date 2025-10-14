from setuptools import setup, find_packages

setup(
    name="graphex-webautomation-plugin",
    version="1.1.2",
    author="The MITRE Corporation",
    description="A plugin for adding playwright nodes to graphex.",
    packages=find_packages(include=["graphex-webautomation-plugin*"]),
    python_requires=">=3.8",
    install_requires=["mitre-graphex>=1.16.0", "playwright==1.46.0"],
)
