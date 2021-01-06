
from bokeh.models import ColorBar, LinearColorMapper, HoverTool, BoxSelectTool, CustomJSHover, BoxZoomTool, ResetTool, \
    WheelZoomTool, PanTool, Range1d, DataRange1d
from bokeh.transform import jitter
from bokeh.plotting import figure, output_file, show
from bokeh.models.widgets import Panel, Tabs
from bokeh.layouts import column, row, layout, widgetbox, grid, GridBox, gridplot
from bokeh.models import CustomJS, Slider, Toggle, Dropdown, MultiChoice, Spinner, Select, ColumnDataSource, Legend, LegendItem
from bokeh.transform import dodge
from bokeh.palettes import RdBu as colors
from bokeh.models import ColorBar, LinearColorMapper, HoverTool, BoxSelectTool
import pandas as pd
import bisect
from math import pi
from numpy import arange
from itertools import chain
from collections import OrderedDict
from bokeh.io import output_file, show


plot = figure(tools="pan,wheel_zoom,box_zoom,reset")
plot.add_tools(BoxSelectTool(dimensions="width"))
output_file("test.html")
df = pd.read_excel(
    "dataset.xlsx")


# tab 1 - Assignment 4 visualisation
regularWardPos = [0, 0, 0, 0, 0]
semiIntensivePos = [0, 0, 0, 0, 0]
intensivePos = [0, 0, 0, 0, 0]

totalAgePos = [0, 0, 0, 0, 0]

regularWardNeg = [0, 0, 0, 0, 0]
semiIntensiveNeg = [0, 0, 0, 0, 0]
intensiveNeg = [0, 0, 0, 0, 0]

totalAgeNeg = [0, 0, 0, 0, 0]

for index, row in df.iterrows():
    if df.iloc[index, 1] == 0 or df.iloc[index, 1] == 1 or df.iloc[index, 1] == 2 or df.iloc[index, 1] == 3:
        if df.iloc[index, 2] == "positive":
            totalAgePos[0] += 1
            if df.iloc[index, 3] == 1:
                regularWardPos[0] += 1
            elif df.iloc[index, 4] == 1:
                semiIntensivePos[0] += 1
            elif df.iloc[index, 5] == 1:
                intensivePos[0] += 1

        if df.iloc[index, 2] == "negative":
            totalAgeNeg[0] += 1
            if df.iloc[index, 3] == 1:
                regularWardNeg[0] += 1
            elif df.iloc[index, 4] == 1:
                semiIntensiveNeg[0] += 1
            elif df.iloc[index, 5] == 1:
                intensiveNeg[0] += 1

    elif df.iloc[index, 1] == 4 or df.iloc[index, 1] == 5 or df.iloc[index, 1] == 6 or df.iloc[index, 1] == 7:
        if df.iloc[index, 2] == "positive":
            totalAgePos[1] += 1
            if df.iloc[index, 3] == 1:
                regularWardPos[1] += 1
            elif df.iloc[index, 4] == 1:
                semiIntensivePos[1] += 1
            elif df.iloc[index, 5] == 1:
                intensivePos[1] += 1

        if df.iloc[index, 2] == "negative":
            totalAgeNeg[1] += 1
            if df.iloc[index, 3] == 1:
                regularWardNeg[1] += 1
            elif df.iloc[index, 4] == 1:
                semiIntensiveNeg[1] += 1
            elif df.iloc[index, 5] == 1:
                intensiveNeg[1] += 1

    elif df.iloc[index, 1] == 8 or df.iloc[index, 1] == 9 or df.iloc[index, 1] == 10 or df.iloc[index, 1] == 11:
        if df.iloc[index, 2] == "positive":
            totalAgePos[2] += 1
            if df.iloc[index, 3] == 1:
                regularWardPos[2] += 1
            elif df.iloc[index, 4] == 1:
                semiIntensivePos[2] += 1
            elif df.iloc[index, 5] == 1:
                intensivePos[2] += 1

        if df.iloc[index, 2] == "negative":
            totalAgeNeg[2] += 1
            if df.iloc[index, 3] == 1:
                regularWardNeg[2] += 1
            elif df.iloc[index, 4] == 1:
                semiIntensiveNeg[2] += 1
            elif df.iloc[index, 5] == 1:
                intensiveNeg[2] += 1

    elif df.iloc[index, 1] == 12 or df.iloc[index, 1] == 13 or df.iloc[index, 1] == 14 or df.iloc[index, 1] == 15:
        if df.iloc[index, 2] == "positive":
            totalAgePos[3] += 1
            if df.iloc[index, 3] == 1:
                regularWardPos[3] += 1
            elif df.iloc[index, 4] == 1:
                semiIntensivePos[3] += 1
            elif df.iloc[index, 5] == 1:
                intensivePos[3] += 1

        if df.iloc[index, 2] == "negative":
            totalAgeNeg[3] += 1
            if df.iloc[index, 3] == 1:
                regularWardNeg[3] += 1
            elif df.iloc[index, 4] == 1:
                semiIntensiveNeg[3] += 1
            elif df.iloc[index, 5] == 1:
                intensiveNeg[3] += 1

    elif df.iloc[index, 1] == 16 or df.iloc[index, 1] == 17 or df.iloc[index, 1] == 18 or df.iloc[index, 1] == 19:
        if df.iloc[index, 2] == "positive":
            totalAgePos[4] += 1
            if df.iloc[index, 3] == 1:
                regularWardPos[4] += 1
            elif df.iloc[index, 4] == 1:
                semiIntensivePos[4] += 1
            elif df.iloc[index, 5] == 1:
                intensivePos[4] += 1

        if df.iloc[index, 2] == "negative":
            totalAgeNeg[4] += 1
            if df.iloc[index, 3] == 1:
                regularWardNeg[4] += 1
            elif df.iloc[index, 4] == 1:
                semiIntensiveNeg[4] += 1
            elif df.iloc[index, 5] == 1:
                intensiveNeg[4] += 1

percentageRegularWardPos = [0, 0, 0, 0, 0]
percentageSemiIntensivePos = [0, 0, 0, 0, 0]
percentageIntensivePos = [0, 0, 0, 0, 0]

percentageRegularWardNeg = [0, 0, 0, 0, 0]
percentageSemiIntensiveNeg = [0, 0, 0, 0, 0]
percentageIntensiveNeg = [0, 0, 0, 0, 0]

for i in range(len(regularWardPos)):
    percentageRegularWardPos[i] = regularWardPos[i] / totalAgePos[i] * 100
    percentageSemiIntensivePos[i] = semiIntensivePos[i] / totalAgePos[i] * 100
    percentageIntensivePos[i] = intensivePos[i] / totalAgePos[i] * 100

    percentageRegularWardNeg[i] = regularWardNeg[i] / totalAgeNeg[i] * 100
    percentageSemiIntensiveNeg[i] = semiIntensiveNeg[i] / totalAgeNeg[i] * 100
    percentageIntensiveNeg[i] = intensiveNeg[i] / totalAgeNeg[i] * 100

wardDevision = ["regular ward", "semi-intensive unit", "intensive care"]

ageDevision = ["child and teen", "young adult and adult", "middle aged", "senior", "elderly"]

positiveReg = ["regular ward positive", "regular ward negative"]
positiveSemi = ["semi-intensive unit positive", "semi-intensive unit negative"]
positiveIntens = ["intensive care positive", "intensive care negative"]

dictDataReg = {'age group': ageDevision,
               "regular ward positive": percentageRegularWardPos,
               "regular ward negative": percentageRegularWardNeg}

dictDataSemi = {'age group': ageDevision,
                "semi-intensive unit positive": percentageSemiIntensivePos,
                "semi-intensive unit negative": percentageSemiIntensiveNeg}

dictDataIntens = {'age group': ageDevision,
                  "intensive care positive": percentageIntensivePos,
                  "intensive care negative": percentageIntensiveNeg}

sourceReg = ColumnDataSource(data=dictDataReg)
sourceSemi = ColumnDataSource(data=dictDataSemi)
sourceIntens = ColumnDataSource(data=dictDataIntens)

colorsReg = ["#2874A6", "#85C1E9"]
colorsSemi = ["#B03A2E", "#F5B7B1"]
colorsIntens = ["#B7950B", "#F9E79F"]

p1 = figure(x_range=ageDevision,
            title="Percentage of age group with positive Covid-19 test in hospital ward", toolbar_location=None,
            tools="")

# dodge('age group', -0.25, range=chart.x_range)

p1.vbar_stack(positiveReg, x=dodge('age group', -0.25, range=p1.x_range), width=0.2, source=dictDataReg,
              color=colorsReg, legend_label=positiveReg)

p1.vbar_stack(positiveSemi, x=dodge('age group', 0.0, range=p1.x_range), width=0.2, source=dictDataSemi,
              color=colorsSemi, legend_label=positiveSemi)

p1.vbar_stack(positiveIntens, x=dodge('age group', 0.25, range=p1.x_range), width=0.2, source=dictDataIntens,
              color=colorsIntens, legend_label=positiveIntens)

p1.y_range.start = 0
p1.x_range.range_padding = 0.1
p1.xgrid.grid_line_color = None
p1.legend.location = "top_left"
p1.legend.orientation = "vertical"
p1.legend.click_policy  = "hide"

# SELECT menu GUI
selectoptions = ["Postive tested on Covid-19 virus", "Negative tested on Covid-19 virus", "Show both"]
resultSelect = Select(title="What to show", options=selectoptions)



p1.add_tools(HoverTool(
    tooltips=[
        ('age group', '@{age group}'),
        ('percentage', '$y:'),
        ('label', '$name'),
        ('percentageAge', '@percentageAge')
    ], mode='vline'
))

# Visualisation 2 - Bar chart - Assignment 3
positiveAge = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
totalAge = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
percentageAge = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

for index, row in df.iterrows():
    for i in range(20):
        if df.iloc[index, 1] == i:
            totalAge[i] += 1
            if df.iloc[index, 2] == "positive":
                positiveAge[i] += 1



for i in range(len(positiveAge)):
    percentageAge[i] = positiveAge[i] / totalAge[i] * 100

print(positiveAge)
print(totalAge)
print(percentageAge)

ageQuantile = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18",
               "19"]

p2 = figure(x_range=ageQuantile,  plot_height=250, title="Percentage positive tests per age quartile",
            toolbar_location="below", tools=[WheelZoomTool(), ResetTool(), PanTool()])
p2.x_range.max_interval = 19

p2.vbar(x=ageQuantile, top=percentageAge, width=0.5)
p2.xgrid.grid_line_color = None
p2.y_range.start = 0


#hover tool p2
p2.add_tools(HoverTool(
    tooltips=[
        ('age quantile', '@x'),
        ('percentage', '$y'),
    ]
))

# Visualisation 3 - Heat map - Assignment 3
dfVirus = df.iloc[:, 21:38]
dfVirus["SARS-Cov-2 exam result"] = df["SARS-Cov-2 exam result"]
del dfVirus['Mycoplasma pneumoniae']

for i in range(16):
    dfVirus.iloc[:, i] = dfVirus.iloc[:, i].replace(["not_detected"], 0)
    dfVirus.iloc[:, i] = dfVirus.iloc[:, i].replace(["detected"], 1)

dfVirus.iloc[:, 16] = dfVirus.iloc[:, 16].replace(["negative"], 0)
dfVirus.iloc[:, 16] = dfVirus.iloc[:, 16].replace(["positive"], 1)

correlation = dfVirus.corr()

colors = list(reversed(colors[11]))  # we want an odd number to ensure 0 correlation is a distinct color
labels = dfVirus.columns
nlabels = len(labels)


def get_bounds(n):
    """Gets bounds for quads with n features"""
    bottom = list(chain.from_iterable([[ii] * nlabels for ii in range(nlabels)]))
    top = list(chain.from_iterable([[ii + 1] * nlabels for ii in range(nlabels)]))
    left = list(chain.from_iterable([list(range(nlabels)) for ii in range(nlabels)]))
    right = list(chain.from_iterable([list(range(1, nlabels + 1)) for ii in range(nlabels)]))
    return top, bottom, left, right


def get_colors(corr_array, colors):
    """Aligns color values from palette with the correlation coefficient values"""
    ccorr = arange(-1, 1, 1 / (len(colors) / 2))
    color = []
    for value in corr_array:
        ind = bisect.bisect_left(ccorr, value)
        color.append(colors[ind - 1])
    return color


p3 = figure(plot_width=600, plot_height=600,
            x_range=(0, nlabels), y_range=(0, nlabels),
            title="Correlation Coefficient Heatmap",
            tools="save", toolbar_location="right")

p3.xgrid.grid_line_color = None
p3.ygrid.grid_line_color = None
p3.xaxis.major_label_orientation = pi / 4
p3.yaxis.major_label_orientation = pi / 4

top, bottom, left, right = get_bounds(nlabels)  # creates sqaures for plot
color_list = get_colors(correlation.values.flatten(), colors)

p3.quad(top=top, bottom=bottom, left=left,
        right=right, line_color='white',
        color=color_list)

#Visualisation 4 select the data that is going te be plotted
SELECTION = [
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
    # 'Serum Glucose', <-- averaged around 4 values per quantile, too few
]

# title of the plot
TITLE = "Several blood chemicals versus Age quantile"

''' Data cleaning =============================================================='''
# selecting the required data
df_blood = df[SELECTION].copy()
print(df_blood)

dfPositive = df_blood[df_blood['SARS-Cov-2 exam result'] == "positive"]
dfNegative = df_blood[df_blood['SARS-Cov-2 exam result'] == "negative"]

dfPosAge = dfPositive['Patient age quantile']
dfNegAge = dfNegative['Patient age quantile']

del dfPositive['SARS-Cov-2 exam result']
del dfNegative['SARS-Cov-2 exam result']

print(dfPositive)

dcPositive = dfPositive.to_dict("list")
dcNegative = dfNegative.to_dict("list")

# print(dcBlood['Patient age quantile'])

bloodvaluelist = list(dcPositive)

bloodvaluelist.remove('Patient age quantile')

figures = []

sourcePos = ColumnDataSource(dfPositive)
sourceNeg = ColumnDataSource(dfNegative)

posneg_list = []
colorPositive = "blue"
colorNegative = "red"

for index in bloodvaluelist:
    #  for the first one don't use x_range, the remaining all will use the same x_range
    if index != "Hematocrit":
        scatter = figure(title=index, plot_width=400, plot_height=300, x_range=figures[0].x_range,
                         y_range=figures[0].y_range,
                         tools="save, pan, reset, wheel_zoom", x_axis_label='age quantile',
                         y_axis_label='standardized test result')
    else:
        scatter = figure(title=index, plot_width=400, plot_height=300, y_range=(-4, 4),
                         tools="save, pan, reset, wheel_zoom", x_axis_label='age quantile',
                         y_axis_label='standardized test result')
    p = scatter.circle(x=jitter("Patient age quantile", 0.5), y=index, size=4, color=colorPositive, alpha=0.5,
                       source=sourcePos, muted_alpha=0.1)
    n = scatter.circle(x=jitter("Patient age quantile", 0.5), y=index, size=4, color=colorNegative, alpha=0.5,
                       source=sourceNeg, muted_alpha=0.1)

    posneg_list += [p]
    posneg_list += [n]

    figures.append(scatter)

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
#end vis4

# Set ticks with labels
ticks = [tick + 0.5 for tick in list(range(nlabels))]
tick_dict = OrderedDict([[tick, labels[ii]] for ii, tick in enumerate(ticks)])
# Create the correct number of ticks for each axis
p3.xaxis.ticker = ticks
p3.yaxis.ticker = ticks
# Override the labels
p3.xaxis.major_label_overrides = tick_dict
p3.yaxis.major_label_overrides = tick_dict

# Setup color bar
mapper = LinearColorMapper(palette=colors, low=-1, high=1)
color_bar = ColorBar(color_mapper=mapper, location=(0, 0))
p3.add_layout(color_bar, 'right')

#hover tool p3
p3.add_tools(HoverTool(
    tooltips=[
        ('value', '$y'),
        ('pa', '$name')
    ]
))

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
OPTIONS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19"]
multi_choice = MultiChoice(value=["foo", "baz"], options=OPTIONS)
multi_choice.js_on_change("value", CustomJS(code="""
    console.log('multi_choice: value=' + this.value, this.toString())
"""))




# plot sizes
p1.plot_width = 600
p1.plot_height = 600
p2.plot_width = 600
p2.plot_height = 600
p3.plot_width = 600
p3.plot_height = 600

# GUI Left column
controls = [dropdown, spinner, toggle, multi_choice]
inputs = column(*controls, sizing_mode='fixed', height=300, width=500)
l1 = layout([[inputs, p1]], sizing_mode='fixed', height=600, width=150)
l2 = layout([[inputs, p2]], sizing_mode='fixed', height=600, width=150)
l3 = layout([[inputs, p3]], sizing_mode='fixed', height=600, width=150)
l4 = layout([[inputs, p4]], sizing_mode='fixed', height=600, width=150)
# Tab setup
tab1 = Panel(child=l1, title="Bar chart1")
tab2 = Panel(child=l2, title="Bar chart2")
tab3 = Panel(child=l3, title="Heat map")
tab4 = Panel(child=l4, title="Splom")

tabs = Tabs(tabs=[tab1, tab2, tab3, tab4])

show(tabs)
