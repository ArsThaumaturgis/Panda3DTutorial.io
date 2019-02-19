---
layout: page
title: Lesson 10
---
Lasing Around
=
_In which we gain control of our laser!_

We will be controlling our laser via the mouse, and so we want to know where the mouse-pointer is. For this we turn to Panda3D's set of "watchers", objects that keep track of certain inputs, the mouse included. And once again, it provides easy access to the mouse-watcher via a variable stored in the ShowBase object, called "mouseWatcherNode".

So, we get the mouse-position like this:

{% highlight python %}
# In the "__init__" method of the Player class:

# This stores the previous position of the mouse,
# as a fall-back in case we don't get a good position
# on a given update.
self.lastMousePos = Vec2(0, 0)
{% endhighlight %}
{% highlight python %}
# In the "update" method of the Player class:

# It's possible that we'll find that we
# don't have the mouse--such as if the pointer
# is outside of the game-window. In that case,
# just use the previous position.
mouseWatcher = base.mouseWatcherNode
if mouseWatcher.hasMouse():
    mousePos = mouseWatcher.getMouse()
else:
    mousePos = self.lastMousePos
{% endhighlight %}

Next, we want to find out what 3D point our 2D mouse-coordinate corresponds with. Now, a 2D point on an image corresponds not to a single 3D point, but to a line travelling "into" the image. What we want, then, is the point on that line that happens to be at floor-height.

So, first we'll figure out what that line is by getting a corresponding point on the near-plane of the "camera", and one on the far-plane of it, by having the camera's lens calculate them for us.

Then, since we're playing on a flat, horizontal level, we can make use of a neat convenience function that Panda provides: its "Plane" class can determine where a line, defined by two points, intersects it. That will give us our 3D point.

{% highlight python %}
# In your import statements:
from panda3d.core import Plane, Point3
{% endhighlight %}
{% highlight python %}
# In the "__init__" method of the "Player" class:

# Construct a plane facing upwards, and centred at (0, 0, 0)
self.groundPlane = Plane(Vec3(0, 0, 1), Vec3(0, 0, 0))
{% endhighlight %}
{% highlight python %}
# Then, in the "update" method of the "Player" class:
mousePos3D = Point3()
nearPoint = Point3()
farPoint = Point3()

# Get the 3D line corresponding with the 
# 2D mouse-position.
# The "extrude" method will store its result in the
# "nearPoint" and "farPoint" objects.
base.camLens.extrude(mousePos, nearPoint, farPoint)

# Get the 3D point at which the 3D line
# intersects our ground-plane.
# Similarly to the above, the "intersectsLine" method
# will store its result in the "mousePos3D" object.
self.groundPlane.intersectsLine(mousePos3D,
                                render.getRelativePoint(base.camera, nearPoint),
                                render.getRelativePoint(base.camera, farPoint))
{% endhighlight %}

(Panda3D distinguishes "points" from "vectors"--a matter on which I disagree with whoever made that distinction in the engine. For the most part the "Point" class can be used or ignored as you prefer. However, note that there are a few cases in which Panda will insist on having a "point", not a "vector" (or vice versa), such as in the code above.)

Finally, now that we have the point that we want, we can use it to direct our ray and orient our character.

To do so, we construct a vector from the player's position to the point, and take just the horizontal part of it, since we're not interested in any difference in z-position. From this, we find the angle that it makes with the positive y-axis--this is the angle at which to face our player-character. (This is much like what we did with the "WalkingEnemy", except that instead of using the vector between the player and the enemy, we're using the vector between the 3D mouse-point and the player.) Then we set the ray's origin to the player's position, and its direction to our vector.

And finally, we store our mouse-pos in "lastMousePos".

{% highlight python %}
# In the "__init__" method of the "Player" class:

# This vector is used to calculate the orientation for
# the character's model. Since the character faces along
# the y-direction, we use the y-axis.
self.yVector = Vec2(0, 1)
{% endhighlight %}
{% highlight python %}
# And in the "update" method of the "Player" class:

firingVector = Vec3(mousePos3D - self.actor.getPos())
firingVector2D = firingVector.getXy()
firingVector2D.normalize()
firingVector.normalize()

heading = self.yVector.signedAngleDeg(firingVector2D)

self.actor.setH(heading)

if firingVector.length() > 0.001:
    self.ray.setOrigin(self.actor.getPos())
    self.ray.setDirection(firingVector)

self.lastMousePos = mousePos
{% endhighlight %}

![Panda-chan runs around, shooting a laser towards the mouse-pointer.](images/tutHarmlessLaser.gif "Bwee! Bzzz!")

Of course, it's not fair that the walking enemy can be hit by both us _and_ the traps, but can't do anything itself. So let's give it the ability to attack, too...

[On to Lesson 11][next]

[next]: tut_lesson11.html
