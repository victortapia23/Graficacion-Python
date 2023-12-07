import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import random

# Define constants for the top-level container
TITLE = "Plantilla Base python OpenGL"  # window's title
CANVAS_WIDTH = 640  # width of the drawable
CANVAS_HEIGHT = 480  # height of the drawable
FPS = 24  # animator's target frames per second
factInc = 5.0  # animator's target frames per second
fovy = 45.0

rotacion = 0.0
despX = 0.0
despY = 0.0
despZ = 0.0

camX = 2.0
camY = 2.0
camZ = 8.0


def display():
    global rotacion, despX, despY, despZ, camX, camY, camZ

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovy, CANVAS_WIDTH / CANVAS_HEIGHT, 0.1, 20.0)
    gluLookAt(camX, camY, camZ, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glColor3f(0.0, 0.0, 1.0)

    glBegin(GL_LINES)
    glVertex3f(-100.0, 0.0, 0.0)
    glVertex3f(100.0, 0.0, 0.0)
    glEnd()

    glBegin(GL_LINES)
    glVertex3f(0.0, -100.0, 0.0)
    glVertex3f(0.0, 100.0, 0.0)
    glEnd()

    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, -100.0)
    glVertex3f(0.0, 0.0, 100.0)
    glEnd()

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    num_points = 5  # Number of control points

    puntosControl = []
    for _ in range(num_points):
        x = random.uniform(-1.0, 1.0)
        y = random.uniform(-1.0, 1.0)
        z = random.uniform(-1.0, 1.0)
        puntosControl.extend([x, y, z])

    glTranslatef(2.0, 2.0, -1.0)
    glBegin(GL_QUADS)
    glColor3f(0.0, 1.0, 0.0)

    num_segments = 100
    delta_t = 1.0 / num_segments

    for i in range(num_segments):
        t1 = i * delta_t
        t2 = (i + 1) * delta_t

        for j in range(num_points - 3):
            p0 = puntosControl[j * 3: j * 3 + 3]
            p1 = puntosControl[(j + 1) * 3: (j + 1) * 3 + 3]
            p2 = puntosControl[(j + 2) * 3: (j + 2) * 3 + 3]
            p3 = puntosControl[(j + 3) * 3: (j + 3) * 3 + 3]

            for t in np.arange(t1, t2, 0.01):
                x = ((1 - t) ** 3) * p0[0] + (3 * (1 - t) ** 2 * t) * p1[0] + (3 * (1 - t) * t ** 2) * p2[0] + (
                            t ** 3) * p3[0]
                y = ((1 - t) ** 3) * p0[1] + (3 * (1 - t) ** 2 * t) * p1[1] + (3 * (1 - t) * t ** 2) * p2[1] + (
                            t ** 3) * p3[1]
                z = ((1 - t) ** 3) * p0[2] + (3 * (1 - t) ** 2 * t) * p1[2] + (3 * (1 - t) * t ** 2) * p2[2] + (
                            t ** 3) * p3[2]

                glVertex3f(x, y, z)

    glEnd()

    rotacion += 5.0
    if rotacion > 360:
        rotacion = 0

    glFlush()


def reshape(window, width, height):
    glViewport(0, 0, width, height)

    if height == 0:
        height = 1

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovy, width / float(height), 0.1, 20.0)

    glMatrixMode(GL_MODELVIEW)


def key_callback(window, key, scancode, action, mods):
    global despX, despY, despZ, rotacion, camX, camY, camZ

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_LEFT:
            despX -= 0.2
        elif key == glfw.KEY_RIGHT:
            despX += 0.2
        elif key == glfw.KEY_DOWN:
            despZ += 0.2
        elif key == glfw.KEY_UP:
            despZ -= 0.2
        elif key == glfw.KEY_PAGE_UP:
            despY += 0.2
        elif key == glfw.KEY_PAGE_DOWN:
            despY -= 0.2
        elif key == glfw.KEY_R:
            rotacion += 5.0
        elif key == glfw.KEY_KP_8:
            camY += 0.2
        elif key == glfw.KEY_KP_2:
            camY -= 0.2
        elif key == glfw.KEY_KP_6:
            camX += 0.2
        elif key == glfw.KEY_KP_4:
            camX -= 0.2
        elif key == glfw.KEY_KP_0:
            camZ += 0.2
        elif key == glfw.KEY_KP_9:
            camZ -= 0.2

        print("despX = {}, despY = {}, despZ = {}".format(despX, despY, despZ))
        print("camX = {}, camY = {}, camZ = {}".format(camX, camY, camZ))


def init():
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)


def main():
    if not glfw.init():
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)

    window = glfw.create_window(CANVAS_WIDTH, CANVAS_HEIGHT, TITLE, None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    init()

    while not glfw.window_should_close(window):
        display()
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
