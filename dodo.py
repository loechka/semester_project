
import glob
from doit.tools import create_folder

DOIT_CONFIG = {'default_tasks': ['all']}


#def task_gitclean():
#    """Clean all generated files not tracked by GIT."""
#    return {
#            'actions': ['git clean -xdf'],
#           }


def task_html():
    """Make HTML documentationi."""
    return {
            'actions': ['sphinx-build -M html docs/source build'],
           }

def task_test():
    """Preform tests."""
    yield {'actions': ['python -m unittest -v'], 'name': "run"}
#def task_test():
#    """Preform tests."""
#    yield {'actions': ['coverage run -m unittest -v'], 'name': "run"}
    
#    yield {'actions': ['coverage report'], 'verbosity': 2, 'name': "report"}


def task_pot():
    """Re-create .pot ."""
    return {
            'actions': ['pybabel extract -o game.pot Game'],
            'file_dep': glob.glob('Game/*.py'),
            'targets': ['game.pot'],
           }


def task_po():
    """Update translations."""
    return {
            'actions': ['pybabel update -D game -d po -i game.pot'],
            'file_dep': ['game.pot'],
            'targets': ['po/ru/LC_MESSAGES/game.po'],
           }


def task_mo():
    """Compile translations."""
    return {
            'actions': [
                (create_folder, ['Game/ru/LC_MESSAGES']),
                'pybabel compile -D game -l ru -i po/ru/LC_MESSAGES/game.po -d Game',
                (create_folder, ['Game/en/LC_MESSAGES']),
                'pybabel compile -D game -l en -i po/en/LC_MESSAGES/game.po -d Game'
                       ],
            'file_dep': [
                        'po/ru/LC_MESSAGES/game.po',
                        'po/en/LC_MESSAGES/game.po'
                        ],
            'targets': [
                        'Game/ru/LC_MESSAGES/game.mo',
                        'Game/en/LC_MESSAGES/game.mo'
                        ],
           }


#def task_sdist():
#    """Create source distribution."""
#    return {
#            'actions': ['python -m build -s'],
#            'task_dep': ['gitclean'],
#           }


#def task_wheel():
#    """Create binary wheel distribution."""
#    return {
#            'actions': ['python -m build -w'],
#            'task_dep': ['mo'],
#           }


def task_app():
    """Run application."""
    return {
            'actions': ['python -m Game'],
            'task_dep': ['mo'],
           }


def task_style():
    """Check style against flake8."""
    return {
            'actions': ['flake8 Game']
           }


def task_docstyle():
    """Check docstrings against pydocstyle."""
    return {
            'actions': ['pydocstyle Game']
           }


def task_check():
    """Perform all checks."""
    return {
            'actions': None,
            'task_dep': ['style', 'docstyle', 'test']
           }


def task_all():
    """Perform all build task."""
    return {
            'actions': None,
            'task_dep': [
                    'check',
                    'html',
                    #'wheel', 'req'
                    ]
           }


#def task_req():
#    """Try to calculate runtime requirements."""
#    return {
#            'actions': ['pymin_reqs -d AppBase'],
#            'verbosity': 2
#           }


#def task_buildreq():
#    """Try to calculate build requirements."""
#    return {
#            'actions': ['python BuildReq.py doit all'],
#            'task_dep': ['gitclean']
#           }


#def task_publish():
#    """Publish distros on test.pypi.org"""
#    return {
#            'task_dep': ['sdist', 'wheel'],
#            'actions': ['twine upload -u __token__ --repository testpypi dist/*'],
#            'verbosity': 2
#           }