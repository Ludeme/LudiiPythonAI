"""
Example UCT implementation in Python, which (with a Java wrapper) can be used
to play in the Ludii general game system.

@author Dennis Soemers
"""

import jpy


class UCT:
    """
    UCT class in Python, implements Ludii's (Java) abstract class "AI"
    """

    def __init__(self):
        """
        Constructor
        """
        print("Python UCT constructor running!")

