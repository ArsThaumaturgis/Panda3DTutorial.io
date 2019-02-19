Bumping into Things
=
_In which we handle basic collision-detection and response_

For the purposes of handling collisions and physics in Panda3D, we have a few options. Of these, perhaps the most prominent two are Panda's built-in collision system, and the Bullet physics system, which Panda provides integration with.

Bullet is an excellent physics system, I think, and very well-suited to situations that call for complex physics.

Panda's built-in system is perhaps less capable, but for simple cases I feel that it works well enough, and is a little easier to use.

So, for the purposes of this tutorial I intend to use Panda's built-in system. 

Before we get into this, if you want more details regarding the elements used here, or even just want to see what other types of physics-elements are available, I recommend that you check the Panda3D manual. It provides a nicely in-depth description of the various elements involved, I feel!

The built-in physics system has three main elements: Traversers, Handlers, and Solids.

* Traversers are the things that check the various physics objects for collisions.
* Handlers determine what happens when a collision occurs (or continues, or ceases to occur).
* Solids are the actual physics-objects themselves--the spheres and boxes and polygonal shapes that do the colliding.

Often enough--and so it is in our case--we can use just a single traverser, and let it check for collisions every update. For this case, the ShowBase class provides a default variable called "cTrav": if you assign a new traverser to this variable, Panda will automatically update it for you.

```python
# In your import statements:
from panda3d.core import CollisionTraverser
```

```python
# In the "__init__" method:
self.cTrav = CollisionTraverser()
# Panda should now automatically update that traverser!
```

Next, we want a handler. There are a number of these, but there are three that we will be using in this tutorial:

* "CollisionHandlerQueue" simply stores collision events in a queue, and lets you access them as you please. You can also sort the queue, allowing you to easily get the first collision.
* "CollisionHandlerEvent" calls events whenever specified collisions occur, continue, or end.
* "CollisionHandlerPusher" prevents nominated solid objects from intersecting other solid objects.

The "pusher" handler is a sub-class of the "event" handler. This means that a "pusher" can also send collision events, a feature that we will be using later...

Making a "pusher" is quite simple:

```python
# In your import statements:
from panda3d.core import CollisionHandlerPusher,
```

```python
# In the "__init__" method:
self.pusher = CollisionHandlerPusher()
```

We'll store our reference to it, be cause we want to be able to add and remove objects as called for.

Then we create a collision-object, in this case for our player-character. This involves creating a solid (we'll just use a sphere), storing that in a collision-node, and then creating a NodePath for that node, attached to our player (so that it moves with the player):

```python
# In your import statements:
from panda3d.core import CollisionSphere, CollisionNode
```

```python
# In the "__init__" method:
colliderNode = CollisionNode("player")
# Add a collision-sphere centred on (0, 0, 0), and with a radius of 0.3
colliderNode.addSolid(CollisionSphere(0, 0, 0, 0.3))
collider = self.tempActor.attachNewNode(colliderNode)
```

If you want to see your collision-object, just call "show" on the collision-object's NodePath. However, this visualisation is for testing and debugging purposes--it may not be efficient, and isn't recommended for a release version of your game.

```python
collider.show()
```

![Panda-chan with a collision sphere](images/collisionSphere.png "Note the white circle--that's our collision sphere")

Now, Panda3D's built-in system doesn't check every object against every other object. (I imagine that this is for reasons of speed--it's much faster to check just a few objects.) So, only certain objects, nominated by you, are considered to be "active", and thus checked. All other physics objects are considered to be "inactive", and not checked.

That is, "active" objects generate collisions with other objects (whether "active" or "inactive"), while "inactive" objects don't generate collisions. "Active" objects collide, and are collided with; "inactive" objects are only collided with.

So, finally, we tell both the traverser and the pusher that this is an object that should collide with things, an "active" object:

```python
# The pusher wants a collider, and a NodePath that
# should be moved by that collider's collisions.
# In this case, we want our player-Actor to be moved.
base.pusher.addCollider(collider, self.tempActor)
# The traverser wants a collider, and a handler
# that responds to that collider's collisions
base.cTrav.addCollider(collider, self.pusher)
```

In our game, the action is effectively two-dimensional: the player moves around on a flat, horizontal surface. Because of this, allowing collision responses to be three-dimensional could result in problems, like the player moving over a wall rather than being stopped by it.

The "pusher" handler has a provision for such cases as this: it allows its responses to be restricted to the horizontal, like so:

```python
self.pusher.setHorizontal(True)
```

Of course, right now there are no other collision objects, so there's nothing for the player to collide with. Let's rectify that, and add some simple walls.

I happen to know that the environment model has its walls at about eight units in each direction, so we'll place our collision-walls accordingly.

The process is pretty much the same as with creating the player's collision-object, but we're going to use long capsule-shaped tubes instead of spheres. We also place the walls in appropriate positions once we've created them.

```python
# In your import statements:
from panda3d.core import CollisionTube
```

```python
# In the "__init__" method:

# Tubes are defined by their start-points, end-points, and radius.
# In this first case, the tube goes from (-8, 0, 0) to (8, 0, 0),
# and has a radius of 0.2.
wallSolid = CollisionTube(-8.0, 0, 0, 8.0, 0, 0, 0.2)
wallNode = CollisionNode("wall")
wallNode.addSolid(wallSolid)
wall = render.attachNewNode(wallNode)
wall.setY(8.0)

wallSolid = CollisionTube(-8.0, 0, 0, 8.0, 0, 0, 0.2)
wallNode = CollisionNode("wall")
wallNode.addSolid(wallSolid)
wall = render.attachNewNode(wallNode)
wall.setY(-8.0)

wallSolid = CollisionTube(0, -8.0, 0, 0, 8.0, 0, 0.2)
wallNode = CollisionNode("wall")
wallNode.addSolid(wallSolid)
wall = render.attachNewNode(wallNode)
wall.setX(8.0)

wallSolid = CollisionTube(0, -8.0, 0, 0, 8.0, 0, 0.2)
wallNode = CollisionNode("wall")
wallNode.addSolid(wallSolid)
wall = render.attachNewNode(wallNode)
wall.setX(-8.0)
```

If we try to run around now, we'll find ourselves stopped at the walls!

![Trying--and failing--to run through a wall](images/tutCollisionWalls.gif "The pusher prevents the player's collision-object from going through the wall's")

(I've called "show" on both our player and the walls for the image above, so that the collision objects are visible.)

With the basics of collision in place, it's time to lay the foundation for our core gameplay...

[On to Lesson 7][next]

[next]: tut_lesson07.html
