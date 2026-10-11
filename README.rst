.. image:: https://github.com/IMIO/plonetheme.imioapps/actions/workflows/main.yml/badge.svg
    :target: https://github.com/IMIO/plonetheme.imioapps/actions/workflows/main.yml
.. image:: https://coveralls.io/repos/github/IMIO/plonetheme.imioapps/badge.svg
    :target: https://coveralls.io/github/IMIO/plonetheme.imioapps

====================
plonetheme.imioapps
====================

Site theme shared between imio's applications.

Fixed header :
--------------

From version 2.1, the header is fixed (always visible), to remove this, add this to the custom CSS
of the theming control panel (Plone 6) :

.. code:: css

  #content-header,
  #mainnavigation-wrapper {
     position: relative;
  }


Dashboard table sticky header :
-------------------------------

From version 2.22, the tablea header is stikcy (will be sticked to the page header when scrolling down),
to remove this, add this to the custom CSS of the theming control panel :

.. code:: css

  table.faceted-table-results th {

    position: inherit;

  }
