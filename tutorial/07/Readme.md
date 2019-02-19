---
layout: page
title: Lesson 7
---
Our Game's Objects
=
_In which we make classes for the player and an enemy_

Now, we have the start of some gameplay, and in particular of a player-character, taking form. But everything is haphazardly placed in our main "Game" class. If we keep building our player-character as we have been, and especially if we also build our enemies in a similar fashion, our code could get very messy, I fear.

So, it's time for some object-oriented development.

As I said at the start of these lessons, this is not a game-design tutorial. Furthermore, little of what I intend to cover in this lesson is terribly Panda-specific. As a result, I intend to somewhat skim over this part. However, I do intend to at least in brief describe what I'm doing here!

To make our code neater and easier to navigate, we'll put these new classes into a file of their own, named "GameObject.py"

For the purposes of this tutorial, we will be creating three types of entity:
* The player
* An enemy that moves towards the player and attacks when in range
* And a "trap" that moves in straight lines across the level, damaging player and other enemy-type alike.

These three all have a number of traits in common: they all have 3D models, they all have colliders, they all move, and so on.

So, we will create a base-class that contains these common elements, called "GameObject". Our player and enemies will be sub-classes of this base-class.

Furthermore, our two enemy-types both have their own elements in common, in particular that they will run some sort of logic that governs their actions. So they will derive from a common sub-class of "GameObject", named "Enemy".

In short, the "GameObject" class will have two sub-classes: "Player" and "Enemy". The "Enemy" class itself will have two sub-classes: "WalkingEnemy" and "TrapEnemy". We'll create the "TrapEnemy" class only later--for now we'll just make the "WalkingEnemy" class.

The shells of our new classes look like this:

{% highlight python %}
class GameObject():
    pass

class Player(GameObject):
    pass

class Enemy(GameObject):
    pass

class WalkingEnemy(Enemy):
    pass
{% endhighlight %}

In a number of places below, we'll want to access "cTrav" and our "pusher" handler. This is done via a Panda-provided globally-accessible variable called "base", which provides a reference to the game's "ShowBase" object--and since that's our "Game" object, that reference is also a reference to our game.

"GameObject" will store a given character's actor and collider, as well as handling its velocity and movement, and the basics of its health. It will also provide a "cleanup" method, for when we want to remove a character.

{% highlight python %}
from panda3d.core import Vec3, Vec2
from direct.actor.Actor import Actor
from panda3d.core import CollisionSphere, CollisionNode

FRICTION = 150.0

class GameObject():
    def __init__(self, pos, modelName, modelAnims, maxHealth, maxSpeed, colliderName):
        self.actor = Actor(modelName, modelAnims)
        self.actor.reparentTo(render)
        self.actor.setPos(pos)

        self.maxHealth = maxHealth
        self.health = maxHealth

        self.maxSpeed = maxSpeed

        self.velocity = Vec3(0, 0, 0)
        self.acceleration = 300.0

        self.walking = False

        # Note the "colliderName"--this will be used for
        # collision-events, later...
        colliderNode = CollisionNode(colliderName)
        colliderNode.addSolid(CollisionSphere(0, 0, 0, 0.3))
        self.collider = self.actor.attachNewNode(colliderNode)
        # See below for an explanation of this!
        self.collider.setPythonTag("owner", self)

    def update(self, dt):
        # If we're going faster than our maximum speed,
        # set the velocity-vector's length to that maximum
        speed = self.velocity.length()
        if speed > self.maxSpeed:
            self.velocity.normalize()
            self.velocity *= self.maxSpeed
            speed = self.maxSpeed

        # If we're walking, don't worry about friction.
        # Otherwise, use friction to slow us down.
        if not self.walking:
            frictionVal = FRICTION*dt
            if frictionVal > speed:
                self.velocity.set(0, 0, 0)
            else:
                frictionVec = -self.velocity
                frictionVec.normalize()
                frictionVec *= frictionVal

                self.velocity += frictionVec

        # Move the character, using our velocity and
        # the time since the last update.
        self.actor.setPos(self.actor.getPos() + self.velocity*dt)

    def alterHealth(self, dHealth):
        self.health += dHealth

        if self.health > self.maxHealth:
            self.health = self.maxHealth

    def cleanup(self):
        # Remove various nodes, and clear the Python-tag--see below!

        if self.collider is not None and not self.collider.isEmpty():
            self.collider.clearPythonTag("owner")
            base.cTrav.removeCollider(self.collider)
            base.pusher.removeCollider(self.collider)

        if self.actor is not None:
            self.actor.cleanup()
            self.actor.removeNode()
            self.actor = None

        self.collider = None
{% endhighlight %}

Something that is worth noting above is the pair of "Python-tag"-related methods--these two:
{% highlight python %}
self.collider.setPythonTag("owner", self)
{% endhighlight %}
{% highlight python %}
self.collider.clearPythonTag("owner")
{% endhighlight %}

What I'm doing here is storing a reference to the GameObject in the collider. When a collision happens, we have access to the colliders involved--but we likely want access to the related GameObject, too. This provides that access.

However, there's a caveat here! The GameObject is storing a reference to the collider, and by adding a Python-tag pointing to the GameObject, the collider now has a reference to the GameObject. That means that we have a circular reference, which can result in the object not being properly garbage-collected.

Thus, when we clean up the GameObject, we clear the Python-tag, and so break the circle, allowing the objects to be garbage-collected.

The "Player" class holds pretty much the same player-logic as we've thus far had in our "Game" class, save that the movement-controls now alter its velocity, rather than just moving it:

{% highlight python %}
class Player(GameObject):
    def __init__(self):
        GameObject.__init__(self,
                            Vec3(0, 0, 0),
                            "Models/PandaChan/act_p3d_chan",
                              {
                                  "stand" : "Models/PandaChan/a_p3d_chan_idle",
                                  "walk" : "Models/PandaChan/a_p3d_chan_run"
                              },
                            5,
                            10,
                            "player")

        # Panda-chan faces "backwards", so we just turn
        # the first sub-node of our Actor-NodePath
        # to have it face as we want.
        self.actor.getChild(0).setH(180)

        # Since our "Game" object is the "ShowBase" object,
        # we can access it via the global "base" variable.
        base.pusher.addCollider(self.collider, self.actor)
        base.cTrav.addCollider(self.collider, base.pusher)

        self.actor.loop("stand")

    def update(self, keys, dt):
        GameObject.update(self, dt)

        self.walking = False

        # If we're  pushing a movement key, add a relevant amount
        # to our velocity.
        if keys["up"]:
            self.walking = True
            self.velocity.addY(self.acceleration*dt)
        if keys["down"]:
            self.walking = True
            self.velocity.addY(-self.acceleration*dt)
        if keys["left"]:
            self.walking = True
            self.velocity.addX(-self.acceleration*dt)
        if keys["right"]:
            self.walking = True
            self.velocity.addX(self.acceleration*dt)

        # Run the appropriate animation for our current state.
        # See the text below this for an explanation
        if self.walking:
            standControl = self.actor.getAnimControl("stand")
            if standControl.isPlaying():
                standControl.stop()

            walkControl = self.actor.getAnimControl("walk")
            if not walkControl.isPlaying():
                self.actor.loop("walk")
        else:
            standControl = self.actor.getAnimControl("stand")
            if not standControl.isPlaying():
                self.actor.stop("walk")
                self.actor.loop("stand")
{% endhighlight %}

Regarding that animation code, the basic idea is that if a character is "walking", then it should loop its "walk" animation, if it wasn't already. If it's not walking, then, as long as it's not playing another animation, it should loop its "stand" animation, if it wasn't already.

There are probably better, or at least more-elegant, ways of doing this (a state-machine--which Panda has a class for--comes to mind). But for our purposes, this will do.

You may also notice further animation code, to similar effect, in the "Enemy" class below.

The "Enemy" class provides a stub "runLogic" method, which is intended to be overridden by its sub-classes, and calls this method in its "update" method. It also provides a "score" value, for when it's killed:

{% highlight python %}
class Enemy(GameObject):
    def __init__(self, pos, modelName, modelAnims, maxHealth, maxSpeed, colliderName):
        GameObject.__init__(self, pos, modelName, modelAnims, maxHealth, maxSpeed, colliderName)

        # This is the number of points to award
        # if the enemy is killed.
        self.scoreValue = 1

    def update(self, player, dt):
        # In short, update as a GameObject, then
        # run whatever enemy-specific logic is to be done.
        # The use of a separate "runLogic" method
        # allows us to customise that specific logic
        # to the enemy, without re-writing the rest.

        GameObject.update(self, dt)

        self.runLogic(player, dt)

        # As with the player, play the appropriate animation.
        if self.walking:
            walkingControl = self.actor.getAnimControl("walk")
            if not walkingControl.isPlaying():
                self.actor.loop("walk")
        else:
            spawnControl = self.actor.getAnimControl("spawn")
            if spawnControl is None or not spawnControl.isPlaying():
                attackControl = self.actor.getAnimControl("attack")
                if attackControl is None or not attackControl.isPlaying():
                    standControl = self.actor.getAnimControl("stand")
                    if not standControl.isPlaying():
                        self.actor.loop("stand")


    def runLogic(self, player, dt):
        pass
{% endhighlight %}

And finally, the "WalkingEnemy" class overrides the "runLogic" method of the "Enemy" class, providing code that has it walk towards the player until it reaches an "attack distance". It also turns to face the player, using the vector between their positions, and the "signedAngleDeg" (i.e. "get the signed angle, in degrees") method provided by Panda's vector-classes.

{% highlight python %}
class WalkingEnemy(Enemy):
    def __init__(self, pos):
        Enemy.__init__(self, pos,
                       "Models/Misc/simpleEnemy",
                       {
                        "stand" : "Models/Misc/simpleEnemy-stand",
                        "walk" : "Models/Misc/simpleEnemy-walk",
                        "attack" : "Models/Misc/simpleEnemy-attack",
                        "die" : "Models/Misc/simpleEnemy-die",
                        "spawn" : "Models/Misc/simpleEnemy-spawn"
                        },
                       3.0,
                       7.0,
                       "walkingEnemy")

        self.attackDistance = 0.75

        self.acceleration = 100.0

        # A reference vector, used to determine
        # which way to face the Actor.
        # Since the character faces along
        # the y-direction, we use the y-axis.
        self.yVector = Vec2(0, 1)

    def runLogic(self, player, dt):
        # In short: find the vector between
        # this enemy and the player.
        # If the enemy is far from the player,
        # use that vector to move towards the player.
        # Otherwise, just stop for now.
        # Finally, face the player.

        vectorToPlayer = player.actor.getPos() - self.actor.getPos()

        vectorToPlayer2D = vectorToPlayer.getXy()
        distanceToPlayer = vectorToPlayer2D.length()

        vectorToPlayer2D.normalize()

        heading = self.yVector.signedAngleDeg(vectorToPlayer2D)

        if distanceToPlayer > self.attackDistance*0.9:
            self.walking = True
            vectorToPlayer.setZ(0)
            vectorToPlayer.normalize()
            self.velocity += vectorToPlayer*self.acceleration*dt
        else:
            self.walking = False
            self.velocity.set(0, 0, 0)

        self.actor.setH(heading)
{% endhighlight %}

With all that done, we want to use these classes in our game.

First we remove the player-code that we had in the "Game" class: "tempActor", its collider, the logic that adds that collider to "pusher" and "cTrav", and the code that checks the key-map to move "tempActor". Note that "GameObject", above, now handles that actor and collider logic, and "Player" handles the key-map checking.

Then we import our "GameObject" module, and--for now--create a temporary instance of each of the "Player" and "WalkingEnemy" classes. This isn't how we'll handle them in the end, but it will serve for testing as we build up the classes.

So, in "Game.py":

{% highlight python %}
# In your import statements:
from GameObject import *
{% endhighlight %}
{% highlight python %}
# In the "__init__" method:
self.player = Player()

self.tempEnemy = WalkingEnemy(Vec3(5, 0, 0))
{% endhighlight %}
{% highlight python %}
# In the "update" method:
self.player.update(self.keyMap, dt)

self.tempEnemy.update(self.player, dt)
{% endhighlight %}

If you run the game now, you should be able to move the player, much as before--but you'll also be chased around (harmlessly--for now) by an enemy!

![The player is chased by an enemy](images/tutHarmlessChase.gif "A merry chase!")

Next, let's see how we handle collision events, via our trap enemy...

[On to Lesson 8][next]

[next]: tut_lesson08.html
