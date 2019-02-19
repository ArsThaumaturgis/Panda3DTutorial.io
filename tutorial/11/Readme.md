---
layout: page
title: Lesson 11
---
An Enemy Attacks!
=
_In which we give our Walking Enemy the means to attack us_

Making our "Walking Enemy" attack the player-character is fairly straightforward.

To start with, the attack itself. This will be fundamentally similar to the player's laser-attack, but instead of using an indefinitely-long ray we will use a limited-length (in fact, quite short) line-segment, thus creating a "melee attack".

{% highlight python %}
# In your "import" statements:
from panda3d.core import CollisionSegment
{% endhighlight %}

{% highlight python %}
# In the "__init__" method of "WalkingEnemy":
segmentNode = CollisionNode("enemyAttackSegment")
segmentNode.addSolid(self.attackSegment)

# A mask that matches the player's, so that
# the enemy's attack will hit the player-character,
# but not the enemy-character (or other enemies)
mask = BitMask32()
mask.setBit(1)

segmentNode.setFromCollideMask(mask)

mask = BitMask32()

segmentNode.setIntoCollideMask(mask)

self.attackSegmentNodePath = render.attachNewNode(segmentNode)
self.segmentQueue = CollisionHandlerQueue()

base.cTrav.addCollider(self.attackSegmentNodePath, self.segmentQueue)

# How much damage the enemy's attack does
# That is, this results in the player-character's
# health being reduced by one.
self.attackDamage = -1
{% endhighlight %}

The detection of hits is once again pretty much the same as in the case of the player: sort the collision-queue, take the first hit (if any), and if that hit was on a GameObject, have that object take damage.

But where the player-character has the attack be controlled by the player's input, the Walking Enemy will control its attack via its "runLogic" method.

{% highlight python %}
# In your "import" statements:
import random
{% endhighlight %}

{% highlight python %}
# In the "__init__" method of "WalkingEnemy":

# The delay between the start of an attack,
# and the attack (potentially) landing
self.attackDelay = 0.3
self.attackDelayTimer = 0
# How long to wait between attacks
self.attackWaitTimer = 0
{% endhighlight %}

{% highlight python %}
# In the "runLogic" method of "WalkingEnemy":

# Set the segment's start- and end- points.
# "getQuat" returns a quaternion--a representation
# of orientation or rotation--that represents the
# NodePath's orientation. This is useful here,
# because Panda's quaternion class has methods to get
# forward, right, and up vectors for that orientation.
# Thus, what we're doing is making the segment point "forwards".
self.attackSegment.setPointA(self.actor.getPos())
self.attackSegment.setPointB(self.actor.getPos() + self.actor.getQuat().getForward()*self.attackDistance)
{% endhighlight %}

Previously, we had the following in the "runLogic" method of "WalkingEnemy":

{% highlight python %}
if distanceToPlayer > self.attackDistance*0.9:
    self.walking = True
    vectorToPlayer.setZ(0)
    vectorToPlayer.normalize()
    self.velocity += vectorToPlayer*self.acceleration*dt
else:
    self.walking = False
    self.velocity.set(0, 0, 0)
{% endhighlight %}

We'll now add to this a bit:

If the enemy is far from the player, and isn't playing its attack animation, it's allowed to move. Furthermore, it resets its attack -waiting and -delaying timers. 

If it's near to the player, it stops moving. If the attack-delay timer is active--that is, it's attacking, and waiting for the point at which an attack "lands"--it runs that timer down. When the timer runs out, it checks the collision-queue for a hit, and if one's detected, it applies damage. On the other hand, if the attack-wait timer is active--that is, it's between attacks, waiting to start an attack--it runs that timer down. When the timer runs out, it starts an attack, and sets the attack-delay timer.

The result looks like this:

{% highlight python %}
if distanceToPlayer > self.attackDistance*0.9:
    attackControl = self.actor.getAnimControl("attack")
    if not attackControl.isPlaying():
        self.walking = True
        vectorToPlayer.setZ(0)
        vectorToPlayer.normalize()
        self.velocity += vectorToPlayer*self.acceleration*dt
        self.attackWaitTimer = 0.2
        self.attackDelayTimer = 0
else:
    self.walking = False
    self.velocity.set(0, 0, 0)

    # If we're waiting for an attack to land...
    if self.attackDelayTimer > 0:
        self.attackDelayTimer -= dt
        # If the time has come for the attack to land...
        if self.attackDelayTimer <= 0:
            # Check for a hit..
            if self.segmentQueue.getNumEntries() > 0:
                self.segmentQueue.sortEntries()
                segmentHit = self.segmentQueue.getEntry(0)

                hitNodePath = segmentHit.getIntoNodePath()
                if hitNodePath.hasPythonTag("owner"):
                    # Apply damage!
                    hitObject = hitNodePath.getPythonTag("owner")
                    hitObject.alterHealth(self.attackDamage)
                    self.attackWaitTimer = 1.0
    # If we're instead waiting to be allowed to attack...
    elif self.attackWaitTimer > 0:
        self.attackWaitTimer -= dt
        # If the wait has ended...
        if self.attackWaitTimer <= 0:
            # Start an attack!
            # (And set the wait-timer to a random amount,
            #  to vary things a little bit.)
            self.attackWaitTimer = random.uniform(0.5, 0.7)
            self.attackDelayTimer = self.attackDelay
            self.actor.play("attack")
{% endhighlight %}

And finally, as with the player-character, there's a bit of cleanup to do:

{% highlight python %}
# In the "WalkingEnemy" class:
def cleanup(self):
    base.cTrav.removeCollider(self.attackSegmentNodePath)
    self.attackSegmentNodePath.removeNode()

    GameObject.cleanup(self)
{% endhighlight %}

And that's it! If you run the game now, you should find that our WalkingEnemy not only chases the player, but attacks when in range, too!

![An enemy chases and attacks the player-character.](images/tutEnemyAttack.gif "Finally! My blades are set free!!! >:D")

This is all very well and good, but right now all those hits and collisions don't have much effect. To start with, let's add some visual feedback: beam-impacts, hit-flashes, and a bit of UI...

[On to Lesson 12][next]

[next]: tut_lesson12.html
