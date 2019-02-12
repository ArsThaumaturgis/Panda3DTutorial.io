---
layout: page
title: Lesson 5
---
Our Next Task
=
_In which we learn about updating via tasks_

Often, we want Panda to run some method repeatedly--as in the case of an "update" loop--or after a certain amount of time. For these purposes, Panda provides "tasks".

Tasks are handled, appropriately, by a class named "TaskManager". And once again, Panda provides a default, globally-accessible manager, in this case in a variable called "taskMgr".

When we want to add a task to be run immediately, we have the task-manager "add" it, and when we want to run a task after a specified amount of time, we ask the task-manager to "doMethodLater". We can also have a running task removed from the manager, if we no longer want it.

We're going to use the task-manager to run an update loop, calling a method named "update".

{% highlight python %}
# In your import statements:
from direct.task import Task
{% endhighlight %}

{% highlight python %}
# In the "__init__" method:
self.updateTask = taskMgr.add(self.update, "update")
{% endhighlight %}

(We're storing the update-task in case we want to do something with it later. We won't in this case, but it's perhaps not bad practice.)

{% highlight python %}
# Elsewhere:
def update(self, task):
    return Task.cont
{% endhighlight %}

Note that we return "Task.cont"--this is important, as it tells Panda that we want to run the task again. Without it, the task would run only once.

Now, let's have those controls actually do something! Specifically, let's move our character around a bit.

You may recall that in an earlier lesson we saw how to set the position of a NodePath. We'll do the same here, setting our "tempActor" NodePath's position to be a short distance from where it was at the start of the update.

But if we just move it by a constant value, variations in frame-rate will vary how fast it moves. So, we will access the time since the last update via another Panda global variable, the "globalClock". We then multiply our movement by this value.

{% highlight python %}
# In your import statements, add "Vec3":
from panda3d.core import Vec4, Vec3
{% endhighlight %}

{% highlight python %}
# Elsewhere:
def update(self, task):
    # Get the amount of time since the last update
    dt = globalClock.getDt()

    # If any movement keys are pressed, use the above time
    # to calculate how far to move the character, and apply that.
    if self.keyMap["up"]:
        self.tempActor.setPos(self.tempActor.getPos() + Vec3(0, 5.0*dt, 0))
    if self.keyMap["down"]:
        self.tempActor.setPos(self.tempActor.getPos() + Vec3(0, -5.0*dt, 0))
    if self.keyMap["left"]:
        self.tempActor.setPos(self.tempActor.getPos() + Vec3(-5.0*dt, 0, 0))
    if self.keyMap["right"]:
        self.tempActor.setPos(self.tempActor.getPos() + Vec3(5.0*dt, 0, 0))
    if self.keyMap["shoot"]:
        print ("Zap!")

    return Task.cont
{% endhighlight %}

(I've also removed the print-statement from "updateKeyMap", by the way, since we now have a more-visual means of seeing at least some of our key-pressed taking effect.)

![Panda-chan running around due to key-movement](images/tutMasicKeyMovement.gif "Run run run.")

Of course, right now we can just run through the walls. That won't do...

[On to Lesson 6][next]

[next]: tut_lesson6.html
