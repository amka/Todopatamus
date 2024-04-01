project('todopatamus',
          version: '0.1.0',
    meson_version: '>= 0.62.0',
  default_options: [ 'warning_level=2', 'werror=false', ],
)

if get_option('profile') == 'release'
  profile = 'release'
else
  profile = 'dev'
endif


i18n = import('i18n')
pymod = import('python')
gnome = import('gnome')
python = pymod.find_installation('python3')

prefix = get_option('prefix')
bindir = get_option('bindir')
datadir = get_option('datadir')
pkgdatadir = join_paths(prefix, datadir, meson.project_name())
pythondir = join_paths(prefix, python.get_install_dir())
localedir = join_paths(prefix, get_option('localedir'))


subdir('bin')
subdir('data')
subdir('po')

install_subdir(
  meson.project_name(),
  install_dir: pythondir
)

gnome.post_install(
     glib_compile_schemas: true,
    gtk_update_icon_cache: true,
  update_desktop_database: true,
)
