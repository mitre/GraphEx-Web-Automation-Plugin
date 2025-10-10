from setuptools import setup, find_packages

setup(
    name="graphex_webautomation_plugin",
    version="1.1.0",
    author="The MITRE Corporation",
    description="A plugin for adding playwright nodes to graphex.",
    packages=find_packages(include=["graphex_webautomation_plugin*"]),
    python_requires=">=3.8",
    install_requires=["graphex>=0.3.0", "playwright==1.46.0"],
)
