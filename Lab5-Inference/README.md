# Decision Tree Inference Engine

This repository provides a **generic decision-tree solver** written in Python.  Given a simple “transition table” defining questions and answer-branches, the engine will ask you questions and follow the tree until it reaches a final classification.  In my example, it “guesses” a scientist based on your answers.

## How It Works

1. **Build a lookup.**  
    The solver reads your transition table (a list of dicts) and indexes them by their `"node"` ID.  
2. **Start at the root.**  
    It begins at the `start_node` (default `"root"`).  
3. **Ask a question.**  
    At each non-leaf node, it prints the `"question"` and the valid answer keys.  
4. **Validate input.**  
    If you type an answer that isn’t in the node’s keys, it prompts you again.  
5. **Follow the branch.**  
    Your answer maps to the next node ID.  The solver repeats steps 3–5.  
6. **Reach a leaf.**  
    A node with a `"classification"` key is a leaf.  The solver prints the result and exits.

---

## Transition Table Format

Each entry in the table is a Python dict:

- **Decision node**  
    ```python
        {
            'node': 'unique_id',
            'question': 'Your yes/no or multiple-choice question?',
            'yes': 'next_node_if_yes',
            'no':  'next_node_if_no',
            # …or any other answer keys…
        }
    ```
- **Leaf node**  
    ```python
        {
            'node': 'some_leaf_id',
            'classification': "Final result string"
        }
    ```


