---
layout: page
title: Lesson 14
---
Sound Decisions
=
_In which we learn about handling sound and music in Panda_

For the most part, dealing with sound and music is pretty simple in Panda3D. You load a sound- or music- file, you play it (perhaps after setting its volume, or telling it to loop), and that's about it!

There are more complex things that can be done (such as using 3D positional sound), but for our purposes, the above will suffice.

One thing that's worth noting is that Panda distinguishes between sound effects and music; it has separate manager-objects for them. This makes it easy to work with one of them as a whole, without affecting the other. For example, you can adjust the overall volume of your game's music, leaving its sound effects unchanged--useful for "sound" and "music" volume-sliders in an options menu.

To start with, let's load and play some music. In a bigger project we might have multiple music-files, to be played under various circumstances (such as in menus, or when the game ends), but for tutorial purposes we're just going to have a single piece of music.

In "Game.py":

{% highlight python %}
# In the "__init__" method:
music = loader.loadMusic("Music/Defending-the-Princess-Haunted.ogg")
music.setLoop(True)
# I find this piece to be pretty loud,
# so I've turned the volume down a lot.
# Adjust to your settings and preferences!
music.setVolume(0.075)
music.play()
{% endhighlight %}

You should now hear music as you play!

You may recall that, in order to loop an animation in an Actor, we just call "loop". Note, then, that this isn't the case for sounds: instead, we first call "setLoop", which doesn't start the sound, but does indicate that it should loop when played, and then call "play", which starts it.

Next, a simple sound-effect. Specifically, we're going to have a sound play whenever an enemy spawns:

{% highlight python %}
# In the "__init__" method:
self.enemySpawnSound = loader.loadSfx("Sounds/enemySpawn.ogg")
{% endhighlight %}

{% highlight python %}
# In the "spawnEnemy" method:
self.enemySpawnSound.play()
{% endhighlight %}

And that's it. You should now hear a sound-effect whenever an enemy spawns.

With the procedure covered, let's quickly add similar sound-effects for:
* The laser hitting something
* The laser hitting nothing
* Walking Enemies attacking
* Walking Enemies dying
* Traps moving
* And Traps hitting something

For most of this, we'll move over to "GameObject.py".

Some of our logic will want to check the status of a given sound, and the status-codes for this are stored in the "AudioSound" class, so we'll import that:

{% highlight python %}
# In your "import" statements:
from panda3d.core import AudioSound
{% endhighlight %}

Then we start adding, looping, and playing sounds. There's a fair bit of this, but it's all pretty simple, and is based on what we just did, so I'll just provide you with the code:

{% highlight python %}
# In the "__init__" method of GameObject:
self.deathSound = None
{% endhighlight %}

{% highlight python %}
# In the "alterHealth" method of GameObject:

# At the start:
previousHealth = self.health

# At the end:
if previousHealth > 0 and self.health <= 0 and self.deathSound is not None:
    self.deathSound.play()
{% endhighlight %}

{% highlight python %}
# In the "__init__" method of Player:
self.laserSoundNoHit = loader.loadSfx("Sounds/laserNoHit.ogg")
self.laserSoundNoHit.setLoop(True)
self.laserSoundHit = loader.loadSfx("Sounds/laserHit.ogg")
self.laserSoundHit.setLoop(True)

self.hurtSound = loader.loadSfx("Sounds/FemaleDmgNoise.ogg")
{% endhighlight %}

{% highlight python %}
# In the "update" method of Player:

# Directly after "if scoredHit:":
# We've hit something, so stop the "no-hit" sound
# and play the "hit something" sound
if self.laserSoundNoHit.status() == AudioSound.PLAYING:
    self.laserSoundNoHit.stop()
if self.laserSoundHit.status() != AudioSound.PLAYING:
    self.laserSoundHit.play()

# Directly after the associated "else":
# We're firing, but hitting nothing, so
# stop the "hit something" sound, and play
# the "no-hit" sound.
if self.laserSoundHit.status() == AudioSound.PLAYING:
    self.laserSoundHit.stop()
if self.laserSoundNoHit.status() != AudioSound.PLAYING:
    self.laserSoundNoHit.play()

# And similarly, after the next "else":
# We're not firing, so stop both the 
# "hit something" and "no-hit" sounds
if self.laserSoundNoHit.status() == AudioSound.PLAYING:
    self.laserSoundNoHit.stop()
if self.laserSoundHit.status() == AudioSound.PLAYING:
    self.laserSoundHit.stop()

# To clarify, both of those last two sections
# go next to calls to "self.beamHitModel.hide()",
# and calls to "render.clearLight"
# Put another way, the skeleton of the code looks
# something like this:
if keys["shoot"]:
    if self.rayQueue.getNumEntries() > 0:
        # ...

        if scoredHit:
            # Section 1, above

            # ...
        else:
            # Section 2, above
            
            # ...
else:
    # ...

    # Section 3, above.
{% endhighlight %}

{% highlight python %}
# In the "alterHealth" method of Player:
self.hurtSound.play()
{% endhighlight %}

{% highlight python %}
# In the "cleanup" method of Player:
self.laserSoundHit.stop()
self.laserSoundNoHit.stop()
{% endhighlight %}

{% highlight python %}
# In the "__init__" method of WalkingEnemy:

# This "deathSound" is the one that will
# be used by the logic that we just added
# to GameObject, above
self.deathSound = loader.loadSfx("Sounds/enemyDie.ogg")
self.attackSound = loader.loadSfx("Sounds/enemyAttack.ogg")
{% endhighlight %}

{% highlight python %}
# In the "runLogic" method of WalkingEnemy:

# Just after "self.actor.play("attack"):
self.attackSound.play()
{% endhighlight %}

{% highlight python %}
# In the "__init__" method of TrapEnemy:
self.impactSound = loader.loadSfx("Sounds/trapHitsSomething.ogg")
self.stopSound = loader.loadSfx("Sounds/trapStop.ogg")
self.movementSound = loader.loadSfx("Sounds/trapSlide.ogg")
self.movementSound.setLoop(True)
{% endhighlight %}

{% highlight python %}
# In the "runLogic" method of TrapEnemy:

# In the "if abs(detector) < 0.5:" section--
# that is, with "self.moveDirection = math.copysign(1, movement):
self.movementSound.play()
{% endhighlight %}

{% highlight python %}
# In the "TrapEnemy" class, we add
# a new "cleanup" method:
def cleanup(self):
    self.movementSound.stop()

    Enemy.cleanup(self)
{% endhighlight %}

We're not quite done yet--but almost. We aren't currently using the sounds that we loaded for the Trap Enemies hitting something, or stopping. That logic we'll put in our collision methods, back in "Game.py":

{% highlight python %}
# In the "stopTrap" method:

# In the "if collider.hasPythonTag("owner"):" section:
trap.movementSound.stop()
trap.stopSound.play()
{% endhighlight %}

{% highlight python %}
# In the "trapHitsSomething" method:

# In the "if collider.hasPythonTag("owner"):" section:
trap.impactSound.play()
{% endhighlight %}

Now we're done! When we play, we should now hear a variety of sounds, including the hum of our laser, the metallic "sikt!" of a Walking Enemy's blades, the boom of Trap Enemies hitting walls, and so on.

This is starting to look almost like a complete game. But there are two major things missing: a way to restart the game after the player loses, and a main menu to present at the game's start...

[This lesson's reference code][refCode]

[On to Lesson 15][next]

[next]: tut_lesson15.html
[soundimage]: http://www.soundimage.org
[refCode]: https://github.com/ArsThaumaturgis/Panda3DTutorial.io/tree/master/ReferenceCode/Lesson14
