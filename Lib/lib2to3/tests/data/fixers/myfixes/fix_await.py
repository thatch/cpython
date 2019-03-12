from lib2to3.fixer_base import BaseFix
from lib2to3.fixer_util import Name

class FixAwait(BaseFix):
    """
    Find calls to await and change their target.
    """

    PATTERN = """power < [AWAIT] name='b' any* >"""

    def transform(self, node, results):
        name = results["name"]
        name.replace(Name("bar", name.prefix))
