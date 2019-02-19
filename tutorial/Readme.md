---
layout: page
title: Start Here
---
Before we begin...
=

What this tutorial is, and what it is not
-

What it is:

* __An introduction to game development using Panda3D.__ It will teach the basic principles of the engine, and techniques for using it--enough to make a simple game.

	Indeed, over the course of these lessons we'll build up exactly that: a basic arena-based, top-down score-shooter. If the genre of the game isn't to your tastes, that's fair enough: it's merely an example--a lens through which to teach Panda3D. The principles taught with it should apply to a wide variety of game-types (even non-action games).

What it is not:

* __A Python tutorial.__ This tutorial assumes a basic knowledge of Python (and ideally of object-oriented programming). You don't have to be an expert, but if you're entirely new to the language then I recommend picking up a Python tutorial before taking on this one!

* __A game design tutorial.__ The game built up in these lessons is intended to teach the basics of Panda3D, rather than to be a great game. (Although I do think that it is somewhat fun.) Furthermore, the focus is on teaching the use of Panda3D--while there will be some mention of game design, I intend to somewhat skim over it.

* __An advanced Panda3D Tutorial.__ Panda3D is capable of much more than is shown here: advanced physics, custom shaders, complex logic, and more besides!

What's covered:
-

* The fundamentals of Panda3D
* Lights and automatic shading
* Input-handling
* Tasks and "update" methods
* Simple collision-detection
* Music and sound effects
* GUI construction
* Building a distributable version
* And more besides!

Reference code:
-

Each lesson provides example code--but these are often fragments (for brevity's sake). If you want to see the code in context, compare it with your own, you can find the full code as of the end of each lesson in the "ReferenceCode" directory. In there you should find one directory for each lesson, containing the full code.

The reference code directory should be available here:

 [https://github.com/ArsThaumaturgis/Panda3DTutorial.io/tree/master/ReferenceCode][refCode]

The assets for the tutorial
-

This tutorial makes use of a variety of assets, from a variety of sources. So that you can build the tutorial game yourself, let me link to them here.

Note that each set of assets has its own license. If you intend to use any of the following in your own works, and especially if you plan on distributing them in any way, I recommend that you check those licenses! (But I am not a lawyer, and this is not legal advice.)

The models and textures:
* Environment, simple enemy, laser, and hit-flashes:

    [https://github.com/ArsThaumaturgis/PandaSampleModels][samplemodels]

* Panda-chan, by wezu:

     [https://github.com/wezu/p3d_samples/tree/master/models][pandaChan]

UI elements:
* [https://github.com/ArsThaumaturgis/PandaSampleModels][samplemodels]
     * (The same as the first model-repository above; they're in the "UI" directory)

Sound effects:
* [https://github.com/ArsThaumaturgis/Panda3DTutorial.io/tree/master/Sounds][soundEffects]

Music:
* [https://soundimage.org/epic-battle/][music]
    * I'm using "Defending the Princess Haunted".
    * The music offered there is in MP3 format, but can be converted to OGG format via free tools. I used Sound Converter: http://soundconverter.org/

Font:
* [https://www.dafont.com/wbx-komik.font][font]

When these assets are mentioned in the tutorial, take note of the directories that I reference. You may want to either adopt the same folder-structure, or adapt the folder-references in the code to whatever structure you use!

And now, let us begin...
-

[On to lesson 1][lesson1]

[lesson1]: tut_lesson01.html
[samplemodels]: https://github.com/ArsThaumaturgis/PandaSampleModels
[pandaChan]: https://github.com/wezu/p3d_samples/tree/master/models
[soundEffects]: https://github.com/ArsThaumaturgis/Panda3DTutorial.io/tree/master/Sounds
[music]: https://soundimage.org/epic-battle/
[font]: https://www.dafont.com/wbx-komik.font
[refCode]: https://github.com/ArsThaumaturgis/Panda3DTutorial.io/tree/master/ReferenceCode
