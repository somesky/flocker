# Copyright Hybrid Logic Ltd.  See LICENSE file for details.

"""
Sphinx extension to add directives to allow files and code to include the
latest installable version of Flocker.
"""

from sphinx.directives.code import CodeBlock, LiteralInclude
from sphinx.roles import XRefRole

from flocker import __version__ as version
from flocker.docs import get_installable_version

from sphinx import addnodes
from sphinx.util import ws_re

PLACEHOLDER = u'|latest-installable|'


def remove_extension(template):
    """
    Given a filename or path of a template file, return the same without the
    template suffix.

    :param unicode template: The filename of or path to a template file which
        ends with '.template'.
    :return: The given filename or path without the '.template' suffix.
    """
    return template[:-len('.template')]


def make_changed_file(rel_filename):
    """
    Given the relative filename of a template file, write a new file with:
        * The same filename, except without '.template' at the end.
        * A placeholder in the new file changed to the latest installable
          version of Flocker.

    :param unicode rel_filename: The relative filename of a template file.
    """
    latest = get_installable_version(version)
    new_rel_filename = remove_extension(rel_filename)
    with open(rel_filename, 'r') as templated_file:
        with open(new_rel_filename, 'w') as new_file:
            new_file.write(templated_file.read().replace(PLACEHOLDER, latest))


class VersionDownload(XRefRole):
    """
    Similar to downloadable files, but:
        * Replaces a placeholder in the downloadable file with the latest
          installable version of Flocker.
        * Replaces the download link with one which strips '.template' from the
          end of the file name.
    """
    nodeclass = addnodes.download_reference

    def process_link(self, env, refnode, has_explicit_title, title, target):
        rel_filename, filename = env.relfn2path(target)
        make_changed_file(rel_filename)
        return (remove_extension(title),
                ws_re.sub(' ', remove_extension(target)))


class VersionLiteralInclude(LiteralInclude):
    """
    Similar to LiteralInclude but replaces a placeholder with the latest
    installable version of Flocker.
    """
    def run(self):
        document = self.state.document
        env = document.settings.env
        rel_filename, filename = env.relfn2path(self.arguments[0])
        make_changed_file(rel_filename)
        self.arguments[0] = remove_extension(self.arguments[0])

        return LiteralInclude.run(self)


class VersionCodeBlock(CodeBlock):
    """
    Similar to CodeBlock but replaces a placeholder with the latest installable
    version of Flocker.

    Usage example:

    .. version-code-block:: console

       $ brew install flocker-|latest-installable|
    """
    def run(self):
        latest = get_installable_version(version)
        self.content = [item.replace(PLACEHOLDER, latest) for
                        item in self.content]
        return CodeBlock.run(self)


def setup(app):
    app.add_directive('version-code-block', VersionCodeBlock)
    app.add_directive('version-literalinclude', VersionLiteralInclude)
    app.add_role('version-download', VersionDownload())
