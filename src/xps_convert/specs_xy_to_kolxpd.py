from pathlib import Path
from collections.abc import Iterable
import numpy as np
import copy

class Specs_XY_Data_Block:
    def __init__(self, data_lines: list[str], header_parameters: dict):
        data_lines = [line.strip() for line in data_lines if line.strip()
                      and not line.startswith('#')]
        self.data = np.array([[float(s) for s in line.split()]
                              for line in data_lines])
        self.parameters = ''
        self.sweeps = ''
        self.scan = ''
        self.cycle = ''
        # default values:
        self.header_parameters = {
            'AxisBindingEn': '0',
            'ItemCount': '0',
            }
        for key in header_parameters:
            self.header_parameters[key] = header_parameters[key]

    @property
    def start(self):
        return self.data[0, 0]
    
    @property
    def end(self):
        return self.data[-1, 0]
    
    @property
    def step(self):
        return (self.end - self.start) / self.data.shape[0]

    def write_as_region(self, 
                        print_cycle: bool=False,
                        print_scan: bool=False,
                        parameters_as_notes: bool=False,
                        no_region_end=False) -> str:
        name = self.header_parameters['Title']
        if print_cycle: 
            name += f' - cycle {self.cycle}'
        if print_scan:
            name += f' - scan {self.scan}'
        if parameters_as_notes:
            notes = self.parameters
        else: 
            notes = self.header_parameters['Notes'] 
        out = f'''[Region]
KolXPDversion=1.8.0.69
Title={name}
Notes={notes}
timeStart=0
timeEnd=0
Color=0
ItemCount={self.header_parameters['ItemCount']}
Start={self.start:.2f}
End={self.end:.2f}
Dwell={self.header_parameters['Dwell']}
DwellSmart={self.header_parameters['Dwell']}
PassEn={self.header_parameters['PassEn']}
ExcitEn={self.header_parameters['ExcitEn']}
Step={self.step:.2f}
Sweeps={self.sweeps}
NumOfPointSets=5
AxisBindingEn={self.header_parameters['AxisBindingEn']}
Smart=0
WF={self.header_parameters['WF']}
AxisConvUsesWF=0
Udet={self.header_parameters['Udet']}
LensMode={self.header_parameters['LensMode']}
UseMonochromator=0
Level=
Cross=1
Asym=0
ChargeShift=0
AreaMult=1
[Data]
#Range {self.start:.2f} {self.end:.2f}
#X Eq {self.start:.2f} {self.step:.2f}
'''
        datastr = np.char.mod('%f', self.data[:,1])
        out += "\n".join(datastr) + '\n'
        if no_region_end:
            return out
        out += '[EndRegion]\n'
        return out

def get_data_avg(data_blocks,
                 header_parameters: dict={}) -> Specs_XY_Data_Block:
    '''
    Takes a collection of Specs_XY_Data_Block objects and returns one with
    averaged data.

    Parameters
    ----------
    data_blocks : iterable of Specs_XY_Data_Block
        The data blocks to collect.
    header : dict of {str: str}
        Header parameters for the Specs_XY_Data_Block. If nothing is passed,
        will use the parameters of data_blocks[0].

    Returns
    -------
    Specs_XY_Data_Block
        A new data block with averaged data.

    '''
    if isinstance(data_blocks, Iterable):
        if not all(isinstance(block, Specs_XY_Data_Block)
                   for block in data_blocks):
            raise TypeError('data_blocks: Expected Iterable of type '
                            'Specs_XY_Data_Block, found '
                            f'{[str(type(block)) for block in data_blocks]}')
    else:
        raise TypeError('data_blocks: expected Iterable.')
    if not all([np.shape(block.data) == np.shape(data_blocks[0].data)]
               for block in data_blocks):
        raise ValueError('Data blocks must contain the same number of '
                         'data points.')
    if not all(np.allclose(block.data[:,0], data_blocks[0].data[:,0])
               for block in data_blocks):
        raise ValueError('Data block energy ranges are not equal.')

    avg_block = copy.deepcopy(data_blocks[0])
    if header_parameters:
        avg_block.header_parameters = copy.copy(header_parameters)
    avg_block.data[:, 1] = (sum([block.data[:, 1] for block in data_blocks])
                            / len(data_blocks))
    return avg_block


def convert_specs_prodigy_xy(source_file: Path) -> str:
    '''
    Creates a KolXPD file from an XY file exported from SpecsLabs Prodigy.
    That file must contain exactly one loop (also works for profiling).
    '''

    def process_region(data_lines: list[str], header_colwidth: int=32) -> str:
        # if the file contains any operations, drop them right away
        # TODO: Could be implemented to keep them with a different name, 
        #   but I don't see the point
        try:
            data_lines = data_lines[
                :next(i for i in range(len(data_lines))
                      if data_lines[i].startswith('# Operation: '))]
        except StopIteration:
            pass
        sub_idx = [i for i in range(len(data_lines))
                   if data_lines[i].startswith('# Cycle:')]
        # everything up until the first Cycle is general header:
        specs_to_kolxpd_header = {
            '# Region:': 'Title',
            '# Analyzer Lens:': 'LensMode',
            '# Excitation Energy:': 'ExcitEn',
            '# Pass Energy:': 'PassEn',
            '# Detector Voltage:': 'Udet',
            '# Eff. Workfunction:': 'WF',
            }
        header_parameters = {}
        comment = ''
        notes = ''
        for line in data_lines[:sub_idx[0]]:
            left_side = line[:header_colwidth].strip()
            right_side = line[header_colwidth:].strip()
            if left_side in specs_to_kolxpd_header:
                header_parameters[specs_to_kolxpd_header[left_side]] = right_side
            elif left_side == '# Scan Variable:':
                 header_parameters['AxisBindingEn'] = '0' if 'Kinetic' in right_side else '1'
            elif left_side == '# Dwell Time:':
                try:
                    dw = float(right_side)*1000  # s to ms
                except ValueError:
                    dw = 0
                header_parameters['Dwell']=f'{dw:0.0f}'
            elif line.startswith('# Comment:'):
                comment = f'comment: {right_side}#0D#0A' if right_side else ''
            else:
                # collect everything unused up to this point into the notes
                notes += f'{left_side[2:]} {right_side}#0D#0A'
        header_parameters['Notes'] = comment + notes

        last_cycle_nr = ''
        data_per_cycle = {}
        total_data = 0
        for i in range(len(sub_idx)):
            cycle_nr = data_lines[sub_idx[i]].split(',')[0].split()[-1]
            if cycle_nr != last_cycle_nr:
                # pure header block - process
                parameters = []
                for line in data_lines[sub_idx[i]:sub_idx[i+1]]:
                    if line.startswith('# Number of Scans:'):
                        sweeps = line.split()[-1].strip()
                    elif line.startswith('# Parameter:'):
                        parameters.append(line.split('# Parameter:')[-1].strip())
            else:
                # contains data -> create a data block
                use_lines = (data_lines[sub_idx[i]:sub_idx[i+1]]
                             if i+1 < len(sub_idx)
                             else data_lines[sub_idx[i]:])
                data_block = Specs_XY_Data_Block(use_lines, header_parameters)
                data_block.sweeps = sweeps  # from general header
                data_block.cycle = int(cycle_nr) + 1
                if parameters:
                    data_block.parameters = ', '.join(parameters)
                if 'Scan: ' in data_lines[sub_idx[i]]:
                    data_block.scan = int(data_lines[sub_idx[i]]
                                          .strip().split()[-1]) + 1
                if cycle_nr in data_per_cycle:
                    data_per_cycle[cycle_nr].append(data_block)
                else:
                    data_per_cycle[cycle_nr] = [data_block]
                total_data += 1
            last_cycle_nr = cycle_nr

        # at this point we have all the data - now decide whether to write
        #  directly as regions, or make another folder (in case of loops etc):
        if total_data == 1:
            # only one data block - just write it
            return data_block.write_as_region()
        print_cycle = True if len(data_per_cycle) > 1 else False
        print_scan = (True if any(len(v) > 1 for v in data_per_cycle.values())
                       else False)
        out = ''
        if print_cycle:
            out += f'''[Folder]
KolXPDversion=1.8.0.69
Title={header_parameters['Title']}
NotesHTML=0
Notes={header_parameters['Notes']}
timeStart=0
timeEnd=0
Color=0
ItemCount={total_data}
'''
        for cycle_nr in data_per_cycle:
            if len(data_per_cycle[cycle_nr]) > 1:
                # also write an overall region with averaged data
                avg_block = get_data_avg(data_per_cycle[cycle_nr])
                avg_block.sweeps = f'{len(data_per_cycle[cycle_nr])}'
                avg_block.header_parameters['ItemCount'] = f'{avg_block.sweeps}'
                out += avg_block.write_as_region(print_cycle=print_cycle,
                                                 print_scan=False,
                                                 parameters_as_notes=True,
                                                 no_region_end=True)
            for data_block in data_per_cycle[cycle_nr]:
                out += data_block.write_as_region(print_cycle=print_cycle,
                                                  print_scan=print_scan,
                                                  parameters_as_notes=True)
            if len(data_per_cycle[cycle_nr]) > 1:
                out += '[EndRegion]\n'
        if print_cycle:
            out += '[EndFolder]\n'
        return out

    def process_group(data_lines: list[str]) -> str:
        group_name = data_lines[0][8:].strip()   # line starts with '# Group:'
        sub_idx = [i for i in range(len(data_lines))
                   if data_lines[i].startswith('# Region:')]
        out = f'''[Folder]
KolXPDversion=1.8.0.69
Title={group_name}
NotesHTML=0
Notes=
timeStart=0
timeEnd=0
Color=0
ItemCount={len(sub_idx)}
'''
        for i in range(len(sub_idx)):
            out += (process_region(data_lines[sub_idx[i]:sub_idx[i+1]])
                    if i+1 < len(sub_idx)
                    else process_region(data_lines[sub_idx[i]:]))
        
        out += '[EndFolder]\n'
        return out
        

    print(f'Converting {source_file}')
    with open(source_file, encoding='latin-1') as readfile:
        data_lines = readfile.readlines()

    sub_idx = [i for i in range(len(data_lines))
                   if data_lines[i].startswith('# Group:')]
    if not sub_idx:
        print("File contains no groups!")
        return

    # everything up until the first Group is general header:
    notes = ''      # collect unused metadata to add to KolXPD notes
    for line in data_lines[:sub_idx[0]]:
        notes += '#' + line.strip() + '#0D#0A'
    out = f'''[Folder]
KolXPDversion=1.8.0.69
Title={source_file.name}
NotesHTML=0
Notes={notes}
timeStart=0
timeEnd=0
Color=0
ItemCount={len(sub_idx)}
'''
        
    # now process each group:
    for i in range(len(sub_idx)):
        out += (process_group(data_lines[sub_idx[i]:sub_idx[i+1]])
                if i+1 < len(sub_idx)
                else process_group(data_lines[sub_idx[i]:]))

    # wrap up
    out += '[EndFolder]'
    return out
