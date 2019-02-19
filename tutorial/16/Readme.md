---
layout: page
title: Lesson 16
---
Packaged with a Neat Little Bow
=
_In which we learn how to build a distributable version of our game_

Panda3D comes with a tool that will--with some guidance from us--automatically build a distributable version of our game, downloading files from the internet as called for.

It requires two files:
* "requirements.txt", which tells it what dependency packages will be required by the final game. (And note that the "panda3d" package itself is such a dependency!)
* And "setup.py", which details how it should build the game.

The "requirements.txt" file is pretty straightforward. Indeed, for our purposes it will have only a single line:

{% highlight text %}
panda3d
```

The "setup.py" file is a bit more complicated.

To start with, the basics: from "setuptools" we import the "setup" method, and then call it, providing the details of our game as parameters. The shell of that code looks like this:

```python
from setuptools import setup

setup(
# Parameters go here...
)
```

There are two parameters that we'll give to it: the name of our game, and a dictionary of options.

In our case, we will technically have a only single option--but that "option" will itself include a bunch of options. The option in question is called "build_apps", and the options that we pass to it describe how to build our game. This includes things like which platforms we want to build for, which files or file-types we want to include or exclude from the final product, and so on.

Thus:

```python
from setuptools import setup

setup(
    name = "Panda-chan and the Endless Horde",
    options = {
        "build_apps" : {
            # Build-options go here...
        }
    }
)
```

Which leaves just the build-options to be filled out.

We're going to use four: "include_patterns", "gui_apps", "plugins", and "platforms".

* "include_patterns" indicates which files should be part of the final product. Some of these will be processed (like "egg" files being converted to "bam" files), while others will be included as-is.

    * These can be specific file-names, or file-patterns.

    * If we have files that we want to exclude, we can do so via "exclude_patterns".



* "gui_apps" indicates that we're building a game that opens a window, and also points it to the location of the "main" Python file for the game. If we wanted to run from a console, we could use "console_apps" instead. Note that if we wanted to, we could build multiple apps, both gui and console.

* "plugins" indicates which Panda3D plugins we want to use. This includes things like OpenGL, OpenAL, FMod, support for additional model-file types, and so on.

* "platforms" is simply what operating systems we want to build for (and in some cases, whether to build for 32- or 64- bit systems). I'll include Windows, Mac, and Linux options in the "platforms" section below--just remove those that you don't want.

Thus we end up with this:

```python
from setuptools import setup

setup(
    name = "Panda-chan and the Endless Horde",
    options = {
        "build_apps" : {
            # Files that we want to include. Specifically:
            #  * All of our image-files (.png)
            #  * All of our sound- and music-files (.ogg)
            #  * All of our text-files (.txt)
            #  * All of our 3D models (.egg)
            #    - These will be automatically converted
            #      to .bam files
            #  * And all of our font-files (in the "Font" folder)
            "include_patterns" : [
                "**/*.png",
                "**/*.ogg",
                "**/*.txt",
                "**/*.egg",
                "Fonts/*"
            ],
            # We want a gui-app, and our "main" Python file
            # is "Game.py"
            "gui_apps" : {
                "Panda-chan and the Endless Horde" : "Game.py"
            },
            # Plugins that we're using. Specifically,
            # we're using OpenGL, and OpenAL audio
            "plugins" : [
                "pandagl",
                "p3openal_audio"
            ],
            # Platforms that we're building for.
            # Remove those that you don't want.
            "platforms" : [
                "manylinux1_x86_64",
                "macosx_10_6_x86_64",
                "win_amd64"
            ]
        }
    }
)
```

Note that if we leave out the "platforms" section entirely, the build-system will automatically build for all of the default platforms. The defaults are the three that I included in our "setup.py" above, I believe.

There are a variety of other options available for use in the "setup.py" script. For a fuller list, and a more in-depth explanation, see the manual!

So, with all of that in place, only one thing remains to be done: to actually run the command that sets our game building!

To do that, we open a console, and run our "setup.py" script, passing to it the "bdist_apps" command. Doing so will have the build-system first build our distributable game, and then package it into a nicely-portable format. (At time of writing, all of the packaging formats are archives.)

The command looks as follows:

{% highlight text %}
python3 setup.py bdist_apps
```

(You could use Python 2.7 at time of writing, I think, but even now it's being slowly deprecated, and furthermore may incur problems.)

Wait for the process to finish, and then check your project directory: you should have two new directories: "build", and "dist".

The "build" directory holds the newly-built game, albeit unpackaged, as well as a cache of the files that the build-system downloaded to make it. (The latter allows it to skip re-downloading files that it already has, should you build more than once.)

The "dist" directory, however, holds the packaged version of the built game--ready to be distributed!

On to Lesson--wait, no, that's it! We have completed the tutorial, and if all has gone well, you should have your first complete Panda3D game! Congratulations and well done on doing so, and I hope that you enjoy the rest of your time with Panda3D, should you choose to continue with it.

