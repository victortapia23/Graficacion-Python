import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

vertices = [
    [-0.5, -0.5, -0.5],
    [0.5, -0.5, -0.5],
    [0.5, 0.5, -0.5],
    [-0.5, 0.5, -0.5],
    [-0.5, -0.5, 0.5],
    [0.5, -0.5, 0.5],
    [0.5, 0.5, 0.5],
    [-0.5, 0.5, 0.5]
]

edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

rotacion_x = 0.0
rotacion_y = 0.0


def main():
    if not glfw.init():
        return

    window = glfw.create_window(640, 480, "OpenGL Window", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    reshape(window, 640, 480)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        display()
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


def key_callback(window, key, scancode, action, mods):
    global rotacion_x, rotacion_y

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)
    elif key == glfw.KEY_R and action == glfw.PRESS:
        rotacion_x += 5.0
    elif key == glfw.KEY_P and action == glfw.PRESS:
        rotacion_y += 5.0


def display():
    global rotacion_x, rotacion_y

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    gluLookAt(2.0, 2.0, 6.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    glRotatef(rotacion_x, 1.0, 0.0, 0.0)
    glRotatef(rotacion_y, 0.0, 1.0, 0.0)

    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

    glFlush()


def reshape(window, width, height):
    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, width / height, 0.1, 10.0)


if __name__ == '__main__':
    main()