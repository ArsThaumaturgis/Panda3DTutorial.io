---
layout: page
title: Lesson 4
---
Taking Control
=
_In which we see how Panda handles input_

Aside from GUI elements, there are two main ways of taking input in Panda3D: key-events, and key-polling. In the former, we have Panda call a nominated method when a key is pressed, released, or repeated. In the latter, we check (whenever we want) whether a key is pressed at that moment.

Aside from the mouse, which we'll get to later, we'll be using key-events in this tutorial. I'm not convinced that one way is strictly better than the other, so the choice is somewhat arbitrary.

The process is pretty simple. To start with, we want somewhere to store our key-information so that we can examine it later. We'll use a simple dictionary, mapping key-names to key-states. "True" means that the key is pressed; "False" means that it's not.

{% highlight python %}
self.keyMap = {
    "up" : False,
    "down" : False,
    "left" : False,
    "right" : False,
    "shoot" : False
}
{% endhighlight %}

(A quick note: don't confuse the "keys" used to access our dictionary with the "keys" that are to be pressed on the keyboard or mouse!)

For the sake of simplicity, I'm just using hard-coded strings as the keys in this dictionary. For a serious project, I recommend using constant (perhaps global) variables to store these key-values: it's easier to make changes, and less likely to cause bugs via typos, I think.

Key-events call a method when the event occurs. In our case, this method will take a dictionary-key corresponding to the keyboard-key, and a value to assign to the associated dictionary-item. We're not quite ready to control a character just yet, so for now let's just print out what's happening so that we can see the response. Like so:

{% highlight python %}
def updateKeyMap(self, controlName, controlState):
    self.keyMap[controlName] = controlState
    print (controlName, "set to", controlState)
{% endhighlight %}

And finally, we'll tell Panda that we're interested in the relevant key-events.

In Panda3D, events are handled by objects of the "DirectObject" class. ShowBase is a sub-class of DirectObject--and our game is a sub-class of ShowBase. That means that our game-class can handle events.

To register our interest in an event, we tell the relevant DirectObject to "accept" that event, passing in a method that we want it to call when the event occurs, and optionally any additional parameters.

In the case of a key-press, the event is simply named for the key, the method to be called is our "updateKeyMap" method, and the parameters are the dictionary-key, and the new state for the dictionary-item associated with it.

{% highlight python %}
self.accept("w", self.updateKeyMap, ["up", True])
{% endhighlight %}

The process is similar for registering interest in a key being released--we just add "-up" to the key's name:

{% highlight python %}
self.accept("w-up", self.updateKeyMap, ["up", False])
{% endhighlight %}

And we repeat the process for all of the relevant controls. In the case of the game that we're making, the controls will be just WASD for movement, and the mouse to aim and shoot. (Mouse-aiming is covered later in the tutorial.)

Thus we end up with the following:

{% highlight python %}
self.accept("w", self.updateKeyMap, ["up", True])
self.accept("w-up", self.updateKeyMap, ["up", False])
self.accept("s", self.updateKeyMap, ["down", True])
self.accept("s-up", self.updateKeyMap, ["down", False])
self.accept("a", self.updateKeyMap, ["left", True])
self.accept("a-up", self.updateKeyMap, ["left", False])
self.accept("d", self.updateKeyMap, ["right", True])
self.accept("d-up", self.updateKeyMap, ["right", False])
self.accept("mouse1", self.updateKeyMap, ["shoot", True])
self.accept("mouse1-up", self.updateKeyMap, ["shoot", False])
{% endhighlight %}

This still doesn't do much, of course. So, let's tie those controls to a more interesting set of reponses...

[On to Lesson 5][next]

[next]: tut_lesson05.html
