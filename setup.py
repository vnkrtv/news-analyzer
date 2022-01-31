import os
from importlib.machinery import SourceFileLoader
from typing import List

from pkg_resources import parse_requirements
from setuptools import find_packages, setup

module_name = 'yaps'

module = SourceFileLoader(
    module_name, os.path.join(module_name, '__init__.py')
).load_module()


def load_requirements(filename: str) -> List[str]:
    requirements = []
    with open(filename, 'r') as fp:
        for req in parse_requirements(fp.read()):
            extras = '[{}]'.format(','.join(req.extras)) if req.extras else ''
            requirements.append(
                '{}{}{}'.format(req.name, extras, req.specifier)
            )
    return requirements


setup(
    name=module_name,
    version=module.__version__,
    author=module.__author__,
    email=module.__email__,
    license=module.__license__,
    description=module.__doc__,
    long_description=open('README.md').read(),
    platforms='all',
    python_requires='>=3.8',
    packages=find_packages(exclude=['tests']),
    install_requires=load_requirements('requirements.txt'),
    extras_require={'dev': load_requirements('requirements.dev.txt')},
    entry_points={
        'console_scripts': [
            '{0}-api = {0}.__main__:main'.format(module_name),
            '{0}-db = {0}.db.__main__:main'.format(module_name),
            '{0}-init-es = {0}.es.__main__:main'.format(module_name),
            '{0}-read-nginx-logs = {0}.utils.log_parser.__main__:main'.format(module_name)
        ]
    },
    include_package_data=True
)
