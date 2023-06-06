# clients\tree_of_thoughts\AsyncMonteCarlo.py
from typing import Any, Dict, Union
import os
import asyncio
import json
import logging
import numpy as np
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TreeofThoughts:
    def __init__(self, model):
        self.model = model
        self.tree: Dict[str, Dict[str, Union[float, Dict[str, Any]]]] = {
            "nodes": {},
        }
        self.best_state = None
        self.best_value = float("-inf")
        self.history = []  # added line initalize history

    def save_tree_to_json(self, file_name):
        self.model.stream_message(json.dumps(self.tree, indent=4))
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open(file_name, 'w') as json_file:
            json.dump(self.tree, json_file, indent=4)

    def logNewState(self, state, evaluation):
        if not (type(state) == str):
            state = " | ".join(state)
        if state in self.tree['nodes']:
            self.tree['nodes'][state]['thoughts'].append(evaluation)
        else:
            self.tree['nodes'][state] = {'thoughts': [evaluation]}

    def adjust_pruning_threshold_precentile(self, evaluated_thoughts, percentile):
        values = np.array(list(evaluated_thoughts.values()))
        if values.size == 0:
            return 0
        return max(np.percentile(values, percentile), 0.1)

    def adjust_pruning_threshold_moving_average(self, evaluated_thoughts, window_size):
        values = list(evaluated_thoughts.values())
        if len(values) < window_size:
            return np.mean(values) if values else 0
        else:
            return max(np.mean(values[-window_size:]), 0.1)

class AsyncMonteCarloTreeofThoughts(TreeofThoughts):
    def __init__(self, model, objective="balance", stream_handler=None):
        super().__init__(model)
        self.stream_handler = stream_handler
        self.objective = objective
        self.solution_found = False
        self.tree: Dict[str, Dict[str, Union[float, Dict[str, Any]]]] = {
            "nodes": {},
            "metrics": {"thoughts": {}, "evaluations": {}},
        }

    def optimize_params(self, num_thoughts, max_steps, max_states):
        if self.objective == 'speed':
            num_thoughts = max(1, num_thoughts - 1)
            max_steps = max(1, max_steps - 1)
            max_states = max(1, max_states - 1)
        elif self.objective == 'reliability':
            num_thoughts += 1
            max_steps += 1
            max_states += 1
        elif self.objective == 'balanace':
            if self.solution_found:
                num_thoughts = max(1, num_thoughts - 1)
                max_steps = max(1, max_steps - 1)
                max_states = max(1, max_states - 1)
            else:
                num_thoughts += 1
                max_steps += 1
                max_states += 1

        return num_thoughts, max_steps, max_states

    async def solve(self,
                    initial_prompt: str,
                    num_thoughts: int,
                    max_steps: int,
                    max_states: int,
                    pruning_threshold: float,
                    #   sleep_time: float,
                    ):
        self.file_name = f"logs/tree_of_thoughts_output_montecarlo.json"
        return await self.monte_carlo_search(
            initial_prompt,
            num_thoughts,
            max_steps,
            max_states,
            pruning_threshold,
            # sleep_time,
        )
# v3

    async def monte_carlo_search(self,
                                 initial_prompt: str,
                                 num_thoughts: int,
                                 max_steps: int,
                                 max_states: int,
                                 pruning_threshold: float,
                                 ):
        current_states = [initial_prompt]
        state_values = {}
        visit_counts = {initial_prompt: 0}
        transposition_table = {}

        best_state = None
        best_value = float('-inf')

        for step in range(1, max_steps + 1):
            selected_states = []

            for state in current_states:
                if state in transposition_table:
                    state_value = transposition_table[state]
                else:
                    await asyncio.sleep(1)
                    thoughts = await self.model.generate_thoughts(state, num_thoughts, initial_prompt)
                    await asyncio.sleep(1)
                    evaluated_thoughts = await self.model.evaluate_states(thoughts, initial_prompt)

                    for thought, value in evaluated_thoughts.items():
                        flattened_state = (state, thought) if isinstance(
                            state, str) else (*state, thought)
                        transposition_table[flattened_state] = value

                for thought, value in evaluated_thoughts.items():
                    flattened_state = (state, thought) if isinstance(
                        state, str) else (*state, thought)
                    
                    self.logNewState(flattened_state, value)

                    if flattened_state not in visit_counts:
                        visit_counts[flattened_state] = 0

                    if visit_counts[state] > visit_counts[flattened_state] and visit_counts[flattened_state] > 0:
                        ucb1_value = value + \
                            np.sqrt(
                                2 * np.log(visit_counts[state]) / visit_counts[flattened_state])

                        if ucb1_value >= pruning_threshold:
                            selected_states.append(flattened_state)
                            state_values[flattened_state] = value

                            # Update the best state if the current state value is greater than the best value
                            if value > best_value:
                                best_state = flattened_state
                                best_value = value

                visit_counts[state] += 1

            if len(selected_states) > max_states:
                current_states = selected_states[:max_states]
            self.save_tree_to_json(self.file_name)

        solution = await self.model.generate_solution(initial_prompt, best_state)
        return solution if solution else best_state
