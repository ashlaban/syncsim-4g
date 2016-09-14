# syncsim-4g
SyncSim-4G (for grading), simplifies grading of lab assignments in the LTU course D0013E.

Setup
=====
When you have decided where to put the tool, run

    ./syncsim-4g.py init

To create the initial file structure. Two folders will be created for you, `in` and `out`. The folder `in` is where you put archives to be processed by the tool. These will then be unpacked to `out` before being run through SyncSim.

Typical Usage
=============

    ./syncsim-4g.py check -l 1a -g 21 --use-preset

Usage
=====

Accepted archive file names
===========================

Should be on the form...

with file ending ...
note that to handle ext x you need program y