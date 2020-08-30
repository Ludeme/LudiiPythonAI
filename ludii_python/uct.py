"""
Example UCT implementation in Python, which (with a Java wrapper) can be used
to play in the Ludii general game system.

The implementation is based on our Example UCT implementation in Java
(see: https://github.com/Ludeme/LudiiExampleAI/blob/master/src/mcts/ExampleUCT.java)

NOTE: because we don't extend the abstract AI class from Java, we can't inherit
the "wantsInterrupt" flag and hence can't make our AI automatically stop
when the Pause button is pressed in the GUI.

@author Dennis Soemers
"""

import math
import numpy as np
import random
import time


def rank_to_util(rank, num_players):
    """
    Helper method to convert a rank into a utility value
    (copied from AIUtils in the Ludii Java code)

    :param rank:
    :param num_players:
    :return:
    """
    if num_players == 1:
        return 2.0 * rank - 1.0
    else:
        return 1.0 - ((rank - 1.0) * (2.0 / (num_players - 1)))


def utilities(context):
    """
    Helper method to compute an array of utility values for a given
    Ludii context object (copied from AIUtils in the Ludii Java code)

    :param context:
    :return:
    """
    ranking = context.trial().ranking()
    utils = np.zeros(len(ranking))
    num_players = len(ranking) - 1

    for p in range(1, len(ranking)):
        rank = ranking[p]
        if num_players > 1 and rank == 0.0:
            rank = context.computeNextDrawRank()

        utils[p] = rank_to_util(rank, num_players)

    return utils


class UCT:
    """
    UCT class in Python, implements Ludii's (Java) abstract class "AI"
    """

    def __init__(self):
        """
        Constructor
        """
        self._player_id = -1

    def init_ai(self, game, player_id):
        """
        Initialises the AI

        :param game:
        :param player_id:
        """
        self._player_id = player_id

    def select_action(self,
                      game,
                      context,
                      max_seconds,
                      max_iterations,
                      max_depth):
        """
        Returns an action to play

        :param game:
        :param context:
        :param max_seconds:
        :param max_iterations:
        :param max_depth:
        :return:
        """
        # Start out by creating a new root node (no tree reuse in this example)
        root = Node(None, None, context)
        num_players = game.players().count()

        # We'll respect any limitations on max seconds and max iterations
        # (don't care about max depth)
        stop_time = time.time() + max_seconds if max_seconds > 0.0 else math.inf
        max_its = max_iterations if max_iterations > 0 else math.inf

        num_iterations = 0

        # Our main loop through MCTS iterations
        while num_iterations < max_its and time.time() < stop_time:
            # Start in root node
            current = root

            # Traverse tree
            while True:
                if current.context.trial().over():
                    # We've reached a terminal state
                    break

                current = self.select(current)

                if current.visit_count == 0:
                    # We've expanded a new node, time for playout!
                    break

            context_end = current.context

            if not context_end.trial().over():
                # Run a playout if we don't already have a terminal
                # game state in node
                context_end = context_end.deepCopy()
                game.playout(context_end,
                             None,
                             -1.0,
                             None,
                             None,
                             0,
                             -1,
                             0.0,
                             None)

            # This computes utilities for all players at the of the playout,
            # which will all be values in [-1.0, 1.0]
            utils = utilities(context_end)

            # Backpropagate utilities through the tree
            while current is not None:
                current.visit_count += 1
                for p in range(1, num_players):
                    current.score_sums[p] += utils[p]
                current = current.parent

            # Increment iteration count
            num_iterations += 1

        # Return the move we wish to play
        return self.final_move_selection(root)

    def select(self, current):
        """
        UCB1 Selection (+ Expansion phase)

        :param current:
        :return:
        """
        if len(current.unexpanded_moves) > 0:
            # Randomly select an unexpanded move (already shuffled,
            # so just remove last element)
            move = current.unexpanded_moves.pop()

            # Create a copy of context
            context = current.context.deepCopy()

            # Apply the move
            context.game().apply(context, move)

            # Create new node and return it
            return Node(current, move, context)

        # Use UCB1 equation to select from all children,
        # with random tie-breaking
        best_child = None
        best_value = -math.inf
        two_parent_log = 2.0 * math.log(max(1, current.visit_count))
        num_best_found = 0

        num_children = len(current.children)
        mover = current.context.state().mover()

        for i in range(num_children):
            child = current.children[i]
            exploit = child.score_sums[mover] / child.visit_count
            explore = math.sqrt(two_parent_log / child.visit_count)

            ucb1_value = exploit + explore

            if ucb1_value > best_value:
                best_value = ucb1_value;
                best_child = child;
                num_best_found = 1;
            elif ucb1_value == best_value:
                rand = random.randint(0, num_best_found + 1)

                if rand == 0:
                    best_child = child

                num_best_found += 1

        return best_child

    def final_move_selection(self, root_node):
        """
        Selects final move to play in the real game (uses the Robust Child
        strategy)

        :param root_node:
        :return:
        """
        best_child = None
        best_visit_count = -math.inf
        num_best_found = 0

        num_children = len(root_node.children)

        for i in range(num_children):
            child = root_node.children[i]
            visit_count = child.visit_count

            if visit_count > best_visit_count:
                best_visit_count = visit_count
                best_child = child
                num_best_found = 1
            elif visit_count == best_visit_count:
                # This case implements random tie-breaking
                rand = random.randint(0, num_best_found + 1)

                if rand == 0:
                    best_child = child

                num_best_found += 1

        return best_child.move_from_parent


class Node:
    """
    Class for Nodes in the search tree built by UCT
    """

    def __init__(self, parent, move_from_parent, context):
        """
        Constructs a new node

        :param parent: Parent node
        :param move_from_parent: Move that leads from parent to this node
        :param context: Context / game state
        """
        self.visit_count = 0
        self.children = []
        self.parent = parent
        self.move_from_parent = move_from_parent
        self.context = context
        game = self.context.game()
        self.score_sums = np.zeros(game.players().count() + 1)
        legal_moves = game.moves(context).moves()
        num_legal_moves = legal_moves.size()
        self.unexpanded_moves = [legal_moves.get(i) for i in range(num_legal_moves)]
        random.shuffle(self.unexpanded_moves)

        if parent is not None:
            parent.children.append(self)

