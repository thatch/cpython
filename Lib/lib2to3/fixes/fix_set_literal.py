"""
Optional fixer to transform set() calls to set literals.
"""

# Author: Benjamin Peterson

from lib2to3 import fixer_base, pytree
from lib2to3.fixer_util import token, syms



class FixSetLiteral(fixer_base.BaseFix):

    BM_compatible = True
    explicit = True

    PATTERN = """atom_expr< 'set' trailer< '('
                     (atom=atom< '[' (items=testlist_comp< any ((',' any)* [',']) >
                                |
                                single=any) ']' >
                     |
                     atom< '(' items=testlist_comp< any ((',' any)* [',']) > ')' >
                     )
                     ')' > >
              """

    def transform(self, node, results):
        single = results.get("single")
        if single:
            # Make a fake testlist_comp
            fake = pytree.Node(syms.testlist_comp, [single.clone()])
            single.replace(fake)
            items = fake
        else:
            items = results["items"]

        # Build the contents of the literal
        literal = [pytree.Leaf(token.LBRACE, "{")]
        literal.extend(n.clone() for n in items.children)
        literal.append(pytree.Leaf(token.RBRACE, "}"))
        # Set the prefix of the right brace to that of the ')' or ']'
        literal[-1].prefix = items.next_sibling.prefix
        maker = pytree.Node(syms.dictorsetmaker, literal)
        maker.prefix = node.prefix

        # If the original was a one tuple, we need to remove the extra comma.
        if len(maker.children) == 4:
            n = maker.children[2]
            n.remove()
            maker.children[-1].prefix = n.prefix

        # Finally, replace the set call with our shiny new literal.
        return maker
