=======================
Using reclass with Salt
=======================

.. warning::

  The latest release of Salt, version 0.16.3, does *not yet* include the
  reclass adapter. You could use the ``cmd_yaml`` adapters, but at least for
  ``ext_pillar``, they are currently not useable, as they `do not export the
  minion ID to the command they run`_.

  Your best bet at this stage is to wait for Salt 0.17, or to run Salt from
  a Git clone, `branch "develop"`_. Sorry about that.

.. _do not export the minion ID to the command they run:
   https://github.com/saltstack/salt/issues/2276
.. _branch "develop": https://github.com/saltstack/salt/tree/develop

Quick start
-----------
The following steps should get you up and running quickly with |reclass| and
`Salt`_. You will need to decide for yourself where to put your |reclass|
inventory. This can be your first ``base`` ``file_root`` (the default), or it
could be ``/etc/reclass``, or ``/srv/salt``. The following shall assume the
latter.

Or you can also just look into ``./examples/salt`` of your |reclass|
checkout (``/usr/share/doc/examples/salt`` on Debian-systems), where the
following steps have already been prepared.

/…/reclass refers to the location of your |reclass| checkout.

.. todo::

  With |reclass| now in Debian, as well as installable from source, the
  following should be checked for path consistency…

#. Complete the installation steps described in the :doc:`installation section
   <install>`.

   Alternatively, you can also tell Salt via the master config file where to
   look for |reclass|, but then you won't be able to interact with
   |reclass| through the command line.

#. Copy the two directories ``nodes`` and ``classes`` from the example
   subdirectory in the |reclass| checkout to e.g. ``/srv/salt``.

   It's handy to symlink |reclass|' Salt adapter itself to that directory::

      $ ln -s /usr/share/reclass/reclass-salt /srv/salt/states/reclass

   As you can now just inspect the data right there from the command line::

      $ ./reclass --top

   If you don't want to do this, you can also let |reclass| know where to
   look for the inventory with the following contents in
   ``$HOME/reclass-config.yml``::

      storage_type: yaml_fs
      base_inventory_uri: /srv/reclass

   Or you can reuse the first entry of ``file_roots`` under ``base`` in the Salt
   master config.

   Note that ``yaml_fs`` is currently the only supported ``storage_type``, and
   it's the default if you don't set it.

#. Check out your inventory by invoking

   ::

      $ reclass-salt --top

   which should return all the information about all defined nodes, which is
   only ``localhost`` in the example. This is essentially the same information
   that you would keep in your ``top.sls`` file.

   If you symlinked the script to your inventory base directory, use

   ::

      $ ./reclass --top

#. See the pillar information for ``localhost``::

      $ reclass-salt --pillar localhost

#. Now add |reclass| to ``/etc/salt/master``, like so::

      reclass: &reclass
          inventory_base_uri: /srv/salt
          reclass_source_path: ~/code/reclass

      master_tops:
          […]
          reclass: *reclass

      ext_pillar:
          - reclass: *reclass

   If you did not install |reclass| (but you are running it from source),
   you can either specify the source path like above, or you can add it to
   ``PYTHONPATH`` before invoking the Salt master, to ensure that Python can
   find it::

      PYTHONPATH=/…/reclass /etc/init.d/salt-master restart

#. Provided that you have set up ``localhost`` as a Salt minion, the following
   commands should now return the same data as above, but processed through
   salt::

      $ salt localhost pillar.items     # shows just the parameters
      $ salt localhost state.show_top   # shows only the states (applications)

   Alternatively, if you don't have the Salt minion running yet::

      $ salt-call pillar.items     # shows just the parameters
      $ salt-call state.show_top   # shows only the states (applications)

#. You can also invoke |reclass| directly, which gives a slightly different
   view onto the same data, i.e. before it has been adapted for Salt::

      $ reclass --inventory
      $ reclass --nodeinfo localhost

Integration with Salt
---------------------
|reclass| hooks into Salt at two different points: ``master_tops`` and
``ext_pillar``. For both, Salt provides plugins. These plugins need to know
where to find |reclass|, so if |reclass| is not properly installed (but
you are running it from source), make sure to export ``PYTHONPATH``
accordingly before you start your Salt master, or specify the path in the
master configuration file, as show above.

Salt has no concept of "nodes", "applications", "parameters", and "classes".
Therefore it is necessary to explain how those correspond to Salt. Crudely,
the following mapping exists:

================= ================
|reclass| concept Salt terminology
================= ================
nodes             hosts
classes           (none) [#nodegroups]_
applications      states
parameters        pillar
================= ================

.. [#nodegroups] See `Salt issue #5787`_ for steps into the direction of letting
   |reclass| provide nodegroup information.

.. _Salt issue #5787: https://github.com/saltstack/salt/issues/5787

Whatever applications you define for a node will become states applicable to
a host. If those applications are added via ancestor classes, then that's
fine, but currently, Salt does not do anything with the classes ancestry.

Similarly, all parameters that are collected and merged eventually end up in
the pillar data of a specific node.

However, the pillar data of a node include all the information about classes
and applications, so you could theoretically use them to target your Salt
calls at groups of nodes defined in the |reclass| inventory, e.g.

::

  salt -I __reclass__:classes:salt_minion test.ping

Unfortunately, this does not work yet, please stay tuned, and let me know
if you figure out a way. `Salt issue #5787`_ is also of relevance.

.. include:: substs.inc
.. include:: extrefs.inc
