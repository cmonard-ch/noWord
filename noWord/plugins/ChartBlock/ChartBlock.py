#!/usr/bin/env python
import os
import sys
sys.path.insert(0, '...')


from reportlab.platypus import Paragraph, Table, TableStyle, PageBreak
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_RIGHT, TA_CENTER

from noWord.common.PluginInterface import PluginInterface
import noWord.common.utils_rp as cmn_utils_rp


class ChartBlock(PluginInterface):
    def __init__(self):
        self.padding = 0.4 * cm
        pass

    def Name(self):
        return 'chart'

    def init(self, context):
        pass

    def prepare(self, block, context):
        pass

    def process(self, block, context):

        # width and height element
        width = block["width"] * \
            cm if "width" in block else context.doc.currentWidth()
        height = block["height"] * \
            cm if "height" in block else 5 * cm

        mode = self.getElemValue(block, 'mode', 'linechart')

        data = block["data"] if "data" in block else None
        if isinstance(data, str):
            data = context.getResource(
                context.resources, block["data"])

        plotdata = block["plotdata"] if "plotdata" in block else None
        if isinstance(plotdata, str):
            plotdata = context.getResource(
                context.resources, block["plotdata"])

        xvalues = block["xvalues"] if "xvalues" in block else None
        if isinstance(xvalues, str):
            xvalues = context.getResource(
                context.resources, block["xvalues"])

        labelAngles = block["labelAngles"] if "labelAngles" in block else None
        if isinstance(labelAngles, str):
            labelAngles = context.getResource(
                context.resources, block["labelAngles"])

        labelXOffsets = block["labelXOffsets"] if "labelXOffsets" in block else None
        if isinstance(labelXOffsets, str):
            labelXOffsets = context.getResource(
                context.resources, block["labelXOffsets"])

        labelYOffsets = block["labelYOffsets"] if "labelYOffsets" in block else None
        if isinstance(labelYOffsets, str):
            labelYOffsets = context.getResource(
                context.resources, block["labelYOffsets"])

        linecolors = block["linecolors"] if "linecolors" in block else None

        lineWidths = block["lineWidths"] if "lineWidths" in block else None
        if isinstance(lineWidths, str):
            lineWidths = context.getResource(
                context.resources, block["lineWidths"])

        backgroundColor = block["backgroundColor"] if "backgroundColor" in block else None
        borderColor = block["borderColor"] if "borderColor" in block else None
        lineLabelFormat = block["lineLabelFormat"] if "lineLabelFormat" in block else None
        yAxisMin = block["yAxisMin"] if "yAxisMin" in block else None
        yAxisMax = block["yAxisMax"] if "yAxisMax" in block else None
        yAxisStep = block["yAxisStep"] if "yAxisStep" in block else None

        if mode == 'linechart':
            return self.makeLineChart(context, width, height, data, xvalues, backgroundColor, borderColor, labelAngles,
                                      labelXOffsets, labelYOffsets, linecolors, lineWidths, lineLabelFormat, yAxisMin,
                                      yAxisMax, yAxisStep)
        if mode == 'barchart':
            return self.makeBarChart(context, width, height, data)
        if mode == 'plotchart':
            return self.makePlotChart(context, width, height, plotdata, xvalues, linecolors)
        else:
            return []

    def makeLineChart(self, context, width, height, data, xvalues, backgroundColor, borderColor, labelAngles,
                      labelXOffsets, labelYOffsets, lineColors, lineWidths, lineLabelFormat, yAxisMin, yAxisMax,
                      yAxisStep):
        content = []

        drawing = Drawing(width, height)

        lp = HorizontalLineChart()
        lp.x = 0
        lp.y = 0
        lp.height = height
        lp.width = width
        lp.data = data
        lp.joinedLines = 1

        if backgroundColor:
            lp.fillColor = colors.HexColor(backgroundColor)

        if borderColor:
            lp.strokeColor = colors.HexColor(borderColor)

        if yAxisMin:
            lp.valueAxis.valueMin = yAxisMin

        if yAxisMax:
            lp.valueAxis.valueMax = yAxisMax

        if yAxisStep:
            lp.valueAxis.valueStep = yAxisStep

        if xvalues:
            lp.categoryAxis.categoryNames = xvalues

        def handleSingleOrList(targetObject, value, propertyName, defaultLength, mapFunc=None):
            if isinstance(value, list):
                for i in range(0, len(value)):
                    setattr(targetObject[i], propertyName, value[i] if not mapFunc else mapFunc(value[i]))
            else:
                for i in range(0, defaultLength):
                    setattr(targetObject[i], propertyName, value if not mapFunc else mapFunc(value))

        if labelAngles:
            handleSingleOrList(lp.categoryAxis.labels, labelAngles, 'angle', len(data[0]))

        if labelXOffsets:
            handleSingleOrList(lp.categoryAxis.labels, labelXOffsets, 'dx', len(data[0]))

        if labelYOffsets:
            handleSingleOrList(lp.categoryAxis.labels, labelYOffsets, 'dy', len(data[0]))

        if lineLabelFormat:
            lp.lineLabelFormat = lineLabelFormat

        if lineColors:
            handleSingleOrList(lp.lines, lineColors, 'strokeColor', len(data), colors.HexColor)

        if lineWidths:
            handleSingleOrList(lp.lines, lineWidths, 'strokeWidth', len(data))

        drawing.add(lp)

        content.append( drawing )

        return content

    def makeBarChart(self, context, width, height, data):
        content = []

        drawing = Drawing(width, height)

        lp = VerticalBarChart()
        lp.x = 0
        lp.y = 0
        lp.height = height
        lp.width = width
        lp.data = data

        drawing.add(lp)

        content.append( drawing )

        return content

    def makePlotChart(self, context, width, height, data, xvalues, linecolors):
        content = []

        drawing = Drawing(width, height)

        plot = LinePlot()
        plot.x = 0
        plot.y = self.padding
        plot.height = height - 2 * self.padding
        plot.width = width
        plot.data = data
        plot.joinedLines = 1
        plot.lineLabelFormat = '%2.0f'

        i = 0
        for color in linecolors :
            plot.lines[i].strokeColor = colors.HexColor(color)
            i+=1

        if xvalues :
            plot.xValueAxis.valueSteps = xvalues

        drawing.add(plot)

        content.append( drawing )

        return content
