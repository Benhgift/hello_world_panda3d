'''
  A game using panda 3d
'''
from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3

class MyApp(ShowBase):
    def loadapanda(self, x=0, y=0, z=0):
        # Load and transform the panda actor.
        pandaActor = Actor("frog")#"models/panda-model")
                               # {"walk": "models/panda-walk4"})
        pandaActor.setScale(0.09-(z*.0008), 0.09-(z*.0008), 0.09-(z*.0008))
        pandaActor.reparentTo(self.render)
        # Loop its animation.
        #if not z: pandaActor.loop("walk")

        # Create the four lerp intervals needed for the panda to
        # walk back and forth.
        pandaPosInterval1 = pandaActor.posInterval(13,
                                                        Point3(0+x, -10+y, 0+z),
                                                        startPos=Point3(0+x, 10+y, 0+z))
        pandaPosInterval2 = pandaActor.posInterval(13,
                                                        Point3(0+x, 10+y, 0+z),
                                                        startPos=Point3(0+x, -10+y, 0+z))
        pandaHprInterval1 = pandaActor.hprInterval(3,
                                                        Point3(180, 0, 0),
                                                        startHpr=Point3(0, 0, 0))
        pandaHprInterval2 = pandaActor.hprInterval(3,
                                                        Point3(0, 0, 0),
                                                        startHpr=Point3(180, 0, 0))

        # Create and play the sequence that coordinates the intervals.
        pandaPace = Sequence(pandaPosInterval1,
                                  pandaHprInterval1,
                                  pandaPosInterval2,
                                  pandaHprInterval2,
                                  name="pandaPace %s" % z)
        pandaPace.loop()
        return pandaActor

    def __init__(self):
        ShowBase.__init__(self)

        # Disable the camera trackball controls.
        self.disableMouse()

        # Load the environment model.
        self.environ = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        self.environ.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.environ.setScale(0.25, 0.25, 0.25)
        self.environ.setPos(-8, 42, 0)

        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        self.pandaActor = self.loadapanda()
        self.pandaActor2 = self.loadapanda(0,0,4)
        self.pandaActor3 = self.loadapanda(0,0,7)

    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 89.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(40 * sin(angleRadians), -40.0 * cos(angleRadians), 18)
        self.camera.setHpr(angleDegrees, -20, 0)
        return Task.cont

app = MyApp()
app.run()
