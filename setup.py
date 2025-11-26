import os
import io
from pathlib import Path

from setuptools import find_namespace_packages, setup

def get_package_data():
    ROOT_PATH = os.path.abspath("./graphex_webautomation_plugin")
    DOCS_PATH = os.path.join(ROOT_PATH, "docs")
    files = []
    for directory, _, filenames in os.walk(DOCS_PATH):
        for filename in filenames:
            path = os.path.join(directory, filename)
            path = path[len(ROOT_PATH) :].strip("/")
            files.append(path)
    return {"graphex_webautomation_plugin": files}

def read_readme():
    readme_path = Path(__file__).parent / "README.md"
    with io.open(readme_path, "r", encoding="utf-8") as f:
        return f.read()

setup(
    name="graphex-webautomation-plugin",
    version="1.1.3",
    author="The MITRE Corporation",
    description="A plugin for adding playwright nodes to graphex.",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/mitre/GraphEx-Web-Automation-Plugin",
    project_urls={
        "Documentation": "https://github.com/mitre/GraphEx-Web-Automation-Plugin/blob/main/graphex_webautomation_plugin/docs/markdown/index.md",
        "Source": "https://github.com/mitre/GraphEx-Web-Automation-Plugin",
        "Issues": "https://github.com/mitre/GraphEx-Web-Automation-Plugin/issues",
        "Changelog": "https://github.com/mitre/GraphEx-Web-Automation-Plugin/blob/main/graphex_webautomation_plugin/docs/markdown/changelog.md",
    },
    license="Apache-2.0",
    license_files=["LICENSE"],
    keywords = ["playwright","playwright-plugin","web-automation","browser-automation","automation","visual-programming","python3","python","pip","pypi","headless","ui-testing","functional-testing","test-automation","page-object","selectors","dom","chromium","firefox","webkit","plugin","extension","middleware","hooks","orchestration","workflow","cli","sdk","http","web","tracing","recorder","fixtures"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    packages=find_namespace_packages(include=["graphex_webautomation_plugin*"]),
    package_data=get_package_data(),
    python_requires=">=3.8",
    install_requires=["mitre-graphex>=1.16.0", "playwright==1.46.0"],
    include_package_data=True
)
