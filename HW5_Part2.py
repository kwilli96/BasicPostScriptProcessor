import re

class OpStack:
    #creates an empty Stack
    def __init__(self):
        self.stack = []
        pass

    #Pops the top value of the stack and returns it
    def Pop(self):
        if len(self.stack) == 0:
            return None
        value = self.stack[-1]
        self.stack = self.stack[:-1]
        return value

    #pushes value onto the top of the stack
    def Push(self,value):
        self.stack.append(value)
        pass

    #checks if there are enough elements
    def enough(self, target):
        if len(self.stack) >= target:
            return True
        else:
            return False
    #returns a copy of the stack
    def Copy(self):
        return self.stack

    #resets the stack to nothing but an empty list
    def Clear(self):
        self.stack = []
        pass
    
    #helper function for Roll. This rotates the entire stack sent to it
    def rotate(self,l, n):
        return l[-n:] + l[:-n]

    #Actual Roll function. This sends the half of the stack being rotated to rotate. cannot spin second half of stack
    def Roll(self,top, rollVal):
        self.stack = self.rotate(self.stack[:top],rollVal) + self.stack[top:]
        pass

    #helper function to see if a dict is in stack
    #removes Dict if found and returns truth value
    def FindDict(self):
        if dict() in self.stack:
            self.stack.remove(dict())
            return True
        else:
            return False

class DictStack:
    #Creates and empty stack
    def __init__(self):
        self.stack = []
        pass

    #removes the most recent dict from the list and returns it
    def Pop(self):
        value = self.stack[-1]
        self.stack = self.stack[:-1]
        return value

    #Pushes a new dict onto the top of the stack. Only send an empty dict() to this
    def Push(self,value):
        self.stack.append(value)
        pass

    #Didn't realize how inappropriate this sounded until after I implemented it into my program.
    #I'll change in part 2
    #Adds the ElementValue to the dict at specified ElementName
    def Add2HotDict(self,ElementName, ElementValue):
        self.stack[-1][ElementName] = ElementValue
        pass

    #Again I will be changing this at some point
    #Just shows the element in the current dictionary
    def LookAtHotDictElement(self,element):
        return self.stack[-1].get(element, None)

class PostFix:
    #creates base _OpStack and _DictStack then adds first dict() to _DictStack
    def __init__(self):
        self._OpStack = OpStack()
        self._DictStack = DictStack()
        self._DictStack.Push(dict())
        pass

    #finds whether value is string or integer then returns the itn value of it
    def EvalValue(self, value):
        if value is str:
            return self._DictStack.LookAtHotDictElement(value)
        else:
            return value

    #these are the arithmitic operators and comparators: add, sub, mul, div, eq, lt, gt
    #They all do basically the same thing:
        #First they pop the topmost 2 values and performs the operation on them.
        #Then They push that new value to the top of the stack
    def Add(self):
        if self._OpStack.enough(2):
            first = self.EvalValue(self._OpStack.Pop())
            second = self.EvalValue(self._OpStack.Pop())
            self._OpStack.Push(second + first)
        pass
    def Sub(self):
        if self._OpStack.enough(2):
            first = self.EvalValue(self._OpStack.Pop())
            second = self.EvalValue(self._OpStack.Pop())
            self._OpStack.Push(first - second)
        pass
    def Mul(self):
        if self._OpStack.enough(2):
            first = self.EvalValue(self._OpStack.Pop())
            second = self.EvalValue(self._OpStack.Pop())
            self._OpStack.Push(first*second)
        pass
    def Div(self):
        if self._OpStack.enough(2):
            first = self.EvalValue(self._OpStack.Pop())
            second = self.EvalValue(self._OpStack.Pop())
            self._OpStack.Push(first/second)
        pass
    def eq(self):
        if self._OpStack.enough(2):
            first = self.EvalValue(self._OpStack.Pop())
            second = self.EvalValue(self._OpStack.Pop())
            self._OpStack.Push(first == second)
        pass
    def lt(self):
        if self._OpStack.enough(2):
            first = self.EvalValue(self._OpStack.Pop())
            second = self.EvalValue(self._OpStack.Pop())
            self._OpStack.Push(first < second)
        pass
    def gt(self):
        if self._OpStack.enough(2):
            first = self.EvalValue(self._OpStack.Pop())
            second = self.EvalValue(self._OpStack.Pop())
            self._OpStack.Push(first > second)
        pass
    #this is the end of the arithmitic operators and comparators.

    #string Operators
    #I don't really know the purpose of these
    def length(self):
        pass
    def get(self):
        pass
    def getinterval(self):
        pass
    
    #boolean Operators
    #all Operators Pop the topmost two values from _OpStack and checks for truth value of them
    #psAnd requires both to be true for true
    def psAnd(self):
        if self._OpStack.enough(2):
            first = self.EvalValue(self._OpStack.Pop())
            second = self.EvalValue(self._OpStack.Pop())
            self._OpStack.Push((first and second))
        pass
    #psOr requires one to be true for true
    def psOr(self):
        if self._OpStack.enough(2):
            first = self.EvalValue(self._OpStack.Pop())
            second = self.EvalValue(self._OpStack.Pop())
            self._OpStack.Push((first or second))
        pass
    #Not reverses truth value of top element
    def psNot(self):
        if self._OpStack.enough(1):
            first = self.EvalValue(self._OpStack.Pop())
            self._OpStack.Push(not first)
        pass
    
    #OpStack manipulation Operators
    #duplicates top element and and pushes onto the stack twice
    def dup(self):
        if self._OpStack.enough(1):
            element = self._OpStack.Pop()
            self._OpStack.Push(element)
            self._OpStack.Push(element)
        pass
    #Exchange flips the top two elements
    def exch(self):
        if self._OpStack.enough(2):
            first = self._OpStack.Pop()
            second = self._OpStack.Pop()
            self._OpStack.Push(first)
            self._OpStack.Push(second)
        pass
    #Pops/pushes the _OpStack and returns it (Meant for testing since _OpStack has built in Pop()/Push() function)
    def OpPop(self):
        return self._OpStack.Pop()

    def OpPush(self, value):
        self._OpStack.Push(value)

    #Will roll _OpStack and permanently alter its configuration.
    #top is split index and amount is index change distance
    def roll(self, top, amount):
        self._OpStack.Roll(top, amount)
        pass
    
    #returns a copy of _OpStack
    def Copy(self):
        return self._OpStack.Copy()

    #Clears _OpStack of all values
    def Clear(self):
        self._OpStack.Clear()
        pass

    #Prints out the entire _OpStack
    def stack(self):
        print("--Top of Stack--")
        for item in self._OpStack.stack:
            print(item)
        print("--Bottom of Stack--")
        pass
    
    #dict manipulation operators
    #adds new dict to _OpStack
    def psDict(self):
        if self._OpStack.enough(1):
            self._OpStack.Pop()
            self._OpStack.Push(dict())
        pass

    #Makes an empty Dict the new current Dict
    def Begin(self):
        if self._OpStack.FindDict():
            self._OpStack.Pop()
            self._DictStack.Push(dict())
        pass

    #Remvoes the Current Dict regardless of dicts remaining
    def End(self):
        self._DictStack.Pop()
        pass

    #defines a value in the current dict
    def psDef(self):
        if self._OpStack.enough(2):
            value = self._OpStack.Pop()
            variable= self._OpStack.Pop()
            self._DictStack.Add2HotDict(variable[1:], value)
        pass

    def DictLookUp(self, ElementName):
        return self._DictStack.LookAtHotDictElement(ElementName)

    #everything past here is for testing the functions
    #NOTE: OpPop() and OpPush() are not tested explicitly since they are used in all testing functions
    #NOTE2: psDef(), psDict(), Begin(), and End() are all tested in psDef() the rest just print succeded
"""    def RunTest(self):
        self.TestEverything()
        pass

    def TestpsDef(self):
        self.OpPush(1) #the number of dicts to add
        self.psDict()
        self.Begin()
        self.OpPush("\\y")
        self.OpPush(3)
        self.psDef()
        value = self.DictLookUp("y")
        self.End()
        newvalue = self.DictLookUp("y")
        if value != newvalue:
            return "Succeeded"
        else:
            return "Failed"
    def Testdup(self):
        self.OpPush(3)
        self.dup()
        if self.OpPop() == 3 and self.OpPop() == 3:
            return "Succeeded"
        else:
            return "Failed"
    def Testexch(self):
        self.OpPush(1)
        self.OpPush(2)
        self.exch()
        if self.OpPop() == 1:
            return "Succeeded"
        else:
            return "Failed"
    def TestRoll(self):
        self.OpPush(1)
        self.OpPush(2)
        self.OpPush(3)
        self.OpPush(4)
        self.OpPush(5)
        self.OpPush(6)
        self.roll(3,2)
        if self.Copy() == [2,3,1,4,5,6]:
            return "Succeeded"
        else:
            return "Failed"
    def TestCopy(self):
        self.OpPush(1)
        self.OpPush(2)
        self.OpPush(3)
        if self.Copy() == [1,2,3]:
            return "Succeeded"
        else:
            return "Failed"
    def TestClear(self):
        self.OpPush(1)
        self.OpPush(2)
        self.OpPush(3)
        self.OpPush(4)
        self.Clear()
        if self.OpPop() == None:
            return "Succeeded"
        else:
            return "Failed"
    def TestStack(self):
        return "Succeeded"
    def TestpsAnd(self):
        self.OpPush(True)
        self.OpPush(False)
        self.psAnd()
        if self.OpPop() == False:
            return "Succeeded"
        else:
            return "Failed"
    def TestpsOr(self):
        self.OpPush(True)
        self.OpPush(False)
        self.psOr()
        if self.OpPop() == True:
            return "Succeeded"
        else:
            return "Failed"
    def TestpsNot(self):
        self.OpPush(True)
        self.psNot()
        self.OpPush(False)
        self.psNot()
        if self.OpPop() == True and self.OpPop() == False:
            return "Succeeded"
        else:
            return "Failed"
    def TestLength(self):
        return "Didn't know what to test"
    def TestGet(self):
        return "Didn't know what to test"
    def TestGetInterval(self):
        return "Didn't know what to test"
    def TestAdd(self):
        self.OpPush(1)
        self.OpPush(2)
        self.Add()
        self.OpPush(-1)
        self.OpPush(5)
        self.Add()
        self.Add()
        if self.OpPop() == 7:
            return "Succeeded"
        else:
            return "Failed"
    def TestSub(self):
        self.OpPush(1)
        self.OpPush(2)
        self.Sub()
        self.OpPush(-3)
        self.OpPush(5)
        self.Sub()
        self.Sub()
        if self.OpPop() == 7:
            return "Succeeded"
        else:
            return "Failed"
    def TestMul(self):
        self.OpPush(1)
        self.OpPush(2)
        self.Mul()
        self.OpPush(3)
        self.OpPush(5)
        self.Mul()
        self.Mul()
        if self.OpPop() == 30:
            return "Succeeded"
        else:
            return "Failed"
    def TestDiv(self):
        self.OpPush(1)
        self.OpPush(2)
        self.Div()
        self.OpPush(-1)
        self.OpPush(5)
        self.Div()
        self.Div()
        if self.OpPop() == -2.5:
            return "Succeeded"
        else:
            return "Failed"
    def Testeq(self):
        self.OpPush(2)
        self.OpPush(2)
        self.eq()
        self.OpPush(3)
        self.OpPush(5)
        self.eq()
        if self.OpPop() == False and self.OpPop() == True:
            return "Succeeded"
        else:
            return "Failed"
            
    def Testlt(self):
        self.OpPush(1)
        self.OpPush(0)
        self.lt()
        self.OpPush(1)
        self.OpPush(1)
        self.lt()
        if self.OpPop() == False and self.OpPop() == True:
            return "Succeeded"
        else:
            return "Failed"
    def Testgt(self):
        self.OpPush(0)
        self.OpPush(1)
        self.gt()
        self.OpPush(1)
        self.OpPush(1)
        self.gt()
        if self.OpPop() == False and self.OpPop() == True:
            return "Succeeded"
        else:
            return "Failed"

    
    def TestEverything(self):
        functionList = {"psDef":self.TestpsDef,"dup":self.Testdup,"exch":self.Testexch,
                        "Roll":self.TestRoll,"Copy":self.TestCopy,"Clear":self.TestClear,"Stack":self.TestStack,"psAnd":self.TestpsAnd,
                        "psOr":self.TestpsOr,"psNot":self.TestpsNot,"Length":self.TestLength,"Get":self.TestGet,"GetInterval":self.TestGetInterval,
                        "Add":self.TestAdd,"Sub":self.TestSub,"Mul":self.TestMul,"Div":self.TestDiv,"eq":self.Testeq,"lt":self.Testlt,"gt":self.Testgt}
        for item in functionList:
            self.Clear()
            print(item, end="")
            for i in range(11-len(item)):
                print(" ", end="")
            print(": ", functionList[item](), sep="")
        
        pass
"""
class Interpreter:
    def __init__(self, s):
        self.tokens = self.Tokenize(s)
        print(self.tokens)
        self.tokens = self.Parse(self.tokens)
        print(self.tokens)
        pass
    
    def Tokenize(self, s):
        return re.findall("/?[a-zA-Z()][a-zA-Z0-9_()]*|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]", s)
    
    def Parse(self, lt):
        res = []
        CurlyLocations = []
        i = 0
        while i < len(lt):
            if lt[i] == '{':
                CurlyLocations.append(i)
            elif lt[i] == '}':
                start = CurlyLocations[-1]
                CurlyLocations = CurlyLocations[:-1]
                res[start:i] = [res[start:i]]
            else:
                res.append(lt[i])
            i += 1

        return res
              
        

#This just creates the postfix class and runs the tests
if __name__ == '__main__':
   TestVar = Interpreter(
    """
    (facto) dup length /n exch def
    /fact {
    0 dict begin
    /n exch def
    n 2 lt
    { 1}
    {n 1 sub fact n mul }
    ifelse
    end
    } def
    n fact stack 
    """)

    
    #tester = PostFix()   
    #tester.RunTest()

    
        
        
    
