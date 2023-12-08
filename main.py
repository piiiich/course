from PyQt5.QtWidgets import QApplication
from geometry import Point, Polygon
from view import PolygonApp
import sys

def main():
    # Example list of points
    points = [Point(50, 50), Point(150, 50), Point(150, 150), Point(50, 150)]

    # Create a Polygon object
    polygon = Polygon(points)

    app = QApplication(sys.argv)
    ex = PolygonApp(polygon)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
