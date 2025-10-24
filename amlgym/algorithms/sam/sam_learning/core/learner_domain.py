"""Module containing the datatype of the output domain that the learning algorithms return."""
import os
from collections import defaultdict
from typing import Set, List, Dict

from pddl_plus_parser.models import (
    SignatureType,
    Predicate,
    PDDLType,
    PDDLConstant,
    PDDLFunction,
    Domain,
    ConditionalEffect,
    CompoundPrecondition,
    UniversalEffect,
    NumericalExpressionTree,
)

from utilities.util_types import NUMERIC_PRECISION

DISJUNCTIVE_PRECONDITIONS_REQ = ":disjunctive-preconditions"
NEGATIVE_PRECONDITIONS_REQ = ":negative-preconditions"
EQUALITY_REQ = ":equality"
UNIVERSAL_PRECONDITIONS_REQ = ":universal-preconditions"
CONDITIONAL_EFFECTS_REQ = ":conditional-effects"
ADDED_LEARNING_REQUIREMENTS = [NEGATIVE_PRECONDITIONS_REQ, EQUALITY_REQ]
DEFAULT_DIGITS = int(os.environ.get(NUMERIC_PRECISION, 4))


class LearnerAction:
    """Class representing an action that the learning algorithm outputs."""

    name: str
    signature: SignatureType
    preconditions: CompoundPrecondition
    discrete_effects: Set[Predicate]
    conditional_effects: Set[ConditionalEffect]
    universal_effects: Set[UniversalEffect]
    numeric_effects: Set[NumericalExpressionTree]

    def __init__(self, name: str, signature: SignatureType):
        self.name = name
        self.signature = signature
        self.preconditions = CompoundPrecondition()
        self.discrete_effects = set()
        self.conditional_effects = set()
        self.universal_effects = set()
        self.numeric_effects = set()

    def __str__(self):
        signature_str_items = []
        for parameter_name, parameter_type in self.signature.items():
            signature_str_items.append(f"{parameter_name} - {str(parameter_type)}")

        signature_str = " ".join(signature_str_items)
        return f"({self.name} {signature_str})"

    @property
    def parameter_names(self) -> List[str]:
        return list(self.signature.keys())

    @property
    def preconditions_str_set(self) -> Set[str]:
        """Returns the set of the string representations of the preconditions."""
        precondition_str_set = set()
        for _, precondition in self.preconditions:
            if isinstance(precondition, Predicate):
                precondition_str_set.add(precondition.untyped_representation)

        return precondition_str_set

    def _signature_to_pddl(self) -> str:
        """Converts the action's signature to the PDDL format.

        :return: the PDDL format of the signature.
        """
        signature_str_items = []
        for parameter_name, parameter_type in self.signature.items():
            signature_str_items.append(f"{parameter_name} - {str(parameter_type)}")

        signature_str = " ".join(signature_str_items)
        return f"({signature_str})"

    def _effects_to_pddl(self) -> str:
        """Converts the effects to the needed PDDL format.

        :return: the PDDL format of the effects.
        """
        simple_effects = "\n\t\t".join(sorted([effect.untyped_representation for effect in self.discrete_effects]))

        conditional_effects = "\n\t\t"
        conditional_effects += "\t\t\n".join([str(conditional_effect) for conditional_effect in self.conditional_effects])

        universal_effects = "\n\t\t"
        universal_effects += "\t\t\n".join([str(universal_effect) for universal_effect in self.universal_effects])

        if len(self.numeric_effects) > 0:
            numeric_effects = "\t\t\n".join([effect.to_pddl() for effect in self.numeric_effects])
            return f"(and {simple_effects}\n" f"\t\t{conditional_effects}\n" f"\t\t{universal_effects}\n" f"{numeric_effects})"

        return f"(and {simple_effects} {conditional_effects} {universal_effects})"

    def to_pddl(self, decimal_digits: int = DEFAULT_DIGITS) -> str:
        """Returns the PDDL string representation of the action.

        :param decimal_digits: the number of decimal digits to use to display the preconditions.
        :return: the PDDL string representing the action.
        """
        action_string = (
            f"(:action {self.name}\n"
            f"\t:parameters {self._signature_to_pddl()}\n"
            f"\t:precondition {self.preconditions.print(decimal_digits=decimal_digits)}\n"
            f"\t:effect {self._effects_to_pddl()})"
        )
        formatted_string = "\n".join([line for line in action_string.split("\n") if line.strip()])
        return f"{formatted_string}\n"

    def to_pddl_legacy(self, should_simplify: bool = True, decimal_digits: int = DEFAULT_DIGITS):
        """Returns the PDDL string representation of the action.

        Note:
            This is for legacy support and should be removed in the future.

        :param should_simplify: whether to simplify the preconditions or not.
        :param decimal_digits: the number of decimal digits to use to display the preconditions.
        :return: the PDDL string representing the action.
        """
        action_string = (
            f"(:action {self.name}\n"
            f"\t:parameters {self._signature_to_pddl()}\n"
            f"\t:precondition {self.preconditions.print(should_simplify=should_simplify, decimal_digits=decimal_digits)}\n"
            f"\t:effect {self._effects_to_pddl()})"
        )
        formatted_string = "\n".join([line for line in action_string.split("\n") if line.strip()])
        return f"{formatted_string}\n"


class LearnerDomain:
    """Class representing the domain that is to be learned by the action model learning algorithm."""

    name: str
    requirements: List[str]
    types: Dict[str, PDDLType]
    constants: Dict[str, PDDLConstant]
    predicates: Dict[str, Predicate]
    functions: Dict[str, PDDLFunction]
    actions: Dict[str, LearnerAction]

    # processes: Dict[str, Action] - TBD
    # events: Dict[str, Action] - TBD

    def __init__(self, domain: Domain):
        self.name = domain.name
        self.requirements = domain.requirements
        self.types = domain.types
        self.constants = domain.constants
        self.predicates = domain.predicates
        self.functions = domain.functions
        self.actions = {}
        for action_name, action_object in domain.actions.items():
            self.actions[action_name] = LearnerAction(name=action_name, signature=action_object.signature)

    def __str__(self):
        return "< Domain definition: %s\n Requirements: %s\n Predicates: %s\n Functions: %s\n Actions: %s\n " "Constants: %s >" % (
            self.name,
            [req for req in self.requirements],
            [str(p) for p in self.predicates.values()],
            [str(f) for f in self.functions.values()],
            [str(a) for a in self.actions.values()],
            [str(c) for c in self.constants],
        )

    def _complete_missing_requirements(self) -> None:
        """Completes the requirements of the domain from the needed requirements of the learning algorithm."""
        for requirement in ADDED_LEARNING_REQUIREMENTS:
            if requirement not in self.requirements:
                self.requirements.append(requirement)

    def _types_to_pddl(self) -> str:
        """Converts the types to a PDDL string.

        :return: the PDDL string representing the types.
        """
        parent_child_map = defaultdict(list)
        if set(self.types.keys()) == {"object"}:
            return "object"

        for type_name, type_obj in self.types.items():
            if type_name == "object":
                continue

            parent_child_map[type_obj.parent.name].append(type_name)

        types_strs = []
        for parent_type, children_types in parent_child_map.items():
            types_strs.append(f"\t{' '.join(children_types)} - {parent_type}")

        return "\n".join(types_strs)

    def _constants_to_pddl(self) -> str:
        """Converts the constants to a PDDL string.

        :return: the PDDL string representing the constants.
        """
        same_type_constant = defaultdict(list)
        for const_name, constant in self.constants.items():
            if const_name == "object":
                continue

            same_type_constant[constant.type.name].append(const_name)

        types_strs = []
        for constant_type_name, constant_objects in same_type_constant.items():
            types_strs.append(f"\t{' '.join(constant_objects)} - {constant_type_name}")

        return "\n".join(types_strs)

    def _functions_to_pddl(self) -> str:
        """Converts the functions to PDDL format.

        :return: the PDDL format of the functions.
        """
        return "\n\t".join([str(f) for f in self.functions.values()])

    def to_pddl(self, should_simplify: bool = True, decimal_digits: int = DEFAULT_DIGITS) -> str:
        """Converts the domain into a PDDL string format.

        :return: the PDDL string representing the domain.
        """
        # TODO: remove the support for legacy PDDL format in the future.
        self._complete_missing_requirements()
        predicates = "\n\t".join([str(p) for p in self.predicates.values()])
        predicates_str = f"(:predicates {predicates}\n)\n\n" if len(self.predicates) > 0 else ""
        types_str = f"(:types {self._types_to_pddl()}\n)\n\n" if len(self.types) > 0 else ""
        actions = "\n".join(action.to_pddl_legacy(should_simplify=should_simplify, decimal_digits=decimal_digits) for action in self.actions.values())
        constants = f"(:constants {self._constants_to_pddl()}\n)\n\n" if len(self.constants) > 0 else ""
        functions = f"(:functions {self._functions_to_pddl()}\n)\n\n" if len(self.functions) > 0 else ""
        return (
            f"(define (domain {self.name})\n"
            f"(:requirements {' '.join(self.requirements)})\n"
            f"{types_str}"
            f"{constants}"
            f"{predicates_str}"
            f"{functions}"
            f"{actions}\n)"
        )
