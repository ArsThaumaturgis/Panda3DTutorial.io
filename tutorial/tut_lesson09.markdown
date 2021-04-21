---
layout: page
title: Lesson 9
---
Mask-erade
=
_In which we make a laser, and learn how to specify what should collide with what._

Our player-character can be hit (ineffectually, but still), but cannot hit back. Let's do something about that. Specifically, let's give our character a laser!

In terms of collisions, our laser will be represented by a "CollisionRay": a line that starts at a given point, and extends indefinitely in a given direction.

We want our laser to keep doing damage as long as it's held on an enemy, so we want new collision-information each update. Furthermore, we only really want the first hit that it makes on a given update, not any further down its length.

We could perhaps use collision-events for this, but an easier way is have our ray be handled by a "CollisionHandlerQueue", tell the queue to sort itself so that the first collision is the first entry, and then just use that.

For the moment, since we don't have a visual representation of the laser, we'll just print out what it hits.

In "GameObject.py":
{% highlight python %}
# In your "import" statements:
from panda3d.core import CollisionRay, CollisionHandlerQueue
{% endhighlight %}
{% highlight python %}
# In the "__init__" method of the "Player" class:
self.ray = CollisionRay(0, 0, 0, 0, 1, 0)

rayNode = CollisionNode("playerRay")
rayNode.addSolid(self.ray)

self.rayNodePath = render.attachNewNode(rayNode)
self.rayQueue = CollisionHandlerQueue()

# We want this ray to collide with things, so
# tell our traverser about it. However, note that,
# unlike with "CollisionHandlerPusher", we don't
# have to tell our "CollisionHandlerQueue" about it.
base.cTrav.addCollider(self.rayNodePath, self.rayQueue)

self.damagePerSecond = -5.0
{% endhighlight %}
{% highlight python %}
# In the "update" method of the "Player" class:

# If we're pressing the "shoot" button, check
# whether the ray has hit anything, and if so,
# examine the collision-entry for the first hit.
# If the thing hit has an "owner" Python-tag, then
# it's a GameObject, and should try to take damage--
# with the exception if "TrapEnemies",
# which are invulnerable.
if keys["shoot"]:
    if self.rayQueue.getNumEntries() > 0:
        self.rayQueue.sortEntries()
        rayHit = self.rayQueue.getEntry(0)
        hitPos = rayHit.getSurfacePoint(render)

        hitNodePath = rayHit.getIntoNodePath()
        print (hitNodePath)
        if hitNodePath.hasPythonTag("owner"):
            hitObject = hitNodePath.getPythonTag("owner")
            if not isinstance(hitObject, TrapEnemy):
                hitObject.alterHealth(self.damagePerSecond*dt)
{% endhighlight %}
{% highlight python %}
# And finally, a bit of extra cleaning up.
# In the Player class, we override
# GameObject's "cleanup" method:
def cleanup(self):
    base.cTrav.removeCollider(self.rayNodePath)

    GameObject.cleanup(self)
{% endhighlight %}

Okay, that's great--but there's a problem: Right now, our laser can hit anything. Including the player-character, on occasion. (It's also not pointing in the correct direction--but we'll get to that presently.)

So what we want next is a way of telling the collision system which things a given collision object can collide with. In the case of Panda's built-in collision-system, this is handled via "BitMask" objects.

BitMasks can be thought of as a set of flags (the "bits"), each either on or off, one or zero. When used by the physics system, only collisions in which the colliders share at least one "on" bit are registered. All others are ignored.

Furthermore, remember that Panda3D distinguishes which node in a collision is the source of the collision, the "from" object, and which is the node that was collided with, the "into" object. So each collider in Panda3D's collision system has two BitMasks: a "from" mask and an "into" mask.

Collisions are thus only registered between two objects when the "from" object's "from" mask shares at least one "on" bit with the "into" object's "into" mask.

By default, colliders have all of their bits "on"--hence our problem, as our ray collides with everything.

Once we've created a BitMask, the simplest way to set which bits are "on" is to call "setBit", providing the index of the bit to be set. If you're comfortable with converting boolean values to base-ten, you can also just initialise the BitMask with a single number.

By default, a newly-created BitMask object has all its bits set to "off".

In our case, we want to make sure that the player has a mask, and that the player's ray has different mask, so that they don't collide. Conversely, we want our enemy to have a mask that matches the ray's, so that they _do_ collide:

{% highlight python %}
# In your "import" statements:
from panda3d.core import BitMask32
{% endhighlight %}
{% highlight python %}
# In the "__init__" method of the "Player" class:
mask = BitMask32()
mask.setBit(1)

# This is the important one for preventing ray-collisions.
# The other is more a gameplay decision.
self.collider.node().setIntoCollideMask(mask)

mask = BitMask32()
mask.setBit(1)

self.collider.node().setFromCollideMask(mask)

# After we've made our ray-node:
mask = BitMask32()

# Note that we set a different bit here!
# This means that the ray's mask and
# the collider's mask don't match, and
# so the ray won't collide with the
# collider.
mask.setBit(2)
rayNode.setFromCollideMask(mask)

mask = BitMask32()
rayNode.setIntoCollideMask(mask)
{% endhighlight %}
{% highlight python %}
# Then, in the "__init__" method of the "WalkingEnemy" class:

# Note that this is the same bit as we used for the ray!
mask = BitMask32()
mask.setBit(2)

self.collider.node().setIntoCollideMask(mask)
{% endhighlight %}
{% highlight python %}
# And in the "__init__" method of the "TrapEnemy" class:

# Trap-enemies should hit both the player and "walking" enemies,
# so we set _both_ bits here!
mask = BitMask32()
mask.setBit(2)
mask.setBit(1)

self.collider.node().setIntoCollideMask(mask)

mask = BitMask32()
mask.setBit(2)
mask.setBit(1)

self.collider.node().setFromCollideMask(mask)
{% endhighlight %}

Now our laser should skip the player, but hit both traps and walking-enemies!

We'll also want some means of representing our laser, and of showing that it has hit something. For that, we'll use a new model, from the file named "bambooLaser". It's a simple quad, narrow, and one unit in length. This we'll attach to our actor, and just scale it to match the laser's length.

{% highlight python %}
# In the "__init__" method of the "Player" class:

# A nice laser-beam model to show our laser
self.beamModel = loader.loadModel("Models/Misc/bambooLaser")
self.beamModel.reparentTo(self.actor)
self.beamModel.setZ(1.5)
# This prevents lights from affecting this particular node
self.beamModel.setLightOff()
# We don't start out firing the laser, so 
# we have it initially hidden.
self.beamModel.hide()
{% endhighlight %}
{% highlight python %}
# In the "update" method of the "Player" class:

# We've seen this bit before--the new stuff is inside
if keys["shoot"]:
    if self.rayQueue.getNumEntries() > 0:
        self.rayQueue.sortEntries()
        rayHit = self.rayQueue.getEntry(0)
        hitPos = rayHit.getSurfacePoint(render)

        hitNodePath = rayHit.getIntoNodePath()
        if hitNodePath.hasPythonTag("owner"):
            hitObject = hitNodePath.getPythonTag("owner")
            if not isinstance(hitObject, TrapEnemy):
                hitObject.alterHealth(self.damagePerSecond*dt)

        # NEW STUFF STARTS HERE

        # Find out how long the beam is, and scale the
        # beam-model accordingly.
        beamLength = (hitPos - self.actor.getPos()).length()
        self.beamModel.setSy(beamLength)

        self.beamModel.show()
else:
    # If we're not shooting, don't show the beam-model.
    self.beamModel.hide()
{% endhighlight %}

![Panda-chan firing a laser](images/laserUp.png "ZAP!")

Of course, right now our laser starts at (0, 0, 0), points in the positive y-direction, and... stays that way. If you lure the "walking enemy" to a point just "above" centre, you may see the laser react, regardless of where you are. 

We'll have our laser fire towards the mouse-cursor, and start at the player-character's position. Furthermore, we'll have our character face the direction in which we're firing. As it happens, these two things work together nicely...

[This lesson's reference code][refCode]

[On to Lesson 10][next]

[next]: tut_lesson10.html
[refCode]: https://github.com/ArsThaumaturgis/Panda3DTutorial.io/tree/master/ReferenceCode/Lesson9
