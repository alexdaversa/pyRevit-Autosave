from pyrevit import HOST_APP
from pyrevit.coreutils.ribbon import ICON_MEDIUM
from pyrevit import script
from pyrevit.userconfig import user_config
from pyrevit import forms

__context__ = "zero-doc"


class GetValueWindow2(forms.TemplateUserInputWindow):
    """Standard form to get simple values from user.

    Args:


    Example:
        >>> from pyrevit import forms
        >>> items = ['item1', 'item2', 'item3']
        >>> forms.SelectFromList.show(items, button_name='Select Item')
        >>> ['item1']
    """

    xaml_source = "C:\\Users\\adaversa\OneDrive - EwingCole\\Documents\\pyKSS\\pyKSS.extension\\pyKSS.tab\\Autosave.panel\\Autosave.stack\\Set Interval.pushbutton\\Slider.xaml"

    def _setup(self, **kwargs):
        self.Width = 400
        # determine value type
        self.value_type = kwargs.get("value_type", "string")
        value_prompt = kwargs.get("prompt", None)
        value_default = kwargs.get("default", None)
        value_max = kwargs.get("max", 100)
        value_min = kwargs.get("min", 0)

        # customize window based on type
        if self.value_type == "slider":
            self.show_element(self.sliderPanel_sp)
            self.sliderPrompt.Text = value_prompt
            self.numberPicker.Minimum = value_min
            self.numberPicker.Maximum = value_max
            self.numberPicker.Value = (
                value_default
                if value_default
                else self.numberPicker.Value.MaximizeValue
            )

    def string_value_changed(self, sender, args):  # pylint: disable=unused-argument
        """Handle string vlaue update event."""
        filtered_rvalues = sorted(
            [x for x in self.reserved_values if self.stringValue_tb.Text == str(x)]
        )
        similar_rvalues = sorted(
            [x for x in self.reserved_values if self.stringValue_tb.Text in str(x)],
            reverse=True,
        )
        filtered_rvalues.extend(similar_rvalues)
        if filtered_rvalues:
            self.reservedValuesList.ItemsSource = filtered_rvalues
            self.show_element(self.reservedValuesListPanel)
            self.okayButton.IsEnabled = self.stringValue_tb.Text not in filtered_rvalues
        else:
            self.reservedValuesList.ItemsSource = []
            self.hide_element(self.reservedValuesListPanel)
            self.okayButton.IsEnabled = True

    def select(self, sender, args):  # pylint: disable=W0613
        """Process input data and set the response."""
        self.Close()
        if self.value_type == "string":
            self.response = self.stringValue_tb.Text
        elif self.value_type == "dropdown":
            self.response = self.dropdown_cb.SelectedItem
        elif self.value_type == "date":
            if self.datePicker.SelectedDate:
                datestr = self.datePicker.SelectedDate.ToString("MM/dd/yyyy")
                self.response = datetime.datetime.strptime(datestr, r"%m/%d/%Y")
            else:
                self.response = None
        elif self.value_type == "slider":
            self.response = self.numberPicker.Value


def ask_for_number_slider2(default=None, prompt=None, title=None, **kwargs):
    """Ask user to select a number value.

    This is a shortcut function that configures :obj:`GetValueWindow` for
    numbers. kwargs can be used to pass on other arguments.

    Args:
        default (str): default unique string. must not be in reserved_values
        prompt (str): prompt message
        title (str): title message
        kwargs (type): other arguments to be passed to :obj:`GetValueWindow`

    Returns:
        str: selected string value

    Example:
        >>> forms.ask_for_string(
        ...     default=50,
        ...     min = 0
        ...     max = 100
        ...     prompt='Select a number:',
        ...     title='test title')
        ... '50'
    """
    return GetValueWindow2.show(
        None, value_type="slider", default=default, prompt=prompt, title=title, **kwargs
    )


default_interval = user_config.autosave.interval / 60
interval = ask_for_number_slider2(
    default=default_interval,
    prompt="Set autosave interval in minutes:",
    title="Autosave Interval",
    min=5,
    max=240,
)
if interval:
    user_config.autosave.interval = interval * 60
    user_config.save_changes()
