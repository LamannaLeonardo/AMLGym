import pandas as pd
from pddl_plus_parser.lisp_parsers import DomainParser, ProblemParser, TrajectoryParser
from typing import List, Union, Optional, Dict

class ExperimentRunner():
    def __init__(self, domain_file= None):
        self.gold_standard = DomainParser(domain_file, partial_parsing=False).parse_domain()
        self.statistics = {"Algorithm": [],
                           "Domain": [],
                           "Num. Of Traces": [],
                           "Threshold": [],
                           "Epsilon": [],
                           "Fold": [],
                           'Epoch': [],
                           'Unobserved_actions': [],
                           "precision_effect":[],
                           'precision_precondition':[],
                           'recall_effect':[],
                           'recall_precondition':[]}

    def export_statistics(self, path):
        df = pd.DataFrame(self.statistics)
        df.to_csv(path,index=False)


    def creat_object_map(self, params, learned_params):
        """
        Creates a mapping between object parameters and their assigned indices.

        This function generates a dictionary that maps each parameter from two given lists
        (`params` and `learned_params`) to a unique string representation of its index.
        The index is assigned based on the parameter's position in the input lists.

        Args:
            params (List[str]): A list of parameter names.
            learned_params (List[str]): A list of corresponding learned parameter names.

        Returns:
            Dict[str, str]: A dictionary mapping each parameter (from both lists) to a string index.

        """
        params_map = {}
        for i in range(len(params)):
            params_map[params[i]] = str(i)
            params_map[learned_params[i]] = str(i)
        return params_map

    def get_predicates(self,predicates,params_map): # TODO: think about a better way to compare predicates other that mapping the predicates to indices.
        preds = []
        for predicate in predicates:
            predicate_str = ''
            if not predicate.is_positive:
                predicate_str += "not "
            predicate_str += predicate.name + " "
            param_lst = []
            for param in predicate.signature:
                param_lst.append(params_map[param])
            predicate_str += " ".join(param_lst)
            preds.append(predicate_str)
        return preds


    def run_single_experiment(self, learned_domain_path, algorithm_name, num_traces, threshold="NA", eps="NA",meta_data = None,fold=0,epoch="NA"):
        """
         Compares the preconditions and effects of actions between a learned PDDL domain and a gold standard domain.

        This function compares the actions, preconditions, and effects of actions from a learned domain
        with a gold standard domain. It calculates the precision, recall, and false positive/false negative
        values for preconditions and effects. It also prints warnings for mismatches in preconditions and effects
        and stores statistical values in `self.statistics`.

        Args:
            learned_domain_path (str): The path to the PDDL file containing the learned domain to compare.
            algorithm_name (str): The name of the algorithm used to learn the domain.
            num_traces (int): The number of traces used in learning the domain.

        Returns:
            None: The function updates the `self.statistics` dictionary with precision, recall, and other metrics.
        """
        learned_domain = DomainParser(learned_domain_path, partial_parsing=False).parse_domain()
        precision_pre, recall_pre, precision_eff, recall_eff = 0 ,0 ,0 ,0
        unobserved = 0

        """Compare preconditions and effects between actions of two PDDL domains."""
        for action in self.gold_standard.actions:
            FP_pre, FN_pre, FP_eff, FN_eff = 0, 0, 0, 0
            TP_pre, TP_eff = 0, 0  # True positives for preconditions and effects


            if action not in learned_domain.actions:
                continue
            if meta_data and meta_data[action] == 'UNOBSERVED':
                precision_eff += 1
                precision_pre += 0
                recall_eff += 0
                recall_pre += 1
                unobserved += 1
                print(f'Action {action} is unobserved.')
                continue
            params_map = self.creat_object_map(self.gold_standard.actions[action].parameter_names,learned_domain.actions[action].parameter_names)
            gold_standard_precond = self.gold_standard.actions[action].preconditions.root.operands
            learned_precond = learned_domain.actions[action].preconditions.root.operands
            new_precond = []
            for predicate in gold_standard_precond:
                if predicate.is_positive:
                    new_precond.append(predicate)
            # gold_standard_precond = self.get_predicates(new_precond, params_map)
            gold_standard_precond = new_precond

            new_precond = []
            for predicate in learned_precond:
                if predicate.is_positive:
                    new_precond.append(predicate)
            # learned_precond = self.get_predicates(new_precond, params_map)
            learned_precond = new_precond
            # Compare precondition order
            if gold_standard_precond != learned_precond:
                print(f"Warning: The preconditions of action {action} have a different order.")

            # True Positives (matching preconditions)
            precond1_set = set(gold_standard_precond)
            TP_pre += len(precond1_set.intersection(set(learned_precond)))

            # False negatives (missing preconditions)
            missing_preconditions = set(gold_standard_precond) - set(learned_precond)
            if missing_preconditions:
                print(f"FALSE NEGATIVE Warning: Missing preconditions in second domain for action {action}: {[p.untyped_representation for p in missing_preconditions]}")
                FN_pre += len(missing_preconditions)

            # False positives (extra preconditions)
            extra_preconditions = set(learned_precond) - set(gold_standard_precond)
            if extra_preconditions:
                print(f"FALSE POSITIVE Warning: Extra preconditions in second domain for action {action}: {[p.untyped_representation for p in extra_preconditions]}")
                FP_pre += len(extra_preconditions)

            # Compare effects similarly
            # gold_effects = self.get_predicates(self.gold_standard.actions[action].discrete_effects, params_map)
            # learned_effects = self.get_predicates(learned_domain.actions[action].discrete_effects, params_map)
            gold_effects = self.gold_standard.actions[action].discrete_effects
            learned_effects = learned_domain.actions[action].discrete_effects
            # Compare effect order
            if gold_effects != learned_effects:
                print(f"Warning: The effects of action {action} have a different order.")

            # True Positives (matching effects)
            effects1_set = set(gold_effects)
            TP_eff += len(effects1_set.intersection(set(learned_effects)))

            # False negatives (missing effects)
            missing_effects = set(gold_effects) - set(learned_effects)
            if missing_effects:
                print(f"FALSE NEGATIVE Warning: Missing effects in second domain for action {action}: {[p.untyped_representation for p in missing_effects]}")
                FN_eff += len(missing_effects)

            # False positives (extra effects)
            extra_effects = set(learned_effects) - set(gold_effects)
            if extra_effects:
                print(f"FALSE POSITIVE Warning: Extra effects in second domain for action {action}: {[p.untyped_representation for p in extra_effects]}")
                FP_eff += len(extra_effects)


            precision_pre += TP_pre / (TP_pre + FP_pre) if (TP_pre + FP_pre) > 0 else 0
            recall_pre += TP_pre / (TP_pre + FN_pre) if (TP_pre + FN_pre) > 0 else 0

            # Precision and Recall for Effects
            precision_eff += TP_eff / (TP_eff + FP_eff) if (TP_eff + FP_eff) > 0 else 0
            recall_eff += TP_eff / (TP_eff + FN_eff) if (TP_eff + FN_eff) > 0 else 0
        num_of_actions = len(self.gold_standard.actions)
        self.statistics["precision_effect"].append(round(precision_eff / num_of_actions, 2))
        self.statistics["precision_precondition"].append(round(precision_pre / num_of_actions, 2))
        self.statistics["recall_effect"].append(round(recall_eff / num_of_actions, 2))
        self.statistics["recall_precondition"].append(round(recall_pre / num_of_actions, 2))
        self.statistics["Threshold"].append(threshold)
        self.statistics["Algorithm"].append(algorithm_name)
        self.statistics['Domain'].append(self.gold_standard.name)
        self.statistics["Num. Of Traces"].append(num_traces)
        self.statistics["Epsilon"].append(eps)
        self.statistics['Fold'].append(fold)
        self.statistics['Unobserved_actions'].append(unobserved)
        self.statistics['Epoch'].append(epoch)




        # Print False Positive, False Negative, Precision, and Recall results ## TODO: REMOVE later!
        print("---------------------------------------------------------------------------------------")
        print(f"False Positives: Preconditions: {FP_pre}, Effects: {FP_eff}")
        print(f"False Negatives: Preconditions: {FN_pre}, Effects: {FN_eff}")
        print(f"Precision: Preconditions: {precision_pre / num_of_actions:.2f}, Effects: {precision_eff / num_of_actions:.2f}")
        print(f"Recall: Preconditions: {recall_pre / num_of_actions:.2f}, Effects: {recall_eff / num_of_actions:.2f}")
        print("---------------------------------------------------------------------------------------")

    def run_experiment(self,algo_lst:List[str],domain_path_lst:List[str], trace_len_lst:List[int], threshold_lst:List[float]= [], eps_lst:List[float] = []):
        for algo in algo_lst:
            for domain_path in domain_path_lst:
                for trace_len in trace_len_lst:
                    # for threshold in threshold_lst:
                    #     for eps in eps_lst:
                    self.run_single_experiment(algo, domain_path, trace_len)