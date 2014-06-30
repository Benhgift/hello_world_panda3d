'''
  A game using panda 3d
'''
import pdb
from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import ClockObject
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from direct.showbase.DirectObject import DirectObject
from panda3d.core import Point3

class FrogActor(Actor):
    def __init__(self, x, y, z, scale, clock, parent=None, name=""):
        self.clock = clock
        self.speed = 180
        # Load
        super(FrogActor, self).__init__("frog")
        # attach to parent
        if parent:
            self.reparentTo(parent)
        # scale
        self.setScale(scale, scale, scale)
        # Loop its animation.
        #if not z: frogActor.loop("walk")

        # Create the four lerp intervals needed for the frog to
        # walk back and forth.
        frogPosInterval1 = self.posInterval(2,
                                                        Point3(0+x, -10+y, 0+z),
                                                        startPos=Point3(0+x, 10+y, 0+z))
        frogPosInterval2 = self.posInterval(2,
                                                        Point3(0+x, 10+y, 0+z),
                                                        startPos=Point3(0+x, -10+y, 0+z))
        # Hpr means turning.
        frogHprInterval1 = self.hprInterval(3,
                                                        Point3(180, 0, 0),
                                                        startHpr=Point3(0, 0, 0))
        frogHprInterval2 = self.hprInterval(3,
                                                        Point3(0, 0, 0),
                                                        startHpr=Point3(180, 0, 0))

        # Create and play the sequence that coordinates the intervals.
        if not name:
            name = hash(self)
        frogPace = Sequence(frogPosInterval1,
                                  frogHprInterval1,
                                  frogPosInterval2,
                                  frogHprInterval2,
                                  name="frogPace %s" % name)
        #frogPace.loop()
        self.setPos(x, y, z)

    def go_forward(self, time_dt):
        self.setPos(self, 0, -self.speed * globalClock.getDt(), 0)

    def go_backward(self, time_dt):
        self.setPos(self, 0, self.speed * globalClock.getDt(), 0)

    def turn_left(self, time_dt):
        self.setH(self.getH()+(self.speed * globalClock.getDt()))

    def turn_right(self, time_dt):
        self.setH(self.getH()-(self.speed * globalClock.getDt()))


class StartWorld(DirectObject):
    pass


class Game(ShowBase):
    #def _set_key(self, key, value):
        #self.key_map[key] = value

    def _make_keymap(self):
        return {"left":0, "right":0, "forward":0, "backward":0}

    def _setup_keys(self):
        self.accept('e', self.key_map.update, [{'forward': 1}])
        self.accept('e-up', self.key_map.update, [{'forward': 0}])
        self.accept('d', self.key_map.update, [{'backward': 1}])
        self.accept('d-up', self.key_map.update, [{'backward': 0}])
        self.accept('s', self.key_map.update, [{'left': 1}])
        self.accept('s-up', self.key_map.update, [{'left': 0}])
        self.accept('f', self.key_map.update, [{'right': 1}])
        self.accept('f-up', self.key_map.update, [{'right': 0}])

    def __init__(self):
        ShowBase.__init__(self)

        self.clock = ClockObject()

        # Disable the camera trackball controls.
        self.disableMouse()

        # Load the environment model.
        self.environ = self._set_up_environment()

        # Set up actors
        scale = .09 -.0008
        self.frogActor = FrogActor(0, 0, 0, scale, self.clock, self.render)
        self.frogActor1 = FrogActor(0, 0, 4, scale*.9, self.clock, self.render)
        self.frogActor2 = FrogActor(0, 0, 7, scale*.7, self.clock, self.render)

        self.inverse_turning = False

        # Add the _follow_player procedure to the task manager.
        self.taskMgr.add(self._follow_player, "_follow_player")
        self.taskMgr.add(self._go_forward, "_go_f")

        # set up keys
        self.key_map = self._make_keymap()
        self._setup_keys()

    def _go_forward(self, task):
        if self.key_map['forward']:
            self.frogActor.go_forward(task.time)
            self.inverse_turning = False
        if self.key_map['backward']:
            self.frogActor.go_backward(task.time)
            self.inverse_turning = True
        if self.key_map['left']:
            if self.inverse_turning:
                self.frogActor.turn_right(task.time)
            else:
                self.frogActor.turn_left(task.time)
        if self.key_map['right']:
            if self.inverse_turning:
                self.frogActor.turn_left(task.time)
            else:
                self.frogActor.turn_right(task.time)
        return Task.cont

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
        self.camera.reparentTo(self.frogActor)
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

app = Game()
app.run()
