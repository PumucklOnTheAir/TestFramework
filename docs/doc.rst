#####################################
Documentation
#####################################

The main documentation lives online under https://freifunk-testframework.readthedocs.org .
It will be instantly generated after a commit to the master branch.

For testing purpose it exist also a live documentation under https://freifunk-testframework.readthedocs.org/en/doc-test/ .
It represents the branch "doc-test". Every developer is free to use this branch for testing the documentation.

How to document
=================
Documentation is based on Sphinx and reStructuredText for description.
More infos about the markups under http://sphinx-doc.org/rest.html.

The module and class description has to be provided in the module file itself as an docstring.
Then it is possible to import the description with following markup::

  .. automodule:: server.ipc
    :members:



How to generate the documentation
===================================

After installing installing all required modules (pip3 install -r requirements.txt) you generate the documentation by your own.
Run *python3 -m sphinx . ./_build/html/* in the *docs/* directory. The documentation in HTML will be placed under *docs/_build/html/*


UML diagrams
=================
UML diagrams will be generated when the documentation is generating.
The images are under *docs/_build/html/uml/*. New classes/packages have to be inserted manual in the last line of the *docs/conf.py*.

With this markup you can add easily add the images to your description::

  .. image:: uml/classes_server.png
    :alt: UML class diagram of the module server
