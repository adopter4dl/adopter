import ast, astunparse, re
import copy

import gast

from pattern_matcher import unparse_attribute


class refactorHelper(object):
    def __init__(self, rules):
        self.rules = []
        self.arg_dict = {}
        for rule in rules:
            self.rules.append(Rule(rule, self.arg_dict))

        dest_alias_map = {}
        if len(self.rules) > 1:
            rule0 = self.rules[0]
            rule1 = self.rules[1]
            for dest_pattern in rule1.destPatterns:
                if isinstance(dest_pattern.output, list):
                    continue
                else:
                    dest_alias_map[dest_pattern.functionCall.functionId.id] = dest_pattern.output.value
            for dest_pattern in rule0.destPatterns:
                if dest_pattern.functionCall.functionId.id in dest_alias_map:
                    if '$' in dest_alias_map[dest_pattern.functionCall.functionId.id]:
                        dest_pattern.functionCall.functionId.is_variable = True
                    dest_pattern.functionCall.functionId.id = dest_alias_map[dest_pattern.functionCall.functionId.id]

            for pi, src_pattern in enumerate(rule0.srcPatterns):
                if pi < len(rule1.srcPatterns):
                    src_pattern.functionCall.definition = rule1.srcPatterns[pi].functionCall
            for pi, dest_pattern in enumerate(rule0.destPatterns):
                if pi < len(rule1.destPatterns):
                    dest_pattern.functionCall.definition = rule1.destPatterns[pi].functionCall


class Rule(object):
    def __init__(self, rule, arg_dict):
        self.srcPatterns = []
        self.destPatterns = []
        self.arg_dict = arg_dict
        self.detect_only = False
        self.in_order = False

        src, dest = rule.split('=>')
        for src_assignment in src.split(';'):
            if src_assignment.strip() == "<any_assignment>":
                self.srcPatterns.append("<any_assignment>")
            else:
                assignment = Assignment(src_assignment.strip(), self)
                if assignment.functionCall.functionId.in_order:
                    self.in_order = True
                self.srcPatterns.append(assignment)
        if dest.strip() == "_":
            self.detect_only = True
            return
        for dest_assignment in dest.split(';'):
            self.destPatterns.append(Assignment(dest_assignment.strip(), self))

    def clear_arg_dict(self):
        for idx in self.arg_dict:
            self.arg_dict[idx] = None

    def setArg(self, arg, val):
        self.arg_dict[arg] = val

    def unorderedPatternMatch(self, call_statements, alias_map, ablation):
        if len(call_statements) < len(self.srcPatterns):
            return None, None
        match = self.unorderedSubSequenceMatch(call_statements, alias_map, ablation)
        if match:
            return match, copy.deepcopy(self.arg_dict)
        else:
            return None, None

    def patternMatch(self, call_statements):
        # self.clear_arg_dict()
        locations = []
        if len(call_statements) < len(self.srcPatterns):
            return locations
        for i in range(len(call_statements) - len(self.srcPatterns) + 1):
            if self.subSequenceMatch(call_statements[i: i + len(self.srcPatterns)]):
                locations.append((i, i + len(self.srcPatterns), copy.deepcopy(self.arg_dict)))
                return locations
        return locations


class FunctionCall(object):
    def __init__(self, func_call, rule):
        self.functionId = None
        self.arguments = []
        self.keywords = []
        self.definition = None
        self.Rule = rule

        parse = re.split(r'[(,)]', func_call)
        if '+' in parse[0]:
            self.functionId = function_Id('Add')
            self.arguments.append(Argument(parse[0].split('+')[0].strip(), self.Rule))
            self.arguments.append(Argument(parse[0].split('+')[1].strip(), self.Rule))
            return

        self.functionId = function_Id(parse[0])
        if len(parse) == 1:
            return
        for arg in parse[1:-1]:
            if '=' in arg:
                self.keywords.append(Keyword(arg.strip(), self.Rule))
            else:
                self.arguments.append(Argument(arg.strip(), self.Rule))


class Keyword(object):
    def __init__(self, argument, rule):
        self.key = ''
        self.argument = None
        self.Rule = rule

        key, arg = argument.split('=')
        self.key = key.strip()
        self.argument = Argument(arg.strip(), self.Rule)


class Argument(object):
    def __init__(self, argument, rule):
        self.assigned = False
        self.variable = None
        self.value = None
        self.Rule = rule

        # check if there is a substring starting with '$' using regex
        self.variable = re.findall(r'\$[a-zA-Z_][a-zA-Z0-9_]*', argument)
        if self.variable:
            self.assigned = False
        else:
            self.assigned = True

        if not self.assigned:
            for arg in self.variable:
                self.Rule.setArg(arg, None)
        self.value = argument


class function_Id(object):
    def __init__(self, func_id):
        if func_id.startswith('@'):
            self.id = func_id[1:]
            self.in_order = False
        else:
            self.id = func_id
            self.in_order = True
        self.is_variable = False


def main():
    pass


"""
All the methods were generated based on the list of nodes from the
"Green Tree Snakes" guide:
https://greentreesnakes.readthedocs.io/en/latest/index.html
"""

import ast


class Visitor(ast.NodeVisitor):

    def visit_Num(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Str(self, node):
        print(node)
        self.generic_visit(node)

    def visit_FormattedValue(self, node):
        print(node)
        self.generic_visit(node)

    def visit_JoinedStr(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Bytes(self, node):
        print(node)
        self.generic_visit(node)

    def visit_List(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Tuple(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Set(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Dict(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Ellipsis(self, node):
        print(node)
        self.generic_visit(node)

    def visit_NameConstant(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Name(self, node):
        print(node)
        print(node.id)
        self.generic_visit(node)

    def visit_Load(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Store(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Del(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Starred(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Expr(self, node):
        print(node)
        self.generic_visit(node)

    def visit_UnaryOp(self, node):
        print(node)
        self.generic_visit(node)

    def visit_UAdd(self, node):
        print(node)
        self.generic_visit(node)

    def visit_USub(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Not(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Invert(self, node):
        print(node)
        self.generic_visit(node)

    def visit_BinOp(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Add(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Sub(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Mult(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Div(self, node):
        print(node)
        self.generic_visit(node)

    def visit_FloorDiv(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Mod(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Pow(self, node):
        print(node)
        self.generic_visit(node)

    def visit_LShift(self, node):
        print(node)
        self.generic_visit(node)

    def visit_RShift(self, node):
        print(node)
        self.generic_visit(node)

    def visit_BitOr(self, node):
        print(node)
        self.generic_visit(node)

    def visit_BitXor(self, node):
        print(node)
        self.generic_visit(node)

    def visit_BitAnd(self, node):
        print(node)
        self.generic_visit(node)

    def visit_MatMult(self, node):
        print(node)
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        print(node)
        self.generic_visit(node)

    def visit_And(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Or(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Compare(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Eq(self, node):
        print(node)
        self.generic_visit(node)

    def visit_NotEq(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Lt(self, node):
        print(node)
        self.generic_visit(node)

    def visit_LtE(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Gt(self, node):
        print(node)
        self.generic_visit(node)

    def visit_GtE(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Is(self, node):
        print(node)
        self.generic_visit(node)

    def visit_IsNot(self, node):
        print(node)
        self.generic_visit(node)

    def visit_In(self, node):
        print(node)
        self.generic_visit(node)

    def visit_NotIn(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Call(self, node):
        print(node)
        self.generic_visit(node)

    def visit_keyword(self, node):
        print(node)
        self.generic_visit(node)

    def visit_IfExp(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Subscript(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Index(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Slice(self, node):
        print(node)
        self.generic_visit(node)

    def visit_ExtSlice(self, node):
        print(node)
        self.generic_visit(node)

    def visit_ListComp(self, node):
        print(node)
        self.generic_visit(node)

    def visit_SetComp(self, node):
        print(node)
        self.generic_visit(node)

    def visit_GeneratorExp(self, node):
        print(node)
        self.generic_visit(node)

    def visit_DictComp(self, node):
        print(node)
        self.generic_visit(node)

    def visit_comprehension(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Assign(self, node):
        print(node)
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        print(node)
        self.generic_visit(node)

    def visit_AugAssign(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Print(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Raise(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Assert(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Delete(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Pass(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Import(self, node):
        print(node)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        print(node)
        self.generic_visit(node)

    def visit_alias(self, node):
        print(node)
        self.generic_visit(node)

    def visit_If(self, node):
        print(node)
        self.generic_visit(node)

    def visit_For(self, node):
        print(node)
        self.generic_visit(node)

    def visit_While(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Break(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Continue(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Try(self, node):
        print(node)
        self.generic_visit(node)

    def visit_TryFinally(self, node):
        print(node)
        self.generic_visit(node)

    def visit_TryExcept(self, node):
        print(node)
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        print(node)
        self.generic_visit(node)

    def visit_With(self, node):
        print(node)
        self.generic_visit(node)

    def visit_withitem(self, node):
        print(node)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Lambda(self, node):
        print(node)
        self.generic_visit(node)

    def visit_arguments(self, node):
        print(node)
        self.generic_visit(node)

    def visit_arg(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Return(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Yield(self, node):
        print(node)
        self.generic_visit(node)

    def visit_YieldFrom(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Global(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Nonlocal(self, node):
        print(node)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        print(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Await(self, node):
        print(node)
        self.generic_visit(node)

    def visit_AsyncFor(self, node):
        print(node)
        self.generic_visit(node)

    def visit_AsyncWith(self, node):
        print(node)
        self.generic_visit(node)


SOURCE = """
def hello(msg):
    a, b = hello(hello(a))
"""

if __name__ == "__main__":
    root = ast.parse(SOURCE)
    visitor = Visitor()
    visitor.visit(root)




if __name__ == '__main__':
    main()
