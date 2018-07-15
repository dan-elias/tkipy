'''
=========
renderers
=========

Tools for formatting data as text

'''
from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET

class xml_renderer(ABC):
    '''
    ABC for XML renderers
    
    These contain methods for rendering data to :class:`xml.etree.ElementTree.Element`
    or :class:`str`
    '''
    def __init__(self, data):
        '''
        Args:
            data: Data to render
        '''
        self.data = data
    @abstractmethod
    def as_elem(self):
        '''
        Representation as :class:`xml.etree.ElementTree.Element`
        '''
        pass
    def __str__(self):
        return ET.tostring(self.as_elem()).decode()
        
class html_table(xml_renderer):
    '''
    Example:
        >>> str(html_table([[1,2], [3,4]], header_row=['col_1', 'col_2']))
        '<table><tr><th>col_1</th><th>col_2</th></tr><tr><td>1</td><td>2</td></tr><tr><td>3</td><td>4</td></tr></table>'
    '''
    def __init__(self, data, header_row=None):
        '''
        Args:
            data (iterable of iterables): Table body contents by row.
            header_row (:class:`collections.abc.iterable`): Header row contents
        '''
        self.data, self.header_row = data, header_row
    def as_elem(self):
        result = ET.Element('table')
        def add_row(row_data, is_header=False):
            row_elem = ET.SubElement(result, 'tr')
            elem_tag = 'th' if is_header else 'td'
            for datum in row_data:
                ET.SubElement(row_elem, elem_tag).text = str(datum)
        if self.header_row is not None:
            add_row(self.header_row, is_header=True)
        for data_row in self.data:
            add_row(data_row, is_header=False)
        return result


if __name__ == '__main__':
    import doctest
    doctest.testmod()
