=====================
sphinxcontrib.algodoc
=====================

Sphinx extension for easy documentation of algorithms written in python.
Knocked up to help document a largeish piece of code... you could call it a Beta version!

.. contents::
    :local:
    :depth: 1
    :backlinks: none
    
------------
Installation
--------------

* Clone the repo
* Copy algodoc.py to YOURPYTHONDIR/site-packages/sphinxcontrib/

--------
Usage
--------

-----------------
In your rst file:
------------------

.. algodoc:: modulename.functionname

   :title: my algorithm
   
OR

.. algodoc:: modulename.classname.functionname

--------------------
In your python code:
-----------------------

    def functionname(bar):
    
    """ docstring
    """
    
    #: Step 1: Set x = 0
    x = 0
    
    #: 1a. Add 100 to x
    x += 100
    
    #:#
    
    #: Step 2: Set y = 1000
    y = 1000
    
    #: 2a. Divide y by 10
    y = y / 10
    
    #:#
    
    #: Step 3: Add Them!
    z = x + y
    
-------
Output:
-------

**my algorithm**

Function: modulename.functionname

*Step 1: Set x = 0*

1a. Add 100 to x

*Step 2: Set y = 1000*

2a. Divde y by 10

*Step 3: Add Them!*



    