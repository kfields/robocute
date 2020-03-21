import os, sys
import pickle

import data

from robocute.world import *
from robocute.persist.grid import ReaderWriter

from robocute.builder import find_dna

class Writer(ReaderWriter):
    def __init__(self, filename, grid):
        super().__init__(filename, grid)

    def write(self):
        self.file = open(self.filename, 'wb')
        self.write_header()
        self.write_rows()
        self.file.close()
        
    def write_header(self):
        pass
    
    def write_rows(self):
        rows = self.grid.rows
        length = len(rows)
        pickle.dump(length, self.file)        
        for row in rows:
            self.write_row(row)
            
    def write_row(self, row):
        cells = row
        length = len(cells)
        pickle.dump(length, self.file)        
        for cell in cells:
            self.write_cell(cell)
            
    def write_cell(self, cell):
        nodes = cell
        length = len(nodes)
        pickle.dump(length, self.file)
        for node in nodes:
            self.write_node(node)
             
    def write_node(self, node):
        dna = node.dna
        if not dna:
            print(node)
        name = dna.name
        pickle.dump(name, self.file)
        
class Reader(ReaderWriter):
    def __init__(self, filename, grid):
        super().__init__(filename, grid)

    def read(self):
        self.file = open(self.filename, 'rb')
        self.read_header()
        self.read_rows()
        self.file.close()
        
    def read_header(self):
        pass
    
    def read_rows(self):
        grid = self.grid
        length = pickle.load(self.file)
        i = 0
        while i < length:
            row = grid.create_row() 
            self.read_row(row)
            grid.rows.append(row)
            i += 1
            
    def read_row(self, row):
        length = pickle.load(self.file)
        i = 0
        while i < length:
            cell = row.create_cell()
            self.read_cell(cell)
            row.append(cell)
            i += 1
            
    def read_cell(self, cell):
        length = pickle.load(self.file)
        if length == 0:
            return
        #else
        ctors = []
        i = 0
        while i < length:
            ctor = self.read_ctor()
            ctors.append(ctor)
            i += 1
        cell.ctors = ctors
            
    def read_ctor(self):
        dnaName = pickle.load(self.file)
        dna = find_dna(dnaName)
        ctor = dna()
        return ctor
        