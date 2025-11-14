from dataclasses import dataclass
import pprint

@dataclass(frozen=True)
class Tree:
    l: object
    r: object

def all_trees(n: int) -> list[Tree | None]:
    if n == 0:
        return [None]
    ls = all_trees(n-1)
    ret = []
    for ts in ls:
        for tree in all_posible_insertions(ts):
            if tree in ret:
                continue
            ret.append(tree)
    return ret

def all_posible_insertions(t: Tree | None) -> list[Tree]:
    if t == None:
        return [Tree(None,None)]
    return [Tree(ls, t.r) for ls in all_posible_insertions(t.l)] + [Tree(t.l, rs) for rs in all_posible_insertions(t.r)]

def subsets(s: set) -> list[set]:
    if not s:
        return [set()]
    copy = s.copy()
    a = copy.pop()
    return [ss.union({a}) for ss in subsets(copy)] + [ss for ss in subsets(copy)]

def printTree(node, level=0):
    if node != None:
        printTree(node.l, level + 1)
        print(' ' * 4 * level + '-> ' + "O")
        printTree(node.r, level + 1)

if __name__ == "__main__":
    #s = {1,2,3}
    #print(subsets(s))
    for tree in all_trees(3):
        print("-"*10)
        printTree(tree)
        print("-"*10)