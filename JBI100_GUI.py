from bokeh.models import ColorBar, LinearColorMapper, HoverTool, BoxSelectTool, CustomJSHover, BoxZoomTool, ResetTool, \
    WheelZoomTool, PanTool, Range1d, DataRange1d
from bokeh.models.widgets.buttons import Button
from bokeh.transform import jitter
from bokeh.plotting import figure, output_file, show
from bokeh.models.widgets import Panel, Tabs
from bokeh.layouts import column, row, layout, widgetbox, grid, GridBox, gridplot
from bokeh.models import CustomJS, Slider, Toggle, Dropdown, MultiChoice, Spinner, Select, ColumnDataSource, Legend, \
    LegendItem
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
from bokeh.io import output_file, show
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Div
from bokeh.models.widgets import Paragraph
from bokeh.models.widgets import PreText

plot = figure(tools="pan,wheel_zoom,box_zoom,reset")
plot.add_tools(BoxSelectTool(dimensions="width"))
output_file("test.html")
df = pd.read_excel(
    r'dataset.xlsx')

# tab 1 - Assignment 4 visualisation - Stacked bar chart ================================================================================================================
# @CHANGE: The number of bins was HARDCODED!!! We can reduce the number of lines by 83... 
# ... we can do so by computing in which bin the age quantile will go using integer division (see def. binofIndex)

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

    if df.iloc[index, 2] == "positive":
        totalAgePos[binofIndex] += 1                    # @CHANGE: instead of having seperate if statements for each bin, use computed bin as index
        if df.iloc[index, 3] == 1:
            regularWardPos[binofIndex] += 1
        elif df.iloc[index, 4] == 1:
            semiIntensivePos[binofIndex] += 1
        elif df.iloc[index, 5] == 1:
            intensivePos[binofIndex] += 1

    if df.iloc[index, 2] == "negative":                 
        totalAgeNeg[binofIndex] += 1
        if df.iloc[index, 3] == 1:                      # @CHANGE: technically, we are still repeating ourselves in the nested if/elif-statements here...
            regularWardNeg[binofIndex] += 1             # ...so it can be done in a cleaner way... if we have time at the end we should invesitage using mappings to optimise this
        elif df.iloc[index, 4] == 1:
            semiIntensiveNeg[binofIndex] += 1
        elif df.iloc[index, 5] == 1:
            intensiveNeg[binofIndex] += 1

percentageRegularWardPos = [0] * nrofBins
percentageSemiIntensivePos = [0] * nrofBins
percentageIntensivePos = [0] * nrofBins

percentageRegularWardNeg = [0] * nrofBins
percentageSemiIntensiveNeg = [0] * nrofBins
percentageIntensiveNeg = [0] * nrofBins

for i in range(len(regularWardPos)):
    percentageRegularWardPos[i] = regularWardPos[i] / (totalAgePos[i] + totalAgeNeg[i]) * 100
    percentageSemiIntensivePos[i] = semiIntensivePos[i] / (totalAgePos[i] + totalAgeNeg[i]) * 100
    percentageIntensivePos[i] = intensivePos[i] / (totalAgePos[i] + totalAgeNeg[i]) * 100

    percentageRegularWardNeg[i] = regularWardNeg[i] / (totalAgePos[i] + totalAgeNeg[i]) * 100
    percentageSemiIntensiveNeg[i] = semiIntensiveNeg[i] / (totalAgePos[i] + totalAgeNeg[i]) * 100
    percentageIntensiveNeg[i] = intensiveNeg[i] / (totalAgePos[i] + totalAgeNeg[i]) * 100

wardDevision = ["regular ward", "semi-intensive unit", "intensive care"]

ageDevision = ["child and teen", "young adult and adult", "middle aged", "senior", "elderly"]

positiveReg = ["regular ward positive", "regular ward negative"]
positiveSemi = ["semi-intensive unit positive", "semi-intensive unit negative"]
positiveIntens = ["intensive care positive", "intensive care negative"]

dictDataReg = {'age group': ageDevision,
               "regular ward positive": percentageRegularWardPos,
               "regular ward negative": percentageRegularWardNeg,
               "percentagePos"        : percentageRegularWardPos,           # a field with an identical name for every datasource for the tooltip
               "percentageNeg"        : percentageRegularWardNeg            # a field with an identical name for every datasource for the tooltip
               }

dictDataSemi = {'age group': ageDevision,
                "semi-intensive unit positive": percentageSemiIntensivePos,
                "semi-intensive unit negative": percentageSemiIntensiveNeg,
                "percentagePos"               : percentageSemiIntensivePos, # a field with an identical name for every datasource for the tooltip
                "percentageNeg"               : percentageSemiIntensiveNeg  # a field with an identical name for every datasource for the tooltip
                }

dictDataIntens = {'age group': ageDevision,
                  "intensive care positive": percentageIntensivePos,
                  "intensive care negative": percentageIntensiveNeg,
                  "percentagePos"          : percentageIntensivePos,        # a field with an identical name for every datasource for the tooltip
                  "percentageNeg"          : percentageIntensiveNeg         # a field with an identical name for every datasource for the tooltip
                  }

sourceReg = ColumnDataSource(data=dictDataReg)
sourceSemi = ColumnDataSource(data=dictDataSemi)
sourceIntens = ColumnDataSource(data=dictDataIntens)

colorsReg = ["#2874A6", "#85C1E9"]      # first dark color, then light color
colorsSemi = ["#B03A2E", "#F5B7B1"]
colorsIntens = ["#B7950B", "#F9E79F"]

p1 = figure(x_range=ageDevision,
            title="Percentage of age group with positive Covid-19 test in hospital ward", toolbar_location=None,
            tools="", y_axis_label="Age group specific percentage per hospital ward")

p1.vbar_stack(positiveReg, x=dodge('age group', -0.25, range=p1.x_range), width=0.2, source=dictDataReg,
              color=colorsReg, legend_label=positiveReg)

p1.vbar_stack(positiveSemi, x=dodge('age group', 0.0, range=p1.x_range), width=0.2, source=dictDataSemi,
              color=colorsSemi, legend_label=positiveSemi)

p1.vbar_stack(positiveIntens, x=dodge('age group', 0.25, range=p1.x_range), width=0.2, source=dictDataIntens,
              color=colorsIntens, legend_label=positiveIntens)

p1.y_range.start = 0
p1.x_range.range_padding = 0.1
p1.xgrid.grid_line_color = None
p1.legend.location = "top_center"
p1.legend.orientation = "vertical"

# SELECT menu GUI
selectoptions = ["Postive tested on Covid-19 virus", "Negative tested on Covid-19 virus", "Show both"]
resultSelect = Select(title="What to show", options=selectoptions)

p1.add_tools(HoverTool(
    tooltips=[
        ('age group', '@{age group}'),
        ('percentage positive', '@percentagePos'),
        ('percentage negative', '@percentageNeg'),
        ('label', '$name'),
    ]
))




# Visualisation 2 - Bar chart - Assignment 3 ============================================================================================================================
positiveAge = [0] * 20
totalAge = [0] * 20
percentageAge = [0] * 20

for index, row in df.iterrows():
    for i in range(20):
        if df.iloc[index, 1] == i:
            totalAge[i] += 1
            if df.iloc[index, 2] == "positive":
                positiveAge[i] += 1

for i in range(len(positiveAge)):
    percentageAge[i] = positiveAge[i] / totalAge[i] * 100

ageQuantile = [str(i) for i in range(20)]

print("\ndebugging info:-------------------------")
print(f"length positiveAge: {len(positiveAge)}")
print(f"length totalAge: {len(totalAge)}")
print(f"length percentageAge: {len(percentageAge)}")
print(f"\nageQuantile({len(ageQuantile)}): {ageQuantile}")
print("\ndebugging info:-------------------------\n")

sourcep2 = ColumnDataSource(data=dict(
    x=ageQuantile,
    y=percentageAge,
))
# sorted on y value, from low to high
sorted_ageQuantile = sorted(ageQuantile, key=lambda x: percentageAge[ageQuantile.index(x)])
p2 = figure(
    x_range=sorted_ageQuantile,
    y_range=(0, int(max(percentageAge)) + 1),
    plot_height=250, title="Percentage positive tests per age quartile", toolbar_location="below",
    tools=[WheelZoomTool(), ResetTool(), PanTool()])
#  sorted on age quantile
p2 = figure(
    x_range=ageQuantile,
    y_range=(0, int(max(percentageAge)) + 1),
    plot_height=250, title="Percentage positive tests per age quartile", toolbar_location="below",
    tools=[WheelZoomTool(), ResetTool(), PanTool()])
p2.x_range.max_interval = 19

p2.vbar(x='x', top='y', width=0.5, source=sourcep2)
p2.xgrid.grid_line_color = None

# hover tool p2
p2.add_tools(HoverTool(
    tooltips=[
        ('age quantile', '@x'),
        ('percentage', '@y')
    ]
))


# Visualisation 3 - Heat map - Assignment 3 =============================================================================================================================
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


# Visualisation 4 select the data that is going te be plotted ===========================================================================================================
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

# selecting the required data
df_blood = df[SELECTION].copy()

dfPositive = df_blood[df_blood['SARS-Cov-2 exam result'] == "positive"]
dfNegative = df_blood[df_blood['SARS-Cov-2 exam result'] == "negative"]

dfPosAge = dfPositive['Patient age quantile']
dfNegAge = dfNegative['Patient age quantile']

del dfPositive['SARS-Cov-2 exam result']
del dfNegative['SARS-Cov-2 exam result']

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
        scatter = figure(
            title=index, 
            plot_width=400, 
            plot_height=300, 
            y_range=(-4, 4),
            tools="save, pan, reset, wheel_zoom, box_select", 
            x_axis_label='age quantile',
            y_axis_label='standardized test result'
        )

    p = scatter.square(x=jitter("Patient age quantile", 0.5), y=index, size=4, color=colorPositive, alpha=0.5,
                       source=sourcePos, muted_alpha=0.1)
    n = scatter.circle(x=jitter("Patient age quantile", 0.5), y=index, size=4, color=colorNegative, alpha=0.5,
                       source=sourceNeg, muted_alpha=0.1)
    
    ''' CHANGE: The problem is that there are 2 distinct datasources, to include the tooltip we need to find a way to combine them
    # hover tool p3
    scatter.add_tools(HoverTool(
        tooltips=[
            ('standardized value:', '$y'),
            ('pa', '$name')
        ]
    ))
    '''

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
# end vis4

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




# Spinner GUI ===========================================================================================================================================================
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

# attempt at linking it all
lab = "Click me!"
but = Button(label = lab)
def clickedcode():      # this function would be called when the button is pressed, but it's not triggering...
    if lab == "Click me!":      # I tried changing the label but that did not happen
        lab = "Clicked"
    else:
        lab = "Click me!"
    print("button was clicked!")       # nothing was printed to the console either

but.on_click(clickedcode)       # links the clickedcode to the button

# select
OPTIONS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19"]
multi_choice = MultiChoice(value=["foo", "baz"], options=OPTIONS)
multi_choice.js_on_change("value", CustomJS(code="""
    console.log('multi_choice: value=' + this.value, this.toString())
"""))

# # SELECT menu GUI
# selectoptions = ["Postive tested on Covid-19 virus", "Negative tested on Covid-19 virus", "Show both"]
# resultSelect = Select(title="What to show", options=selectoptions)

title = Div(
    text="<b>Visualisation tool of patients tested for Covid-19 of the Hospital Israelita Albert Einstein, at São Paulo, Brazil</b>",
    style={'font-size': '200%', 'color': 'black'}, width=800)

text = [title]
# gridplot
p = gridplot([[p1, p2], [None, p3]], plot_width=400, plot_height=400)
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
l2 = layout([[p2]], sizing_mode='fixed', height=600, width=150)
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
show(layout)
