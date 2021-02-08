#!/usr/bin/env python3

import tests.configuration_provider_test
import tests.catch_game_test
import tests.audio_capture_test

#--------------------
# Used to determine if individual block's of code work as expected. Not real tests, that would be too much effort for this project.
#--------------------
#tests.configuration_provider_test.cfg_base_twice()
#tests.catch_game_test.all()
tests.audio_capture_test.all()