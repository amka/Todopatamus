blueprints = custom_target('blueprints',
  input: files(
    'ui/window.blp',
    'ui/help-overlay.blp',
    'ui/todos-column.blp',
    'ui/todo-listitem.blp',
    'ui/todo-entry.blp',
    'ui/todo-details.blp',
    'ui/todo-details-dialog.blp',
    'ui/sidebar-column.blp',
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)


gnome.compile_resources('todopatamus',
  'todopatamus.gresource.xml',
  gresource_bundle: true,
  dependencies: blueprints,
  install: true,
  install_dir: pkgdatadir,
)

desktop_file = i18n.merge_file(
        input: 'com.tenderowl.todopatamus.desktop.in',
       output: 'com.tenderowl.todopatamus.desktop',
         type: 'desktop',
       po_dir: '../po',
      install: true,
  install_dir: get_option('datadir') / 'applications'
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils, args: [desktop_file])
endif

appstream_file = i18n.merge_file(
        input: 'com.tenderowl.todopatamus.metainfo.xml.in',
       output: 'com.tenderowl.todopatamus.metainfo.xml',
       po_dir: '../po',
      install: true,
  install_dir: get_option('datadir') / 'metainfo'
)

appstreamcli = find_program('appstreamcli', required: false, disabler: true)
test('Validate appstream file', appstreamcli,
     args: ['validate', '--no-net', '--explain', appstream_file])

install_data('com.tenderowl.todopatamus.gschema.xml',
  install_dir: get_option('datadir') / 'glib-2.0' / 'schemas'
)

compile_schemas = find_program('glib-compile-schemas', required: false, disabler: true)
test('Validate schema file',
     compile_schemas,
     args: ['--strict', '--dry-run', meson.current_source_dir()])

subdir('icons')
