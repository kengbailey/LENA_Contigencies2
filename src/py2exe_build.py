from distutils.core import setup
import py2exe

setup_dict = dict(
    windows=[{
        'script': 'control.py',
        "icon_resources": [(1, "icon.ico")]
    }]
)

setup(**setup_dict)
setup(**setup_dict)