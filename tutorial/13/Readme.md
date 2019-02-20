Endless Enemies
=
_In which we spawn enemies, and have them die when out of health_

Up until now, we've only had a single Walking Enemy and Trap Enemy each, hard-coded in our "Game" class. Not only do we have no means of spawning more, but the Walking Enemies don't die when they run out of health.

In this lesson, we'll change that.

Once again, this is mostly game-logic, which I intend to skim over.

To start with, two minor changes in "GameObject.py". These simply have the Walking Enemy play a "spawn" animation when its constructed, and skip the behaviour in "runLogic" until the "spawn" animation is done:

```python
# In the "__init__" method of WalkingEnemy:
self.actor.play("spawn")
```

```python
# In the "runLogic" method of WalkingEnemy:

# At the start of the method:
spawnControl = self.actor.getAnimControl("spawn")
if spawnControl is not None and spawnControl.isPlaying():
    return
```

Now, on to "Game.py".

First, delete the code related to "self.tempEnemy" and "self.tempTrap", in both the "\_\_init\_\_" and "update" methods.

What we're going to do is keep a few lists: one of enemies, one of traps, one of "dead enemies" (so that we can clean them up, but only after they've finished animating), and one of spawn-points for enemies.

The spawn-points will simply be positions spaced evenly along the walls, and when spawning an enemy, we'll randomly choose one as the location for the new enemy.

Traps will be placed at the start of the level. They'll similarly use a list of positions, but, to prevent the placement of two traps in the same spot, we'll remove positions as we choose them.

We'll also create a new "startGame" method to contain the logic for the spawning of traps, creation of the player, and a few other things. While not terribly useful just yet, it will come in handy once we add the ability to restart the game when the player-character dies.

```python
# In your "import" statements:
import random
```

```python
# In the "__init__" method:

# Start off with no player; the
# player-character will be created
# in the "startGame" method, below.
# Note that this replaces the
# "self.player = Player()" line
# that was here
self.player = None

# Our enemies, traps, and "dead enemies"
self.enemies = []
self.trapEnemies = []

self.deadEnemies = []

# Set up some spawn points
self.spawnPoints = []
numPointsPerWall = 5
for i in range(numPointsPerWall):
    coord = 7.0/numPointsPerWall + 0.5
    self.spawnPoints.append(Vec3(-7.0, coord, 0))
    self.spawnPoints.append(Vec3(7.0, coord, 0))
    self.spawnPoints.append(Vec3(coord, -7.0, 0))
    self.spawnPoints.append(Vec3(coord, 7.0, 0))

# Values to control when to spawn enemies, and
# how many enemies there may be at once
self.initialSpawnInterval = 1.0
self.minimumSpawnInterval = 0.2
self.spawnInterval = self.initialSpawnInterval
self.spawnTimer = self.spawnInterval
self.maxEnemies = 2
self.maximumMaxEnemies = 20

self.numTrapsPerSide = 2

self.difficultyInterval = 5.0
self.difficultyTimer = self.difficultyInterval

# Start the game!
self.startGame()
```

```python
# Elsewhere in the Game class:

def startGame(self):
    # We'll add this method presently.
    # In short, clean up anything in the
    # level--enemies, traps, etc.--before
    # starting a new one.
    self.cleanup()

    self.player = Player()

    self.maxEnemies = 2
    self.spawnInterval = self.initialSpawnInterval

    self.difficultyTimer = self.difficultyInterval

    sideTrapSlots = [
        [],
        [],
        [],
        []
    ]
    trapSlotDistance = 0.4
    slotPos = -8 + trapSlotDistance
    while slotPos < 8:
        if abs(slotPos) > 1.0:
            sideTrapSlots[0].append(slotPos)
            sideTrapSlots[1].append(slotPos)
            sideTrapSlots[2].append(slotPos)
            sideTrapSlots[3].append(slotPos)
        slotPos += trapSlotDistance

    # Create one trap on each side, repeating
    # for however many traps there should be
    # per side.
    for i in range(self.numTrapsPerSide):
        # Note that we "pop" the chosen location,
        # so that it won't be chosen again.
        slot = sideTrapSlots[0].pop(random.randint(0, len(sideTrapSlots[0])-1))
        trap = TrapEnemy(Vec3(slot, 7.0, 0))
        self.trapEnemies.append(trap)

        slot = sideTrapSlots[1].pop(random.randint(0, len(sideTrapSlots[1])-1))
        trap = TrapEnemy(Vec3(slot, -7.0, 0))
        self.trapEnemies.append(trap)

        slot = sideTrapSlots[2].pop(random.randint(0, len(sideTrapSlots[2])-1))
        trap = TrapEnemy(Vec3(7.0, slot, 0))
        trap.moveInX = True
        self.trapEnemies.append(trap)

        slot = sideTrapSlots[3].pop(random.randint(0, len(sideTrapSlots[3])-1))
        trap = TrapEnemy(Vec3(-7.0, slot, 0))
        trap.moveInX = True
        self.trapEnemies.append(trap)
```

Next, we'll add a method to clean up a level once we're done with it. 

Furthermore, it might be a good idea to clean up not only when starting a new level, but also when exiting the game. To that end, we'll tell Panda that, when the user indicates that they want to quit, we want to run a custom exit-function. This function will run our new clean-up method, then quit.

```python
# In the "__init__" method:
self.exitFunc = self.cleanup
```

```python
# Elsewhere in the Game class:
def cleanup(self):
    # Call our various cleanup methods,
    # empty the various lists,
    # and make the player "None" again.

    for enemy in self.enemies:
        enemy.cleanup()
    self.enemies = []

    for enemy in self.deadEnemies:
        enemy.cleanup()
    self.deadEnemies = []

    for trap in self.trapEnemies:
        trap.cleanup()
    self.trapEnemies = []

    if self.player is not None:
        self.player.cleanup()
        self.player = None

def quit(self):
    # Clean up, then exit

    self.cleanup()

    base.userExit()
```

If we run the game now, we'll be able to move around as before, and we'll have traps scattered randomly around the walls. The traps won't, however, move. (Because they're not being updated--yet.)

Next, we'll add a method to spawn an enemy. This is pretty straightforward: pick a spawn-point, create an enemy at that point, and add the new enemy to our list of enemies:

```python
def spawnEnemy(self):
    if len(self.enemies) < self.maxEnemies:
        spawnPoint = random.choice(self.spawnPoints)

        newEnemy = WalkingEnemy(spawnPoint)

        self.enemies.append(newEnemy)
```

And finally, we'll implement the logic to make it all do something. In short, the logic looks something like this:
* If the player isn't "None", and has health, run this logic.
* Update the player.
* Count down the spawn-timer; if it finishes, attempt to spawn an enemy, and reset the timer.
* Update the enemies and traps.
* Find enemies that have just died. For each of those:
    * Exclude them from the list of enemies
    * Remove their colliders
    * Award to the player their score-value
    * And add them to the list of "dead enemies"
* If there were any dead enemies, update the player's score-UI.
* Check the "dead enemies" to see if any have finished animating their "die" animation; if so, remove them and clean them up.
* And finally, run the difficulty timer down; if it finishes, make the game a little more difficult by increasing the maximum number of enemies, and decreasing the time between spawns.

In code form:

```python
# In the "update" method:

# If the player is dead, or we're not
# playing yet, ignore this logic.
if self.player is not None:
    if self.player.health > 0:
        self.player.update(self.keyMap, dt)

        # Wait to spawn an enemy...
        self.spawnTimer -= dt
        if self.spawnTimer <= 0:
            # Spawn one!
            self.spawnTimer = self.spawnInterval
            self.spawnEnemy()

        # Update all enemies and traps
        [enemy.update(self.player, dt) for enemy in self.enemies]
        [trap.update(self.player, dt) for trap in self.trapEnemies]

        # Find the enemies that have just
        # died, if any
        newlyDeadEnemies = [enemy for enemy in self.enemies if enemy.health <= 0]
        # And re-build the enemy-list to exclude
        # those that have just died.
        self.enemies = [enemy for enemy in self.enemies if enemy.health > 0]

        # Newly-dead enemies should have no collider,
        # and should play their "die" animation.
        # In addition, increase the player's score.
        for enemy in newlyDeadEnemies:
            enemy.collider.removeNode()
            enemy.actor.play("die")
            self.player.score += enemy.scoreValue
        if len(newlyDeadEnemies) > 0:
            self.player.updateScore()

        self.deadEnemies += newlyDeadEnemies

        # Check our "dead enemies" to see
        # whether they're still animating their
        # "die" animation. In not, clean them up,
        # and drop them from the "dead enemies" list.
        enemiesAnimatingDeaths = []
        for enemy in self.deadEnemies:
            deathAnimControl = enemy.actor.getAnimControl("die")
            if deathAnimControl is None or not deathAnimControl.isPlaying():
                enemy.cleanup()
            else:
                enemiesAnimatingDeaths.append(enemy)
        self.deadEnemies = enemiesAnimatingDeaths

        # Make the game more difficult over time!
        self.difficultyTimer -= dt
        if self.difficultyTimer <= 0:
            self.difficultyTimer = self.difficultyInterval
            if self.maxEnemies < self.maximumMaxEnemies:
                self.maxEnemies += 1
            if self.spawnInterval > self.minimumSpawnInterval:
                self.spawnInterval -= 0.1
```

And now we have something like a real game! Enemies spawn and attack us! Traps destroy player-character and enemy alike! We can even gain points for each enemy defeated! And when at last we fall to the endless horde, play stops!

![Panda-chan runs, shoots, is chased, and springs traps!](../images/tutStartOfAGame.gif "So much moving stuff!")

It... is all a bit quiet, however, isn't it? Perhaps some sound and music would help...

[On to Lesson 14][next]

[next]: tut_lesson14.html
