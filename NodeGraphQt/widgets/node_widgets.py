#!/usr/bin/python
from PyQt5 import QtCore, QtGui, QtWidgets

from NodeGraphQt.constants import ViewerEnum, Z_VAL_NODE_WIDGET
from NodeGraphQt.errors import NodeWidgetError
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt

import os
import random
import gkeepapi
import json







# for i in os.listdir():
#     print(i)

DownloadsFolderPictures = os.listdir("AirNotes")
DownloadsFolderPictures.sort()

for file in DownloadsFolderPictures:
    if file.endswith(".DS_Store"):
        DownloadsFolderPictures.remove(file)




styles = [
    "background-color: qradialgradient(spread:pad, cx:0.842365, cy:0.9345, radius:0.989518, fx:0.980296, fy:0, stop:0.206897 rgba(24, 35, 52, 255), stop:0.901478 rgba(43, 101, 118, 255), stop:1 rgba(42, 108, 116, 255));",
    "background-color: qradialgradient(spread:pad, cx:0.416257, cy:0.34659, radius:0.825346, fx:0.120689, fy:0.699, stop:0.123153 rgba(46, 122, 132, 255), stop:0.438424 rgba(60, 105, 118, 255), stop:0.817734 rgba(24, 35, 52, 255));",
    "background-color: qradialgradient(spread:pad, cx:0.702113, cy:1, radius:0.825346, fx:0.194581, fy:0.920591, stop:0.123153 rgba(46, 122, 132, 255), stop:0.438424 rgba(60, 105, 118, 255), stop:0.817734 rgba(24, 35, 52, 255));",
    "background-color: qradialgradient(spread:pad, cx:0.667631, cy:0.244318, radius:0.767829, fx:0, fy:0.0455909, stop:0.123153 rgba(46, 122, 132, 255), stop:0.438424 rgba(60, 105, 118, 255), stop:0.817734 rgba(24, 35, 52, 255));",
    "background-color: qradialgradient(spread:pad, cx:0, cy:0.377682, radius:0.989518, fx:0.527094, fy:1, stop:0.206897 rgba(24, 35, 52, 255), stop:0.901478 rgba(43, 101, 118, 255), stop:1 rgba(46, 109, 116, 255));",
    "background-color: qradialgradient(spread:pad, cx:0.842365, cy:0.9345, radius:0.989518, fx:0.980296, fy:0, stop:0.206897 rgba(24, 35, 52, 255), stop:0.901478 rgba(43, 101, 118, 255), stop:1 rgba(42, 108, 116, 255));",
    "background-color: qradialgradient(spread:pad, cx:0.389163, cy:0.616318, radius:1.1894, fx:0.108, fy:0, stop:0.206897 rgba(24, 35, 52, 255), stop:0.901478 rgba(43, 101, 118, 255), stop:1 rgba(42, 108, 116, 255));",
]

class _NodeGroupBox(QtWidgets.QGroupBox):

    def __init__(self, label, parent=None):
        super(_NodeGroupBox, self).__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        # layout.setRowStretch(1, 2)
        # layout.setColumnStretch(2, 2)
        # layout.setSpacing(1)
        self.setTitle(label)

    def setTitle(self, text):
        margin = (0, 2, 0, 0) if text else (0, 0, 0, 0)
        self.layout().setContentsMargins(*margin)
        super(_NodeGroupBox, self).setTitle(text)

    def setTitleAlign(self, align='center'):
        text_color = self.palette().text().color().getRgb()
        print(*text_color)
        print(self.palette().text())
        style_dict = {
            'QGroupBox': {
                'font': '500 13pt "0Arame"',
                'background-color': 'rgba(0, 0, 0, 0)',
                'border': '0px solid rgba(0, 0, 0, 0)',
                'margin-top': '1px',
                'padding-bottom': '2px',
                'padding-left': '1px',
                'padding-right': '1px',
                'font-size': '8pt',
            },
            'QGroupBox::title': {
                'font': '500 13pt "0Arame"',
                'subcontrol-origin': 'margin',
                'subcontrol-position': 'top center',
                'color': 'rgba({0}, {1}, {2}, 100)'.format(*text_color),
                'padding': '0px',
            }
        }
        if self.title():
            style_dict['QGroupBox']['padding-top'] = '14px'
        else:
            style_dict['QGroupBox']['padding-top'] = '2px'

        if align == 'center':
            style_dict['QGroupBox::title']['subcontrol-position'] = 'top center'
        elif align == 'left':
            style_dict['QGroupBox::title']['subcontrol-position'] += 'top left'
            style_dict['QGroupBox::title']['margin-left'] = '4px'
        elif align == 'right':
            style_dict['QGroupBox::title']['subcontrol-position'] += 'top right'
            style_dict['QGroupBox::title']['margin-right'] = '4px'
        stylesheet = ''
        for css_class, css in style_dict.items():
            style = '{} {{\n'.format(css_class)
            for elm_name, elm_val in css.items():
                style += '  {}:{};\n'.format(elm_name, elm_val)
            style += '}\n'
            stylesheet += style

        print(stylesheet)
        self.setStyleSheet(stylesheet)

    def add_node_widget(self, widget):
        # import random
        # x = random.randint(0, 2)
        # y = random.randint(0, 2)
        self.layout().addWidget(widget) #, x, y) #, 1, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)

    def get_node_widget(self):
        return self.layout().itemAt(0).widget()







class NodeBaseWidget(QtWidgets.QGraphicsProxyWidget):
    """
    This is the main wrapper class that allows a ``QtWidgets.QWidget`` to be
    added in a :class:`NodeGraphQt.BaseNode` object.

    Args:
        parent (NodeGraphQt.BaseNode.view): parent node view.
        name (str): property name for the parent node.
        label (str): label text above the embedded widget.
    """

    value_changed = pyqtSignal(str, object)
    """
    Signal triggered when the ``value`` attribute has changed.
    
    (This is connected to the :meth: `BaseNode.set_property` function when the 
    widget is added into the node.)

    :parameters: str, object
    :emits: property name, propety value
    """

    def __init__(self, parent=None, name=None, label=''):
        super(NodeBaseWidget, self).__init__(parent)
        self.setZValue(Z_VAL_NODE_WIDGET)
        self._name = name
        self._label = label
        self._node = None

    def setToolTip(self, tooltip):
        tooltip = tooltip.replace('\n', '<br/>')
        tooltip = '<b>{}</b><br/>{}'.format(self.name, tooltip)
        super(NodeBaseWidget, self).setToolTip(tooltip)

    def on_value_changed(self, *args, **kwargs):
        """
        This is the slot function that
        Emits the widgets current :meth:`NodeBaseWidget.value` with the
        :attr:`NodeBaseWidget.value_changed` signal.

        Args:
            args: not used.
            kwargs: not used.

        Emits:
            str, object: <node_property_name>, <node_property_value>
        """
        self.value_changed.emit(self.get_name(), self.get_value())

    @property
    def type_(self):
        """
        Returns the node widget type.

        Returns:
            str: widget type.
        """
        return str(self.__class__.__name__)

    @property
    def node(self):
        """
        Returns the node object this widget is embedded in.
        (This will return ``None`` if the widget has not been added to
        the node yet.)

        Returns:
            NodeGraphQt.BaseNode: parent node.
        """
        return self._node

    def get_icon(self, name):
        """
        Returns the default icon from the Qt framework.

        Returns:
            str: icon name.
        """
        return self.style().standardIcon(QtWidgets.QStyle.StandardPixmap(name))

    def get_name(self):
        """
        Returns the parent node property name.

        Returns:
            str: property name.
        """
        return self._name

    def set_name(self, name):
        """
        Set the property name for the parent node.

        Important:
            The property name must be set before the widget is added to
            the node.

        Args:
            name (str): property name.
        """
        if not name:
            return
        if self.node:
            raise NodeWidgetError(
                'Can\'t set property name widget already added to a Node'
            )
        self._name = name

    def get_value(self):
        """
        Returns the widgets current value.

        You must re-implement this property to if you're using a custom widget.

        Returns:
            str: current property value.
        """
        raise NotImplementedError

    def set_value(self, text):
        """
        Sets the widgets current value.

        You must re-implement this property to if you're using a custom widget.

        Args:
            text (str): new text value.
        """
        raise NotImplementedError

    def get_custom_widget(self):
        """
        Returns the embedded QWidget used in the node.

        Returns:
            QtWidgets.QWidget: nested QWidget
        """
        widget = self.widget()
        return widget.get_node_widget()

    def set_custom_widget(self, widget):
        """
        Set the custom QWidget used in the node.

        Args:
            widget (QtWidgets.QWidget): custom.
        """
        if self.widget():
            raise NodeWidgetError('Custom node widget already set.')
        group = _NodeGroupBox(self._label)
        group.add_node_widget(widget)
        self.setWidget(group)

    def get_label(self):
        """
        Returns the label text displayed above the embedded node widget.

        Returns:
            str: label text.
        """
        return self._label

    def set_label(self, label=''):
        """
        Sets the label text above the embedded widget.

        Args:
            label (str): new label ext.
        """
        if self.widget():
            self.widget().setTitle(label)
        self._label = label


class NodeComboBox(NodeBaseWidget):
    """
    Displays as a ``QComboBox`` in a node.

    **Inherited from:** :class:`NodeBaseWidget`

    .. note::
        `To embed a` ``QComboBox`` `in a node see func:`
        :meth:`NodeGraphQt.BaseNode.add_combo_menu`
    """

    def __init__(self, parent=None, name='', label='', items=None):
        super(NodeComboBox, self).__init__(parent, name, label)
        self.setZValue(Z_VAL_NODE_WIDGET + 1)
        combo = QtWidgets.QComboBox()
        combo.setMinimumHeight(24)
        combo.addItems(items or [])
        combo.currentIndexChanged.connect(self.on_value_changed)
        combo.clearFocus()
        self.set_custom_widget(combo)

    @property
    def type_(self):
        return 'ComboNodeWidget'

    def get_value(self):
        """
        Returns the widget current text.

        Returns:
            str: current text.
        """
        combo_widget = self.get_custom_widget()
        return str(combo_widget.currentText())

    def set_value(self, text=''):
        combo_widget = self.get_custom_widget()
        if type(text) is list:
            combo_widget.clear()
            combo_widget.addItems(text)
            return
        if text != self.get_value():
            index = combo_widget.findText(text, QtCore.Qt.MatchExactly)
            combo_widget.setCurrentIndex(index)

    def add_item(self, item):
        combo_widget = self.get_custom_widget()
        combo_widget.addItem(item)

    def add_items(self, items=None):
        if items:
            combo_widget = self.get_custom_widget()
            combo_widget.addItems(items)

    def all_items(self):
        combo_widget = self.get_custom_widget()
        return [combo_widget.itemText(i) for i in range(combo_widget.count())]

    def sort_items(self, reversed=False):
        items = sorted(self.all_items(), reverse=reversed)
        combo_widget = self.get_custom_widget()
        combo_widget.clear()
        combo_widget.addItems(items)

    def clear(self):
        combo_widget = self.get_custom_widget()
        combo_widget.clear()


class NodeLineEdit(NodeBaseWidget):
    """
    Displays as a ``QLineEdit`` in a node.

    **Inherited from:** :class:`NodeBaseWidget`

    .. note::
        `To embed a` ``QLineEdit`` `in a node see func:`
        :meth:`NodeGraphQt.BaseNode.add_text_input`
    """

    def __init__(self, parent=None, name='', label='', text=''):
        super(NodeLineEdit, self).__init__(parent, name, label)

        plt = self.palette()
        bg_color = plt.alternateBase().color().getRgb()
        text_color = plt.text().color().getRgb()
        text_sel_color = plt.highlightedText().color().getRgb()
        style_dict = {
            'QLineEdit': {
                'font': '500 13pt "0Arame"',
                "background": "qradialgradient(spread:pad, cx:0.842365, cy:0.9345, radius:0.989518, fx:0.980296, fy:0, stop:0.206897 rgba(24, 35, 52, 255), stop:0.901478 rgba(43, 101, 118, 255), stop:1 rgba(42, 108, 116, 255));",
                # 'background': 'rgba({0},{1},{2},20)'.format(*bg_color),
                'border': '1px solid rgb({0},{1},{2})'
                          .format(*ViewerEnum.GRID_COLOR.value),
                'border-radius': '3px',
                'color': 'rgba({0},{1},{2},150)'.format(*text_color),
                'selection-background-color': 'rgba({0},{1},{2},100)'
                                              .format(*text_sel_color),
            }
        }
        stylesheet = ''
        for css_class, css in style_dict.items():
            style = '{} {{\n'.format(css_class)
            for elm_name, elm_val in css.items():
                style += '  {}:{};\n'.format(elm_name, elm_val)
            style += '}\n'
            stylesheet += style
        ledit = QtWidgets.QLineEdit()
        ledit.setText(text)
        ledit.setStyleSheet(stylesheet)
        ledit.setAlignment(QtCore.Qt.AlignCenter)
        ledit.editingFinished.connect(self.on_value_changed)
        ledit.clearFocus()
        self.set_custom_widget(ledit)
        self.widget().setMaximumWidth(140)

    @property
    def type_(self):
        return 'LineEditNodeWidget'

    def get_value(self):
        """
        Returns the widgets current text.

        Returns:
            str: current text.
        """
        return str(self.get_custom_widget().text())

    def set_value(self, text=''):
        """
        Sets the widgets current text.

        Args:
            text (str): new text.
        """
        if text != self.get_value():
            self.get_custom_widget().setText(text)
            self.on_value_changed()


class NodeCheckBox(NodeBaseWidget):
    """
    Displays as a ``QCheckBox`` in a node.

    **Inherited from:** :class:`NodeBaseWidget`

    .. note::
        `To embed a` ``QCheckBox`` `in a node see func:`
        :meth:`NodeGraphQt.BaseNode.add_checkbox`
    """

    def __init__(self, parent=None, name='', label='', text='', state=False):
        super(NodeCheckBox, self).__init__(parent, name, label)
        _cbox = QtWidgets.QCheckBox(text)
        _cbox.setChecked(state)
        _cbox.setMinimumWidth(80)


        # font = QtGui.QFont()
        # font.setFamily("OCR A Extended")

        font = _cbox.font()
        font.setFamily("OCR A Extended")
        font.setPointSize(11)
        _cbox.setFont(font)
        _cbox.stateChanged.connect(self.on_value_changed)
        self.set_custom_widget(_cbox)
        self.widget().setMaximumWidth(140)

    @property
    def type_(self):
        return 'CheckboxNodeWidget'

    def get_value(self):
        """
        Returns the widget checked state.

        Returns:
            bool: checked state.
        """
        return self.get_custom_widget().isChecked()

    def set_value(self, state=False):
        """
        Sets the widget checked state.

        Args:
            state (bool): check state.
        """
        if state != self.get_value():
            self.get_custom_widget().setChecked(state)


class NodeButton(NodeBaseWidget):

    def __init__(self, parent=None, name='', label='', text='hi'):
        super(NodeButton, self).__init__(parent, name, label)

        Form = QtWidgets.QWidget()
        horizontalLayoutWidget = QtWidgets.QWidget(Form)
        horizontalLayoutWidget.setGeometry(QtCore.QRect(40, 30, 731, 251))
        horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        horizontalLayout = QtWidgets.QHBoxLayout(horizontalLayoutWidget)
        horizontalLayout.setContentsMargins(0, 0, 0, 0)
        horizontalLayout.setObjectName("horizontalLayout")
        horizontalLayout_2 = QtWidgets.QHBoxLayout()
        horizontalLayout_2.setObjectName("horizontalLayout_2")
        pushButton_4 = QtWidgets.QPushButton(horizontalLayoutWidget)
        pushButton_4.setObjectName("pushButton_4")
        pushButton_4.setText("PushButton_4")
        horizontalLayout_2.addWidget(pushButton_4)
        pushButton_3 = QtWidgets.QPushButton(horizontalLayoutWidget)
        pushButton_3.setObjectName("pushButton_3")
        pushButton_3.setText("PushButton_3")
        horizontalLayout_2.addWidget(pushButton_3)
        pushButton_2 = QtWidgets.QPushButton(horizontalLayoutWidget)
        pushButton_2.setObjectName("pushButton_2")
        pushButton_2.setText("PushButton_2")
        horizontalLayout_2.addWidget(pushButton_2)
        horizontalLayout.addLayout(horizontalLayout_2)
        pushButton = QtWidgets.QPushButton(horizontalLayoutWidget)
        pushButton.setObjectName("pushButton")
        pushButton.setText("PushButton")
        horizontalLayout.addWidget(pushButton)
        self.set_custom_widget(horizontalLayoutWidget)

    @property
    def type_(self):
        return 'ButtonNodeWidget'



class NodeImage(NodeBaseWidget):

    def __init__(self, parent=None, name='', label='', text=''):
        super(NodeImage, self).__init__(parent, name, label)

        font = QtGui.QFont()
        font.setFamily("OCR A Extended")
        font.setPointSize(16)

        Form = QtWidgets.QWidget()
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 511, 341))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")

        if text == "h":
            self.label.setFixedSize(540, 291) #471, 291 #these can be adjusted
        elif text == "v":
            self.label.setFixedSize(448, 471) #360, 471

        self.label.setScaledContents(True)


        # self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)

        if text == "h":
            self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        elif text == "v":
            self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)



        self.comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setFont(font)
        self.comboBox.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.3867, cy:0.392045, radius:0.825346, fx:0.110837, fy:0.125, stop:0.123153 rgba(74, 115, 132, 255), stop:0.817734 rgba(24, 35, 52, 255));\n"
"\n"
"border :1px solid rgb(181, 212, 210);")
        self.comboBox.addItems(DownloadsFolderPictures)
        self.verticalLayout.addWidget(self.comboBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setText("PREV")
        self.pushButton_3.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.3867, cy:0.392045, radius:0.825346, fx:0.110837, fy:0.125, stop:0.123153 rgba(74, 115, 132, 255), stop:0.817734 rgba(24, 35, 52, 255));\n"
"\n"
"border :1px solid rgb(181, 212, 210);")

        self.pushButton_3.setFont(font)
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText("OPEN")
        self.pushButton_2.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.3867, cy:0.392045, radius:0.825346, fx:0.110837, fy:0.125, stop:0.123153 rgba(74, 115, 132, 255), stop:0.817734 rgba(24, 35, 52, 255));\n"
"\n"
"border :1px solid rgb(181, 212, 210);")

        self.pushButton_2.setFont(font)
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("NEXT")
        self.pushButton.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.3867, cy:0.392045, radius:0.825346, fx:0.110837, fy:0.125, stop:0.123153 rgba(74, 115, 132, 255), stop:0.817734 rgba(24, 35, 52, 255));\n"
"\n"
"border :1px solid rgb(181, 212, 210);")


 
        self.pushButton.setFont(font)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout.addWidget(self.pushButton)


        #new bit
        self.horizontalSlider = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        # self.horizontalSlider.setPageStep(0)
        self.verticalLayout.addWidget(self.horizontalSlider)
        #end of new bit



        self.set_custom_widget(self.verticalLayoutWidget)
        self.pushButton.clicked.connect(self.NextPhoto_1)
        self.pushButton_2.clicked.connect(self.OpenPhoto_1)
        self.pushButton_3.clicked.connect(self.PreviousPhoto_1)
        self.horizontalSlider.valueChanged.connect(self.scaletext)

    @property
    def type_(self):
        return 'ImageNodeWidget'

    def get_value(self):
        return self.get_custom_widget()

    def set_value(self, state=False):
        if state != self.get_value():
            self.get_custom_widget()

    def OpenPhoto_1(self):
        path = self.comboBox.currentText()
        self.label.setPixmap(QtGui.QPixmap(str(f"AirNotes/{path}")))


    def NextPhoto_1(self):
        try:
            path = self.comboBox.currentText()
            for position, names in enumerate(DownloadsFolderPictures):
                if path == names:
                    image = DownloadsFolderPictures[position+1]
                    print(image)
                    break

            pos = self.comboBox.currentIndex()
            if pos+2 == self.comboBox.count():
                pos = 0
            self.comboBox.setCurrentIndex(pos+1)
            self.label.setPixmap(QtGui.QPixmap(str(f"AirNotes/{image}")))
        except IndexError:
            print("IndexError")

    def PreviousPhoto_1(self):
        path = self.comboBox.currentText()
        for position, names in enumerate(DownloadsFolderPictures):
            if path == names:
                image = DownloadsFolderPictures[position-1]
                print(image)
                break

        pos = self.comboBox.currentIndex()
        print(pos)
        if pos == -1:
            pos = self.comboBox.count()
            image = DownloadsFolderPictures[-1]

        self.comboBox.setCurrentIndex(pos-1)
        self.label.setPixmap(QtGui.QPixmap(str(f"AirNotes/{image}")))

    def scaletext(self, value):
        value = value 
        print(round((value/100)*len(DownloadsFolderPictures)))
        value = round((value/100)*len(DownloadsFolderPictures))
        for position, names in enumerate(DownloadsFolderPictures):
            if position == value:
                self.comboBox.setCurrentIndex(value)
                self.label.setPixmap(QtGui.QPixmap(str(f"AirNotes/{names}")))
                break
        # mixer.music.load(f"SoundEffects/Transparent.mp3")
        # mixer.music.play()




with open('GoogleKeepCredentials.json') as json_file:
    data = json.load(json_file)

    for p in data['Credentials']:
        email = p["email"]
        password = p["password"]

keep = gkeepapi.Keep()
success = keep.login(email, password)






print(keep.all())
notes_ = []
titles_ = []
notesPlusTitles = []
for j, i in enumerate(keep.all()):
    print(i.title)
    if i.title == "":
        title = j
    else:
        title = i.title
    titles_.append(str(title))
    notes_.append(str(i.text))
    notesPlusTitles.append([str(title), str(i.text)])




class NodeScrollText(NodeBaseWidget):

    def __init__(self, parent=None, name='', label='', text='hi'):
        super(NodeScrollText, self).__init__(parent, name, label)

        font = QtGui.QFont()
        font.setFamily("OCR A Extended")
        font.setPointSize(16)

        
        Form = QtWidgets.QWidget()


        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 511, 341))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")


        scrollArea_2 = QtWidgets.QScrollArea(self.verticalLayoutWidget)
        # scrollArea_2.setGeometry(QtCore.QRect(0, 0, 221, 181))
        scrollArea_2.setFixedSize(318, 180) #291, 180
        scrollArea_2.setWidgetResizable(True)
        scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        # scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 219, 179))
        self.scrollAreaWidgetContents_2.setFixedSize(318, 180)
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.textEdit_2 = QtWidgets.QTextEdit(self.scrollAreaWidgetContents_2)
        # self.textEdit_2.setGeometry(QtCore.QRect(0, 0, 211, 171))
        font = QtGui.QFont()
        font.setFamily("OCR A Extended")
        font.setPointSize(20)
        self.textEdit_2.setFont(font)
        self.textEdit_2.setFixedSize(318, 180)


        styles = [
            "background-color: qradialgradient(spread:pad, cx:0.842365, cy:0.9345, radius:0.989518, fx:0.980296, fy:0, stop:0.206897 rgba(24, 35, 52, 255), stop:0.901478 rgba(43, 101, 118, 255), stop:1 rgba(42, 108, 116, 255));",
            "background-color: qradialgradient(spread:pad, cx:0.416257, cy:0.34659, radius:0.825346, fx:0.120689, fy:0.699, stop:0.123153 rgba(46, 122, 132, 255), stop:0.438424 rgba(60, 105, 118, 255), stop:0.817734 rgba(24, 35, 52, 255));",
            "background-color: qradialgradient(spread:pad, cx:0.702113, cy:1, radius:0.825346, fx:0.194581, fy:0.920591, stop:0.123153 rgba(46, 122, 132, 255), stop:0.438424 rgba(60, 105, 118, 255), stop:0.817734 rgba(24, 35, 52, 255));",
            "background-color: qradialgradient(spread:pad, cx:0.667631, cy:0.244318, radius:0.767829, fx:0, fy:0.0455909, stop:0.123153 rgba(46, 122, 132, 255), stop:0.438424 rgba(60, 105, 118, 255), stop:0.817734 rgba(24, 35, 52, 255));",
            "background-color: qradialgradient(spread:pad, cx:0, cy:0.377682, radius:0.989518, fx:0.527094, fy:1, stop:0.206897 rgba(24, 35, 52, 255), stop:0.901478 rgba(43, 101, 118, 255), stop:1 rgba(46, 109, 116, 255));",
            "background-color: qradialgradient(spread:pad, cx:0.842365, cy:0.9345, radius:0.989518, fx:0.980296, fy:0, stop:0.206897 rgba(24, 35, 52, 255), stop:0.901478 rgba(43, 101, 118, 255), stop:1 rgba(42, 108, 116, 255));",
            "background-color: qradialgradient(spread:pad, cx:0.389163, cy:0.616318, radius:1.1894, fx:0.108, fy:0, stop:0.206897 rgba(24, 35, 52, 255), stop:0.901478 rgba(43, 101, 118, 255), stop:1 rgba(42, 108, 116, 255));",
        ]
        # random.choice(styles)


        """
        background-color: qradialgradient(spread:pad, cx:0.842365, cy:0.9345, radius:0.989518, fx:0.980296, fy:0, stop:0.206897 rgba(24, 35, 52, 255), stop:0.901478 rgba(43, 101, 118, 255), stop:1 rgba(42, 108, 116, 255));
        background-color: qradialgradient(spread:pad, cx:0, cy:0.377682, radius:0.989518, fx:0.527094, fy:1, stop:0.206897 rgba(24, 35, 52, 255), stop:0.901478 rgba(43, 101, 118, 255), stop:1 rgba(46, 109, 116, 255));
        """

        self.textEdit_2.setStyleSheet(random.choice(styles))

        self.textEdit_2.setObjectName("textEdit_2")
        scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout.addWidget(scrollArea_2)

        
        font2 = QtGui.QFont()
        font2.setFamily("OCR A Extended")
        font2.setPointSize(16)

        self.comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setFont(font2)
        self.comboBox.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.3867, cy:0.392045, radius:0.825346, fx:0.110837, fy:0.125, stop:0.123153 rgba(74, 115, 132, 255), stop:0.817734 rgba(24, 35, 52, 255));\n"
"\n"
"border :1px solid rgb(181, 212, 210);")
        self.comboBox.addItems(titles_)
        self.verticalLayout.addWidget(self.comboBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setText("PREV")
        self.pushButton_3.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.3867, cy:0.392045, radius:0.825346, fx:0.110837, fy:0.125, stop:0.123153 rgba(74, 115, 132, 255), stop:0.817734 rgba(24, 35, 52, 255));\n"
"\n"
"border :1px solid rgb(181, 212, 210);")

        self.pushButton_3.setFont(font2)
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText("OPEN")
        self.pushButton_2.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.3867, cy:0.392045, radius:0.825346, fx:0.110837, fy:0.125, stop:0.123153 rgba(74, 115, 132, 255), stop:0.817734 rgba(24, 35, 52, 255));\n"
"\n"
"border :1px solid rgb(181, 212, 210);")
        self.pushButton_2.setFont(font2)
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("NEXT")
        self.pushButton.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.3867, cy:0.392045, radius:0.825346, fx:0.110837, fy:0.125, stop:0.123153 rgba(74, 115, 132, 255), stop:0.817734 rgba(24, 35, 52, 255));\n"
"\n"
"border :1px solid rgb(181, 212, 210);")
 
        self.pushButton.setFont(font2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout.addWidget(self.pushButton)

        self.set_custom_widget(self.verticalLayoutWidget)
        self.pushButton.clicked.connect(self.NextPhoto_1)
        self.pushButton_2.clicked.connect(self.OpenPhoto_1)
        self.pushButton_3.clicked.connect(self.PreviousPhoto_1)

    @property
    def type_(self):
        return 'ScrollNodeWidget'

    def get_value(self):
        return self.get_custom_widget()

    def set_value(self, state=False):
        if state != self.get_value():
            # self.textEdit_2.toPlainText()
            self.get_custom_widget()

    def OpenPhoto_1(self):
        try:
            self.textEdit_2.setText(notes_[self.comboBox.currentIndex()])
        except IsADirectoryError:
            pass


    def NextPhoto_1(self):
        try:
            length = len(self.comboBox)
            path = self.comboBox.currentText()
            pos = self.comboBox.currentIndex()

            if length-1 == pos:
                print("cant move")
            else:
                self.comboBox.setCurrentIndex(pos+1)

            print(len(self.comboBox), self.comboBox.currentIndex()-1)
            self.textEdit_2.setText(notes_[self.comboBox.currentIndex()])

        except (IndexError, UnboundLocalError):
            print("IndexError")








    def PreviousPhoto_1(self):
        try:
            length = len(self.comboBox)
            path = self.comboBox.currentText()
            pos = self.comboBox.currentIndex() 

            if pos == 0:
                print("cant move")
            else:
                self.comboBox.setCurrentIndex(pos-1)
                self.textEdit_2.setText(notes_[pos-1])

            print(len(self.comboBox), self.comboBox.currentIndex())
            print(titles_[self.comboBox.currentIndex()])
            self.textEdit_2.setText(notes_[self.comboBox.currentIndex()])

        except (IndexError, UnboundLocalError):
            pass










# class NodeScrollText(NodeBaseWidget):

#     def __init__(self, parent=None, name='', label='', text='hi'):
#         super(NodeScrollText, self).__init__(parent, name, label)
#         Form = QtWidgets.QWidget()
#         Form.setStyleSheet("background-color: rgb(0, 0, 0);")
#         widget = QtWidgets.QWidget(Form)
#         widget.setFixedSize(291, 180)
#         # widget.setGeometry(QtCore.QRect(30, 60, 211, 171))
#         widget.setObjectName("widget")
#         scrollArea_2 = QtWidgets.QScrollArea(widget)
#         # scrollArea_2.setGeometry(QtCore.QRect(0, 0, 221, 181))
#         scrollArea_2.setFixedSize(291, 180)
#         scrollArea_2.setWidgetResizable(True)
#         scrollArea_2.setObjectName("scrollArea_2")
#         scrollAreaWidgetContents_2 = QtWidgets.QWidget()
#         # scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 219, 179))
#         scrollAreaWidgetContents_2.setFixedSize(291, 180)
#         scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
#         self.textEdit_2 = QtWidgets.QTextEdit(scrollAreaWidgetContents_2)
#         # self.textEdit_2.setGeometry(QtCore.QRect(0, 0, 211, 171))
#         font = QtGui.QFont()
#         font.setFamily("OCR A Extended")
#         font.setPointSize(20)
#         self.textEdit_2.setFont(font)
#         self.textEdit_2.setFixedSize(291, 180)
#         self.textEdit_2.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.3867, cy:0.392045, radius:0.825346, fx:0.110837, fy:0.125, stop:0.123153 rgba(87, 147, 154, 255), stop:0.817734 rgba(21, 54, 79, 255));\n"
# "color: rgb(255, 255, 255);")

#         self.textEdit_2.setObjectName("textEdit_2")
#         scrollArea_2.setWidget(scrollAreaWidgetContents_2)
#         self.set_custom_widget(scrollArea_2)

#     @property
#     def type_(self):
#         return 'ScrollnNodeWidget'

#     def get_value(self):
#         return self.get_custom_widget()

#     def set_value(self, state=False):
#         if state != self.get_value():
#             # self.textEdit_2.toPlainText()
#             self.get_custom_widget()







class NodeTitle(NodeBaseWidget):

    def __init__(self, parent=None, name='', label='', text='hi'):
        super(NodeTitle, self).__init__(parent, name, label)
        self.label = QtWidgets.QLabel(text)
        self.label.setFixedSize(1012, 179)
        self.label.setText("")
        self.set_custom_widget(self.label)


    @property
    def type_(self):
        return 'TitleWidget'

    def get_value(self):
        return self.get_custom_widget()

    def set_value(self, state=False):
        if state != self.get_value():
            # self.textEdit_2.toPlainText()
            self.get_custom_widget()




# class NodeImage(NodeBaseWidget):

#     def __init__(self, parent=None, name='', label='', text='hi'):
#         super(NodeImage, self).__init__(parent, name, label)
#         _image = QtWidgets.QLabel()
#         # _cbox.setChecked(state)
#         _image.setFixedSize(291, 180)
#         _image.setPixmap(QtGui.QPixmap("AirNotes/IMG_5490.JPG"))
#         _image.setScaledContents(True)

#         # _image.stateChanged.connect(self.on_value_changed)
#         self.set_custom_widget(_image)

#     @property
#     def type_(self):
#         return 'ImageNodeWidget'

#     def get_value(self):
#         """
#         Returns the widget checked state.

#         Returns:
#             bool: checked state.
#         """
#         return self.get_custom_widget()

#     def set_value(self, state=False):
#         """
#         Sets the widget checked state.

#         Args:
#             state (bool): check state.
#         """
#         if state != self.get_value():
#             self.get_custom_widget()

# class NodeScrollText(NodeBaseWidget):

#     def __init__(self, parent=None, name='', label='', text='hi'):
#         super(NodeScrollText, self).__init__(parent, name, label)

#         Form = QtWidgets.QWidget()
#         Form.setStyleSheet("background-color: rgb(0, 0, 0);")
#         scrollArea = QtWidgets.QScrollArea(Form)
#         scrollArea.setGeometry(QtCore.QRect(140, 90, 231, 151))
#         scrollArea.setWidgetResizable(True)
#         scrollArea.setObjectName("scrollArea")
#         scrollAreaWidgetContents = QtWidgets.QWidget()
#         scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 229, 149))
#         scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
#         textEdit = QtWidgets.QTextEdit(scrollAreaWidgetContents)
#         textEdit.setGeometry(QtCore.QRect(0, 0, 231, 151))
#         textEdit.setStyleSheet("background-color: rgb(0, 255, 225);")
#         textEdit.setObjectName("textEdit")
#         scrollArea.setWidget(scrollAreaWidgetContents)
#         self.set_custom_widget(scrollArea)

#     @property
#     def type_(self):
#         return 'ScrollnNodeWidget'


# class NodeButton(NodeBaseWidget):

#     def __init__(self, parent=None, name='', label='', text='hi'):
#         super(NodeButton, self).__init__(parent, name, label)
#         _button = QtWidgets.QPushButton()
#         _button.setText(text)
#         # _cbox.setChecked(state)
#         _button.setMinimumWidth(80)

#         font = _button.font()
#         font.setPointSize(11)
#         _button.setFont(font)
#         # _button.stateChanged.connect(self.on_value_changed)
#         self.set_custom_widget(_button)
#         self.widget().setMaximumWidth(170)

#     @property
#     def type_(self):
#         return 'ButtonNodeWidget'