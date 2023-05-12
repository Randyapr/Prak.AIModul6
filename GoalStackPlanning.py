# base Classes
# Predicate = ON, ONTABLE, CLEAR, HOLDING, ARMEMPTY

class PREDICATE:
  def __str__(self):
    pass
    
  def __repr__(self):
    pass

  def __eq__(self, other):
    pass

  def get_action (self, world_state) :
    pass

#OPERATIONS = Stack, Unstack, Pickup, Putdown
class Operation:
  def __str__(self):
    pass

  def __repr__(self):
    pass

  def __eq__(self, other):
    pass

  def precondition(self):
    pass

  def delete(self):
    pass

  def add(self):
    pass

class ON(PREDICATE):

  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __str__(self):
    return "ON({x},{y})".format(x=self.x, y=self.y)

  def __repr__(self):
    return self.__str__()

  def __eq__(self, other):
    return self.__dict__ == other.__dict__ and self.__class__ == other.__class__

  def __hash__(self):
    return hash(str(self))

  def get_action(self, world_state):
    return StackOp (self.x, self.y)

class ONTABLE (PREDICATE):
  def __init__(self, x):
    self.x = x
  
  def __str__(self):
    return "ONTABLE({x})", format(x=self.x)

  def __repr__(self):
    return self.__str__()

  def __eq__(self, other):
    return self.__dict__ == other.__dict__ and self.__class__ == other.__class__

  def __hash__(self):
    return hash(str(self))

  def get_action(self, world_state):
    return PutdownOp(self.x)

class CLEAR(PREDICATE):
  def __init__(self, x):
    self.x = x

  def __str__(self):
    return "CLEAR({x})".format(x=self.x)
    self.x = x

  def __repr__(self):
    return self.__str__()

  def __eq__(self, other):
    return self.__dict__ == other.__dict__ and self.__class__ == other.__class__

  def __hash__(self):
    return hash(str(self))
  
  def get_action (self, world_state):
    for predicate in world_state:
      if isinstance(predicate, ON) and predicate.y == self.x:
        return UnstackOp (predicate.x, predicate.y)

    return None

class HOLDING (PREDICATE):

  def __init__(self, x):
    self.x = x
  
  def __str__(self):
    return "HOLDING({x})".format(x=self.x)

  def __repr__(self):
    return self.__str__()

  def __rq__(self, other):
    return self.__dict__ == other.__dict__ and self.__class__ == other.__class__

  def __hash___(self):
    return hash(str(self))

  def get_action(self, world_state):
    x = self.x
    if ONTABLE(x) in world_state:
      return PickupOp(x)
    else:
      for predicate in world_state:
        if isinstance(predicate, ON) and predicate.x == x:
          return UnstackOp(x, predicate.y)

class ARMEMPTY (PREDICATE):
  def __init__(self):
    pass

  def __str__(self):
    return "ARMEMPTY"

  def __repr__(self):
    return self.__str__()

  def __eq__(self, other):
    return self.__dict__ == other.__dict__ and self.__class__ == other.__class__

  def __hash__(self):
    return hash(str(self))
  
  def get_action(self, world_state=[]):
    for predicate in world_state:
      if isinstance(predicate, HOLDING):
        return PutdownOp(predicate.x)
    return None

class StackOp(Operation):
  def __init__(self, x,y):
    self.x = x
    self.y = y

  def __str__(self):
    return "STACK({x},{y})".format(x=self.x, y=self.y)

  def __repr__(self):
    return self.__str__()

  def __eq__(self, other):
    return self.__dict__ == other.__dict__ and self.__class__ == other.__class__

  def precondition(self):
    return [CLEAR(self.y), HOLDING(self.x)]

  def delete(self):
    return [CLEAR(self.y), HOLDING(self.x)]

  def add(self):
    return [ARMEMPTY (), ON(self.x, self.y)]

class UnstackOp(Operation):
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __str__(self):
    return "UNSTACK({x}, {y})".format(x=self.x, y=self.y)

  def __repr__(self):
    return self.__str__()

  def __eq__(self, other):
    return self.__dict__ == other.__dict__ and self.__class__ == other.__class__

  def precondition(self):
    return [ARMEMPTY (), ON(self.x, self.y)]

  def delete(self):
    return [ARMEMPTY (), ON (self.x, self.y)]

  def add(self):
    return [CLEAR(self.y), HOLDING(self.x)]

class PickupOp (Operation):
  def __init__(self, x):
    self.x = x

  def __str__(self):
    return "PICKUP({x})".format(x=self.x)

  def __repr__(self):
    return self.__str__()

  def __eq__(self, other):
    return self.__dict__ == other.__dict__ and self.__class__ == other.__class__

  def precondition(self):
    return [CLEAR(self.x), ONTABLE(self.x), ARMEMPTY()]

  def delete(self):
    return [ARMEMPTY(), ONTABLE(self.x)]

  def add(self):
    return [HOLDING(self.x)]

class PutdownOp (Operation):
  def __init(self,x):
    self.x = x

  def __str__(self):
    return "PUTDOWN({x})".format(x=self.x)

  def __repr__(self):
    return self.__str__()

  def __eq__(self, other):
    return self.__dict__ == other.__dict__ and self.__class__ == other.__class__

  def precondition(self):
    return [HOLDING(self.x)]

  def delete(self):
    return [HOLDING(self.x)]

  def add(self):
    return [ARMEMPTY(ONTABLE(self.x))]

  def isPredicate (obj):
    predicates = [ON, ONTABLE, CLEAR, HOLDING, ARMEMPTY]
    for predicate in predicates:
      if isinstance(obj, predicate):
        return True
    return False

  def isOperation (obj):
    operations = [StackOp, UnstackOp, PickupOp, PutdownOp]
    for operation in operations:
      if isinstance(obj, operation):
        return True
    return False

  def arm_status(world_state):
    for predicate in world_state:
      if isinstance(predicate, HOLDING):
        return predicate
    return ARMEMPTY()

class GoalStackPlanner:

  def __init__(self, initial_state, goal_state):
    self.initial_state = initial_state
    self.goal_state = goal_state

  def get_steps(self):
    # store steps
    steps = []

    #program stack
    stack = []

    #world ctate/basis pengetahuan
    world_state = self.initial_state.copy()

    #initially push the goal state as compound goal on to the stack
    stack.append(self.goal_state.copy())

    #repeat until the stack is empty
    while len(stack) !=0:
      #get the top of the stack
      stack_top = stack[-1]

      #if stack top is compound goal, push its unsatisfied goals onto stack
      if type(stack_top) is list:
        compound_goal= stack.pop()
        for goal in compound_goal:
          if goal not in world_state:
            stack.append(goal)

      elif isOperation(stack_top):
        operation = stack[-1]
        all_preconditions_satisfied = True

        #check if any precondition is unstatisfied and pus on to program stack
        for predicate in operation.delete():
          if predicate not in world_state:
            all_preconditions_statisfied = False
            stack.append(predicate)

        if all_preconditions_statisfied:
          stack.pop()
          steps.append(operation)

          for predicate in operation.delete():
            world_state.remove(predicate)
          for predicate in operation.add():
            world_state.append(predicate)
      elif stack_top in world_state:
        stack.pop()
      else:
        unsatisfied_goal = stack.pop()
        action = unsatisfied_goal.get_action(world_state)
        stack.append(action)
        for predicate in action.precondition():
          if predicate not in world_state:
            stack.append(predicate)

      return steps
if __name__ == '__main__':
  initial_state = [
      ON('B', 'A'),
      ONTABLE('A'), ONTABLE('C'), ONTABLE('D'),
      CLEAR('B'), CLEAR('C'), CLEAR('D'),
      ARMEMPTY()
  ]
  goal_state = [
      ON ('B', 'D'), ON('C', 'A'),
      ONTABLE('D'), ONTABLE('A'),
      CLEAR('B'), CLEAR('C'),
      ARMEMPTY()
  ]
  goal_stack = GoalStackPlanner(initial_state=initial_state,goal_state=goal_state)
  steps = goal_stack.get_steps()
  print(steps)
