'''
  A game using panda 3d
'''
from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3

class FrogActor(Actor):
    def __init__(self, x, y, z, scale, name=""):
        # Load and transform the panda actor.
        super(self, "frog")
        pandaActor.setScale(scale, scale, scale)
        # Loop its animation.
        #if not z: pandaActor.loop("walk")

        # Create the four lerp intervals needed for the panda to
        # walk back and forth.
        pandaPosInterval1 = pandaActor.posInterval(2,
                                                        Point3(0+x, -10+y, 0+z),
                                                        startPos=Point3(0+x, 10+y, 0+z))
        pandaPosInterval2 = pandaActor.posInterval(2,
                                                        Point3(0+x, 10+y, 0+z),
                                                        startPos=Point3(0+x, -10+y, 0+z))
        # Hpr means turning. 
        pandaHprInterval1 = pandaActor.hprInterval(3,
                                                        Point3(180, 0, 0),
                                                        startHpr=Point3(0, 0, 0))
        pandaHprInterval2 = pandaActor.hprInterval(3,
                                                        Point3(0, 0, 0),
                                                        startHpr=Point3(180, 0, 0))

        # Create and play the sequence that coordinates the intervals.
        if not name:
            name = hash(self)
        pandaPace = Sequence(pandaPosInterval1,
                                  pandaHprInterval1,
                                  pandaPosInterval2,
                                  pandaHprInterval2,
                                  name="pandaPace %s" % name)
        pandaPace.loop()
        

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # Disable the camera trackball controls.
        self.disableMouse()

        # Load the environment model.
        self.environ = self._set_up_environment()

        # Set up actors
        scale = .09 -.0008
        self.frogActor = FrogActor(0, 0, 0, scale)
        frogActor.reparentTo(self.render)
        self.frogActor = FrogActor(0, 0, 0, scale)
        frogActor.reparentTo(self.render)
        self.pandaActor2 = self.loadapanda(0,0,4)
        self.pandaActor3 = self.loadapanda(0,0,7)

        # Add the _follow_player procedure to the task manager.
        self.taskMgr.add(self._follow_player, "_follow_player")

    def _set_up_environment(self):
        # Set up the environment model.
        environ = self.loader.loadModel("models/environment")

        # Reparent the model to render.
        environ.reparentTo(self.render)

        # Apply scale and position transforms on the model.
        environ.setScale(0.25, 0.25, 0.25)
        environ.setPos(-8, 42, 0)
        return environ

    def _follow_player(self, task):
        self.camera.reparentTo(self.pandaActor)
        self.camera.setPos(-20,190,150)
        self.camera.setHpr(180, -20, 0)
        #self.camera.setPos(self.pandaActor.getX()-40, self.pandaActor.getY()-40, 50)
        #self.camera.lookAt(self.pandaActor)
        return Task.cont

    # Define a procedure to move the camera.
    def _spinCameraTask(self, task):
        angleDegrees = task.time * 89.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(40 * sin(angleRadians), -40.0 * cos(angleRadians), 18)
        self.camera.setHpr(angleDegrees, -20, 0)
        return Task.cont

app = MyApp()
app.run()
