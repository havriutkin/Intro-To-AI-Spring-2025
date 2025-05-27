import sys

class DecisionTreeSolver:
    """
    Each table entry is a dict with:
      - 'node': unique node ID
      - 'question': text to ask at this node (absent if leaf)
      - one or more keys for possible answers,
        each mapping to the next node ID
      - OR, at a leaf node, a 'classification' key
    """

    def __init__(self, transition_table, start_node='root'):
        # build lookup by node id
        self.nodes = {entry['node']: entry for entry in transition_table}
        self.start_node = start_node

    def solve(self, input_func=input, print_func=print):
        """
        Walk the tree, asking questions until get to a classification leaf.
        """
        current = self.start_node

        while True:
            node = self.nodes.get(current)
            if node is None:
                print_func(f"[Error] Unknown node '{current}'.")
                return None

            if 'classification' in node:
                print_func(f"Result: {node['classification']}")
                return node['classification']

            question = node.get('question', '[No question specified]')

            # collect valid answer keys (exclude 'node' and 'question')
            options = [k for k in node.keys() if k not in ('node', 'question')]
            prompt = f"{question} ({'/'.join(options)}): "

            answer = input_func(prompt).strip().lower()
            if answer not in node:
                print_func(f"Invalid answer. Please choose from {options}.")
                continue

            current = node[answer]


if __name__ == '__main__':
    # Scientist inference transition table
    transition_table = [
        {
            'node': 'root',
            'question': 'What is their primary field?',
            'physics': 'physics1',
            'biology': 'biology1',
            'chemistry': 'chemistry1',
            'mathematics': 'math1',
            'computer_science': 'cs1',
            'other': 'unknown'
        },

        # Physics branch
        {
            'node': 'physics1',
            'question': 'Are they known for relativity?',
            'yes': 'einstein',
            'no': 'physics2'
        },
        {
            'node': 'physics2',
            'question': 'Are they known for laws of motion?',
            'yes': 'newton',
            'no': 'physics3'
        },
        {
            'node': 'physics3',
            'question': 'Are they a pioneer of quantum theory (e.g. black‐body radiation)?',
            'yes': 'planck',
            'no': 'physics4'
        },
        {
            'node': 'physics4',
            'question': 'Did they formulate the uncertainty principle?',
            'yes': 'heisenberg',
            'no': 'unknown'
        },

        # Biology branch
        {
            'node': 'biology1',
            'question': 'Did they propose evolution by natural selection?',
            'yes': 'darwin',
            'no': 'biology2'
        },
        {
            'node': 'biology2',
            'question': 'Are they considered the father of genetics?',
            'yes': 'mendel',
            'no': 'unknown'
        },

        # Chemistry branch
        {
            'node': 'chemistry1',
            'question': 'Did they discover radioactivity?',
            'yes': 'marie_curie',
            'no': 'chemistry2'
        },
        {
            'node': 'chemistry2',
            'question': 'Did they create the periodic table?',
            'yes': 'mendeleev',
            'no': 'unknown'
        },

        # Mathematics branch
        {
            'node': 'math1',
            'question': 'Are they known as the father of geometry?',
            'yes': 'euclid',
            'no': 'math2'
        },
        {
            'node': 'math2',
            'question': 'Did they make major contributions to number theory?',
            'yes': 'gauss',
            'no': 'math3'
        },
        {
            'node': 'math3',
            'question': 'Did they lay foundations for graph theory?',
            'yes': 'euler',
            'no': 'unknown'
        },

        # Computer Science branch
        {
            'node': 'cs1',
            'question': 'Did they invent the concept of a universal Turing machine?',
            'yes': 'turing',
            'no': 'cs2'
        },
        {
            'node': 'cs2',
            'question': 'Are they known for public‐key cryptography?',
            'yes': 'diffie_hellman',
            'no': 'unknown'
        },

        # Leaf classifications
        {'node': 'einstein',       'classification': "It's Albert Einstein"},
        {'node': 'newton',         'classification': "It's Isaac Newton"},
        {'node': 'planck',         'classification': "It's Max Planck"},
        {'node': 'heisenberg',     'classification': "It's Werner Heisenberg"},
        {'node': 'darwin',         'classification': "It's Charles Darwin"},
        {'node': 'mendel',         'classification': "It's Gregor Mendel"},
        {'node': 'marie_curie',    'classification': "It's Marie Curie"},
        {'node': 'mendeleev',      'classification': "It's Dmitri Mendeleev"},
        {'node': 'euclid',         'classification': "It's Euclid"},
        {'node': 'gauss',          'classification': "It's Carl Friedrich Gauss"},
        {'node': 'euler',          'classification': "It's Leonhard Euler"},
        {'node': 'turing',         'classification': "It's Alan Turing"},
        {'node': 'diffie_hellman', 'classification': "It's Whitfield Diffie & Martin Hellman"},
        {'node': 'unknown',        'classification': "Scientist not in database"}
    ]

    solver = DecisionTreeSolver(transition_table, start_node='root')
    solver.solve()
