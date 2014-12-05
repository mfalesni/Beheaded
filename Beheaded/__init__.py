#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
#   Author(s): Milan Falesnik   <milan@falesnik.net>
#                               <mfalesni@redhat.com>
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from Runner import Run
import os
import subprocess
import signal
import shlex
import time


class UnableToFindFreeDisplayException(Exception):
    pass


class XvfbNotInstalledException(Exception):
    pass


class FFMpegNotInstalledException(Exception):
    pass


class ExtensionUnsupportedException(Exception):
    pass


class Headless(object):

    @property
    def nonfree_displays(self):
        displays = Run.command("ls /tmp/.X11-unix")
        assert displays, "Folder /tmp/.X11-unix not found!"
        return [int(x[1:]) for x in displays.stdout.strip().split("\n") if x.startswith("X")]

    def __init__(self, display="auto", width=1280, height=1024, bit_depth=24):
        if display != "auto":
            disp = int(display)
            assert disp not in self.nonfree_displays, "Selected display number (%d) already exists!" % disp
            self.display = disp
        else:
            start = 100
            while start in self.nonfree_displays and start < 999:
                start += 1
            if start in self.nonfree_displays:
                raise UnableToFindFreeDisplayException("Unable to find a free local display number!")
            self.display = start
        self.width = int(width)
        self.height = int(height)
        self.depth = int(bit_depth)
        assert self.depth in [16, 24], "Only 24-bit and 32-bit depths supported"

    def start(self):
        self.old_display = os.environ.get("DISPLAY", None)
        os.environ["DISPLAY"] = ":%d" % self.display
        try:
            self.Xvfb = self._start_Xvfb()
        except OSError:
            raise XvfbNotInstalledException("Xvfb is probably not installed!")
        return self

    def __enter__(self):
        return self.start()

    def stop(self):
        self.Xvfb.terminate()
        if self.old_display:
            os.environ["DISPLAY"] = self.old_display
        else:
            del os.environ["DISPLAY"]

    def __exit__(self, type, value, traceback):
        self.stop()

    def _start_Xvfb(self):
        cmd = "Xvfb :%d -screen 0 %dx%dx%d" % (self.display, self.width, self.height, self.depth)
        # TODO check if Xvfb is running
        return subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


class Record(object):

    def __init__(self, filename, xvfb=None, framerate=25):
        self.filename = filename
        ext = filename.rsplit(".", 1)[-1].strip()
        ext_codecs = {
            "mov": "qtrle",
            "mp4": "mpeg4",
            "mpg": "mpeg1video",
            "webm": "libvpx"
        }
        try:
            self.codec = ext_codecs[ext]
        except KeyError:
            raise self.ExtensionUnsupportedException("Extension .%s unsupported! (supported are %s)" % (ext, ", ".join([".%s" % x for x in ext_codecs.keys()])))
        self.framerate = framerate
        if self.codec == "mpeg1video":
            assert self.framerate not in [15]
        if xvfb is None:
            self.xvfb = Headless()
            self.terminate_x = True
        else:
            self.xvfb = xvfb
            self.terminate_x = False

    def start(self):
        try:
            if self.terminate_x:
                self.xvfb.start()
            self.recorder = self._start_ffmpeg(self.xvfb)
            # TODO: Check if ffmpeg is running
        except OSError:
            raise FFMpegNotInstalledException("ffmpeg is probably not installed!")

    def __enter__(self):
        return self.start()

    def stop(self):
        if self.codec in ["libvpx"]:    # To prevent cutting the recording too soon
            time.sleep(3)
        self.recorder.terminate()
        (stdout, stderr) = self.recorder.communicate(None)
        returncode = self.recorder.wait()
        if self.terminate_x:
            self.xvfb.stop()

    def __exit__(self, type, value, traceback):
        self.stop()

    def _start_ffmpeg(self, xvfb):
        cmd = "ffmpeg -y -r %d -g 600 -s %dx%d -f x11grab -i :%d -vcodec %s %s" % (
            self.framerate,
            xvfb.width,
            xvfb.height,
            xvfb.display,
            self.codec,
            self.filename
        )
        return subprocess.Popen(shlex.split(cmd),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                )
