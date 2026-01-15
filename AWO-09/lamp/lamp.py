import math
import cmath
import random
import os.path
import subprocess
import errno
import re
from enum import Enum
import xml.etree.ElementTree as ET
import svg.path

class Plane(Enum):
    FILTER = 0
    APERTURE = 1
    SCREEN = 2

class Mode(Enum):
    NONE = 0
    APERTURE = 1
    FILTER = 2
    BOTH = 3

def line_circle_intersection(line_start, line_end, circle_center, radius):
    # Extract the coordinates from the complex numbers
    x1, y1 = line_start.real, line_start.imag
    x2, y2 = line_end.real, line_end.imag
    cx, cy = circle_center.real, circle_center.imag

    # Compute the direction vector of the line
    dx, dy = x2 - x1, y2 - y1

    # Compute the coefficients of the quadratic equation (a*t^2 + b*t + c = 0)
    a = dx ** 2 + dy ** 2
    b = 2 * (dx * (x1 - cx) + dy * (y1 - cy))
    c = (x1 - cx) ** 2 + (y1 - cy) ** 2 - radius ** 2

    # Compute the discriminant
    discriminant = b ** 2 - 4 * a * c

    # Check the number of solutions based on the discriminant
    pos = []
    if discriminant < 0:
        # No intersection
        pass
    elif discriminant == 0:
        # One solution (tangent)
        pos.append(-b / (2 * a))
    else:
        # Two solutions (normal intersection)
        sqrt_discriminant = math.sqrt(discriminant)
        pos.append((-b + sqrt_discriminant) / (2 * a))
        pos.append((-b - sqrt_discriminant) / (2 * a))

    # Calculate intersection points
    intersect = []
    for t in pos:
        #if t >= 0 and t <= 1:
        intersect_x = x1 + t * dx
        intersect_y = y1 + t * dy
        intersect.append(complex(intersect_x, intersect_y))
    return intersect

class Style(object):
    """ Class for the style attribute of a SVG element. """

    def __init__(self, style, parent=None):

        """ Parse style string into a dictionary. """

        # Parse style string
        if style == None:
            style = {}
        else:
            style = dict([x.split(":") for x in style.split(";") if x.strip()])

        # Merge style with parent style
        if parent != None:
            style = parent.combine(style)
        self._style = style

    def __str__(self):

        """ Construct style string. """

        return ";".join(["%s:%s" % x for x in self._style.items()])

    def keys(self):

        return self._style.keys()

    def __getitem__(self, key):

        """ Get value of style attribute. """

        if key in self._style:
            return self._style[key]
        return None
        # raise KeyError("Unknown style key %s" % key)

    def __setitem__(self, key, value):

        """ Set value of style attribute. """

        self._style[key] = str(value)

    def combine(self, style):

        """ Add missing style items to child style. """

        for key in self._style:
            if key not in style:
                style[key] = self._style[key]
        return style


RE_SCALE = r"^scale\((.+)\)$"
RE_ROTATE = r"^rotate\((.+)\)$"
RE_TRANSLATE = r"^translate\((.+)\)$"
RE_MATRIX = r"^matrix\((.+)\)$"


class Transform(object):
    """ Class for the transform attribute of a SVG element. """

    def __init__(self, transform, parent=None):

        """ Parse transform string. """

        # Identity transform
        if transform is None:
            matrix = [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]

        # Matrix as list
        elif isinstance(transform, list):
            assert len(transform) == 6
            matrix = transform

        # Scaling transform
        elif "scale" in transform:
            m = re.match(RE_SCALE, transform)
            s = m.group(1)
            if "," in s:
                try:
                    sx, sy = [float(x) for x in s.split(",", 1)]
                except:
                    raise ValueError("Unknown transform definition %s" % transform)
                matrix = [sx, 0.0, 0.0, sy, 0.0, 0.0]
            else:
                try:
                    s = float(s)
                except:
                    raise ValueError("Unknown transform definition %s" % transform)
                matrix = [s, 0.0, 0.0, s, 0.0, 0.0]

        # Rotating transform
        elif "rotate" in transform:
            m = re.match(RE_ROTATE, transform)
            a = m.group(1)
            if "," in a:
                try:
                    a, cx, cy = [float(x) for x in a.split(",", 2)]
                except:
                    raise ValueError("Unknown transform definition %s" % transform)
                matrix = [math.cos(a), math.sin(a), -math.sin(a), math.cos(a),
                          cx * (1 - math.cos(a)) + cy * math.sin(a),
                          cy * (1 - math.cos(a)) - cx * math.sin(a)]
            else:
                try:
                    a = math.radians(float(a))
                except:
                    raise ValueError("Unknown transform definition %s" % transform)
                matrix = [math.cos(a), math.sin(a), -math.sin(a), math.cos(a), 0, 0]

        # Translating transform
        elif "translate" in transform:
            m = re.match(RE_TRANSLATE, transform)
            t = m.group(1)
            if "," in t:
                try:
                    tx, ty = [float(x) for x in t.split(",", 1)]
                except:
                    raise ValueError("Unknown transform definition %s" % transform)
                matrix = [1.0, 0.0, 0.0, 1.0, tx, ty]
            else:
                try:
                    t = float(t)
                except:
                    raise ValueError("Unknown transform definition %s" % transform)
                matrix = [1.0, 0.0, 0.0, 1.0, t, 0.0]

        # Matrix transform
        elif "matrix" in transform:
            m = re.match(RE_MATRIX, transform)
            try:
                matrix = [float(x) for x in m.group(1).split(",", 5)]
            except:
                raise ValueError("Unknown transform definition %s" % transform)

        # Unknown transform
        else:
            raise ValueError("Unknown transform definition %s" % transform)

        # Apply parent transformation and store combined matrix
        if parent is not None:
            matrix = parent.combine(matrix)
        self._matrix = matrix

        # Build inverse transform
        a, b, c, d, dx, dy = self._matrix
        det = a * d - b * c
        self._invmatrix = [d / det, -b / det, -c / det, a / det, dx, dy]

    def __str__(self):

        """ Construct transform string. """

        return "matrix(%g,%g,%g,%g,%g,%g)" % tuple(self._matrix)

    def combine(self, child):

        """ Expand given child matrix to include this parent
        transformation. """

        # Pick elements from child and parent matrices
        if isinstance(child, Transform):
            child = child._matrix
        a_c, b_c, c_c, d_c, dx_c, dy_c = child
        a_p, b_p, c_p, d_p, dx_p, dy_p = self._matrix

        # Calculate combined transformation matrix
        # A = A_c*A_p
        # b = A_c*b_p + b_c
        # Transform: Ax + b -> x
        a = a_c * a_p + b_c * c_p
        b = a_c * b_p + b_c * d_p
        c = c_c * a_p + d_c * c_p
        d = c_c * b_p + d_c * d_p
        dx = a_c * dx_p + b_c * dy_p + dx_c
        dy = c_c * dx_p + d_c * dy_p + dy_c

        # Return combined matrix
        return [a, b, c, d, dx, dy]

    def calc(self, point):

        """ Transform single or multiple points (complex numbers) and/or
        widths (real numbers). """

        # Transform tuple of points or widths
        if type(point) == type(()):
            return tuple(self.calc(x) for x in point)

        # Transform list of points or widths
        if type(point) == type([]):
            return list(self.calc(x) for x in point)

        # Transform point
        if type(point) == type(1j):
            a, b, c, d, dx, dy = self._matrix
            x = a * point.real + b * point.imag + dx
            y = c * point.real + d * point.imag + dy
            return x + 1j * y

        # Transform width
        a, b, c, d, dx, dy = self._matrix
        scale = 0.5 * (math.sqrt(a * a + c * c) + math.sqrt(b * b + d * d))
        return point * scale

    def inv_calc(self, point):

        """ Inverse transform single or multiple points (complex numbers)
        and/or widths (real numbers). """

        # Inverse transform tuple of points or widths
        if type(point) == type(()):
            return tuple(self.invcalc(x) for x in point)

        # Inverse transform list of points or widths
        if type(point) == type([]):
            return list(self.invcalc(x) for x in point)

        # Inverse transform point
        if type(point) == type(1j):
            a, b, c, d, dx, dy = self._invmatrix
            x = a * (point.real - dx) + b * (point.imag - dy)
            y = c * (point.real - dx) + d * (point.imag - dy)
            return x + 1j * y

        # Inverse transform width
        a, b, c, d, dx, dy = self._matrix
        scale = 0.5 * (math.sqrt(a * a + c * c) + math.sqrt(b * b + d * d))
        return point / scale

    def inverse(self):

        a, b, c, d, dx, dy = self._matrix
        det = a * d - b * c
        matrix = [d / det, -b / det, -c / det, a / det, (-d * dx + b * dy) / det, (c * dx - a * dy) / det]
        return Transform(matrix)

class PathDraw(object):
    """ Class for the d attribute of a SVG path element. """

    def __init__(self, draw):

        """ Parse d string. """

        self._draw = draw
        self._svgpath = svg.path.parse_path(draw)
        self._lengths = None

    def __str__(self):

        """ Construct d string. """

        if self._svgpath:
            return self._svgpath.d()
        return self._draw

    def __len__(self):

        """ Return number of path elements. """

        return len(self._svgpath)

    def length(self, error=None):

        """ Return approximate length of the path. """

        if self._lengths == None:
            self._lengths = [x.length(error) for x in self._svgpath]
        return sum(self._lengths)

class Path(object):

    def __init__(self, ns, path, style=None, transform=None, id=None):

        # Store namespace
        self.ns = ns

        # Store XML path element
        self._path = path
        if id:
            self.id = id
        else:
            self.id = self._path.attrib["id"]

        # Parse style attribute
        self.parent_style = style
        self.mystyle = path.get("style")
        self._style = Style(self.mystyle, self.parent_style)

        # Build transformation based on parents
        self.parent_transform = transform
        self.mytransform = path.get("transform")
        self._transform = Transform(self.mytransform, self.parent_transform)

        # Parse SVG path
        self._draw = PathDraw(path.attrib["d"])

        # Set stroke attributes
        self.stroke_width = self.transform(float(self._style["stroke-width"]))
        self.has_stroke = self._style["stroke"] != "none" and self.stroke_width > 0.0

    def transform(self, point):

        """ Transform single or multiple points (complex numbers) and/or
        widths (real numbers). """

        return self._transform.calc(point)

    def inv_transform(self, point):

        """ Inverse transform single or multiple points (complex
        numbers) and/or widths (real numbers). """

        return self._transform.inv_calc(point)

    def __len__(self):

        """ Return number of path elements. """

        return len(self._draw)

    def length(self, error=None):

        """ Return scaled approximate length of the path. """

        if error != None:
            error = self.inv_transform(error)
        return self.transform(self._draw.length(error))

class Arc(Path):

    def __init__(self, ns, path, style=None, transform=None, id=None, **kwargs):

        # Duplicate arc object
        if isinstance(path, Arc):
            arc = path
            path = path._path
            style = arc.parent_style
            transform = arc.parent_transform
            super(Arc, self).__init__(ns, path, style, transform, id)

            self.type = kwargs.get("type") or arc.type
            self.arctype = kwargs.get("arctype") or arc.arctype
            self.start = kwargs.get("start") or arc.start
            self.end = kwargs.get("end") or arc.end
            self.cx = kwargs.get("cx") or arc.cx
            self.cy = kwargs.get("cy") or arc.cy
            self.rx = kwargs.get("rx") or arc.rx
            self.ry = kwargs.get("ry") or arc.ry
            self.open = kwargs.get("open") or arc.open
            if "radius" in kwargs:
                self.rx = self.ry = kwargs["radius"]

        else:
            super(Arc, self).__init__(ns, path, style, transform, id)

            sodipodi = f"{{{self.ns['sodipodi']}}}"
            self.type = self._path.attrib[f"{sodipodi}type"]
            self.arctype = self._path.attrib[f"{sodipodi}arc-type"]
            self.start = kwargs.get("start") or float(self._path.attrib[f"{sodipodi}start"])
            self.end = kwargs.get("end") or float(self._path.attrib[f"{sodipodi}end"])
            self.cx = kwargs.get("cx") or float(self._path.attrib[f"{sodipodi}cx"])
            self.cy = kwargs.get("cy") or float(self._path.attrib[f"{sodipodi}cy"])
            self.rx = kwargs.get("rx") or float(self._path.attrib[f"{sodipodi}rx"])
            self.ry = kwargs.get("ry") or float(self._path.attrib[f"{sodipodi}ry"])
            if f"{sodipodi}open" in self._path.attrib:
                self.open = self._path.attrib[f"{sodipodi}open"]
            else:
                self.open = None
            if "radius" in kwargs:
                self.rx = self.ry = kwargs["radius"]

        assert self.open == "true"
        assert self.arctype == "arc"
        assert abs(self.rx - self.ry) <= 1e-7

        self._draw = PathDraw(self.draw())

    def attrib(self):

        myattrib = {
            "id": self.id,
            "inkscape:label": self.id,
            "sodipodi:type": self.type,
            "sodipodi:arc-type": self.arctype,
            "sodipodi:start": f"{self.start:.6g}",
            "sodipodi:end": f"{self.end:.6g}",
            "sodipodi:cx": f"{self.cx:.6g}",
            "sodipodi:cy": f"{self.cy:.6g}",
            "sodipodi:rx": f"{self.rx:.6g}",
            "sodipodi:ry": f"{self.ry:.6g}",
            "d": self.draw(),
        }
        if self.mystyle:
            myattrib["style"] = self.mystyle
        if self.open:
            myattrib["sodipodi:open"] = self.open
        if self.mytransform:
            myattrib["transform"] = self.mytransform
        return myattrib

    def clip(self, lines):

        transform = self._transform.inverse()
        low_start = transform.calc(lines["low"][0])
        low_end = transform.calc(lines["low"][1])
        high_start = transform.calc(lines["high"][0])
        high_end = transform.calc(lines["high"][1])

        center = complex(self.cx, self.cy)
        radius = 0.5 * (self.rx + self.ry)

        angles = [cmath.phase(p - center) for p in line_circle_intersection(low_start, low_end, center, radius)] + [self.start]
        angles = [a + 2*math.pi if a < 0 else a for a in angles]
        self.start = max(angles)
        angles = [cmath.phase(p - center) for p in line_circle_intersection(high_start, high_end, center, radius)] + [self.end]
        angles = [a + 2*math.pi if a < 0 else a for a in angles]
        self.end = min(angles)

        self._draw = PathDraw(self.draw())

    def split(self, plane, lines):

        assert isinstance(plane, Plane)
        if plane == Plane.APERTURE:
            start, end = lines["aperture"]
        elif plane == Plane.FILTER:
            start, end = lines["filter"]
        elif plane == Plane.SCREEN:
            start, end = lines["screen"]
        else:
            raise ValueError("Plane must be either APERTURE, FILTER or SCREEN")

        center = complex(self.cx, self.cy)
        radius = 0.5 * (self.rx + self.ry)

        transform = self._transform.inverse()
        start = transform.calc(start)
        end = transform.calc(end)
        intersect = line_circle_intersection(start, end, center, radius)
        if len(intersect) <= 1:
            return [self]

        clip_start, clip_end = self.start, self.end
        if clip_start > clip_end:
            clip_start -= 2 * math.pi
        i = 0
        arcs = []
        start, end = sorted([cmath.phase(p - center) for p in intersect])
        if start > clip_start:
            arcs.append(Arc(self.ns, self, start=clip_start, end=start, id=f"{self.id}-{i}"))
            i += 1
        if end < clip_end:
            arcs.append(Arc(self.ns, self, start=end, end=clip_end, id=f"{self.id}-{i}"))
            i += 1
        return arcs

    def draw(self):

        r = 0.5 * (self.rx + self.ry)
        x0 = self.cx + r * math.cos(self.start)
        y0 = self.cy + r * math.sin(self.start)

        start = self.start
        end = self.end
        if end < start:
            end += 2 * math.pi
        num = math.ceil((end - start) / (0.5*math.pi))
        angle = [start + i * (end - start) / num for i in range(num+1)]
        x = [self.cx + r * math.cos(angle[i]) for i in range(num+1)]
        y = [self.cy + r * math.sin(angle[i]) for i in range(num+1)]

        d = f"m {x0:.6g},{y0:.6g}"
        for i in range(1, num+1):
            d += f" a {r:.6g},{r:.6g} 0 0,1 {x[i]-x[i-1]:.6g},{y[i]-y[i-1]:.6g}"
        return d

    def __str__(self):

        return f"Arc(arctype='{self.arctype}', radius=({self.rx}, {self.ry}), angles=({self.start*180/math.pi:.1f}°, {self.end*180/math.pi:.1f}°), center=({self.cx}, {self.cy}))"

class InkscapeFile(object):
    """ Class of inkscape SVG file. """

    def __init__(self, fn, step_sizes, mode):

        """ Parse inkscape SVG file. """

        # Store file name
        self.fn = fn
        print("Inkscape file %s" % fn)

        # Build XML namespace dictionary
        self.ns = dict([x for _, x in ET.iterparse(fn, events=["start-ns"])])
        for key, value in self.ns.items():
            ET.register_namespace(key, value)
            #print(f"Namespace item '{key}': {value}")

        # Build XML tree
        self.tree = ET.parse(fn)
        self.root = self.tree.getroot()

        # Determine standard unit
        self.std_unit = self.units()

        # Determine conversion factor from standard unit to pt
        self.pt_factor = {
            "cm": 72.0 / 2.54,
            "in": 72.0,
            "pt": 1.0,
            "pc": 12.0,
            "mm": 72.0 / 25.4,
            "px": None}[self.std_unit]

        assert isinstance(mode, Mode)
        self.mode = mode

        # Get bounding box
        self.get_lines()

        # Expand arc path elements
        assert(isinstance(step_sizes, dict))
        self.step_sizes = step_sizes
        self.expand_arcs()

    def __str__(self):

        """ Construct SVG file string. """

        return ET.tostring(self.root, encoding="unicode")

    def expandtag(self, tag):

        """ Determine tag string including namespace. """

        # No expansion, if no name space dictionary is given
        if self.ns == None:
            return tag

        # Expand namespace key in tag string
        if ":" in tag:
            key, tag = tag.split(":", 1)
            return "{%s}%s" % (self.ns[key], tag)

        # Handle default namespace key
        return "{%s}%s" % (self.ns[""], tag)

    def units(self):

        """ Return standard spatial units used in the SVG document. """

        tag = self.expandtag("sodipodi:namedview")
        docinfo = self.root.find(tag)
        tag = self.expandtag("inkscape:document-units")
        return docinfo.attrib[tag]

    def get_lines(self, element=None, transform=None):

        inkscape = f"{{{self.ns['inkscape']}}}"

        if element is None:
            self.lines = {}
            element = self.root

        # Build transformation based on parents
        transform = Transform(element.get("transform"), transform)

        for elem in element.findall("rect", self.ns):
            try:
                origin, color, id = self.get_label(elem)
            except ValueError:
                continue
            if origin != "bbox":
                continue
            llx = float(elem.attrib['x'])
            lly = float(elem.attrib['y'])
            urx = llx + float(elem.attrib['width'])
            ury = lly + float(elem.attrib['height'])
            bbox_transform = Transform(elem.get("transform"), transform)
            ll = bbox_transform.calc(complex(llx, lly))
            lr = bbox_transform.calc(complex(urx, lly))
            ul = bbox_transform.calc(complex(llx, ury))
            ur = bbox_transform.calc(complex(urx, ury))
            self.lines["low"] = ll, lr
            self.lines["high"] = ul, ur
            self.lines["screen"] = lr, ur
            self.set_display(elem, False)

        for elem in element.findall("path", self.ns):
            try:
                origin, color, id = self.get_label(elem)
            except ValueError:
                continue
            if origin != "filter":
                continue
            draw = svg.path.parse_path(elem.attrib["d"])
            assert len(draw) == 2
            assert isinstance(draw[0], svg.path.Move)
            assert isinstance(draw[1], svg.path.Line)
            line_transform = Transform(elem.get("transform"), transform)
            start = line_transform.calc(draw[1].start)
            end = line_transform.calc(draw[1].end)
            self.lines["filter"] = start, end
            self.set_display(elem, self.mode in (Mode.FILTER, Mode.BOTH))

        for elem in element.findall("path", self.ns):
            try:
                origin, color, id = self.get_label(elem)
            except ValueError:
                continue
            if origin != "pinhole":
                continue
            draw = svg.path.parse_path(elem.attrib["d"])
            assert len(draw) == 2
            assert isinstance(draw[0], svg.path.Move)
            assert isinstance(draw[1], svg.path.Line)
            line_transform = Transform(elem.get("transform"), transform)
            start = line_transform.calc(draw[1].start)
            end = line_transform.calc(draw[1].end)
            self.lines["aperture"] = start, end
            self.set_display(elem, self.mode in (Mode.APERTURE, Mode.BOTH))

        for child in element.findall("g", self.ns):
            self.get_lines(child, transform)

    def expand_arcs(self, element=None, style=None, transform=None):

        # Start with root element
        if element is None:
            element = self.root

        # Build style dictionary based on parents
        style = Style(element.get("style"), style)

        # Build transformation based on parents
        transform = Transform(element.get("transform"), transform)

        # Collect child arcs from this element
        sodipodi = f"{{{self.ns['sodipodi']}}}"
        for path in element.findall("path", self.ns):
            if path.attrib.get(f"{sodipodi}type", None) != "arc":
                continue

            try:
                origin, color, id = self.get_label(path)
            except ValueError:
                continue

            if color not in step_sizes:
                continue
            if origin not in ("lamp", "aperture"):
                continue

            if self.mode == Mode.NONE:
                if origin != "lamp":
                    self.set_display(path, False)
                    continue
            elif self.mode == Mode.APERTURE:
                pass
            elif self.mode == Mode.FILTER:
                if origin != "lamp":
                    self.set_display(path, False)
                    continue
            elif self.mode == Mode.BOTH:
                if origin == "aperture" and color != "red":
                    self.set_display(path, False)
                    continue
            else:
                raise ValueError(f"Unknown mode {self.mode}")

            dr = self.step_sizes[color]

            rx = float(path.attrib.get(f"{sodipodi}rx", None))
            ry = float(path.attrib.get(f"{sodipodi}ry", None))
            if abs(rx-ry) > 1e-7:
                continue
            r = 0.5*(rx+ry)

            parent = next(p for p in self.tree.iter() if path in p)
            id = path.attrib["id"]
            group = ET.Element("svg:g", id=f"{id}-group")
            i = 0
            while True:
            #for a in range(20):
                arc = Arc(self.ns, path, style, transform, f"{id}-{i:02d}", radius=r+i*dr)
                arc.clip(self.lines)

                plane = None
                if self.mode == Mode.NONE:
                    plane = Plane.SCREEN
                elif self.mode == Mode.APERTURE:
                    if origin == "lamp":
                        plane = Plane.APERTURE
                    else:
                        plane = Plane.SCREEN
                elif self.mode == Mode.FILTER:
                    if color == "red":
                        plane = Plane.SCREEN
                    else:
                        plane = Plane.FILTER
                elif self.mode == Mode.BOTH:
                    if origin == "lamp":
                        if color == "red":
                            plane = Plane.APERTURE
                        else:
                            plane = Plane.FILTER
                    else:
                        plane = Plane.SCREEN

                arcs = arc.split(plane, self.lines)
                if not arcs:
                    #print("Stop:", i)
                    break
                for arc in arcs:
                    arc_element = ET.Element("path", attrib=arc.attrib())
                    group.append(arc_element)
                i += 1
            parent.remove(path)
            parent.append(group)

        # Recursively collect arcs from all child elements
        for child in element.findall("g", self.ns):
            self.expand_arcs(child, style, transform)

    def get_label(self, element):

        inkscape = f"{{{self.ns['inkscape']}}}"
        label = element.attrib.get(f"{inkscape}label") or element.attrib["id"]
        label = label.split("-")
        if len(label) != 3:
            raise ValueError
        origin, color, id = label
        return origin, color, id

    def set_display(self, element, value):

        style = Style(element.get("style"))
        if value:
            style["display"] = "inline"
        else:
            style["display"] = "none"
        element.attrib["style"] = str(style)

    def write_svg(self, name=None):

        """ Store inkscape SVG file. """

        # Determine file name
        if name == None:
            name = "out"
        fn = f"{os.path.splitext(self.fn)[0]}-{name}.svg"

        # Store inkscape file
        with open(fn, "w") as fp:
            fp.write(str(self))
        print(f"Wrote file '{fn}'")


if __name__ == "__main__":

    fn = "lamp.svg"
    step_sizes = {
        'blue': 5.1,
        'red': 6.2,
    }

    InkscapeFile(fn, step_sizes, Mode.NONE).write_svg("none")
    InkscapeFile(fn, step_sizes, Mode.APERTURE).write_svg("aperture")
    InkscapeFile(fn, step_sizes, Mode.FILTER).write_svg("filter")
    InkscapeFile(fn, step_sizes, Mode.BOTH).write_svg("both")

