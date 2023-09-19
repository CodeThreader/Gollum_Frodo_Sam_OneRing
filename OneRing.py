import numpy as np
class AI_Agent:
  
  initial_state = np.array([[1,0],[1,0],[1,0],[1,0]])
  goal_state = np.array([[0,1],[0,1],[0,1],[0,1]])
  legal_moves = [(0, 0, 1, 1), (1,0,1,0), (0, 1, 1,0), (0, 0, 1,0)]
  traversed_states = []
  
  def get_meaningful_moves(self, state):

    # These two lines is nothing else but the means-ends method. 
    # No need to try other combinations when the ring waits to be picked up.
      if state[0][0] == state[1][0] == state[2][0] ==0 and state[3][0] == 1:
          return [(0, 0, 1,0)]

      # Riverbank on the left == 0;   
      riverbank = 1 - state[2][0]
          
      remaining_legal_moves = self.legal_moves.copy()
      if state[0][riverbank] == 0:
        remaining_legal_moves.remove((1,0,1,0))
      if state[1][riverbank] == 0:
        remaining_legal_moves.remove((0,1,1,0)) 
      if state[3][riverbank] == 0:
        remaining_legal_moves.remove((0,0,1,1))              
              

      return remaining_legal_moves 
          
      
      
  def __init__(self):
    self.name = "AI agent for Gollum, Frodo, Sam and the One Ring."

    # Creating variables for easier understanding when refering to numpy matrix.
    self.Gollum = 0
    self.Frodo = 1
    self.Sam = 2
    self.One_Ring = 3
    
    self.left = 1
    self.right = 0    
    
    # All possible legal problems states are generated and stored before the agent start traversing.
    # This will avoid for the agent to travers in funny states by mistakes.
    self.legal_states = []
    
    
    self.generate_states_smartly()
    
   
  def is_legal_state(self, state):
      result = True

      # The ring is either with Sam or alone, regardless what side of the river.
      for riverbank in [self.left, self.right]:
        if state[self.One_Ring][riverbank] == 1 and state[self.Sam][riverbank] == 0:
            if state[self.Gollum][riverbank] == 1 or state[self.Frodo][riverbank] == 1:
                return False
          
      return result
    

  def generate_states_smartly(self):
      # Gollum = g
      # Frodo = f
      # Sam = s
      # One Ring = 0

      ones_state = [self.left, self.right]
      
      for g in ones_state:
          for f in ones_state:
              for s in ones_state:
                  for o in ones_state:
                      temp_state =  np.zeros((4,2))
                      temp_state[0][0] = g
                      temp_state[0][1] = 1 - g
                      temp_state[1][0] = f
                      temp_state[1][1] = 1 - f
                      temp_state[2][0] = s
                      temp_state[2][1] = 1 - s
                      temp_state[3][0] = o
                      temp_state[3][1] = 1 - o    
                      
                      if self.is_legal_state(temp_state):
                        self.legal_states.append(temp_state)                                                           
                      
  def move_to_matrix(self, legal_move):
      result = np.zeros((4,2))
      one_of_them = 0
      for status in legal_move:
          for riverbank in [self.left, self.right]:
              result[one_of_them][riverbank] = status
          one_of_them += 1
      return result
          

              
  def state_found_in_states(self, state, states):
      result = False
      for temp_state in states:
          if (state == temp_state).all():
              return True          
      return result
  
           
  def cross_river(self):
      temp_state = self.initial_state
      self.traversed_states.append(temp_state)

      # Safe-guard loop.
      loop = 0
      while (temp_state != self.goal_state).any():
          loop +=1
          prefered_legal_moves = self.get_meaningful_moves(temp_state)
          for legal_move in prefered_legal_moves:
              xor_matrix = self.move_to_matrix(legal_move)
              next_state = np.array((temp_state != xor_matrix),dtype=bool).astype(int)
              if not self.state_found_in_states(next_state, self.traversed_states):
                  if  self.state_found_in_states(next_state, self.legal_states):
                      temp_state = next_state
                      self.traversed_states.append(temp_state)
                      print(legal_move)
                      #print(temp_state)
                      break
                  else:
                      continue
                  
          if loop > 1000:
              print("Maxed out!")          
              break
      
      if loop <= 1000:
        print("Final state reached:")
        print(temp_state)  
              
    
      

if __name__ == "__main__":
    one_ring_agent = AI_Agent()
    one_ring_agent.cross_river()
