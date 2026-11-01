"""The setup files from project.json, through the client's generator.

main() writes the three setup files for this directory, whose data is
generated and labelled synthetic. own_setup() writes a setup whose source
is the Principal's own files, declared historical, into another directory
with the tool, evaluator and researcher modules beside it. The generator
supplies administrative defaults only.
"""
from __future__ import annotations
from copy import deepcopy
from pathlib import Path
import json
import shutil
import sys
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'client'))
from arh_client.project import Project, FILE

MODULES = ('tool.py', 'evaluator.py', 'researcher.py')


def own_setup(directory, dataset='Tables the Principal supplies from local storage', budget='100.00'):
    """A historical-class setup for the Principal's own files, with the modules it names copied beside it."""
    directory = Path(directory); directory.mkdir(parents=True, exist_ok=True)
    for m in MODULES: shutil.copyfile(HERE / m, directory / m)
    data = deepcopy(Project.load(HERE).data); data['project'] = 'signal-groups-own'; data['budget'] = budget
    data['sources'] = [{'id': 'SRC-SIG-OWN', 'prefix': 'signals-', 'class': 'historical', 'description': dataset}]
    data['formation'].update({'class': 'historical', 'synthetic': False})
    (directory / FILE).write_text(json.dumps(data, indent=1) + '\n')
    return Project.load(directory).write_setup()


def main():
    print('wrote setup for', Project.load(HERE).write_setup())


if __name__ == '__main__': main()
