#!/usr/bin/env python3

import regex
from pathlib import Path

sorry_regex = regex.compile(r'(.*)-- sorry.*')
root = Path(__file__).parent/'src'

if __name__ == '__main__':
    for path in (root/'solutions').glob('**/*.lean'):
        if path.name == 'numbers.lean':
            continue # Rob's exercises need hand-crafted extraction
        print(path)
        out = root/'exercises_sources'/path.relative_to(root/'solutions')
        out.parent.mkdir(exist_ok=True)
        with out.open('w') as outp:
            with path.open() as inp:
                state = 'normal'
                for line in inp:
                    m = sorry_regex.match(line)
                    if state == 'normal':
                        if m:
                            state = 'sorry'
                        else:
                            outp.write(line)
                    else:
                        if m:
                            state = 'normal'
                            outp.write(m.group(1)+ 'sorry\n')

            outp.write('\n')


