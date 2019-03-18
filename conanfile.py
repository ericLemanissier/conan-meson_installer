#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
import os


class MesonInstallerConan(ConanFile):
    name = "meson_installer"
    version = "0.50.0"
    description = "Meson is a project to create the best possible next-generation build system"
    topics = ("conan", "meson", "mesonbuild", "build-system")
    url = "https://github.com/bincrafters/conan-meson_installer"
    homepage = "https://github.com/mesonbuild/meson"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "	Apache-2.0"
    no_copy_source = True
    exports = ["LICENSE.md", "5111.diff"]
    requires = "ninja_installer/1.8.2@bincrafters/stable"
    _source_subfolder = "source_subfolder"
    _meson_cmd = """@echo off
CALL python %~dp0/meson.py %*
"""
    _meson_sh = """#!/usr/bin/env bash
meson_dir=$(dirname "$0")
exec "$meson_dir/meson.py" "$@"
"""

    def source(self):
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version),
                  sha256="a2f425cb9133c43b35d74ee68ae55a53f1baa727a3fcddf1c664f46245781a05")
        extracted_dir = "meson-" + self.version
        self.run("dir")
        os.rename(extracted_dir, self._source_subfolder)

        # create wrapper scripts
        with open(os.path.join(self._source_subfolder, "meson.cmd"), "w") as f:
            f.write(self._meson_cmd)
        with open(os.path.join(self._source_subfolder, "meson"), "w") as f:
            f.write(self._meson_sh)
        tools.patch(self._source_subfolder, "5111.diff")

    @staticmethod
    def _chmod_plus_x(filename):
        if os.name == 'posix':
            os.chmod(filename, os.stat(filename).st_mode | 0o111)

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="*", dst=".", src=self._source_subfolder)

    def package_info(self):
        meson_root = self.package_folder
        self.output.info('Appending PATH environment variable: %s' % meson_root)
        self.env_info.PATH.append(meson_root)

        self._chmod_plus_x(os.path.join(meson_root, "meson"))
        self._chmod_plus_x(os.path.join(meson_root, "meson.py"))

    def package_id(self):
        self.info.header_only()
