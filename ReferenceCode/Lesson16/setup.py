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
            # we're using OpenGL and OpenAL audio
            "plugins" : [
                "pandagl",
                "p3openal_audio"
            ],
            # Platforms that we're building for.
            # Remove those that you don't want.
            "platforms" : [
                "manylinux1_x86_64",
                #"macosx_10_6_x86_64",
                #"win_amd64"
            ]
        }
    }
)
