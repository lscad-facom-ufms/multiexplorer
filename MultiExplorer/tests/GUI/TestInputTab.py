from unittest import TestCase
from mock import Mock
from MultiExplorer.tests.Utils import data_provider
from MultiExplorer.src.GUI.Frames import InputTab


def test_is_valid_data_provider():
    step = Mock()

    step.get_user_inputs = Mock()

    step.get_user_inputs.return_value = {}

    valid_input = Mock()

    valid_input.is_valid = Mock()

    valid_input.is_valid.return_value = True

    valid_input_2 = Mock()

    valid_input_2.is_valid = valid_input.is_valid

    invalid_input = Mock()

    invalid_input.is_valid = Mock()

    invalid_input.is_valid.return_value = False

    invalid_input_2 = Mock()

    invalid_input_2.is_valid = invalid_input.is_valid

    return (
        (step, {
            'valid_input': valid_input,
            'valid_input_2': valid_input_2,
        }, True),
        (step, {
            'valid_input': valid_input,
            'invalid_input': invalid_input,
        }, False),
        (step, {
            'invalid_input': invalid_input,
            'invalid_input_2': invalid_input_2,
        }, False),
    )


class TestInputTab(TestCase):
    @data_provider(test_is_valid_data_provider)
    def test_is_valid(self, step, inputs, expected):
        input_tab = InputTab(step)

        input_tab.inputs = inputs

        input_tab.display_as_valid = Mock()

        input_tab.display_as_invalid = Mock()

        self.assertEquals(expected, input_tab.is_valid())

        if expected is True:
            input_tab.display_as_valid.assert_called_once()

        if expected is False:
            input_tab.display_as_invalid.assert_called_once()
