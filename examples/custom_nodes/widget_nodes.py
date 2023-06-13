from NodeGraphQt import BaseNode

import os



class DropdownMenuNode(BaseNode):
    """
    An example node with a embedded added QCombobox menu.
    """

    # unique node identifier.
    __identifier__ = 'nodes.widget'

    # initial default node name.
    NODE_NAME = 'menu'

    def __init__(self):
        super(DropdownMenuNode, self).__init__()

        # create input & output ports
        self.add_input('in 1')
        self.add_output('out 1')
        self.add_output('out 2')

        # create the QComboBox menu.
        items = ['item 1', 'item 2', 'item 3']
        self.add_combo_menu('my_menu', 'Menu Test', items=items)


class TextInputNode(BaseNode):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'nodes.widget'

    # initial default node name.
    NODE_NAME = 'text'

    def __init__(self):
        super(TextInputNode, self).__init__()

        # create input & output ports
        self.add_input('in')
        self.add_output('out')

        # create QLineEdit text input widget.
        self.add_text_input('my_input', 'Text Input', tab='widgets')


class CheckboxNode(BaseNode):
    """
    An example of a node with 2 embedded QCheckBox widgets.
    """

    # set a unique node identifier.
    __identifier__ = 'nodes.widget'

    # set the initial default node name.
    NODE_NAME = 'checkbox'

    def __init__(self):
        super(CheckboxNode, self).__init__()

        # create the checkboxes.
        self.add_checkbox('cb_2', '', 'Working on', False)
        self.add_checkbox('cb_1', '', 'Finished', True)

        # create input and output port.
        self.add_input('in',  multi_input=True, color=(200, 100, 0))
        self.add_input('in 2',  multi_input=True, color=(200, 100, 0))
        self.add_output('out', multi_output=True, color=(0, 100, 200))
        self.add_output('out 2', multi_output=True, color=(0, 100, 200))


class ButtonNode(BaseNode):
    """
    An example of a node with 2 embedded QButton widget.
    """

    # set a unique node identifier.
    __identifier__ = 'nodes.widget'

    # set the initial default node name.
    NODE_NAME = 'button'

    def __init__(self):
        super(ButtonNode, self).__init__()

        # create the checkboxes.
        self.add_checkbox('cb_1', '', 'Checkbox 1', True)
        self.add_checkbox('cb_2', '', 'Checkbox 2', False)
        self.add_button("button 1")

        # create input and output port.
        self.add_input('in', color=(200, 100, 0))
        self.add_output('out', color=(0, 100, 200))




class TitleNode(BaseNode):


    # set a unique node identifier.
    __identifier__ = 'nodes.widget'

    # set the initial default node name.
    NODE_NAME = 'Title'

    def __init__(self):
        super(TitleNode, self).__init__()

        # create the checkboxes.
        self.add_title('title_1', '', 'Title 1', True)
        # self.add_checkbox('cb_2', '', 'Checkbox 2', False)

# class ImageNodeV(BaseNode):
#     """
#     An example of a node with 2 embedded QButton widget.
#     """

#     # set a unique node identifier.
#     __identifier__ = 'nodes.widget'

#     # set the initial default node name.
#     NODE_NAME = 'Sketch'

#     def __init__(self):
#         super(ImageNodeV, self).__init__()
#         self.add_image("picture_menu", text = "v")

#         # create input and output port.
#         self.add_input('in', color=(200, 100, 0))
#         self.add_output('out', color=(0, 100, 200))
#         self.add_output('out 2')
#         self.add_output('out 3')
#         self.add_output('out 4')

# class ImageNodeH(BaseNode):
#     """
#     An example of a node with 2 embedded QButton widget.
#     """

#     # set a unique node identifier.
#     __identifier__ = 'nodes.widget'

#     # set the initial default node name.
#     NODE_NAME = 'Sketch'

#     def __init__(self):
#         super(ImageNodeH, self).__init__()
#         self.add_image("picture_menu", text = "h")
  
#         # create input and output port.
#         self.add_input('in', color=(200, 100, 0))
#         self.add_output('out', color=(0, 100, 200))
#         self.add_output('out 2')
#         self.add_output('out 3')
#         self.add_output('out 4')


# class ScrollNode(BaseNode):
#     """
#     An example of a node with 2 embedded QButton widget.
#     """

#     # set a unique node identifier.
#     __identifier__ = 'nodes.widget'

#     # set the initial default node name.
#     NODE_NAME = 'Scrollable notes'

#     def __init__(self):
#         super(ScrollNode, self).__init__()
#         self.add_scrolltext('st_2')

#         # create input and output port.
#         self.add_input('in', color=(200, 100, 0))
#         self.add_output('out', color=(0, 100, 200))
#         self.add_output('out 2')
#         self.add_output('out 3')
#         self.add_output('out 4')