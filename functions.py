# Import standard libraries
import re

# Create function to fix the model column


def normalize_ford_f_series(model):
    # Check if model starts with 'ford f'
    try:
        if model.startswith('ford f'):
            # Ensure there is a '-' between 'f' and the number
            model = re.sub(r'ford f(\d+)', r'ford f-\1', model)
            # Check if model ends with 'sd'
            if model[-2:] == 'sd':
                # replace remove the the last two characters and concatenate 'super duty'
                model = model[:-2] + 'super duty'
        return model
    except AttributeError:
        return model

# Test the function


def test_normalize_ford_f_series():
    assert normalize_ford_f_series('ford f150') == 'ford f-150'
    assert normalize_ford_f_series('ford fusion se') == 'ford fusion se'
    assert normalize_ford_f_series(
        'ford f150 supercrew cab xlt') == 'ford f-150 supercrew cab xlt'
    assert normalize_ford_f_series('ford f250 sd') == 'ford f-250 super duty'
    assert normalize_ford_f_series('ford f-350 sd') == 'ford f-350 super duty'
    assert normalize_ford_f_series('toyota camry sd') == 'toyota camry sd'
    assert normalize_ford_f_series(None) == None
    assert normalize_ford_f_series('') == ''
