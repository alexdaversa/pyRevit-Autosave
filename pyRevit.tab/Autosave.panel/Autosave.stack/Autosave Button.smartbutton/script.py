from pyrevit import HOST_APP
from pyrevit.runtime.types import DocumentTabEventUtils
from pyrevit.coreutils.ribbon import ICON_MEDIUM
from pyrevit import script
from pyrevit.userconfig import user_config
from pyrevit.revit import tabs
from pyrevit import forms
from pyrevit.revit import ui
import pyrevit.extensions as exts

__context__ = "zero-doc"
__title__ = "Autosave"


def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
    on_icon = ui.resolve_icon_file(script_cmp.directory, exts.DEFAULT_ON_ICON_FILE)
    off_icon = ui.resolve_icon_file(script_cmp.directory, exts.DEFAULT_OFF_ICON_FILE)
    if user_config.has_section("autosave") and user_config.autosave.has_option(
        "enabled"
    ):
        button_icon = script_cmp.get_bundle_file(
            on_icon if user_config.autosave.get_option("enabled") else off_icon
        )
    else:
        user_config.add_section("autosave")
        user_config.autosave.interval = 900
        user_config.autosave.enabled = False
        user_config.save_changes()
        button_icon = script_cmp.get_bundle_file(
            on_icon if user_config.autosave.get_option("enabled") else off_icon
        )
    ui_button_cmp.set_icon(button_icon, icon_size=ICON_MEDIUM)


def toggle_autosave():
    if user_config.autosave.enabled == False:
        user_config.autosave.enabled = True
    else:
        user_config.autosave.enabled = False
    user_config.save_changes()
    return user_config.autosave.enabled


if __name__ == "__main__":
    is_active = toggle_autosave()
    script.toggle_icon(is_active)
