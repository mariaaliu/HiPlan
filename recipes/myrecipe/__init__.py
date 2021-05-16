from pythonforandroid.recipe import IncludedFilesBehaviour, CppCompiledComponentsPythonRecipe
import os
import sys

class MyRecipe(IncludedFilesBehaviour, CppCompiledComponentsPythonRecipe):
    version = 'stable'
    src_filename = "../../../phase-engine"
    name = 'phase-engine'

    depends = ['setuptools']

    call_hostpython_via_targetpython = False
    install_in_hostpython = True

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        env['LDFLAGS'] += ' -lc++_shared'
        return env

recipe = MyRecipe()