import sys
import sublime
st_version = 3

# With the way ST3 works, the sublime module is not "available" at startup
# which results in an empty version number
if sublime.version() == '' or int(sublime.version()) > 3000:
    st_version = 3
    from imp import reload

# Python allows reloading modules on the fly, which allows us to do live upgrades.
# The only caveat to this is that you have to reload in the dependency order.
#
# Thus is module A depends on B and we don't reload B before A, when A is reloaded
# it will still have a reference to the old B. Thus we hard-code the dependency
# order of the various Package Control modules so they get reloaded properly.
#
# There are solutions for doing this all programatically, but this is much easier
# to understand.

reload_mods = []
for mod in sys.modules:
    if mod[0:15].lower().replace(' ', '_') == 'mavensmate.lib.' and sys.modules[mod] != None:
        reload_mods.append(mod)

# print(reload_mods)

mod_prefix = 'lib'
if st_version == 3:
    mod_prefix = 'MavensMate.' + mod_prefix

mods_load_order = [
    '',
    '.apex_extensions',
    '.command_helper',
    '.community',
    '.completioncommon',
    '.exceptions',
    '.mm_installer',
    '.mm_interface',
    '.mm_merge',
    '.mm_response_handlers',
    '.parsehelp',
    '.platform_util',
    '.printer',
    '.resource_bundle'
    '.threads',
    '.vf',
    '.views'
]

for suffix in mods_load_order:
    mod = mod_prefix + suffix
    if mod in reload_mods:
        reload(sys.modules[mod])
