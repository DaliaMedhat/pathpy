"""Converter to networkx objects"""
#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : to_paths.py -- Converter classes to paths
# Author    : Ingo Scholtes <scholtes@uni-wuppertal.de>
# Time-stamp: <Wed 2021-04-14 17:31 ingo>
#
# Copyright (c) 2016-2021 Pathpy Developers
# =============================================================================
from __future__ import annotations
from typing import Any, List, Union, Optional
from functools import singledispatch
from collections import defaultdict, deque

from pathpy import logger

from pathpy.core.network import Network

from networkx import Graph, DiGraph, MultiDiGraph, MultiGraph


def to_networkx(network):
    if network.directed and network.multiedges:
        G = MultiDiGraph()
    elif not network.directed and network.multiedges:
        G = MultiGraph()
    elif network.directed and not network.multiedges:
        G = DiGraph()
    else:
        G = Graph()
    G.add_nodes_from([ (v, network.nodes[v].attributes.to_dict()) for v in network.nodes.uids])
    G.add_edges_from([ (network.edges[e].v.uid, network.edges[e].w.uid, network.edges[e].attributes.to_dict()) for e in network.edges.uids])
    return G

def from_networkx(graph):
    n = Network(directed=graph.is_directed(), multiedges=graph.is_multigraph())
    for v in graph.nodes:
        n.add_node(v, **graph.nodes[v])
    for e in graph.edges:
        n.add_edge(e[0], e[1], **graph.edges[e])
    return n