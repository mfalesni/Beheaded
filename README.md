Beheaded
========

Author: Milan Falešník (milan@falesnik.net, mfalesni@redhat.com)
Generic X window and recording for headless setups.

Installation:
=============
* <code>pip install Beheaded</code>

Requires <code>Runner</code> python package to be installed (pip handles that).

Usage:
======
The basic step is to import required objects into namespace

    from Beheaded import Headless, Record

Obviously, if you don't need recording, the do not import <code>Record</code>.

Headless:
=========
Headless's constructor signature:

    Headless(display="auto", width=1280, height=1024, bit_depth=24)

<code>Headless</code> can be used both in normal and context-managed mode.

    X = Headless()
    X.start()
    ... do stuff ...
    X.stop()

and

    with Headless() as X:
        ... do stuff ...

are functionally equivalent.

Record:
=======
Record's constructor signature:

    Record(filename, xvfb, framerate=25)

* <code>filename</code> specifies the target video file name
* <code>xvfb</code> specifies the <code>Headless</code> object, or anything that provides <code>width</code>, <code>height</code> and <code>display</code> attributes.

<code>Record</code> can be used both in normal and context-managed mode.

    rec = Record("filename.webm", X)
    rec.start()
    ... do stuff ...
    rec.stop()

and

    with Record():
        ... do stuff ...

are functionally equivalent.

Combining:
==========
Works obviously as expected:

    with Headless() as X:
        with Record("filename.webm", X):
            ... do stuff ...

To-Do:
======
* add checks whether Xvfb or ffmpeg really run