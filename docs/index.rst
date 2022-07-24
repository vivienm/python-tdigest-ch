tdigest-ch
==========

A Python port of ClickHouse t-digest data structures, implemented in Rust.

The `t-digest`_ data structure is designed around computing
accurate quantile estimates from streaming data. Two t-digests can be merged,
making the data structure ideal for map-reduce settings.

.. _t-digest: https://github.com/tdunning/t-digest/blob/main/docs/t-digest-paper/histo.pdf


API Reference
-------------

.. currentmodule:: tdigest_ch

.. autoclass:: tdigest_ch.TDigest
   :members:
   :undoc-members:
   :special-members: __ior__, __len__, __or__


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
