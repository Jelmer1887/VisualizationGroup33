'''
JBI100 - Visualisation 2020/2021 Group 33 Visualisation Tool
Group:
- Wouter
- Sjoerd
- Rick
- Marloes
- Jelmer

Visualisation framework: Bokeh libary
Visualisation coded following examples from documentation:
https://docs.bokeh.org/en/latest/docs/user_guide.html

Providing data-sources for plot; basic structure following example from documentation: 
https://docs.bokeh.org/en/latest/docs/user_guide/data.html#providing-data 
https://docs.bokeh.org/en/latest/docs/user_guide/data.html#columndatasource 
https://docs.bokeh.org/en/latest/docs/user_guide/data.html#pandas 
'''

from bokeh.core.enums import Dimensions
from bokeh.models import ColorBar, LinearColorMapper, HoverTool, BoxSelectTool, CustomJSHover, BoxZoomTool, ResetTool, \
    WheelZoomTool, PanTool, Range1d, DataRange1d, glyph
from bokeh.models.widgets.buttons import Button
from bokeh.transform import jitter, transform
from bokeh.plotting import figure, output_file, show
from bokeh.models.widgets import Panel, Tabs
from bokeh.layouts import column, row, layout, widgetbox, grid, GridBox, gridplot
from bokeh.models import CustomJS, Slider, Toggle, Dropdown, MultiChoice, Spinner, Select, ColumnDataSource, Legend, \
    LegendItem, BasicTicker
from bokeh.transform import dodge
from bokeh.palettes import RdBu
from bokeh.models import ColorBar, LinearColorMapper, HoverTool, BoxSelectTool
import pandas as pd
import bisect
from math import pi
from numpy import arange
from itertools import chain
from collections import OrderedDict
from bokeh.io import output_file, show
from bokeh.io import output_file, show
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Div
from bokeh.models.widgets import Paragraph
from bokeh.models.widgets import PreText
from bokeh.models import ColorPicker
from bokeh.plotting import figure, curdoc # for the server

plot = figure(tools="pan,wheel_zoom,box_zoom,reset")        # I need to know if this is still needed?
plot.add_tools(BoxSelectTool(dimensions="width"))
#output_file("test.html")                                    # sets outputfile for the resulting webpage tool


# // DATA PROCESSING ====================================================================================================================================================
# The following section contains ALL data (pre)processing done on the dataset. This includes:
# - Extracting data from the dataset
# - Removing empty entries
# - grouping data
# - computing new data from available columns

df = pd.read_excel(r'dataset.xlsx')         # import all data from the dataset as pandas dataframe

# Stacked Barchart Percentage computation -----------------------------------------------------------------------------
nrofBins = 5                                # nr of bins to put age quantiles in to
binSize = 20/nrofBins                       # nr of age quantiles per bin

regularWardPos = [0] * nrofBins             # shortcut: list of zeroes to store nr of people per ward per bin
semiIntensivePos = [0] * nrofBins
intensivePos = [0] * nrofBins

regularWardNeg = [0] * nrofBins
semiIntensiveNeg = [0] * nrofBins
intensiveNeg = [0] * nrofBins

totalAgePos = [0] * nrofBins
totalAgeNeg = [0] * nrofBins


for index, row in df.iterrows():

    binofIndex = int(df.iloc[index, 1] / binSize)       # computes in which bin the current age quantile would be

    # count the number of positive and negative patients per bin and per ward
    if df.iloc[index, 2] == "positive":
        totalAgePos[binofIndex] += 1                    
        if df.iloc[index, 3] == 1:
            regularWardPos[binofIndex] += 1
        elif df.iloc[index, 4] == 1:
            semiIntensivePos[binofIndex] += 1
        elif df.iloc[index, 5] == 1:
            intensivePos[binofIndex] += 1

    if df.iloc[index, 2] == "negative":                 
        totalAgeNeg[binofIndex] += 1
        if df.iloc[index, 3] == 1:                      # technically, we are still repeating ourselves in the nested if/elif-statements here...
            regularWardNeg[binofIndex] += 1             # ...so it can be done in a cleaner way... if we have time at the end we should invesitage using mappings to optimise this
        elif df.iloc[index, 4] == 1:
            semiIntensiveNeg[binofIndex] += 1
        elif df.iloc[index, 5] == 1:
            intensiveNeg[binofIndex] += 1

percentageRegularWardPos = [0] * nrofBins               # lists containing percentages computed from the data
percentageSemiIntensivePos = [0] * nrofBins
percentageIntensivePos = [0] * nrofBins

percentageRegularWardNeg = [0] * nrofBins
percentageSemiIntensiveNeg = [0] * nrofBins
percentageIntensiveNeg = [0] * nrofBins

for i in range(len(regularWardPos)):
    percentageRegularWardPos[i] = regularWardPos[i] / (totalAgePos[i] + totalAgeNeg[i]) * 100       # compute percentages
    percentageSemiIntensivePos[i] = semiIntensivePos[i] / (totalAgePos[i] + totalAgeNeg[i]) * 100
    percentageIntensivePos[i] = intensivePos[i] / (totalAgePos[i] + totalAgeNeg[i]) * 100

    percentageRegularWardNeg[i] = regularWardNeg[i] / (totalAgePos[i] + totalAgeNeg[i]) * 100
    percentageSemiIntensiveNeg[i] = semiIntensiveNeg[i] / (totalAgePos[i] + totalAgeNeg[i]) * 100
    percentageIntensiveNeg[i] = intensiveNeg[i] / (totalAgePos[i] + totalAgeNeg[i]) * 100

# [END] Stacked Barchart Percentage computation -----------------------------------------------------------------------

# Barchart percentage per age quantile computation --------------------------------------------------------------------
positiveAge = [0] * 20                              # list counting positively tested persons per age quantile
totalAge = [0] * 20                                 # list counting the total amount of people in an age quantile
percentageAge = [0] * 20                            # list containing percentage of positively tested per age quantile

for index, row in df.iterrows():                    # go over all entries in the dataframe
    rowAge = df.iloc[index, 1]
    totalAge[rowAge] += 1                           # increment counter for corresponding age quantile
    if df.iloc[index, 2] == "positive":
        positiveAge[rowAge] += 1                    # increment counter for corresponding postively tested counter

# compute percentage of positively tested per age quantile using a list comprehension (quicker than loop)
percentageAge = [(positiveAge[i]/totalAge[i]) * 100 for i in range(len(positiveAge))]

print("\ndebugging info:-------------------------") # some debugging info
print(f"length positiveAge: {len(positiveAge)}")
print(f"length totalAge: {len(totalAge)}")
print(f"length percentageAge: {len(percentageAge)}")
print("\n----------------------------------------\n")

# [END] Barchart percentage per age quantile computation --------------------------------------------------------------

# Heatmap data selection and colors/bounds computations ---------------------------------------------------------------
dfVirus = df.iloc[:, 21:38]                         # copy only relevant data columns using a list-slice
dfVirus["SARS-Cov-2 exam result"] = df["SARS-Cov-2 exam result"]    # add covid result to the copy
del dfVirus['Mycoplasma pneumoniae']                # remove this column because it has too few entries

for i in range(16):
    dfVirus.iloc[:, i] = dfVirus.iloc[:, i].replace(["not_detected"], 0)    # change strings to 0
    dfVirus.iloc[:, i] = dfVirus.iloc[:, i].replace(["detected"], 1)        # change strings to 1

dfVirus.iloc[:, 16] = dfVirus.iloc[:, 16].replace(["negative"], 0)          # change strings to 0
dfVirus.iloc[:, 16] = dfVirus.iloc[:, 16].replace(["positive"], 1)          # change strings to 1

correlation = dfVirus.corr()                        # create correlation object

correlation = dfVirus.corr()                        # create correlation object
correlation.index.name = 'virusnames1'
correlation.columns.name = 'virusnames2'

correlation = correlation.stack().rename("value").reset_index() # needed for hovertool

# changed range to make small deviations better possible, blue negative and red positive values
mapper = LinearColorMapper(
    palette=RdBu[9], low=2*correlation.value.min() , high=-2*correlation.value.min())

# [END] Heatmap data selection and colors/bounds computations ---------------------------------------------------------

# Grid of bloodplots data selection/cleaning and restructuring --------------------------------------------------------
SELECTION = [                           # list of column to be used in visualisation (blood value columns)
    'SARS-Cov-2 exam result',
    'Patient age quantile',
    'Hematocrit',
    'Hemoglobin',
    'Platelets',
    'Red blood Cells',
    'Lymphocytes',
    'Mean corpuscular hemoglobin concentration (MCHC)',
    'Leukocytes',
    'Basophils',
    'Mean corpuscular hemoglobin (MCH)',
    'Eosinophils',
    'Mean corpuscular volume (MCV)',
    'Monocytes',
    'Red blood cell distribution width (RDW)',
    # 'Serum Glucose', <-- averaged around 4 values per quantile, too few entries! So not included
]

# selecting the required data
df_blood = df[SELECTION].copy()         # copy selection from main dataframe

dfPositive = df_blood[df_blood['SARS-Cov-2 exam result'] == "positive"]     # filter positive values
dfNegative = df_blood[df_blood['SARS-Cov-2 exam result'] == "negative"]     # filter negative values

dfPosAge = dfPositive['Patient age quantile']   # lists of ages
dfNegAge = dfNegative['Patient age quantile']

del dfPositive['SARS-Cov-2 exam result']        # remove covid test result from copy
del dfNegative['SARS-Cov-2 exam result']        # remove covid test result from copy

dcPositive = dfPositive.to_dict("list")         # convert dataframes to dictionaries
dcNegative = dfNegative.to_dict("list")

bloodvaluelist = list(dcPositive)               # convert df of blood values for axis to list

bloodvaluelist.remove('Patient age quantile')   # remove x-axis column from dictionary for axis 

# // VISUALISATIONS CODE ================================================================================================================================================

# tab 1 - Stacked bar chart -------------------------------------------------------------------------------------------

wardDevision = ["regular ward", "semi-intensive unit", "intensive care"]    # legend names for the wards

ageDevision = ["Child and teen", "Young adult and adult", "Middle aged", "Senior", "Elderly"]   # labels of the bins
if len(ageDevision) != nrofBins: raise ValueError (f"nr of labels for bins doesn't match nr of bins! ({len(ageDevision)} != {nrofBins})")

positiveReg = ["Regular ward positive", "Regular ward negative"]            # labels of the positive and negative parts
positiveSemi = ["Semi-intensive unit positive", "Semi-intensive unit negative"]
positiveIntens = ["Intensive care positive", "Intensive care negative"]

# Basic structure following example from documentation: https://docs.bokeh.org/en/latest/docs/user_guide/data.html#providing-data 
# dictionaries for plotting the data
dictDataReg = {'age group': ageDevision,
               "Regular ward positive": percentageRegularWardPos,
               "Regular ward negative": percentageRegularWardNeg,
               "percentagePos"        : percentageRegularWardPos,           # a field with an identical name for every datasource for the tooltip
               "percentageNeg"        : percentageRegularWardNeg,            # a field with an identical name for every datasource for the tooltip
               "absolutePos"          : regularWardPos,                     # a field with the absolute number of people positive tested
               "absoluteNeg"          : regularWardNeg                      # a field with the absolute number of people negative tested
               }

dictDataSemi = {'age group': ageDevision,
                "Semi-intensive unit positive": percentageSemiIntensivePos,
                "Semi-intensive unit negative": percentageSemiIntensiveNeg,
                "percentagePos"               : percentageSemiIntensivePos, # a field with an identical name for every datasource for the tooltip
                "percentageNeg"               : percentageSemiIntensiveNeg,  # a field with an identical name for every datasource for the tooltip
                "absolutePos"                 : semiIntensivePos,           # a field with the absolute number of people positive tested
                "absoluteNeg"                 : semiIntensiveNeg            # a field with the absolute number of people negative tested
                }

dictDataIntens = {'age group': ageDevision,
                  "Intensive care positive": percentageIntensivePos,
                  "Intensive care negative": percentageIntensiveNeg,
                  "percentagePos"          : percentageIntensivePos,        # a field with an identical name for every datasource for the tooltip
                  "percentageNeg"          : percentageIntensiveNeg,         # a field with an identical name for every datasource for the tooltip
                  "absolutePos"            : intensivePos,                  # a field with the absolute number of people positive tested
                  "absoluteNeg"            : intensiveNeg                   # a field with the absolute number of people negative tested
                  }

sourceReg = ColumnDataSource(data=dictDataReg)          # convert dictionaries to datasources
sourceSemi = ColumnDataSource(data=dictDataSemi)
sourceIntens = ColumnDataSource(data=dictDataIntens)

# colors of the bars
colorsReg = ["#2874A6", "#85C1E9"]      # first dark color, then light color
colorsSemi = ["#B03A2E", "#F5B7B1"]
colorsIntens = ["#B7950B", "#F9E79F"]


# creating the bars
p1 = figure(x_range=ageDevision,
            title="Percentage of age group in hospital ward seperated by COVID-19 test result", toolbar_location="right",
            tools=([WheelZoomTool(), ResetTool(), PanTool(), "save"]), y_axis_label="Age group specific percentage per hospital ward")

p1.vbar_stack(positiveReg, x=dodge('age group', -0.25, range=p1.x_range), width=0.2, source=dictDataReg,
              color=colorsReg, legend_label=positiveReg)

p1.vbar_stack(positiveSemi, x=dodge('age group', 0.0, range=p1.x_range), width=0.2, source=dictDataSemi,
              color=colorsSemi, legend_label=positiveSemi)

p1.vbar_stack(positiveIntens, x=dodge('age group', 0.25, range=p1.x_range), width=0.2, source=dictDataIntens,
              color=colorsIntens, legend_label=positiveIntens)

# plot properties
p1.y_range.start = 0
p1.x_range.range_padding = 0.1
p1.xgrid.grid_line_color = None
p1.legend.location = "top_center"   # legend location
p1.legend.orientation = "vertical"  # legend orientation (items below each other)

# SELECT menu GUI       # @help@ What does this do??
selectoptions = ["Postive tested on Covid-19 virus", "Negative tested on Covid-19 virus", "Show both"]
resultSelect = Select(title="What to show", options=selectoptions)

# Hover tooltips
p1.add_tools(HoverTool(
    tooltips=[
        ('Age group', '@{age group}'),
        ('Percentage negative', '@percentageNeg{0.00}%'),
        ('Percentage positive', '@percentagePos{0.00}%'),
        ('Number of negative patients', '@absoluteNeg'),
        ('Number of positive patients', '@absolutePos'),
        ('label', '$name'),
    ]
))

# [END] tab 1 - Stacked bar chart -------------------------------------------------------------------------------------

# tab 2 - Bar chart ---------------------------------------------------------------------------------------------------
# Basic structure following example from documentation: https://docs.bokeh.org/en/latest/docs/user_guide/data.html#providing-data 
ageQuantile = [str(i) for i in range(20)]           # list of labels
sourcep2 = ColumnDataSource(data=dict(  # create and convert dictionary to datasource
    x=ageQuantile,
    y=percentageAge,
    total = totalAge,
    positive = positiveAge
))

# // 2 different versions of the plot, to re-arrange the data

# 1) figure sorted on y value, from low to high
sorted_ageQuantile = sorted(ageQuantile, key=lambda x: percentageAge[ageQuantile.index(x)])
p2 = figure(
    # axis properties
    x_range = sorted_ageQuantile,
    y_range = (0, int(max(percentageAge)) + 1),
    y_axis_label = "Percentage of age group with a positive Covid-19 test", 
    x_axis_label = "Age quantiles",

    # plot properties
    plot_height = 250, 
    title = "Percentage positive tests per age quartile", 
    toolbar_location = "right",
    tools = [WheelZoomTool(), ResetTool(), PanTool(), "save", "tap"],
)

# 2) figure sorted on age quantile
p2 = figure(
    # axis properties
    x_range=ageQuantile,
    y_range=(0, int(max(percentageAge)) + 1),
    y_axis_label="Percentage of age group with a positive Covid-19 test", 
    x_axis_label = "Age quantiles",

    # plot properties
    plot_height=250, 
    title="Percentage positive tests per age quantile", 
    toolbar_location="right",
    tools=[WheelZoomTool(), ResetTool(), PanTool(), BoxSelectTool(), "save", "tap"],
)

p2.x_range.max_interval = 19    # sets x-axis maximum

vbar_renderer = p2.vbar(                 # creates bars
    x='x', 
    top='y', 
    width=0.5, 
    source=sourcep2,            # defines source
    color = 'blue',             # default color of the bars

    # properties of selected / unselected bars
    #selection_fill_alpha = 1.0,                     # opacity of selected bar
    #nonselection_fill_alpha=0.2,                    # opacity of non-selected bar
)
from bokeh.models.glyphs import VBar
vbar_selected = VBar(
    fill_alpha = 0.2,
    fill_color = 'blue',
    line_color = 'blue',
    hatch_pattern = 'right_diagonal_line',
    hatch_color = 'blue',
    hatch_alpha = 1.0,
    hatch_weight = 0.5
)
vbar_nonselected = VBar(
    fill_alpha = 0.2,
    fill_color = 'blue',
    line_color = 'blue'
)
vbar_renderer.selection_glyph = vbar_selected
vbar_renderer.nonselection_glyph = vbar_nonselected

p2.xgrid.grid_line_color = None     # removes gridlines

picker = ColorPicker(title="Line Color")            # allows to change the color of the bars
picker.js_link('color', vbar_renderer.selection_glyph, 'fill_color')        # link the selected bar color properties to the selector
picker.js_link('color', vbar_renderer.selection_glyph, 'line_color')
picker.js_link('color', vbar_renderer.selection_glyph, 'hatch_color')
picker.js_link('color', vbar_renderer.nonselection_glyph, 'fill_color')     # link the non-selected bar color properties to the selector
picker.js_link('color', vbar_renderer.nonselection_glyph, 'line_color')
picker.js_link('color', vbar_renderer.glyph, 'fill_color')                  # link the bar color properties to the selector for when no bar has been selected
picker.js_link('color', vbar_renderer.glyph, 'line_color')


# hover tool p2
p2.add_tools(HoverTool(
    tooltips=[
        ('Age quantile', '@x'),
        ('Percentage', '@y{0.00} %'),
        ('Number of patients', '@total'),
        ('Number of positive patients', '@positive')
    ]
))

# [END] tab 2 - Bar chart ---------------------------------------------------------------------------------------------

# tab 3 - Heat map ----------------------------------------------------------------------------------------------------
#  based on https://stackoverflow.com/questions/39191653/python-bokeh-how-to-make-a-correlation-plot

p3 = figure(plot_width=600, plot_height=600,                # figure object for the heatmap
            x_range=list(correlation.virusnames1.drop_duplicates()),
            y_range=list(correlation.virusnames2.drop_duplicates()),
            title="Correlation Coefficient between different virusses", toolbar_location="right",
            tools=[WheelZoomTool(), ResetTool(), PanTool(), "save"]
            )

# Create square for heatmap
p3.rect(
    x="virusnames1",
    y="virusnames2",
    width=1,
    height=1,
    source=ColumnDataSource(correlation),
    line_color='white',
    fill_color=transform('value', mapper))

p3.xgrid.grid_line_color = None                             # remove gridlines
p3.ygrid.grid_line_color = None
p3.xaxis.major_label_orientation = pi / 4                   # rotate labels by 45deg (pi/4 rad => 45deg)
p3.yaxis.major_label_orientation = pi / 4

# Add legend
color_bar = ColorBar(
    color_mapper=mapper,
    location=(0, 0),
    ticker=BasicTicker(desired_num_ticks=13))  # number of values next to the legend

p3.add_layout(color_bar, 'right')

# add hovertool
p3.add_tools(HoverTool(
    tooltips=[
        ('Virus 1', '@virusnames1'),
        ('Virus 2', '@virusnames2'),
        ('Correlation coefficient', '@value{0.00}'),
    ]
))
# [END] tab 3 - Heat map ----------------------------------------------------------------------------------------------

# tab 4 - splom plot --------------------------------------------------------------------------------------------------
# Based on example from documentation: https://docs.bokeh.org/en/latest/docs/user_guide/data.html#pandas 
figures = []                                                # list to contain all subplots

# title of the plot
TITLE = "Several blood chemicals versus Age quantile"

sourcePos = ColumnDataSource(dfPositive)                    # convert dataframes to datasources
sourceNeg = ColumnDataSource(dfNegative)

posneg_list = []                                            # list to contain all dots in a plot
colorPositive = "blue"                                      # color of positively tested
colorNegative = "red"                                       # color of negatively tested

for index in bloodvaluelist:                                # create subplots for every bloodtype
    #  for the first one don't use x_range, the remaining all will use the same x_range
    if index != "Hematocrit":                               # a seperate plot is made for the first entry
        scatter = figure(
            title=index, 
            plot_width=400, 
            plot_height=300, 
            x_range=figures[0].x_range,
            y_range=figures[0].y_range,
            tools="save, pan, reset, wheel_zoom, box_select", 
            x_axis_label='age quantile',
            y_axis_label='standardized test result'
        )

    else:
        scatter = figure(                                   # plots for all the other blood values
            title=index,                                    # ... these are the same but they copy their axis from the first one
            plot_width=400, 
            plot_height=300, 
            y_range=(-4, 4),
            tools="save, pan, reset, wheel_zoom, box_select", 
            x_axis_label='age quantile',
            y_axis_label='standardized test result'
        )

    # create dot objects for the points in the plots
    p = scatter.square(x=jitter("Patient age quantile", 0.5), y=index, size=4, color=colorPositive, alpha=0.5,
                       source=sourcePos, muted_alpha=0.1)
    n = scatter.circle(x=jitter("Patient age quantile", 0.5), y=index, size=4, color=colorNegative, alpha=0.5,
                       source=sourceNeg, muted_alpha=0.1)

    posneg_list += [p]                                      # add dots to list
    posneg_list += [n]

    figures.append(scatter)                                 # add figure to the list of subfigures

# Lines with the same color will share a same legend item
legend_items = [LegendItem(label="Covid-19 positive",
                           renderers=[thing for thing in posneg_list if thing.glyph.line_color == colorPositive]),
                LegendItem(label="Covid-19 negative",
                           renderers=[thing for thing in posneg_list if thing.glyph.line_color == colorNegative])]

# use a dummy figure for the legend
dum_fig = figure(plot_width=300, plot_height=600, outline_line_alpha=0, toolbar_location=None)

# set the components of the figure invisible
for fig_component in [dum_fig.grid[0], dum_fig.ygrid[0], dum_fig.xaxis[0], dum_fig.yaxis[0]]:
    fig_component.visible = False

# The points referred by the legend need to be present in the figure ,so add them to figure renderers
dum_fig.renderers += posneg_list

# set the figure range outside of the range of all glyphs
dum_fig.x_range.end = 1005
dum_fig.x_range.start = 1000

# add the legend
dum_fig.add_layout(Legend(click_policy='mute', location='top_left', border_line_alpha=0, items=legend_items))

# copy list to make it later possible to delete/ add items for the list without using original list (NOT YET USED)
show_figures = figures

splom = gridplot(show_figures, ncols=3, toolbar_location='right')
p4 = gridplot([[splom, dum_fig]], toolbar_location=None)
# [END] tab 4 - splom plot --------------------------------------------------------------------------------------------

# // TOOL GUI ===========================================================================================================================================================

# Spinner GUI
spinner = Spinner(title="Size", low=0, high=4, step=0.1, value=1, width=300)
# spinner.js_link('value', points.glyph, 'radius')

# Dropdown menu GUI
menu = [("Item 1", "item_1"), ("Item 2", "item_2"), None, ("Item 3", "item_3")]
dropdown = Dropdown(label="Dropdown button", button_type="warning", menu=menu)
dropdown.js_on_event("menu_item_click", CustomJS(code="console.log('dropdown: ' + this.item, this.toString())"))


# Toggle button GUI
toggle = Toggle(label="Button", button_type="success")
toggle.js_on_click(CustomJS(code="""
    console.log('toggle: active=' + this.active, this.toString())
"""))

# choice menu GUI
OPTIONS = [str(i) for i in range(20)]
multi_choice = MultiChoice(value=["foo", "baz"], options=OPTIONS)
multi_choice.js_on_change("value", CustomJS(code="""
    console.log('multi_choice: value=' + this.value, this.toString())
"""))

# # SELECT menu GUI
# selectoptions = ["Postive tested on Covid-19 virus", "Negative tested on Covid-19 virus", "Show both"]
# resultSelect = Select(title="What to show", options=selectoptions)

# TOOL BUTTON CALLBACKS -----------------------------------------------------------------------------------------------
# Test button GUI
lab = "Click me!"
but = Button(label = lab)
def callback_button1():         # simple test callback -> changes lable on button and reports a click to the console
    print("button was clicked!")

but.on_click(callback_button1)       # links the clickedcode to the button

# [END] TOOL BUTTON CALLBACKS -----------------------------------------------------------------------------------------

# general webpage & plots
title = Div(
    text="<b>Visualisation tool of patients tested for Covid-19 of the Hospital Israelita Albert Einstein, at São Paulo, Brazil</b>",
    style={'font-size': '200%', 'color': 'black'}, width=800
)

text = [title]
# gridplot
p = gridplot([[p1, p2], [None, p3]], plot_width=400, plot_height=400, merge_tools = False)
# plot sizes
p1.plot_width = 600
p1.plot_height = 600
p2.plot_width = 600
p2.plot_height = 600
p3.plot_width = 600
p3.plot_height = 600

# GUI Left column
controls = [dropdown, spinner, toggle, multi_choice, but]
# inputs = column(*controls, sizing_mode='fixed', height=300, width=500)
l1 = layout([[p1]], sizing_mode='fixed', height=600, width=150)
l2 = layout([[p2, picker]], sizing_mode='fixed', height=600, width=150)
l3 = layout([[p3]], sizing_mode='fixed', height=600, width=150)
l4 = layout([[p4]], sizing_mode='fixed', height=600, width=150)

# Tab setup
tab1 = Panel(child=l1, title="Division per hospital ward")
tab2 = Panel(child=l2, title="Age covid-19 patients")
tab3 = Panel(child=l3, title="Heat map")
tab4 = Panel(child=l4, title="Scatter plot bloodvalues")
tab5 = Panel(child=p, title="All visualisations")

tabs = Tabs(tabs=[tab5, tab1, tab2, tab3, tab4])

layout = layout([[text], [controls, tabs]])
#show(layout)
print(totalAge)

curdoc().add_root(layout)
