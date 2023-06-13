#!/usr/bin/python
from collections import OrderedDict

from PyQt5 import QtGui, QtCore, QtWidgets

from NodeGraphQt.constants import (
    ITEM_CACHE_MODE,
    ICON_NODE_BASE,
    NodeEnum,
    PortEnum,
    PortTypeEnum,
    Z_VAL_NODE
)
from NodeGraphQt.errors import NodeWidgetError
from NodeGraphQt.qgraphics.node_abstract import AbstractNodeItem
from NodeGraphQt.qgraphics.node_overlay_disabled import XDisabledItem
from NodeGraphQt.qgraphics.node_text_item import NodeTextItem
from NodeGraphQt.qgraphics.port import PortItem, CustomPortItem




from PyQt5.QtGui import QPolygon
from PyQt5.QtCore import QPoint
import random

class NodeItem(AbstractNodeItem):
    """
    Base Node item.

    Args:
        name (str): name displayed on the node.
        parent (QtWidgets.QGraphicsItem): parent item.
    """

    def __init__(self, name='node', parent=None):
        super(NodeItem, self).__init__(name, parent)
        # pixmap = QtGui.QPixmap(ICON_NODE_BASE)
        # if pixmap.size().height() > NodeEnum.ICON_SIZE.value:
        #     pixmap = pixmap.scaledToHeight(
        #         NodeEnum.ICON_SIZE.value,
        #         QtCore.Qt.SmoothTransformation
        #     )
        # self._properties['icon'] = ICON_NODE_BASE
        # self._icon_item = QtWidgets.QGraphicsPixmapItem(pixmap, self)
        # self._icon_item.setTransformationMode(QtCore.Qt.SmoothTransformation)
        self._text_item = NodeTextItem(self.name, self)
        self._x_item = XDisabledItem(self, 'DISABLED')
        self._input_items = OrderedDict()
        self._output_items = OrderedDict()
        self._widgets = OrderedDict()
        self._proxy_mode = False
        self._proxy_mode_threshold = 70






    # def paint(self, painter, option, widget):


    #     """
    #     Draws the node base not the ports or text.

    #     Args:
    #         painter (QtGui.QPainter): painter used for drawing the item.
    #         option (QtGui.QStyleOptionGraphicsItem):
    #             used to describe the parameters needed to draw.
    #         widget (QtWidgets.QWidget): not used.
    #     """
    #     self.auto_switch_mode()

    #     painter.save()
    #     painter.setPen(QtCore.Qt.NoPen)
    #     painter.setBrush(QtCore.Qt.NoBrush)

    #     # base background.
    #     margin = 1.0
    #     rect = self.boundingRect()
    #     rect = QtCore.QRectF(rect.left() + margin,
    #                          rect.top() + margin,
    #                          rect.width() - (margin * 2),
    #                          rect.height() - (margin * 2))

    #     radius = 10.0
    #     print(*self.color)

    #     gradient = QtGui.QRadialGradient(0.3867, 0.392045, 0.825346, 0.110837, 0.125)
    #     gradient.setSpread(QtGui.QGradient.PadSpread)
    #     gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
    #     gradient.setColorAt(0.123153, QtGui.QColor(74, 115, 132))
    #     gradient.setColorAt(0.817734, QtGui.QColor(24, 35, 52))
    #     brush = QtGui.QBrush(gradient)


    #     # gradient = QtGui.QPixmap("background_test.jpg")
    #     # brush = QtGui.QBrush(gradient)


    #     painter.setBrush(brush)
    #     painter.drawRoundedRect(rect, radius, radius)

    #     # light overlay on background when selected.
    #     if self.selected:

    #         gradient = QtGui.QRadialGradient(0.3867, 0.392045, 0.825346, 0.110837, 0.125)
    #         gradient.setSpread(QtGui.QGradient.PadSpread)
    #         gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
    #         gradient.setColorAt(0.123153, QtGui.QColor(74, 115, 132))
    #         gradient.setColorAt(0.817734, QtGui.QColor(24, 35, 52))
    #         brush = QtGui.QBrush(gradient)

    #         # gradient = QtGui.QPixmap("background_test.jpg")
    #         # brush = QtGui.QBrush(gradient)


    #         painter.setBrush(brush)
    #         # painter.setBrush(QtGui.QColor(*NodeEnum.SELECTED_COLOR.value))
    #         painter.drawRoundedRect(rect, radius, radius)

    #     # node name background.
    #     padding = 3.0, 2.0
    #     text_rect = self._text_item.boundingRect()
    #     text_rect = QtCore.QRectF(text_rect.x() + padding[0],
    #                               rect.y() + padding[1],
    #                               rect.width() - padding[0] - margin,
    #                               text_rect.height() - (padding[1] * 2))
    #     if self.selected:


    #         gradient = QtGui.QRadialGradient(0.3867, 0.392045, 0.825346, 0.110837, 0.125)
    #         gradient.setSpread(QtGui.QGradient.PadSpread)
    #         gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
    #         gradient.setColorAt(0.123153, QtGui.QColor(74, 115, 132))
    #         gradient.setColorAt(0.817734, QtGui.QColor(24, 35, 52))
    #         brush = QtGui.QBrush(gradient)

    #         painter.setBrush(brush)

    #         # painter.setBrush(QtGui.QColor(*NodeEnum.SELECTED_COLOR.value))
    #     else:
    #         painter.setBrush(QtGui.QColor(0, 0, 0, 80))
    #     painter.drawRoundedRect(text_rect, 3.0, 3.0)

    #     # node border
    #     if self.selected:
    #         border_width = 1.2
    #         border_color = QtGui.QColor(
    #             *NodeEnum.SELECTED_BORDER_COLOR.value
    #         )
    #     else:
    #         border_width = 0.8
    #         border_color = QtGui.QColor(*self.border_color)

    #     border_rect = QtCore.QRectF(rect.left(), rect.top(),
    #                                 rect.width(), rect.height())

    #     print("dimentions:", rect.left(), rect.top(),
    #                                 rect.width(), rect.height())

    #     pen = QtGui.QPen(border_color, border_width)
    #     pen.setCosmetic(self.viewer().get_zoom() < 0.0)
    #     path = QtGui.QPainterPath()
    #     path.addRoundedRect(border_rect, radius, radius)
    #     painter.setBrush(QtCore.Qt.NoBrush)
    #     painter.setPen(pen)
    #     painter.drawPath(path)

    #     painter.restore()


    def paint(self, painter, option, widget):

        print(self.type_)

        rect = self.boundingRect()
        margin = 1.0
        rect = QtCore.QRectF(rect.left() + margin,
                             rect.top() + margin,
                             rect.width() - (margin * 2),
                             rect.height() - (margin * 2))

        # print("dimentions:", rect.left(), rect.top(),
        #                             int(round(rect.width())), int(round(rect.height())))

        margin = 1.0



        # Horizontal_dimentions = (680, 443)
        # Vertical_dimentions = (585, 632)
        # scroll_dimentions = (493, 291)


        # node border
        if self.selected:
            border_width = 1.2
            border_color = QtGui.QColor(
                *NodeEnum.SELECTED_BORDER_COLOR.value
            )
        else:
            border_width = 0.8
            border_color = QtGui.QColor(*self.border_color)


        self.auto_switch_mode()
        painter.save()


        painter.setPen(QtGui.QPen(QtGui.QColor(85, 120, 150), 0, QtCore.Qt.SolidLine))
        painter.setBrush(QtCore.Qt.NoBrush)


        # brush = QtGui.QBrush(gradient)
        # painter.setBrush(brush)


        # print(bool(random.getrandbits(1)))


        # if self.type_ == "nodes.custom.ports.ImageNodeV"
        # if self.type_ == "nodes.custom.ports.ImageNodeH"
        # if self.type_ == "nodes.custom.ports.ScrollNode"

        if self.type_ == "nodes.custom.ports.ImageNodeH":



            if False: #bool(random.choice([True, False]))
                gradient = QtGui.QPixmap("NodeGraphQt/qgraphics/f1.png")
                brush = QtGui.QBrush(gradient)
                painter.setBrush(brush)
                points = QtGui.QPolygon([
                QtCore.QPoint(66,0),
                QtCore.QPoint(617,0),
                QtCore.QPoint(683,66),
                QtCore.QPoint(683,380),
                QtCore.QPoint(617,446),
                QtCore.QPoint(66,446),
                QtCore.QPoint(0, 380),
                QtCore.QPoint(0, 66), ])
                painter.drawPolygon(points)
                print("Horizontal image 1")
            else:
                gradient = QtGui.QPixmap("NodeGraphQt/qgraphics/f1.png")
                brush = QtGui.QBrush(gradient)
                painter.setBrush(brush)
                points = QPolygon([
                QPoint(40,10),
                QPoint(394,11),
                QPoint(404,0),
                QPoint(553,0),
                QPoint(683,131),
                QPoint(683,396),
                QPoint(633,445),
                QPoint(50,445),
                QPoint(0,396),
                QPoint(0,324),
                QPoint(13,313),
                QPoint(13, 213),
                QPoint(13, 214),
                QPoint(0, 203),
                QPoint(0, 50)])
                painter.drawPolygon(points)
                print("Horizontal image 2")

                # QPoint(683,202),
                # QPoint(670, 214),
                # QPoint(670, 312),
                # QPoint(683,324),


        elif self.type_ == "nodes.custom.ports.ImageNodeV":
            gradient = QtGui.QPixmap("NodeGraphQt/qgraphics/f3.png")
            brush = QtGui.QBrush(gradient)
            painter.setBrush(brush)
            points = QPolygon([
            QPoint(130,0),
            QPoint(488,0),
            QPoint(537,50),
            QPoint(575,50),
            QPoint(588,63),
            QPoint(588,572),
            QPoint(575, 585),
            QPoint(537, 585),
            QPoint(488,635),
            QPoint(50,635),
            QPoint(0,585),
            QPoint(0,443),
            QPoint(13,430),
            QPoint(13,285),
            QPoint(0, 273),
            QPoint(0, 130)])
            painter.drawPolygon(points)
            print("Vertical image")


        elif self.type_ == "nodes.custom.ports.ScrollNode":
            gradient = QtGui.QPixmap("NodeGraphQt/qgraphics/f2.png")
            brush = QtGui.QBrush(gradient)
            painter.setBrush(brush)
            points = QPolygon([
            QPoint(50,13),
            QPoint(234,13),
            QPoint(247,0),
            QPoint(395,0),
            QPoint(495,100),
            QPoint(495,259),
            QPoint(460, 293),

            QPoint(23, 293),
            QPoint(13,282),
            QPoint(13,234),
            QPoint(0,220),
            QPoint(0,63)])
            painter.drawPolygon(points)
            print("Scroll image")

        elif self.type_ == "nodes.widget.TitleNode":
            painter.drawPixmap(0, 0, 1012, 179, QtGui.QPixmap("NodeGraphQt/qgraphics/prime_title.png"))
            print("Title")

        else:

        # base background.
            margin = 1.0
            rect = self.boundingRect()
            rect = QtCore.QRectF(rect.left() + margin,
                                rect.top() + margin,
                                rect.width() - (margin * 2),
                                rect.height() - (margin * 2))

            radius = 10.0
            gradient = QtGui.QRadialGradient(0.3867, 0.392045, 0.825346, 0.110837, 0.125)
            gradient.setSpread(QtGui.QGradient.PadSpread)
            gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
            gradient.setColorAt(0.123153, QtGui.QColor(74, 115, 132))
            gradient.setColorAt(0.817734, QtGui.QColor(24, 35, 52))
            brush = QtGui.QBrush(gradient)
            painter.setBrush(brush)
            painter.drawRoundedRect(rect, radius, radius)

            # light overlay on background when selected.
            if self.selected:
                gradient = QtGui.QRadialGradient(0.3867, 0.392045, 0.825346, 0.110837, 0.125)
                gradient.setSpread(QtGui.QGradient.PadSpread)
                gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
                gradient.setColorAt(0.123153, QtGui.QColor(74, 115, 132))
                gradient.setColorAt(0.817734, QtGui.QColor(24, 35, 52))
                brush = QtGui.QBrush(gradient)
                # gradient = QtGui.QPixmap("background_test.jpg")
                # brush = QtGui.QBrush(gradient)
                painter.setBrush(brush)
                # painter.setBrush(QtGui.QColor(*NodeEnum.SELECTED_COLOR.value))
                painter.drawRoundedRect(rect, radius, radius)

            # node name background.
            padding = 3.0, 2.0
            text_rect = self._text_item.boundingRect()
            text_rect = QtCore.QRectF(text_rect.x() + padding[0],
                                    rect.y() + padding[1],
                                    rect.width() - padding[0] - margin,
                                    text_rect.height() - (padding[1] * 2))
            if self.selected:
                gradient = QtGui.QRadialGradient(0.3867, 0.392045, 0.825346, 0.110837, 0.125)
                gradient.setSpread(QtGui.QGradient.PadSpread)
                gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
                gradient.setColorAt(0.123153, QtGui.QColor(74, 115, 132))
                gradient.setColorAt(0.817734, QtGui.QColor(24, 35, 52))
                brush = QtGui.QBrush(gradient)
                painter.setBrush(brush)
                # painter.setBrush(QtGui.QColor(*NodeEnum.SELECTED_COLOR.value))
            else:
                painter.setBrush(QtGui.QColor(0, 0, 0, 80))
            painter.drawRoundedRect(text_rect, 3.0, 3.0)

            # node border
            if self.selected:
                border_width = 1.2
                border_color = QtGui.QColor(
                    *NodeEnum.SELECTED_BORDER_COLOR.value
                )
            else:
                border_width = 0.8
                border_color = QtGui.QColor(*self.border_color)

            border_rect = QtCore.QRectF(rect.left(), rect.top(),
                                        rect.width(), rect.height())

            print("dimentions:", rect.left(), rect.top(),
                                        rect.width(), rect.height())

            pen = QtGui.QPen(border_color, border_width)
            pen.setCosmetic(self.viewer().get_zoom() < 0.0)
            path = QtGui.QPainterPath()
            path.addRoundedRect(border_rect, radius, radius)
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.setPen(pen)
            painter.drawPath(path)

            # painter.restore()




        pen = QtGui.QPen(border_color, border_width)
        pen.setCosmetic(self.viewer().get_zoom() < 0.0)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(pen)

        painter.restore()









    def mousePressEvent(self, event):
        """
        Re-implemented to ignore event if LMB is over port collision area.

        Args:
            event (QtWidgets.QGraphicsSceneMouseEvent): mouse event.
        """
        if event.button() == QtCore.Qt.LeftButton:
            for p in self._input_items.keys():
                if p.hovered:
                    event.ignore()
                    return
            for p in self._output_items.keys():
                if p.hovered:
                    event.ignore()
                    return
        super(NodeItem, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Re-implemented to ignore event if Alt modifier is pressed.

        Args:
            event (QtWidgets.QGraphicsSceneMouseEvent): mouse event.
        """
        if event.modifiers() == QtCore.Qt.AltModifier:
            event.ignore()
            return
        super(NodeItem, self).mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        """
        Re-implemented to emit "node_double_clicked" signal.

        Args:
            event (QtWidgets.QGraphicsSceneMouseEvent): mouse event.
        """
        if event.button() == QtCore.Qt.LeftButton:

            # enable text item edit mode.
            items = self.scene().items(event.scenePos())
            if self._text_item in items:
                self._text_item.set_editable(True)
                self._text_item.setFocus()
                event.ignore()
                return

            viewer = self.viewer()
            if viewer:
                viewer.node_double_clicked.emit(self.id)
        super(NodeItem, self).mouseDoubleClickEvent(event)

    def itemChange(self, change, value):
        """
        Re-implemented to update pipes on selection changed.

        Args:
            change:
            value:
        """
        if change == self.ItemSelectedChange and self.scene():
            self.reset_pipes()
            if value:
                self.highlight_pipes()
            self.setZValue(Z_VAL_NODE)
            if not self.selected:
                self.setZValue(Z_VAL_NODE + 1)

        return super(NodeItem, self).itemChange(change, value)

    def _tooltip_disable(self, state):
        """
        Updates the node tooltip when the node is enabled/disabled.

        Args:
            state (bool): node disable state.
        """
        tooltip = '<b>{}</b>'.format(self.name)
        if state:
            tooltip += ' <font color="red"><b>(DISABLED)</b></font>'
        tooltip += '<br/>{}<br/>'.format(self.type_)
        self.setToolTip(tooltip)

    def _set_base_size(self, add_w=0.0, add_h=0.0):
        """
        Sets the initial base size for the node.

        Args:
            add_w (float): add additional width.
            add_h (float): add additional height.
        """
        self._width, self._height = self.calc_size(add_w, add_h)
        if self._width < NodeEnum.WIDTH.value:
            self._width = NodeEnum.WIDTH.value
        if self._height < NodeEnum.HEIGHT.value:
            self._height = NodeEnum.HEIGHT.value

    def _set_text_color(self, color):
        """
        set text color.

        Args:
            color (tuple): color value in (r, g, b, a).
        """

        text_color = QtGui.QColor(*color)
        for port, text in self._input_items.items():
            text.setDefaultTextColor(text_color)
            text.setFont(QtGui.QFont('OCR A Extended'))
        for port, text in self._output_items.items():
            text.setDefaultTextColor(text_color)
            text.setFont(QtGui.QFont('OCR A Extended'))
        self._text_item.setDefaultTextColor(text_color)
        self._text_item.setFont(QtGui.QFont('OCR A Extended'))

    def activate_pipes(self):
        """
        active pipe color.
        """
        ports = self.inputs + self.outputs
        for port in ports:
            for pipe in port.connected_pipes:
                pipe.activate()

    def highlight_pipes(self):
        """
        Highlight pipe color.
        """
        ports = self.inputs + self.outputs
        for port in ports:
            for pipe in port.connected_pipes:
                pipe.highlight()

    def reset_pipes(self):
        """
        Reset all the pipe colors.
        """
        ports = self.inputs + self.outputs
        for port in ports:
            for pipe in port.connected_pipes:
                pipe.reset()

    def calc_size(self, add_w=0.0, add_h=0.0):
        """
        Calculates the minimum node size.

        Args:
            add_w (float): additional width.
            add_h (float): additional height.

        Returns:
            tuple(float, float): width, height.
        """
        # width, height from node name text.
        text_w = self._text_item.boundingRect().width()
        text_h = self._text_item.boundingRect().height()

        # width, height from node ports.
        port_width = 0.0
        p_input_text_width = 0.0
        p_output_text_width = 0.0
        p_input_height = 0.0
        p_output_height = 0.0
        for port, text in self._input_items.items():
            if not port.isVisible():
                continue
            if not port_width:
                port_width = port.boundingRect().width()
            t_width = text.boundingRect().width()
            if text.isVisible() and t_width > p_input_text_width:
                p_input_text_width = text.boundingRect().width()
            p_input_height += port.boundingRect().height()
        for port, text in self._output_items.items():
            if not port.isVisible():
                continue
            if not port_width:
                port_width = port.boundingRect().width()
            t_width = text.boundingRect().width()
            if text.isVisible() and t_width > p_output_text_width:
                p_output_text_width = text.boundingRect().width()
            p_output_height += port.boundingRect().height()

        port_text_width = p_input_text_width + p_output_text_width

        # width, height from node embedded widgets.
        widget_width = 0.0
        widget_height = 0.0
        for widget in self._widgets.values():
            w_width = widget.boundingRect().width()
            w_height = widget.boundingRect().height()
            if w_width > widget_width:
                widget_width = w_width
            widget_height += w_height

        side_padding = 0.0
        if all([widget_width, p_input_text_width, p_output_text_width]):
            port_text_width = max([p_input_text_width, p_output_text_width])
            port_text_width *= 2
        elif widget_width:
            side_padding = 10

        width = port_width + max([text_w, port_text_width]) + side_padding
        height = max([text_h, p_input_height, p_output_height, widget_height])
        if widget_width:
            # add additional width for node widget.
            width += widget_width
        if widget_height:
            # add bottom margin for node widget.
            height += 4.0
        height *= 1.05

        # additional width, height.
        width += add_w
        height += add_h
        return width, height

    # def align_icon(self, h_offset=0.0, v_offset=0.0):
    #     """
    #     Align node icon to the default top left of the node.

    #     Args:
    #         v_offset (float): additional vertical offset.
    #         h_offset (float): additional horizontal offset.
    #     """
    #     icon_rect = self._icon_item.boundingRect()
    #     text_rect = self._text_item.boundingRect()
    #     x = self.boundingRect().left() + 2.0
    #     y = text_rect.center().y() - (icon_rect.height() / 2)
    #     self._icon_item.setPos(x + h_offset, y + v_offset)

    def align_label(self, h_offset=0.0, v_offset=0.0):
        """
        Center node label text to the top of the node.

        Args:
            v_offset (float): vertical offset.
            h_offset (float): horizontal offset.
        """
        rect = self.boundingRect()
        text_rect = self._text_item.boundingRect()
        x = rect.center().x() - (text_rect.width() / 2)
        self._text_item.setPos(x + h_offset, rect.y() + v_offset)

    def align_widgets(self, v_offset=0.0):
        """
        Align node widgets to the default center of the node.

        Args:
            v_offset (float): vertical offset.
        """
        if not self._widgets:
            return
        rect = self.boundingRect()
        y = rect.y() + v_offset
        inputs = [p for p in self.inputs if p.isVisible()]
        outputs = [p for p in self.outputs if p.isVisible()]
        for widget in self._widgets.values():
            widget_rect = widget.boundingRect()
            # widget.widget().setFont(QtGui.QFont('OCR A Extended'))
            if not inputs:
                x = rect.left() + 10
                widget.widget().setTitleAlign('left')
            elif not outputs:
                x = rect.right() - widget_rect.width() - 10
                widget.widget().setTitleAlign('right')
            else:
                x = rect.center().x() - (widget_rect.width() / 2)
                widget.widget().setTitleAlign('center')
                # widget.widget().setFont(QtGui.QFont('OCR A Extended'))

            widget.setPos(x, y)
            y += widget_rect.height()

    def align_ports(self, v_offset=0.0, v_out_offset=0.0, h_out_offset=0.0):
        
        """
        Align input, output ports in the node layout.

        Args:
            v_offset (float): port vertical offset.
        """
        width = self._width
        txt_offset = PortEnum.CLICK_FALLOFF.value - 2
        spacing = 1

        # adjust input position
        inputs = [p for p in self.inputs if p.isVisible()]
        if inputs:
            port_width = inputs[0].boundingRect().width()
            port_height = inputs[0].boundingRect().height()
            port_x = (port_width / 2) * -1
            # port_x = port_x + h_out_offset

            # if self.type_ == "nodes.custom.ports.ImageNodeV"
            # if self.type_ == "nodes.custom.ports.ImageNodeH"
            # if self.type_ == "nodes.custom.ports.ScrollNode"


            port_y = v_offset #this is where you change the position of the nodes
            for port in inputs:
                port.setPos(port_x, port_y)
                port_y += port_height + spacing
        # adjust input text position
        for port, text in self._input_items.items():
            if port.isVisible():
                txt_x = port.boundingRect().width() / 2 - txt_offset
                text.setPos(txt_x, port.y() - 1.5)
                text.setFont(QtGui.QFont('OCR A Extended'))

        # adjust output position
        outputs = [p for p in self.outputs if p.isVisible()]
        if outputs:
            port_width = outputs[0].boundingRect().width()
            port_height = outputs[0].boundingRect().height()
            port_x = width - (port_width / 2)
            port_x = port_x + h_out_offset

            # if self.type_ == "nodes.custom.ports.ImageNodeV"
            # if self.type_ == "nodes.custom.ports.ImageNodeH"
            # if self.type_ == "nodes.custom.ports.ScrollNode"

            port_y = v_out_offset #this is where you change the position of the nodes
            for port in outputs:
                port.setPos(port_x, port_y)
                port_y += port_height + spacing
        # adjust output text position
        for port, text in self._output_items.items():
            if port.isVisible():
                txt_width = text.boundingRect().width() - txt_offset
                txt_x = port.x() - txt_width
                text.setPos(txt_x, port.y() - 1.5)
                text.setFont(QtGui.QFont('OCR A Extended'))


    def draw_node(self):
        """
        Re-draw the node item in the scene.
        (re-implemented for vertical layout design)
        """
        height = self._text_item.boundingRect().height() + 4.0

        # setup initial base size.
        self._set_base_size(add_h=height)
        # set text color when node is initialized.
        self._set_text_color(self.text_color)
        # set the tooltip
        self._tooltip_disable(self.disabled)

        # --- set the initial node layout ---
        # (do all the graphic item layout offsets here)

        # align label text

        if self.type_ == "nodes.custom.ports.ImageNodeH":
            self.align_label(h_offset=138)
            # self.align_icon(h_offset=42.0, v_offset=3.0)
            self.align_ports(v_offset=56, v_out_offset=137)
            self.align_widgets(v_offset=(height+20))

        elif self.type_ == "nodes.custom.ports.ImageNodeV":
            self.align_label(h_offset=31)
            # self.align_icon(h_offset=2.0, v_offset=1.0)
            self.align_ports(v_offset=134, v_out_offset=67) #h_out_offset=-67
            self.align_widgets(v_offset=(height+20))

        elif self.type_ == "nodes.custom.ports.ScrollNode":
            self.align_label(h_offset=73)
            # self.align_icon(h_offset=2.0, v_offset=1.0)
            self.align_ports(v_offset=72, v_out_offset=110)
            self.align_widgets(v_offset=height)

        elif self.type_ == "nodes.widget.TitleNode":
            self._text_item.setVisible(False)
            # self.align_label(h_offset=73)
            # self.align_ports(v_offset=72, v_out_offset=110)
            self.align_widgets(v_offset=height)

        else:
            self.align_label(h_offset=0.0)
            # align icon
            # self.align_icon(h_offset=2.0, v_offset=1.0)
            # arrange input and output ports.
            self.align_ports(v_offset=height, v_out_offset=height)
            # arrange node widgets (changing how far down the pages the wirgets have been moved)
            self.align_widgets(v_offset=height)



        self.update()

    def post_init(self, viewer=None, pos=None):
        """
        Called after node has been added into the scene.
        Adjust the node layout and form after the node has been added.

        Args:
            viewer (NodeGraphQt.widgets.viewer.NodeViewer): not used
            pos (tuple): cursor position.
        """
        self.draw_node()

        # set initial node position.
        if pos:
            self.xy_pos = pos

    def auto_switch_mode(self):
        """
        Decide whether to draw the node with proxy mode.
        (this is called at the start in the "self.paint()" function.)
        """
        if ITEM_CACHE_MODE is QtWidgets.QGraphicsItem.ItemCoordinateCache:
            return

        rect = self.sceneBoundingRect()
        l = self.viewer().mapToGlobal(
            self.viewer().mapFromScene(rect.topLeft()))
        r = self.viewer().mapToGlobal(
            self.viewer().mapFromScene(rect.topRight()))
        # width is the node width in screen
        width = r.x() - l.x()

        self.set_proxy_mode(width < self._proxy_mode_threshold)

    def set_proxy_mode(self, mode):
        """
        Set whether to draw the node with proxy mode.
        (proxy mode toggles visibility for some qgraphic items in the node.)

        Args:
            mode (bool): true to enable proxy mode.
        """
        if mode is self._proxy_mode:
            return
        self._proxy_mode = mode

        visible = not mode

        # disable overlay item.
        self._x_item.proxy_mode = self._proxy_mode

        # node widget visibility.
        for w in self._widgets.values():
            w.widget().setVisible(visible)

        # input port text visibility.
        for port, text in self._input_items.items():
            if port.display_name:
                text.setVisible(visible)

        # output port text visibility.
        for port, text in self._output_items.items():
            if port.display_name:
                text.setVisible(visible)

        self._text_item.setVisible(visible)
        # self._icon_item.setVisible(visible)

    # @property
    # def icon(self):
    #     return self._properties['icon']

    # @icon.setter
    # def icon(self, path=None):
    #     self._properties['icon'] = path
    #     path = path or ICON_NODE_BASE
    #     pixmap = QtGui.QPixmap(path)
    #     if pixmap.size().height() > NodeEnum.ICON_SIZE.value:
    #         pixmap = pixmap.scaledToHeight(
    #             NodeEnum.ICON_SIZE.value,
    #             QtCore.Qt.SmoothTransformation
    #         )
    #     self._icon_item.setPixmap(pixmap)
    #     if self.scene():
    #         self.post_init()

    #     self.update()

    @AbstractNodeItem.width.setter
    def width(self, width=0.0):
        w, h = self.calc_size()
        width = width if width > w else w
        AbstractNodeItem.width.fset(self, width)

    @AbstractNodeItem.height.setter
    def height(self, height=0.0):
        w, h = self.calc_size()
        h = 70 if h < 70 else h
        height = height if height > h else h
        AbstractNodeItem.height.fset(self, height)

    @AbstractNodeItem.disabled.setter
    def disabled(self, state=False):
        AbstractNodeItem.disabled.fset(self, state)
        for n, w in self._widgets.items():
            w.widget().setDisabled(state)
        self._tooltip_disable(state)
        self._x_item.setVisible(state)

    @AbstractNodeItem.selected.setter
    def selected(self, selected=False):
        AbstractNodeItem.selected.fset(self, selected)
        if selected:
            self.highlight_pipes()

    @AbstractNodeItem.name.setter
    def name(self, name=''):
        AbstractNodeItem.name.fset(self, name)
        if name == self._text_item.toPlainText():
            return
        self._text_item.setPlainText(name)
        if self.scene():
            self.align_label()
        self.update()

    @AbstractNodeItem.color.setter
    def color(self, color=(100, 100, 100, 255)):
        AbstractNodeItem.color.fset(self, color)
        if self.scene():
            self.scene().update()
        self.update()

    @AbstractNodeItem.text_color.setter
    def text_color(self, color=(100, 100, 100, 255)):
        AbstractNodeItem.text_color.fset(self, color)
        self._set_text_color(color)
        self.update()

    @property
    def text_item(self):
        """
        Get the node name text qgraphics item.

        Returns:
            NodeTextItem: node text object.
        """
        return self._text_item

    @property
    def inputs(self):
        """
        Returns:
            list[PortItem]: input port graphic items.
        """
        return list(self._input_items.keys())

    @property
    def outputs(self):
        """
        Returns:
            list[PortItem]: output port graphic items.
        """
        return list(self._output_items.keys())

    def _add_port(self, port):
        """
        Adds a port qgraphics item into the node.

        Args:
            port (PortItem): port item.

        Returns:
            PortItem: port qgraphics item.
        """
        text = QtWidgets.QGraphicsTextItem(port.name, self)
        text.font().setPointSize(8)
        text.setFont(text.font())
        text.setVisible(port.display_name)
        text.setCacheMode(ITEM_CACHE_MODE)
        if port.port_type == PortTypeEnum.IN.value:
            self._input_items[port] = text
        elif port.port_type == PortTypeEnum.OUT.value:
            self._output_items[port] = text
        if self.scene():
            self.post_init()
        return port

    def add_input(self, name='input', multi_port=False, display_name=True,
                  locked=False, painter_func=None):
        """
        Adds a port qgraphics item into the node with the "port_type" set as
        IN_PORT.

        Args:
            name (str): name for the port.
            multi_port (bool): allow multiple connections.
            display_name (bool): display the port name.
            locked (bool): locked state.
            painter_func (function): custom paint function.

        Returns:
            PortItem: input port qgraphics item.
        """
        if painter_func:
            port = CustomPortItem(self, painter_func)
        else:
            port = PortItem(self)
        port.name = name
        port.port_type = PortTypeEnum.IN.value
        port.multi_connection = multi_port
        port.display_name = display_name
        port.locked = locked
        return self._add_port(port)

    def add_output(self, name='output', multi_port=False, display_name=True,
                   locked=False, painter_func=None):
        """
        Adds a port qgraphics item into the node with the "port_type" set as
        OUT_PORT.

        Args:
            name (str): name for the port.
            multi_port (bool): allow multiple connections.
            display_name (bool): display the port name.
            locked (bool): locked state.
            painter_func (function): custom paint function.

        Returns:
            PortItem: output port qgraphics item.
        """
        if painter_func:
            port = CustomPortItem(self, painter_func)
        else:
            port = PortItem(self)
        port.name = name
        port.port_type = PortTypeEnum.OUT.value
        port.multi_connection = multi_port
        port.display_name = display_name
        port.locked = locked
        return self._add_port(port)

    def _delete_port(self, port, text):
        """
        Removes port item and port text from node.

        Args:
            port (PortItem): port object.
            text (QtWidgets.QGraphicsTextItem): port text object.
        """
        port.setParentItem(None)
        text.setParentItem(None)
        self.scene().removeItem(port)
        self.scene().removeItem(text)
        del port
        del text

    def delete_input(self, port):
        """
        Remove input port from node.

        Args:
            port (PortItem): port object.
        """
        self._delete_port(port, self._input_items.pop(port))

    def delete_output(self, port):
        """
        Remove output port from node.

        Args:
            port (PortItem): port object.
        """
        self._delete_port(port, self._output_items.pop(port))

    def get_input_text_item(self, port_item):
        """
        Args:
            port_item (PortItem): port item.

        Returns:
            QGraphicsTextItem: graphic item used for the port text.
        """
        return self._input_items[port_item]

    def get_output_text_item(self, port_item):
        """
        Args:
            port_item (PortItem): port item.

        Returns:
            QGraphicsTextItem: graphic item used for the port text.
        """
        return self._output_items[port_item]

    @property
    def widgets(self):
        return self._widgets.copy()

    def add_widget(self, widget):
        self._widgets[widget.get_name()] = widget

    def get_widget(self, name):
        widget = self._widgets.get(name)
        if widget:
            return widget
        raise NodeWidgetError('node has no widget "{}"'.format(name))

    def has_widget(self, name):
        return name in self._widgets.keys()

    def from_dict(self, node_dict):
        super(NodeItem, self).from_dict(node_dict)
        widgets = node_dict.pop('widgets', {})
        for name, value in widgets.items():
            if self._widgets.get(name):
                self._widgets[name].value = value


class NodeItemVertical(NodeItem):
    """
    Vertical Node item.

    Args:
        name (str): name displayed on the node.
        parent (QtWidgets.QGraphicsItem): parent item.
    """

    def __init__(self, name='node', parent=None):
        super(NodeItemVertical, self).__init__(name, parent)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.text_item.setFont(font)

    def paint(self, painter, option, widget):
        """
        Draws the node base not the ports.

        Args:
            painter (QtGui.QPainter): painter used for drawing the item.
            option (QtGui.QStyleOptionGraphicsItem):
                used to describe the parameters needed to draw.
            widget (QtWidgets.QWidget): not used.
        """
        self.auto_switch_mode()

        painter.save()
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.NoBrush)

        # base background.
        margin = 1.0
        rect = self.boundingRect()
        rect = QtCore.QRectF(rect.left() + margin,
                             rect.top() + margin,
                             rect.width() - (margin * 2),
                             rect.height() - (margin * 2))

        radius = 4.0
        painter.setBrush(QtGui.QColor(*self.color))
        painter.drawRoundedRect(rect, radius, radius)

        # light overlay on background when selected.
        if self.selected:
            painter.setBrush(
                QtGui.QColor(*NodeEnum.SELECTED_COLOR.value)
            )
            painter.drawRoundedRect(rect, radius, radius)

        # top & bottom edge background.
        padding = 2.0
        height = 10
        if self.selected:
            painter.setBrush(QtGui.QColor(*NodeEnum.SELECTED_COLOR.value))
        else:
            painter.setBrush(QtGui.QColor(0, 0, 0, 80))
        for y in [rect.y() + padding, rect.height() - height - 1]:
            edge_rect = QtCore.QRectF(rect.x() + padding, y,
                                     rect.width() - (padding * 2), height)
            painter.drawRoundedRect(edge_rect, 3.0, 3.0)

        # node border
        border_width = 0.8
        border_color = QtGui.QColor(*self.border_color)
        if self.selected:
            border_width = 1.2
            border_color = QtGui.QColor(
                *NodeEnum.SELECTED_BORDER_COLOR.value
            )
        border_rect = QtCore.QRectF(rect.left(), rect.top(),
                                    rect.width(), rect.height())

        pen = QtGui.QPen(border_color, border_width)
        pen.setCosmetic(self.viewer().get_zoom() < 0.0)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(pen)
        painter.drawRoundedRect(border_rect, radius, radius)

        painter.restore()

    # def align_icon(self, h_offset=0.0, v_offset=0.0):
    #     """
    #     Align node icon to the right side of the node.

    #     Args:
    #         v_offset (float): vertical offset.
    #         h_offset (float): horizontal offset.
    #     """
    #     center_y = self.boundingRect().center().y()
    #     icon_rect = self._icon_item.boundingRect()
    #     text_rect = self._text_item.boundingRect()
    #     x = self.boundingRect().right() + h_offset
    #     y = center_y - text_rect.height() - (icon_rect.height() / 2) + v_offset
    #     self._icon_item.setPos(x, y)

    def align_label(self, h_offset=0.0, v_offset=0.0):
        """
        Align node label to the right side of the node.

        Args:
            v_offset (float): vertical offset.
            h_offset (float): horizontal offset.
        """
        rect = self._text_item.boundingRect()
        x = self.boundingRect().right() + h_offset
        y = self.boundingRect().center().y() - (rect.height() / 2) + v_offset
        self.text_item.setPos(x, y)

    def align_ports(self, v_offset=0.0, h_offset=0.0):
        """
        Align input, output ports in the node layout.
        """
        # adjust input position
        inputs = [p for p in self.inputs if p.isVisible()]
        if inputs:
            port_width = inputs[0].boundingRect().width()
            port_height = inputs[0].boundingRect().height()
            half_width = port_width/2
            delta = self._width / (len(inputs)+1)
            port_x = delta
            port_y = (port_height / 2) * -1
            for port in inputs:
                port.setPos(port_x - half_width, port_y)
                port_x += delta

        # adjust output position
        outputs = [p for p in self.outputs if p.isVisible()]
        if outputs:
            port_width = outputs[0].boundingRect().width()
            port_height = outputs[0].boundingRect().height()
            half_width = port_width / 2
            delta = self._width / (len(outputs)+1)
            port_x = delta
            port_y = self._height - (port_height / 2)
            for port in outputs:
                port.setPos(port_x-half_width, port_y)
                port_x += delta

    def align_widgets(self, v_offset=0.0):
        """
        Align node widgets to the default center of the node.

        Args:
            v_offset (float): vertical offset.
        """
        if not self._widgets:
            return
        rect = self.boundingRect()
        y = rect.center().y() + v_offset
        widget_height = 0.0
        for widget in self._widgets.values():
            widget_rect = widget.boundingRect()
            widget_height += widget_rect.height()
        y -= widget_height / 2

        for widget in self._widgets.values():
            widget_rect = widget.boundingRect()
            x = rect.center().x() - (widget_rect.width() / 2)
            widget.widget().setTitleAlign('center')
            widget.setPos(x, y)
            y += widget_rect.height()

    def draw_node(self):
        """
        Re-draw the node item in the scene.
        """
        # setup initial base size.
        self._set_base_size()
        # set text color when node is initialized.
        self._set_text_color(self.text_color)
        # set the tooltip
        self._tooltip_disable(self.disabled)

        # --- setup node layout ---
        # (do all the graphic item layout offsets here)

        # align label text
        self.align_label(h_offset=6)
        # align icon
        # self.align_icon(h_offset=6, v_offset=4)
        # arrange input and output ports.
        self.align_ports()
        # arrange node widgets
        self.align_widgets()

        self.update()

    def calc_size(self, add_w=0.0, add_h=0.0):
        """
        Calculate minimum node size.

        Args:
            add_w (float): additional width.
            add_h (float): additional height.
        """
        p_input_width = 0.0
        p_output_width = 0.0
        p_input_height = 0.0
        p_output_height = 0.0
        for port in self._input_items.keys():
            if port.isVisible():
                p_input_width += port.boundingRect().width()
                if not p_input_height:
                    p_input_height = port.boundingRect().height()
        for port in self._output_items.keys():
            if port.isVisible():
                p_output_width += port.boundingRect().width()
                if not p_output_height:
                    p_output_height = port.boundingRect().height()

        widget_width = 0.0
        widget_height = 0.0
        for widget in self._widgets.values():
            if widget.boundingRect().width() > widget_width:
                widget_width = widget.boundingRect().width()
            widget_height += widget.boundingRect().height()

        width = max([p_input_width, p_output_width, widget_width]) + add_w
        height = p_input_height + p_output_height + widget_height + add_h
        return width, height

    def add_input(self, name='input', multi_port=False, display_name=True,
                  locked=False, painter_func=None):
        """
        Adds a port qgraphics item into the node with the "port_type" set as
        IN_PORT

        Args:
            name (str): name for the port.
            multi_port (bool): allow multiple connections.
            display_name (bool): (not used).
            locked (bool): locked state.
            painter_func (function): custom paint function.

        Returns:
            PortItem: port qgraphics item.
        """
        return super(NodeItemVertical, self).add_input(
            name, multi_port, False, locked, painter_func)

    def add_output(self, name='output', multi_port=False, display_name=True,
                   locked=False, painter_func=None):
        """
        Adds a port qgraphics item into the node with the "port_type" set as
        OUT_PORT

        Args:
            name (str): name for the port.
            multi_port (bool): allow multiple connections.
            display_name (bool): (not used).
            locked (bool): locked state.
            painter_func (function): custom paint function.

        Returns:
            PortItem: port qgraphics item.
        """
        return super(NodeItemVertical, self).add_output(
            name, multi_port, False, locked, painter_func)
