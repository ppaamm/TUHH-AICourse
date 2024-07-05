class FST():
    
    def __init__(self, transitions, terminal_states):
        # Transitions are quadruple (source_node, target_node, input_char, output_char)
        self.transitions = transitions
        self.terminal_states = terminal_states
        
    
    def generate(self, initial_node = 0, input_tape = "", output_tape = ""):  
        results = []
        
        if initial_node in self.terminal_states:
            results.append( (input_tape, output_tape))
        
        for transition in self.transitions:
            if transition[0] == initial_node:
                trans_input = input_tape + transition[2]
                trans_output = output_tape + transition[3]
                for end_solutions in self.generate(transition[1], trans_input, trans_output):
                    results.append(end_solutions)
        return results
    

transitions = { (0, 1, 'a', 'b'), 
                (1, 2, 'a', 'b'),
                (1, 3, 'c', 'd')}
terminal_states = { 1, 2 }


fst = FST(transitions, terminal_states)

                    
                
        
        

