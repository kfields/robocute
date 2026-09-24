from loguru import logger

from robocute.base import *
from robocute.node import GameNode

from robocute import dna_dict
from robocute import class_dict


def find_dna(name):
    return dna_dict[name]


def add_dna(dna):
    dna_dict[dna.name] = dna


def add_class(cls):
    name = cls.__name__
    class_dict[name] = cls
    # dna = Dna('class', name, 'No Title', 'No Image Source', name, [])
    dna = Dna("class", name, "No Title", None, name, [])
    dna.cls = cls
    dna_dict[name] = dna
    #
    cls.dna = dna  #!!!


def add_classes(clsList):
    for cls in clsList:
        add_class(cls)


def build_thing(dna, app=None):
    cls = dna.cls
    # print(cls.__name__)
    #
    thing = cls(dna)
    #
    if dna and dna.has_assignments():
        for assign in dna.assignments:
            thing.__setattr__(assign[0], assign[1])
    #
    if app:
        thing.register(app)
    #
    return thing


def build_thing_at(app, dna, coord, cell):
    thing = build_thing(dna)
    if isinstance(thing, GameNode):
        cell.push_node(thing, coord)
    thingCoord = Coord(coord.x, coord.y, cell.height)
    thing.register(app, thingCoord)


def build(app, body, coord, cell):
    ctors = compile_ctors(body)
    thing = execute_ctors(app, ctors, coord, cell)
    return thing


def compile_ctors(body):
    if body == "":
        return None
    # else
    ctors = eval(body, {}, dna_dict)
    return ctors


def execute_ctors(app, ctors, coord, cell):
    # wrap if necessary
    if not isinstance(ctors, list):
        ctors = [ctors]
    for ctor in ctors:
        thing = ctor()
        if isinstance(thing, GameNode):
            cell.push_node(thing, coord)
        thingCoord = Coord(coord.x, coord.y, cell.height)
        thing.register(app, thingCoord)
    #
    return thing


class Constructor:
    def __init__(self, dna, *args, **kargs):
        self.dna = dna
        self.args = args
        self.kargs = kargs

    def __call__(self):
        return build_thing(self.dna)


class Dna:
    def __init__(self, type, name, title, img_src, cls_name, assignments):
        self.type = type
        self.name = name
        self.title = title
        self.img_src = img_src
        self.cls_name = cls_name
        self.cls = eval(cls_name, class_dict)
        dna_dict[name] = self

        self.block_height = 2

        self.assignments = assignments  # list of property value tuples

        if self.has_assignments():
            for assign in self.assignments:
                self.__setattr__(assign[0], assign[1])

    def __call__(self, *args, **kargs):
        return Constructor(self, args, kargs)

    def __repr__(self):
        return f"Dna(type={self.type}, name={self.name}, title={self.title}, img_src={self.img_src}, cls_name={self.cls_name}, assignments={self.assignments})"

    def add_assignment(self, prop, val):
        self.assignments.append((prop, val))

    def has_assignments(self):
        return not len(self.assignments) == 0
