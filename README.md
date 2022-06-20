<img align="right" src="./resources/ludii-logo-64x64.png">

# Ludii Python AI

[![license](https://img.shields.io/github/license/Ludeme/LudiiPythonAI)](LICENSE)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
[![twitter](https://img.shields.io/twitter/follow/ludiigames?style=social)](https://twitter.com/intent/follow?screen_name=ludiigames)

This repository contains information and examples for implementing general-game-playing AIs
in Python, with a Java wrapper around them, such that they can subsequently be used
in the Java-based Ludii General Game System.

- For general information on implementing AIs for Ludii (not in Python), see: https://github.com/Ludeme/LudiiExampleAI
- For general tutorials about Ludii, see: https://ludiitutorials.readthedocs.io

## Requirements

- Java version 8 or higher (including JDK)
- Python 3 (probably 3.6 or higher)

## Getting Started

The example in this repository consists of two parts:

1. A simple AI algorithm (UCT) implemented in Python.

2. A Java-based wrapper for your AI; this one is implemented following the standard
[Ludii Example AI](https://github.com/Ludeme/LudiiExampleAI) instructions, such that
it can be packaged in a JAR file, and loaded and used through the GUI of Ludii. In
the case of this repo, the Java code does not actually implement any AI algorithms,
but only contains code that, using the [jpy bridge](https://github.com/bcdev/jpy),
calls the Python-based AI code.

### Installing jpy

The code in this repository requires jpy to provide communication between Java and
Python, but jpy itself is not included and must instead be manually downloaded and
built by the end user. To do this, we refer to the [jpy repository](https://github.com/bcdev/jpy).

After following the instructions for building jpy, you should find the built library's
files somewhere under `/jpy/build/`. The exact files and location can be different for
different OSes. Generally, they will be `*.so` files for Unix, or `*.pyd` files for Windows.
These files, alongside the `jpyconfig.properties` and jpy's JAR files created by jpy's build process,
should be copied over into `/LudiiPythonAI/libs/`. This is the directory where the 
[Java code as we've implemented it](src/ludii_python_ai/LudiiPythonAI.java) will search
for these files, though you could modify that yourself if you prefer. The `jpyconfig.properties`
file as you copied it into this directory may also need to be manually modified (in any text editor)
to ensure that it still points to the correct locations for the jpy library files.

### Setting up Java project

Set up a Java project in your favourite IDE for Java, using the source code from this repository
to start with. The JAR file from jpy should be added to the build path. Additionally, Ludii's own
JAR file (downloaded from https://ludii.games/download.php) should also be added to the build
path (it may be convenient to also copy this file into `/LudiiPythonAI/libs/`).

Our [LudiiPythonAI.java](src/ludii_python_ai/LudiiPythonAI.java) provides an example implementation
that redirects calls from the Ludii GUI to the [Python-based UCT implementation](ludii_python/uct.py).
The [build.xml Ant script](build.xml) can be used to package this Java code in a JAR file that can
subsequently be loaded in Ludii's GUI using 
[the standard instructions for loading third-party AIs](https://github.com/Ludeme/LudiiExampleAI#loading-ai-in-the-ludii-application).

Note that this JAR file will not actually include the Python code or the jpy library files. For this reason,
the JAR file should be kept exactly where it is created and directly loaded from that location, such
that [our Java implementation](src/ludii_python_ai/LudiiPythonAI.java) can correctly find these files. Alternatively,
you may modify that Java code to change how it locates these files.

## Citing Information

When using Ludii in any publications (for example for running experiments, or
for visual inspections of your agent's behaviour during development, etc.), 
please cite [our paper on the Ludii system](http://ecai2020.eu/papers/1248_paper.pdf).
This can be done using the following BibTeX entry:


	@inproceedings{Piette2020Ludii,
            author      = "{\'E}. Piette and D. J. N. J. Soemers and M. Stephenson and C. F. Sironi and M. H. M. Winands and C. Browne",
            booktitle   = "Proceedings of the 24th European Conference on Artificial Intelligence (ECAI 2020)",
            title       = "Ludii -- The Ludemic General Game System",
            pages       = "411-418",
            year        = "2020",
            editor      = "G. De Giacomo and A. Catala and B. Dilkina and M. Milano and S. Barro and A. Bugarín and J. Lang",
            series      = "Frontiers in Artificial Intelligence and Applications",
            volume      = "325",
			publisher	= "IOS Press"
        }

## Background Info

This repository contains information and examples for the development of Python-based
AI implementations, with a Java wrapper such that they can subsequently be loaded
into the Java-based Ludii General Game System.

This work, as well as the full Ludii system itself, are developed for the
Digital Ludeme Project. More info on the project and the system can be found on:

- http://www.ludeme.eu/
- http://ludii.games/

## Contact Info

The preferred method for getting help with troubleshooting, suggesting or
requesting additional is [creating new Issues on the github repository](https://github.com/Ludeme/LudiiPythonAI/issues).
Alternatively, the following email address may be used: `ludii(dot)games(at)gmail(dot)com`.

## Acknowledgements

This repository is part of the European Research Council-funded Digital Ludeme Project (ERC Consolidator Grant \#771292), being run by Cameron Browne at Maastricht University's Department of Advanced Computing Sciences. 

<a href="https://erc.europa.eu/"><img src="./resources/LOGO_ERC-FLAG_EU_.jpg" title="Funded by the European Research Council" alt="European Research Council Logo" height="384"></a>
