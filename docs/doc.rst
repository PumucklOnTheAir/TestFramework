#############
Documentation
#############

The main documentation can be found online on https://freifunk-testframework.readthedocs.org .
It will be generated instantly after a commit to the master branch.

For testing purpose there is a live documentation on https://freifunk-testframework.readthedocs.org/en/doc-test/ .
It represents the branch "doc-test". Every developer is free to use this branch for testing the documentation.

How to document
===============
Documentation is based on Sphinx and reStructuredText for description.
More infos about the markups under http://sphinx-doc.org/rest.html.

The module and class description has to be provided in the module file itself as a docstring.
Then it is possible to import the description with following markup::

  .. automodule:: server.ipc
    :members:

How to generate the documentation
=================================

After installing installing all required modules (pip3 install -r requirements.txt) you generate the documentation yourself.
Run *python3 -m sphinx . ./_build/html/* in the *docs/* directory. The documentation in HTML will be placed in *docs/_build/html/*


UML diagrams
============
UML diagrams will be generated when the documentation is generating.
The images are under *docs/_build/html/uml/*. New classes/packages have to be inserted manually in the last line of the *docs/conf.py*.

With this markup you can easily add the images to your description::

  .. image:: uml/classes_server.png
    :alt: UML class diagram of the module server
