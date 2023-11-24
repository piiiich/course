"""
    Airport and flights visualization.
    This module allows the visualization of an airport and its flights
    on a scalable graphics view
"""

from PyQt5.QtCore import QCoreApplication, QRectF, Qt, pyqtSignal
from PyQt5.QtGui import QBrush, QColor, QKeySequence, QPainterPath, QPen
from PyQt5.QtWidgets import (QGraphicsEllipseItem, QGraphicsItemGroup,
                             QGraphicsLineItem, QGraphicsPathItem,
                             QGraphicsRectItem, QGraphicsScene, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QShortcut,
                             QSlider, QVBoxLayout, QWidget)

import circuit
import traffic
from pan_zoom_view import PanZoomView
from time_manager import TimeManager

# Constants
WIDTH = 800           # Initial window width (pixels)
HEIGHT = 450          # Initial window height (pixels)

# Color constants (SVG color keyword names as defined by w3c
# https://www.w3.org/TR/SVG/types.html#ColorKeywords)
CIR_COLOR = "darkgrey"   # Airport elements color
DEP_COLOR = "red"  # Stands color

# Brushes
DEP_BRUSH = QBrush(QColor(DEP_COLOR))


class RadarView(QWidget):
    """ An interactive view of a circuit and its racers """

    def __init__(self, simu):
        super().__init__()

        #### Simulation data and control
        self.simulation = simu
        # Create and setup the time manager in charge of running the simulation
        self.time_manager = TimeManager(self.simulation)

        #### RadarView global settings
        # Settings
        self.setWindowTitle('Race in ' + self.simulation.airport.name)
        self.resize(WIDTH, HEIGHT)

        # Create the root layout allowing to align the RadarView children vertically
        root_layout = QVBoxLayout(self)

        #### Airport and aircraft
        # Create the scene that holds the airport and aircraft items
        self.scene = QGraphicsScene()

        # Create the view that displays the scene
        self.view = PanZoomView(self.scene)
        # Invert y axis for the view
        # (oriented upwards in the real world and downwards in the Qt coordinate system)
        self.view.scale(1, -1)

        # Airport items
        self.add_airport_items()          # Create airport items and add them to the graphic scene
        self.view.fit_scene_in_view()     # Make the scene fit in the view
        root_layout.addWidget(self.view)  # Add the view to the root layout

        #### Toolbar
        # (allows the user to control the simulation playback)
        toolbar = self.create_toolbar()
        root_layout.addLayout(toolbar)

        # Ask time manager to send all its signals in order to initialize the values of the widgets
        # connected to it (convenience method to avoid having to initialize them one by one)
        self.time_manager.send_initialization_signals()

        #### Show this widget
        self.show()

    def create_toolbar(self):
        """ Create the toolbar """
        #### Toolbar (a horizontal layout to hold time controls)
        toolbar = QHBoxLayout()

        #### Buttons
        # Factor the creation of buttons in a nested function
        def add_button(text, slot):
            button = QPushButton(text)    # Create and setup the button
            toolbar.addWidget(button)     # Add it to its parent
            button.clicked.connect(slot)  # Connect the button's clicked signal to the slot

        # Add buttons to toolbar
        # (using lambda function allows to pass extra arguments to slots)
        add_button('-', lambda: self.view.zoom_view(1/1.1))
        add_button('+', lambda: self.view.zoom_view(1.1))
        toolbar.addStretch()
        add_button('<<', lambda: self.time_manager.set_time_increment(-5))
        add_button(' <', lambda: self.time_manager.set_time_increment(-1))
        add_button('|>', self.time_manager.play_pause)
        add_button(' >', lambda: self.time_manager.set_time_increment(1))
        add_button('>>', lambda: self.time_manager.set_time_increment(5))

        #### Time entry
        # Add a QLineEdit to display simulation's time and let the user change it at will
        time_entry = QLineEdit()
        toolbar.addWidget(time_entry)
        time_entry.setInputMask("00:00:00")

        # Slot to react to user's entries on the time entry widget
        def on_time_entry_change():
            # Modify time in time manager according to the user's input
            self.time_manager.set_time(traffic.time_step(time_entry.text()))
            time_entry.clearFocus()

        # Connect the QLineEdit's editingFinished signal to slot
        time_entry.editingFinished.connect(on_time_entry_change)

        # Conversely, react to time changes in time manager:
        # change the value displayed by the time entry
        self.time_manager.time_changed.connect(lambda int_val: time_entry.setText(traffic.hms(int_val)))

        #### Shortcuts
        # Factor the creation of shotcuts in a nested function
        def add_shortcut(text, slot):
            shortcut = QShortcut(QKeySequence(text), self)
            shortcut.activated.connect(slot)

        # Add shortcuts
        add_shortcut('-', lambda: self.view.zoom_view(1/1.1))
        add_shortcut('+', lambda: self.view.zoom_view(1.1))
        add_shortcut(' ', self.time_manager.play_pause)
        add_shortcut('q', QCoreApplication.instance().quit)

        ##### [TP1]
        # Create a slider to let the user change the simulation time increment
        speed_sld = QSlider(Qt.Horizontal)
        speed_sld.setMinimum(-5)
        speed_sld.setMaximum(5)

        # React to slider's value changes: modify simulation's time increment in the time manager
        speed_sld.valueChanged.connect(self.time_manager.set_time_increment)

        # Conversely, react to time increment changes in time manager:
        # change the value displayed by the slider
        self.time_manager.time_increment_changed.connect(speed_sld.setValue)

        # Create labels to display the slider's description and value
        descr_lbl = QLabel("Speed")
        value_lbl = QLabel()
        value_lbl.setFixedWidth(25)

        # React to time increment changes in time manager:
        # change the value displayed by the label
        self.time_manager.time_increment_changed.connect(lambda int_val: value_lbl.setText(str(int_val)))

        # Add slider and labels to toolbar
        toolbar.addStretch()
        toolbar.addWidget(descr_lbl)
        toolbar.addWidget(speed_sld)
        toolbar.addWidget(value_lbl)

        return toolbar

    def add_airport_items(self):
        """ Add the airport (as a group) to the QGraphicsScene, drawn by the QGraphicsView """
        # Create a group to hold all the airport items, add it to the scene
        # and make sure it is drawn in background
        airport_group = QGraphicsItemGroup()
        self.scene.addItem(airport_group)

        # Taxiways
        pen = QPen(QColor(CIR_COLOR), circuit.LINE_WIDTH)
        pen.setCapStyle(Qt.RoundCap)
        for ext_line in self.simulation.circuit.ext_lines:
            path = QPainterPath()
            path.moveTo(ext_line.coords[0].x, ext_line.coords[0].y)
            for xy in ext_line.coords[1:]:
                path.lineTo(xy.x, xy.y)
            item = QGraphicsPathItem(path, airport_group)
            item.setPen(pen)
            item.setToolTip('Ext_line ' + ext_line.taxi_name)

        # Runways
        pen = QPen(QColor(CIR_COLOR), circuit.LINE_WIDTH)
        for int_line in self.simulation.circuit.int_lines:
            (p1, p2) = int_line.coords
            item = QGraphicsLineItem(p1.x, p1.y, p2.x, p2.y, airport_group)
            item.setPen(pen)
            item.setToolTip('Int_line ' + int_line.name)
