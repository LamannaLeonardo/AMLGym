import re
from dataclasses import dataclass
from typing import List

from unified_planning.model import UPState
from unified_planning.plans import ActionInstance


@dataclass
class Trajectory:

    states: List[UPState]
    actions: List[ActionInstance]

    def __str__(self):

        def format_pddl_string(literals: List[str]) -> str:
            return ' '.join([f"({l.replace('(', ' ').replace(')', '').replace(',', ' ')})"
                             for l in sorted(literals)])

        init_state = re.findall(r'(\w+(?:\([^\)]*\))?)\s*:\s*true', str(self.states[0]))  # positive literals
        trajectory_str = f"(:state {format_pddl_string(init_state)})"
        for i in range(len(self.actions)):
            a = f"({repr(self.actions[i]).replace('(', ' ').replace(')', '').replace(',', '')})"
            s = re.findall(r'(\w+(?:\([^\)]*\))?)\s*:\s*true', str(self.states[i + 1]))  # positive literals
            trajectory_str += f"\n\n(:action {a})"
            trajectory_str += f"\n\n(:state {format_pddl_string(s)})"

        trajectory_str = f"(:trajectory\n\n{trajectory_str}\n\n)".replace('  ', ' ')
        return trajectory_str

    def __repr__(self):
        return str(self)

    def write(self, file_path):
        with open(file_path, 'w') as f:
            f.write(str(self))
