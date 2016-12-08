#
# REMIND: This file is now obsolete. A better implementation of this exists in jove.py which sorts
# the views by last touch date.
#
import sublime, sublime_plugin, os
isSt2 = False

try:
  import sublime_api
except ImportError:
  isSt2 = True

# This code is inspired and modified from https://github.com/phildopus/sublime-goto-open-file/blob/master/GotoOpenFile.py
class GotoOpenFileCommand(sublime_plugin.TextCommand):

  def run(self, edit, active_group=False):
    window = sublime.active_window()

    selector = ViewSelector(window, active_group)
    window.show_quick_panel(selector.get_items(), selector.select)


class ViewSelector(object):

  def __init__(self, window, active_group):
    self.window = window
    if active_group:
      self.views = window.views_in_group(window.active_group())
    else:
      self.views = window.views()

  def select(self, index):
    if index != -1:
      if not isSt2:
        wid = sublime.active_window().id()
        vid = sublime.active_window().views()[index].id()
        sublime_api.window_focus_view(wid, vid)
      else:
        sublime.active_window().focus_view(self.views[index])

  def get_items(self):
    return [[self.__get_display_name(view), self.__get_path(view)] for view in self.views]

  def __get_display_name(self, view):
    mod_star = '*' if view.is_dirty() else ''

    if view.is_scratch() or not view.file_name():
      disp_name = view.name() if len(view.name()) > 0 else 'untitled'
    else:
      disp_name = os.path.basename(view.file_name())

    return '%s%s' % (disp_name, mod_star)

  def __get_path(self, view):
    if view.is_scratch():
      return ''

    if not view.file_name():
      return '<unsaved>'

    folders = self.window.folders()

    for folder in folders:
      if os.path.commonprefix([folder, view.file_name()]) == folder:
        relpath = os.path.relpath(view.file_name(), folder)

        if len(folders) > 1:
          return os.path.join(os.path.basename(folder), relpath)

        return relpath

    return view.file_name()
