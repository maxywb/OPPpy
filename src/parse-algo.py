Operator Precedence Parsing

Having precedence relations allows to identify handles as follows:[7]

    scan the string from left until seeing •>
    scan backwards (from right to left) over any =• until seeing <•
    everything between the two relations <• and •>, including any intervening or surrounding nonterminals, forms the handle

It is generally not necessary to scan the entire sentential form to find the handle.
[edit] Operator Precedence Parsing Algorithm[8]


***********************************************************************************************
***********************************************************************************************
***********************************************************************************************


Initialize: Set ip to point to the first symbol of w$
Repeat:
  If $ is on the top of the stack and ip points to $ then return
  else
    Let a be the top terminal on the stack, and b the symbol pointed to by ip
    if a <• b or a =• b then
      push b onto the stack
      advance ip to the next input symbol
    else if a •> b then
      repeat
        pop the stack
      until the top stack terminal is related by <• to the terminal most recently popped
    else error()
  end
******************************************************************************
ip = FIRST_INPUT_SYMBOL

while True:
    # ending condition
    if EOF is TOP_OF_STACK and IP == EOF:
        return
    
    else:
        a = TOP_OF_STACK
        b = ip
        if a <. b or a=. b:
            PUSH_ONTO_STACK(b)
            ip = NEXT_INPUT_SYMBOL
        else if a .> b:
            next = TOP_OF_STACK
            while not a <. next:
                next = POP_STACK()
        else:
            raise error
#end
        

def asdf(stack):

     # make the node
        node = TreeNode()
        token = orderedTokens.pop()
        node.type = token.type
        node.value = token.value
        
        # if the node is a terminal, return
        if IS_TERMINAL(node):
            return node
        
        else:
            node.right = recurse(stack)
            node.left = recurse(stack)
