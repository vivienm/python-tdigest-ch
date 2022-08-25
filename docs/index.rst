tdigest-ch
==========

A Python library for estimating quantiles in a stream,
using `ClickHouse t-digest <ClickHouseRefTDigest_>`_ data structure.

The `t-digest <Dunning19_>`_ data structure is designed around computing
accurate quantile estimates from streaming data. Two t-digests can be merged,
making the data structure well suited for map-reduce settings.

.. _Dunning19: https://github.com/tdunning/t-digest/blob/main/docs/t-digest-paper/histo.pdf
.. _ClickHouseRefTDigest: https://clickhouse.com/docs/en/sql-reference/aggregate-functions/reference/quantiletdigest/


API reference
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
