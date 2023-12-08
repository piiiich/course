import geometry as geo

def main():
    # Example list of points
    points = [geo.Point(50, 50), geo.Point(150, 50), geo.Point(150, 150), geo.Point(50, 150)]

    # Create a Polygon object
    polygon = geo.Polygon(points)

if __name__ == '__main__':
    main()