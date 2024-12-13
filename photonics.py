import numpy as np
from abc import ABC, abstractmethod

# a class for defining your optical system. An optical system will consist of a series of
# lenses, mirrors, and free space.
class OpticalSystem:
    def __init__(self, name: str = 'OpticalSystem'):
        self.system = []
        self.name = name

    def __str__(self):
        return f'{self.name}({self.system})'

    # remove all components from optical system
    def clear(self):
        self.system = []

    # add a component to your optical system
    def add(self, component):
        if isinstance(component, OpticalComponent):
            self.system.append(component)
        else:
            raise TypeError("Class method add must be called with an instance of OpticalComponent subclass.")

    # build the equivalent ray transfer matrix of the optical system    
    def build_matrix(self):
        new_matrix = self.system[len(self.system)-1].matrix
        for i in range(len(self.system)-2, -1, -1):
            new_matrix = np.dot(new_matrix, self.system[i].matrix)
        return new_matrix

    # propagate a beam vector through this optical system
    def propagate(self, beam):
        if isinstance(beam, Beam):
            new_matrix = self.build_matrix()
            result = np.dot(new_matrix, beam.matrix)
            result = np.round(result, 2)
            return result
        else:
            raise TypeError('Class method propagate must be called with an instance of Beam class.')

# class for a laser beam
class Beam:
    def __init__(self, height: float = 0.0, angle: float = 0.0):
        self.height = float(height)
        self.angle = float(angle)
        self.matrix = np.array([[float(height)], [float(angle)]])

# An abstract class that will serve as the basis for all kinds of optical components
class OpticalComponent(ABC):
    def build_matrix(self, other):
        return np.dot(self.matrix, other.matrix)
    
    def propagate(self, beam):
        if isinstance(beam, Beam):
            return np.dot(self.matrix, beam.matrix)
        else:
            raise TypeError('Class method propagate must be called with an instance of Beam class.')
    
# class for propogation through free space
class FreeSpace(OpticalComponent):
    def __init__(self, distance: float = 0.0):
        self.distance = float(distance)
        self.matrix = np.array([[1, distance], [0, 1]])

    def __repr__(self):
        return f'FreeSpace(d = {self.distance})'
    
class PlanarBoundary(OpticalComponent):
    def __init__(self, n1: float = 1.003, n2: float = 1.003, name: str = 'PlanarBoundary'):
        self.n1 = float(n1)
        self.n2 = float(n2)
        self.name = name
        self.matrix = np.array([[1, 0], [0, n1/n2]])

    def __repr__(self):
        return f'{self.name}(n1 = {self.n1}, n2 = {self.n2})'

# class for refraction at a planar boundary
class SphericalBoundary(OpticalComponent):
    def __init__(self, radius: float = 1.0, n1: float = 1.003, n2: float = 1.003, name: str = 'SphericalBoundary'):
        self.n1 = float(n1)
        self.n2 = float(n2)
        self.radius = float(radius)
        self.name = name
        self.matrix = np.array([[1, 0], [-(n2-n1)/(n2*radius), n1/n2]])

    def __repr__(self):
        return f'{self.name}(n1 = {self.n1}, n2 = {self.n2}, r = {self.radius})'

# class for thin lens
class ThinLens(OpticalComponent):
    def __init__(self, focal_length: float = 1.0, name: str = 'ThinLens'):
        self.name = name
        self.focal_length = float(focal_length)
        self.matrix = np.array([[1, 0], [-1/focal_length, 1]])

    def __repr__(self):
        return f'{self.name}(f = {self.focal_length})'

# class for reflection from a planar mirror
class PlanarMirror(OpticalComponent):
    def __init__(self, name: str = 'PlanarMirror'):
        self.name = name
        self.matrix = np.array([[1, 0], [0, 1]])

    def __repr__(self):
        return f'{self.name}'
    
# class for reflection from a spherical mirror
class SphericalMirror(OpticalComponent):
    def __init__(self, radius: float = 1.0, name: str = 'SphericalMirror'):
        self.name = name
        self.radius = float(radius)
        self.matrix = np.array([[1,0], [2/radius, 1]])

    def __repr__(self):
        return f'{self.name}(r = {self.radius})'

# class for refraction through a thick lens
class ThickLens(OpticalComponent):
    def __init__(self, r1: float = 1.0, r2: float = 1.0, width: float = 0.0, n1: float = 1.003, n2: float = 1.003, name: str = 'ThickLens'):
        self.r1 = float(r1)
        self.r2 = float(r2)
        self.width = float(width)
        self.n1 = float(n1)
        self.n2 = float(n2)
        self.name = name
        self.matrix = self._make_matrix()

    def _make_matrix(self):
        pb1 = SphericalBoundary(radius = self.r1, n1 = self.n1, n2 = self.n2)
        pb2 = SphericalBoundary(radius = self.r2, n1 = self.n2, n2 = self.n1)
        fs = FreeSpace(self.width)
        return pb2.build_matrix(fs).dot(pb1.matrix)
    
    def __repr__(self):
        return f'{self.name}(r1 = {self.r1}, r2 = {self.r2}, w = {self.width}, n1 = {self.n1}, n2 = {self.n2})'

