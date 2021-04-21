---
layout: page
title: Lesson 8
---
It's a Trap!
=
_In which we learn about collision events, and make a sliding trap enemy_

With the basics in place, it's back to Panda-specific matters!

Specifically, we're going to look at getting collision events from our collision-handler, and use them for a deadly "sliding block trap" enemy.

To start with, let's make the enemy, in our "GameObject.py" file.

Since this enemy is intended to collide into other things, we add its collider to our "pusher" handler, and to "cTrav".

In terms of logic, the trap simply compares its position to the player's, and if the player comes within range of its line of movement, it starts moving. This is controlled by the "moveDirection" variable: when it's zero, the trap isn't moving; when it's one or minus one, it moves in one or the other direction.

In "GameObject.py":
{% highlight python %}
# In your "import" statements:
import math
{% endhighlight %}

{% highlight python %}
# Elsewhere:
class TrapEnemy(Enemy):
    def __init__(self, pos):
        Enemy.__init__(self, pos,
                       "Models/Misc/trap",
                       {
                        "stand" : "Models/Misc/trap-stand",
                        "walk" : "Models/Misc/trap-walk",
                        },
                       100.0,
                       10.0,
                       "trapEnemy")

        base.pusher.addCollider(self.collider, self.actor)
        base.cTrav.addCollider(self.collider, base.pusher)

        self.moveInX = False

        self.moveDirection = 0

        # This will allow us to prevent multiple
        # collisions with the player during movement
        self.ignorePlayer = False

    def runLogic(self, player, dt):
        if self.moveDirection != 0:
            self.walking = True
            if self.moveInX:
                self.velocity.addX(self.moveDirection*self.acceleration*dt)
            else:
                self.velocity.addY(self.moveDirection*self.acceleration*dt)
        else:
            self.walking = False
            diff = player.actor.getPos() - self.actor.getPos()
            if self.moveInX:
                detector = diff.y
                movement = diff.x
            else:
                detector = diff.x
                movement = diff.y

            if abs(detector) < 0.5:
                self.moveDirection = math.copysign(1, movement)

    def alterHealth(self, dHealth):
        pass
{% endhighlight %}

Next, let's add a temporary testing-trap to the level, in our "Game.py" file:

{% highlight python %}
# In the "__init__" method:
self.tempTrap = TrapEnemy(Vec3(-2, 7, 0))
{% endhighlight %}
{% highlight python %}
# In the "update" method:
self.tempTrap.update(self.player, dt)
{% endhighlight %}

For now, the trap will move, but never stop attempting to move. Similarly, while it will collide with other objects, it won't do any harm.

What we want, essentially, is to be informed when a collision occurs, and run some code. To that end, we will use collision events.

Recall that, when I first described the collision-handlers that we would be using, I mentioned "CollisionHandlerEvent", and that "CollisionHandlerPusher"--which we're using--is a subclass of "CollisionHandlerEvent". As I said then, this means that our "pusher" can provide collision-events, just as any "CollisionHandlerEvent" can.

To start with, we tell our handler what sort of events we want. There is a basic syntax that describes these things, but for our purposes I'll just describe what we're doing here, specifically. For a full explanation of this syntax, check the manual!

In short, we're going to tell the "pusher" that we want "in" events--that is, the initial collision of two objects--that have the pattern "some-named-from-node" colliding into "some-named-into-node". We could also ask for nodes continuing to collide ("again" events), and ceasing to collide ("out" events), if we wanted to.

Thus, we ask the "pusher" to add an "in"-pattern, of the form "%fn-into-%in". "%fn" will be replaced with the name of the "from" collision-object (the object that is "doing" the colliding), while "%in" will be replaced with the name of the "into" collision-object (the object that is "being collide with"). The "-into-" between "%fn" and "%in" doesn't have any effect, save to make the events clearer to us, I believe.

In "Game.py":
{% highlight python %}
# In the "__init__" method:
self.pusher.add_in_pattern("%fn-into-%in")
{% endhighlight %}

Next, we want to actually receive those events. This works just like key-events, except that instead of the name of a key, we use the pattern that we specified above, but with collider-names. If you're not sure of where those names come from, check the names given to the collision-nodes in the previous lesson!

{% highlight python %}
# In the "__init__" method:
self.accept("trapEnemy-into-wall", self.stopTrap)
self.accept("trapEnemy-into-trapEnemy", self.stopTrap)
self.accept("trapEnemy-into-player", self.trapHitsSomething)
self.accept("trapEnemy-into-walkingEnemy", self.trapHitsSomething)
{% endhighlight %}

When those events occur, Panda will call the methods named "stopTrap" and "trapHitsSomething", as appropriate. Of course, we don't yet have those, so let's make them. (If we don't, our game will likely crash.)

When a collision-event method is called, it's given a "collision entry". This entry provides a variety of pieces of information: the nodes that collided, where they collided, the surface-normal at the collision, and so on.

The "stopTrap" method will be called when the trap hits a wall, so we simply tell it to no longer move (by setting "moveDirection" to "0"), and reset its "ignorePlayer" variable, so that it can hit the player if it moves again.

The "trapHitsSomething" method will be called when the trap hits the player or an enemy. In this case, if it hits the player, have it subtract one health-point. It's deadlier to enemies, however--a one-hit kill by virtue of doing more damage than they have health.

Note the use of our Python-tags to access the GameObjects associated with the colliders.

{% highlight python %}
    def stopTrap(self, entry):
        collider = entry.getFromNodePath()
        if collider.hasPythonTag("owner"):
            trap = collider.getPythonTag("owner")
            trap.moveDirection = 0
            trap.ignorePlayer = False

    def trapHitsSomething(self, entry):
        collider = entry.getFromNodePath()
        if collider.hasPythonTag("owner"):
            trap = collider.getPythonTag("owner")

            # We don't want stationary traps to do damage,
            # so ignore the collision if the "moveDirection" is 0
            if trap.moveDirection == 0:
                return

            collider = entry.getIntoNodePath()
            if collider.hasPythonTag("owner"):
                obj = collider.getPythonTag("owner")
                if isinstance(obj, Player):
                    if not trap.ignorePlayer:
                        obj.alterHealth(-1)
                        trap.ignorePlayer = True
                else:
                    obj.alterHealth(-10)
{% endhighlight %}

Our player and enemy don't really react to taking damage just yet--but at least we can see the trap going back and forth now.

![A "trap" moving back and forth, colliding harmlessly](images/tutHarmlessTrap.gif "Bump. Bump.")

We'll get to reactions to damage soon enough, but first, let's provide our player with a way to fight back...

[This lesson's reference code][refCode]

[On to Lesson 9][next]

[next]: tut_lesson09.html
[refCode]: https://github.com/ArsThaumaturgis/Panda3DTutorial.io/tree/master/ReferenceCode/Lesson8
