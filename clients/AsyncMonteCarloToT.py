import time
import numpy as np
from typing import Any, Dict, Union
from tree_of_thoughts import MonteCarloTreeofThoughts

class AsyncMonteCarloTreeofThoughts(MonteCarloTreeofThoughts):
    async def solve(self,
                    initial_prompt: str,
                    num_thoughts: int,
                    max_steps: int,
                    max_states: int,
                    pruning_threshold: float,
                    ):
        self.file_name = f"logs/tree_of_thoughts_output_montecarlo.json"
        return await self.monte_carlo_search(
            initial_prompt,
            num_thoughts,
            max_steps,
            max_states,
            pruning_threshold,
        )

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
                    thoughts = await self.model.generate_thoughts(state, num_thoughts, initial_prompt)
                    evaluated_thoughts = await self.model.evaluate_states(thoughts, initial_prompt)

                    for thought, value in evaluated_thoughts.items():
                        flattened_state = (state, thought) if isinstance(state, str) else (*state, thought)
                        transposition_table[flattened_state] = value

                for thought, value in evaluated_thoughts.items():
                    flattened_state = (state, thought) if isinstance(state, str) else (*state, thought)

                    if flattened_state not in visit_counts:
                        visit_counts[flattened_state] = 0

                    if visit_counts[state] > visit_counts[flattened_state] and visit_counts[flattened_state] > 0:
                        ucb1_value = value + np.sqrt(2 * np.log(visit_counts[state]) / visit_counts[flattened_state])

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
