General Information
=======================================

About
----------
``configurio`` is a powerful and easy to use tool for working with various configuration files. It provides a friendly, high-level interaction layer with configuration files, relieving the developer of the task of manually reading, writing, modifying and verifying files.


.. _general-supported-langs:

Supported Languages
--------------------------------------
List of currently supported languages. Languages, listed in **Native Support** are supported by python without any external packages, while **External Support** requires external packages to be installed. For more information go here: :doc:`guide_installation`

- Native Support:
    - ``JSON``
- External Support
    - ``YAML`` <= 1.2

Module Hierarchy
--------------------------------
- ``configurio`` - Contains main language parsers and module meta information imports for easy access.
    - ``core`` - Realisation of basic features, that will be inherited and used in other modules.
    - ``meta`` - Meta information, like version, author, etc.
    - ``configs`` - Submodule with realisation of main features for different languages
        - ``json``
        - ``yaml``
        - ``ini``
    - ``tests`` - PyTest unit testing suite