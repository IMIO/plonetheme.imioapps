from setuptools import find_packages
from setuptools import setup


version = "3.0.0.dev0"

long_description = (
    open("README.rst").read() + "\n\n" + open("CHANGES.rst").read() + "\n"
)

setup(
    name="plonetheme.imioapps",
    version=version,
    description="Plone theme for most Imio applications",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 6 - Mature",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.2",
        "Framework :: Plone :: Addon",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="Plone IMIO",
    author="IMIO team",
    author_email="devs@imio.be",
    url="https://github.com/IMIO/plonetheme.imioapps/",
    license="gpl",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10",
    install_requires=[
        "setuptools",
        "collective.messagesviewlet>=1.0b4",
        "imio.helpers",
        "plone.api",
        "plone.app.layout",
        "plone.base",
        "plone.formwidget.namedfile",
        "plone.resource",
        "Products.CMFCore",
        "Products.CMFPlone",
        "Products.GenericSetup",
        "Zope",
        "zope.i18nmessageid",
        "zope.interface",
        "zope.schema",
    ],
    extras_require={
        "test": [
            "plone.app.robotframework",
            "plone.app.testing",
            "plone.testing",
        ]
    },
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
