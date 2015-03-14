# --------------------------------------------------- #
# This code was written by Alzy, dawg.
#.....................................
#---------------------------------------------------- #
from __future__ import with_statement
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from ConfigurableButtonElement import ConfigurableButtonElement
from _Framework.SessionComponent import SessionComponent
from _Framework.TransportComponent import TransportComponent


class MPDtwentysexy(ControlSurface):
    """script for MPD26: MPDtwentysexy"""
    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        with self.component_guard():
            self._suppress_send_midi = True
            self._suppress_session_highlight = True
            self._control_is_with_automap = False
            is_momentary = True
            self._suggested_input_port = 'Akai MPD26'
            self._suggested_output_port = 'Akai MPD26'

            """SESSION ViEW"""
            session = SessionComponent(4,4)
            session.name = 'Session_Control'
            matrix = ButtonMatrixElement()
            matrix.name = 'Button_Matrix'
            up_button = ButtonElement(False, MIDI_CC_TYPE, 0, 115)
            down_button = ButtonElement(False, MIDI_CC_TYPE, 0, 116)
            up_button.name = 'Bank_Select_Up_Button'
            down_button.name = 'Bank_Select_Down_Button'
            session.set_scene_bank_buttons(down_button, up_button)
            for row in range(4):
                button_row = []
                button_notes = [48, 44, 40, 36]
                scene = session.scene(row)
                scene.name = 'Scene_' + str(row)
                for column in range(4):
                    button = ConfigurableButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, button_notes[row] +  column )
                    button.name = str(column) + '_Clip_' + str(row) + '_Button'
                    button_row.append(button)
                    clip_slot = scene.clip_slot(column)
                    clip_slot.name = str(column) + '_Clip_Slot_' + str(row)
                    clip_slot.set_launch_button(button)
                matrix.add_row(tuple(button_row))

            self._suppress_session_highlight = False
            self._suppress_send_midi = False
            self.set_highlighting_session_component(session)
            #self._set_session_highlight(0,session._scene_offset,4,4,False)
            
            """TRANSPORT CONTROLS"""
            stop_button = ButtonElement(False, MIDI_CC_TYPE, 0, 117)
            play_button = ButtonElement(False, MIDI_CC_TYPE, 0, 118)
            transport = TransportComponent()
            transport.set_stop_button(stop_button)
            transport.set_play_button(play_button)

    def _set_session_highlight(self, track_offset, scene_offset, width, height, include_return_tracks):
        if not self._suppress_session_highlight:
            ControlSurface._set_session_highlight(self, track_offset, scene_offset, width, height, include_return_tracks)

    def disconnect(self):
        """clean things up on disconnect"""
        ControlSurface.disconnect(self)
        return None