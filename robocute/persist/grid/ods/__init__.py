import xml.dom.minidom

from loguru import logger

from robocute import resources
from robocute.world import Grid

from robocute.builder import compile_ctors

OD_TABLE_NS = 'urn:oasis:names:tc:opendocument:xmlns:table:1.0'


def get_text(node) -> str:
    """Concatenate all text beneath an XML node, depth first."""
    parts = []
    for child in node.childNodes:
        if child.nodeType == child.ELEMENT_NODE:
            parts.append(get_text(child))
        elif child.nodeType == child.TEXT_NODE:
            parts.append(child.data)
    return ''.join(parts)


def get_repeat(node, attr: str) -> int:
    """Read an ODS `number-*-repeated` attribute, defaulting to 1."""
    value = node.getAttributeNS(OD_TABLE_NS, attr)
    return int(value) if value else 1


class Reader:
    """Load a level from an OpenDocument spreadsheet into a grid.

    Each spreadsheet cell holds constructor text for one grid cell. The grid's
    dimensions are the hard bound: rows and cells beyond them are ignored.

    The bound is enforced by the length of the list being filled, checked
    *before* each append. The previous version threaded a separate index and
    checked it after appending, so whenever the limit fell inside a repeated
    element -- which in ODS is always, since trailing empty rows and cells are
    written as a single element repeated up to about a million times -- it
    appended one extra. For rows that was fatal: the extra empty row was last,
    `reverse()` moved it to index 0, every real row shifted up by one, and the
    spreadsheet's first row landed at index `row_count`, outside the grid.

    Expects `grid.rows` to be empty on entry; existing rows count against the
    limit.
    """

    def __init__(self, filename, app, grid: Grid):
        self.filename = filename
        self.app = app
        self.grid = grid
        self.m_odf = resources.load_zip(filename)
        self.filelist = self.m_odf.infolist()
        self.content = xml.dom.minidom.parseString(self.m_odf.read('content.xml'))

    # ------------------------------------------------------------------
    # Limits
    # ------------------------------------------------------------------

    def rows_full(self) -> bool:
        return len(self.grid.rows) >= self.grid.row_count

    def row_full(self, grid_row) -> bool:
        return len(grid_row) >= self.grid.col_count

    # ------------------------------------------------------------------
    # Reading
    # ------------------------------------------------------------------

    def read(self):
        if self.grid.rows:
            logger.warning(
                f"Reader: grid already has {len(self.grid.rows)} rows; "
                f"they count against row_count"
            )
        self.read_sheets()
        # Spreadsheet row 0 is the back of the world; grid row 0 is the front.
        self.grid.rows.reverse()
        logger.debug(
            f"Reader: {self.filename} -> {len(self.grid.rows)} rows "
            f"(grid row_count={self.grid.row_count})"
        )

    def read_sheets(self):
        sheets = self.content.getElementsByTagNameNS(OD_TABLE_NS, 'table')
        for sheet in sheets:
            if self.rows_full():
                return
            self.read_sheet(sheet)

    def read_sheet(self, sheet):
        self.read_rows(sheet)

    def read_rows(self, sheet):
        for row in sheet.getElementsByTagNameNS(OD_TABLE_NS, 'table-row'):
            if self.rows_full():
                return
            self.read_row(row)

    def read_row(self, row):
        # Must return, not merely skip, once full: a repeat count of about a
        # million is normal for the trailing empty rows.
        for _ in range(get_repeat(row, 'number-rows-repeated')):
            if self.rows_full():
                return
            self.grid.rows.append(self.read_cells(row))

    def read_cells(self, row):
        grid_row = self.grid.create_row()
        for cell in row.getElementsByTagNameNS(OD_TABLE_NS, 'table-cell'):
            if self.row_full(grid_row):
                break
            self.read_cell(cell, grid_row)
        return grid_row

    def read_cell(self, cell, grid_row):
        # Every repeat of a cell has identical text, so compile once and share.
        # Sharing is safe: Cell.clone already shares ctors between cells.
        ctors = compile_ctors(get_text(cell))
        for _ in range(get_repeat(cell, 'number-columns-repeated')):
            if self.row_full(grid_row):
                return
            grid_cell = grid_row.create_cell()
            grid_cell.ctors = ctors
            grid_row.append(grid_cell)