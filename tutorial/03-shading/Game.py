#####################################################
#                                                   #
# Original code copyright (c) 2019 Ian Eborn.       #
# http://thaumaturge-art.com                        #
#                                                   #
# Licensed under the MIT license.                   #
# See "FinalGame/codeLicense".txt, or               #
# https://opensource.org/licenses/MIT               #
#                                                   #
#####################################################

from direct.showbase.ShowBase import ShowBase

from direct.actor.Actor import Actor
from panda3d.core import Spotlight, AmbientLight, DirectionalLight
from panda3d.core import Vec4
from panda3d.core import WindowProperties

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()

        properties = WindowProperties()
        properties.setSize(1000, 750)
        self.win.requestProperties(properties)

        mainLight = DirectionalLight("main light")
        self.mainLightNodePath = render.attachNewNode(mainLight)
        self.mainLightNodePath.setHpr(45, -45, 0)
        render.setLight(self.mainLightNodePath)

        ambientLight = AmbientLight("ambient light")
        ambientLight.setColor(Vec4(0.2, 0.2, 0.2, 1))
        self.ambientLightNodePath = render.attachNewNode(ambientLight)
        render.setLight(self.ambientLightNodePath)

        render.setShaderAuto()

        self.environment = loader.loadModel("Models/Misc/environment")
        self.environment.reparentTo(render)

        self.tempActor = Actor("Models/PandaChan/act_p3d_chan", {"walk" : "Models/PandaChan/a_p3d_chan_run"})
        self.tempActor.getChild(0).setH(180)
        self.tempActor.reparentTo(render)
        self.tempActor.loop("walk")

        self.camera.setPos(0, 0, 32)
        self.camera.setP(-90)

game = Game()
game.run()
