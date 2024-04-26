from PIL import Image


table = Image.open("assets/images/table.png")
WIDTH, HEIGHT = table.size
BOTTOM_PANEL = 50
FPS = 120

POCKETS = [
    (55, 63), 
    (592, 48), 
    (1134, 64), 
    (55, 616), 
    (592, 629), 
    (1134, 616)
]

CUSHIONS = [
    [(88, 56), (109, 77), (555, 77), (564, 56)],
    [(621, 56), (630, 77), (1081, 77), (1102, 56)],
    [(89, 621), (110, 600), (556, 600), (564, 621)],
    [(622, 621), (630, 600), (1081, 600), (1102, 621)],
    [(56, 96), (77, 117), (77, 560), (56, 581)],
    [(1143, 96), (1122, 117), (1122, 560), (1143, 581)],
]

IMPULSE_DIRECTION = (-1500, 0)

CUE_LINE_WIDTH = 5

POCKET_RADIUS = 33
BALL_RADIUS = 18
BALL_MASS = 5

ELASTICITY = 0.8
MAX_BIAS = 0
MAX_FORCE = 10000
