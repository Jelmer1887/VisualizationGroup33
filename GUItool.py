# imports
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, output_file, show
from bokeh.models.widgets import Panel, Tabs
from bokeh.layouts import column, row, layout, widgetbox
from bokeh.models import CustomJS, Slider, Toggle, Dropdown, MultiChoice, Spinner
from bokeh.transform import dodge
from bokeh.palettes import RdBu as colors
from bokeh.models import ColorBar, LinearColorMapper, HoverTool, BoxSelectTool
import pandas as pd
import bisect
from math import pi
from numpy import arange
from itertools import chain
from collections import OrderedDict

# why is 'plot' created??? I can't find any place that add any data to it... (see p1)
plot = figure(tools="pan,wheel_zoom,box_zoom,reset")    # create figure object
plot.add_tools(BoxSelectTool(dimensions="width"))       # add interactive tools to plot
output_file("test.html")                                # set output path
df = pd.read_excel('archive\dataset.xlsx')              # dataset path (relative to script)


#tab 1 - Assignment 4 visualisation
# !LOOK! the age_quantiles are binned per 4 entries... BUT ITS HARDCODED!!!
# what if we want to increase or decreate the binsize? than we need to add or remove a lot of if/elif statements
# we can put it in a loop to simplify it (see below)
# consider using the following aproach:
'''
binnumber = 5                               # number of bins
binsize = int(20/binnumber)                 # number of age_quantiles in one bin

# lists to store number of people per category per bin in
regularWardPos   = [0]*binsize              # creates a list of zeroes of length 'binsize'
semiIntensivePos = [0]*binsize
intensivePos     = [0]*binsize

regularWardNeg   = [0]*binsize
semiIntensiveNeg = [0]*binsize
intensiveNeg     = [0]*binsize

totalAgePos      = [0]*binsize
totalAgeNeg      = [0]*binsize
'''
regularWardPos = [0]*5                      # list of zeroes for each bin and type of patient (see second visualisation for explanetion of list of zeroes)
semiIntensivePos = [0]*5
intensivePos = [0]*5

regularWardNeg = [0]*5
semiIntensiveNeg = [0]*5
intensiveNeg = [0]*5

totalAgePos = [0]*5
totalAgeNeg = [0]*5


for index, row in df.iterrows():                        # iterate over dataframe rows

    # extracting number of patients per age group per ward per test result
    # The bins follow a pattern, which can thus be put into a loop to prevent repetition, replace 93 lines of code with 26:
    '''
    for bin in binnumber:                       # iterate over the bins
        binStartAge = bin * binsize             # computes at which age quantile a bin starts

        # checks if age_quantile at 'index' is in the current bin:
        if binStartAge <= df.iloc[index, 1] and df.iloc[index, 1] < (binStartAge + binnumber):

            if df.iloc[index, 2] == "positive":     # if patient is positive...
                totalAgePos[bin] += 1               # ... increment counter for number of people in current bin that are positive

                # identify at which ward the *positive* patient is in and increment corresponding counter
                if df.iloc[index, 3] == 1:
                    regularWardPos[bin] += 1
                elif df.iloc[index, 4] == 1:
                    semiIntensivePos[bin] += 1
                elif df.iloc[index, 5] == 1:
                    intensivePos[bin] += 1

            if df.iloc[index, 2] == "negative":     # if patient is negative...
                totalAgeNeg[bin] += 1               # ... increment counter for number of people in current bin that are negative

                # identify at which ward the *negative* patient is in and increment corresponding counter
                if df.iloc[index, 3] == 1:
                    regularWardNeg[bin] += 1
                elif df.iloc[index, 4] == 1:
                    semiIntensiveNeg[bin] += 1
                elif df.iloc[index, 5] == 1:
                    intensiveNeg[bin] += 1  
    '''

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

# lists of zeroes to store percentages per bin per type
percentageRegularWardPos   = [0]*5      # !LOOK! replaced [0,0,0,0,0] with [0]*5... the 5 shouldn't be hardcoded (change to binnumber??? (see above))
percentageSemiIntensivePos = [0]*5
percentageIntensivePos     = [0]*5

percentageRegularWardNeg   = [0]*5
percentageSemiIntensiveNeg = [0]*5
percentageIntensiveNeg     = [0]*5

for i in range(len(regularWardPos)):
    # compute percentages of positive and negative patients per age group per ward
    percentageRegularWardPos[i] = regularWardPos[i] / totalAgePos[i] * 100
    percentageSemiIntensivePos[i] = semiIntensivePos[i] / totalAgePos[i] * 100
    percentageIntensivePos[i] = intensivePos[i] / totalAgePos[i] * 100

    percentageRegularWardNeg[i] = regularWardNeg[i] / totalAgeNeg[i] * 100
    percentageSemiIntensiveNeg[i] = semiIntensiveNeg[i] / totalAgeNeg[i] * 100
    percentageIntensiveNeg[i] = intensiveNeg[i] / totalAgeNeg[i] * 100


# Legend and axis labels
wardDevision = ["regular ward", "semi-intensive unit", "intensive care"]
ageDevision = ["child and teen", "young adult and adult", "middle aged", "senior", "elderly"]
positiveReg = ["regular ward positive", "regular ward negative"]
positiveSemi = ["semi-intensive unit positive", "semi-intensive unit negative"]
positiveIntens = ["intensive care positive", "intensive care negative"]

# packaging data into dictionary format
dictDataReg = {
    'age group': ageDevision,
    "regular ward positive" : percentageRegularWardPos,
    "regular ward negative" : percentageRegularWardNeg
}
dictDataSemi = {
    'age group': ageDevision,
    "semi-intensive unit positive" : percentageSemiIntensivePos,
    "semi-intensive unit negative" : percentageSemiIntensiveNeg
}
dictDataIntens = {
    'age group': ageDevision,
    "intensive care positive": percentageIntensivePos,
    "intensive care negative": percentageIntensiveNeg
}

# converting dictionaries into datasources
sourceReg = ColumnDataSource(data=dictDataReg)
sourceSemi = ColumnDataSource(data=dictDataSemi)
sourceIntens = ColumnDataSource(data=dictDataIntens)

# colors for the bars
colorsReg = ["#2874A6", "#85C1E9"]      # regular ward color  [positive test, negative test]
colorsSemi = ["#B03A2E", "#F5B7B1"]     # semi-intense ward color [positive test, negative test]
colorsIntens = ["#B7950B", "#F9E79F"]   # intensive ward color  [positive test, negative test]

p1 = figure(
    x_range=ageDevision,                # sets x-axis
    title="Percentage of age group with positive Covid-19 test in hospital ward", # title of the plot
    toolbar_location=None,              # sets location of the toolbar (nowhere)
    tools=""                            # disables tools
)

#dodge('age group', -0.25, range=chart.x_range)

# adds stacked bars to the plot
p1.vbar_stack(
    positiveReg,                        # sets y-axis for bars (using keys of source)
    x=dodge('age group', -0.25, range=p1.x_range), # sets x-axis
    width=0.2,                          # width of bars
    source=dictDataReg,                 # datasource for the bars
    color= colorsReg,                   # colors of the bars
    legend_label=positiveReg            # set legend label
)

p1.vbar_stack(
    positiveSemi,                       # sets y-axis for bars (using keys of source)
    x=dodge('age group', 0.0, range=p1.x_range), # sets x-axis
    width=0.2,                          # width of bars
    source=dictDataSemi,                # datasource for the bars
    color= colorsSemi,                  # colors of the bars
    legend_label=positiveSemi           # set legend label
)

p1.vbar_stack(
    positiveIntens,                     # sets y-axis for bars (using keys of source)
    x=dodge('age group', 0.25, range=p1.x_range), # sets x-axis
    width=0.2,                          # width of bars
    source=dictDataIntens,              # datasource for the bars
    color= colorsIntens,                # colors of the bars
    legend_label=positiveIntens         # set legend label
)

# plot properties
p1.y_range.start = 0                    # y-range starting point
p1.x_range.range_padding = 0.1          # additional space between x-axis values
p1.xgrid.grid_line_color = None         # removes gridlines
p1.legend.location = "top_left"         # sets location of Legend
p1.legend.orientation = "vertical"      # sets orientation of the Legend (vertical -> entries below each other)


#Visualisation 2 - Bar chart - Assignment 3
# !LOOK! instead of putting 20 zeroes in a list manually, consider using a list comprehension or a lsit operation
'''
positiveAge = [0 for iter in range(0,20)]   # list comprehension (puts 0 in the list as it loops 20 times)
positiveAge = [0]*20                        # list operation (multiply [0] by 20 => [0]+[0]+...+[0] = [0, 0, ..., 0])

# make lists of zeroes to store number of patients in:
positiveAge   = [0]*20
totalAge      = [0]*20
percentageAge = [0]*20
'''
positiveAge   = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
totalAge      = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
percentageAge = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

for index, row in df.iterrows():        # iterate over dataset
    # !LOOK!
    # contains 'if/elif' statement for each age quantile... this is quite bad practise: 
    # say we want to change "positive" to "negative", then we need to change it 20 times!
    # rule of thumb: if you're repeating an if statement with only one number that's changing, you can make it shorter!
    # in this case: consider using the index of the 'totalAge' as a comparison, which would replace 80 lines of code with 4:
    '''
    for age_quantile in range(len(totalAge)):   # loops over integers 0 to 19
        totalAge[age_quantile] += 1             # increments counter for number of people of age 'age_quantile'
        if df.iloc[index, 2] == "positive":     # if patient is positive...
            positiveAge[age_quantile] += 1      # ... increment counter for number of people of age 'age_quantile' that is positive
    '''

    if df.iloc[index, 1] == 0:
        totalAge[0] += 1
        if df.iloc[index, 2] == "positive":
            positiveAge[0] += 1
    elif df.iloc[index, 1] == 1:
        totalAge[1] += 1
        if df.iloc[index, 2] == "positive":
            positiveAge[1] += 1
    elif df.iloc[index, 1] == 2:
        totalAge[2] += 1
        if df.iloc[index, 2] == "positive":
            positiveAge[2] += 1
    elif df.iloc[index, 1] == 3:
        totalAge[3] += 1
        if df.iloc[index, 2] == "positive":
            positiveAge[3] += 1
    elif df.iloc[index, 1] == 4:
        totalAge[4] += 1
        if df.iloc[index, 2] == "positive":
            positiveAge[4] += 1
    elif df.iloc[index, 1] == 5:
        totalAge[5] += 1
        if df.iloc[index, 2] == "positive":
            positiveAge[5] += 1
    elif df.iloc[index, 1] == 6:
        totalAge[6] += 1
        if df.iloc[index, 2] == "positive":
            positiveAge[6] += 1
    elif df.iloc[index, 1] == 7:
        totalAge[7] += 1
        if df.iloc[index, 2] == "positive":
            positiveAge[7] += 1
    elif df.iloc[index, 1] == 8:
        totalAge[8] += 1
        if df.iloc[index, 2] == "positive":
            positiveAge[8] += 1
    elif df.iloc[index, 1] == 9:
        totalAge[9] += 1
        if df.iloc[index, 2] == "positive":
            positiveAge[9] += 1
    elif df.iloc[index, 1] == 10:
        totalAge[10] += 1
        if df.iloc[index, 2] == "positive":
            positiveAge[10] += 1
    elif df.iloc[index, 1] == 11:
        totalAge[11] += 1
        if df.iloc[index, 2] == "positive":
            positiveAge[11] += 1
    elif df.iloc[index, 1] == 12:
        totalAge[12] += 1
        if df.iloc[index, 2] == "positive":
            positiveAge[12] += 1
    elif df.iloc[index, 1] == 13:
        totalAge[13] += 1
        if df.iloc[index, 2] == "positive":
            positiveAge[13] += 1
    elif df.iloc[index, 1] == 14:
        totalAge[14] += 1
        if df.iloc[index, 2] == "positive":
            positiveAge[14] += 1
    elif df.iloc[index, 1] == 15:
        totalAge[15] += 1
        if df.iloc[index, 2] == "positive":
            positiveAge[15] += 1
    elif df.iloc[index, 1] == 16:
        totalAge[16] += 1
        if df.iloc[index, 2] == "positive":
            positiveAge[16] += 1
    elif df.iloc[index, 1] == 17:
        totalAge[17] += 1
        if df.iloc[index, 2] == "positive":
            positiveAge[17] += 1
    elif df.iloc[index, 1] == 18:
        totalAge[18] += 1
        if df.iloc[index, 2] == "positive":
            positiveAge[18] += 1
    elif df.iloc[index, 1] == 19:
        totalAge[19] += 1
        if df.iloc[index, 2] == "positive":
            positiveAge[19] += 1

for age in range(len(positiveAge)):       # compute percentage of positvely tested patients per age quantile
    percentageAge[age] = positiveAge[age] / totalAge[age] *100

print(positiveAge)      # debugging
print(totalAge)         # debugging
print(percentageAge)    # debugging

# !LOOK! list of labels for the x-axis of the plot
# theres a pattern in the numbers, so it can be simplified! Consider using a list comprehension:
# ageQuantile = [str(number) for number in range(20)]  # generates a list of numbers from 0 to 19 in string format
ageQuantile = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19"]

# create plot 2 object
p2 = figure(
    x_range=ageQuantile,                        # x-axis labels / range
    plot_height=250,                            # height of the plot in pixels
    title="Percentage positive tests per age quartile", # title of the plot
    toolbar_location=None,                      # loaction of the toolbar (None -> nowhere)
    tools=""                                    # disables toolbar/tools
)
# adds bars to the plot 2 object
p2.vbar(
    x=ageQuantile,                              # specifies at which x-axis each bar should be placed
    top=percentageAge,                          # specifies y-axis (height of the bars)
    width=0.5                                   # specifies width of the bars
)

# plot 2 properties
p2.xgrid.grid_line_color = None                 # disables gridlines
p2.y_range.start = 0                            # sets starting point for y-axis

#Visualisation 3 - Heat map - Assignment 3
dfVirus = df.iloc[:,  21:38]                    # copy virus related column from dataset
dfVirus["SARS-Cov-2 exam result"] = df["SARS-Cov-2 exam result"] # add covid-test results to virus copy of dataset
del dfVirus['Mycoplasma pneumoniae']            # removing virusses with close to none entries

for i in range(16):                             # iterate over dataframe
    # replace human langue values for virusses by easy to work with 1 and 0 values
    dfVirus.iloc[:, i] = dfVirus.iloc[:, i].replace(["not_detected"], 0)
    dfVirus.iloc[:, i] = dfVirus.iloc[:, i].replace(["detected"], 1)

# replace human langue values for covid test result by easy to work with 1 and 0 values
dfVirus.iloc[:, 16] = dfVirus.iloc[:, 16].replace(["negative"], 0)
dfVirus.iloc[:, 16] = dfVirus.iloc[:, 16].replace(["positive"], 1)

correlation = dfVirus.corr()                    # create correlation object

colors = list(reversed(colors[11]))             # we want an odd number to ensure 0 correlation is a distinct color
labels = dfVirus.columns                        # use the dataframe column names (Virusses) as labels for the plot
nlabels = len(labels)                           # specify number of labels

def get_bounds(n):
    """Gets bounds for quads with n features"""
    bottom = list(chain.from_iterable([[ii]*nlabels for ii in range(nlabels)]))
    top = list(chain.from_iterable([[ii+1]*nlabels for ii in range(nlabels)]))
    left = list(chain.from_iterable([list(range(nlabels)) for ii in range(nlabels)]))
    right = list(chain.from_iterable([list(range(1,nlabels+1)) for ii in range(nlabels)]))
    return top, bottom, left, right

def get_colors(corr_array, colors):
    """Aligns color values from palette with the correlation coefficient values"""
    ccorr = arange(-1, 1, 1/(len(colors)/2))
    color = []
    for value in corr_array:
        ind = bisect.bisect_left(ccorr, value)
        color.append(colors[ind-1])
    return color

# create heatmap plot object
p3 = figure(
    plot_width=600,                             # plot width in pixels
    plot_height=600,                            # plot height in pixels
    x_range=(0,nlabels),                        # x-range (number of entries on the x-axis)
    y_range=(0,nlabels),                        # y-range (number of entries on the y-axis)
    title="Correlation Coefficient Heatmap",    # title of the plot
    tools="save",                               # activates save tool
    toolbar_location = "right"                  # specifies location of the toolbar relative to the plot
)

# plot 3 properties
p3.xgrid.grid_line_color = None                 # disables x-gridlines
p3.ygrid.grid_line_color = None                 # disables y-gridlines
p3.xaxis.major_label_orientation = pi/4         # rotates x-labels by 45 degrees (pi/4 rad => 45 deg)
p3.yaxis.major_label_orientation = pi/4         # rotates y-labels by 45 degrees

top, bottom, left, right = get_bounds(nlabels)  # creates sqaures for plot
color_list = get_colors(correlation.values.flatten(), colors)   # makes list of colors for values

# specifies how a square in the heatmap looks
p3.quad(
    top    = top, 
    bottom = bottom, 
    left   = left,
    right  = right, 
    line_color = 'white',
    color = color_list
)

# Set ticks with labels
ticks = [tick+0.5 for tick in list(range(nlabels))]
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

#Spinner GUI
spinner = Spinner(title="Size", low=0, high=4, step=0.1, value=1, width=80)
#spinner.js_link('value', points.glyph, 'radius')

#Dropdown menu GUI
menu = [("Item 1", "item_1"), ("Item 2", "item_2"), None, ("Item 3", "item_3")]
dropdown = Dropdown(label="Dropdown button", button_type="warning", menu=menu)
dropdown.js_on_event("menu_item_click", CustomJS(code="console.log('dropdown: ' + this.item, this.toString())"))

#Toggle button GUI
toggle = Toggle(label="Button", button_type="success")
toggle.js_on_click(CustomJS(code="""
    console.log('toggle: active=' + this.active, this.toString())
"""))
OPTIONS = ["Attribute1", "Attribute2", "Attribute3", "Attribute4"]
multi_choice = MultiChoice(value=["foo", "baz"], options=OPTIONS)
multi_choice.js_on_change("value", CustomJS(code="""
    console.log('multi_choice: value=' + this.value, this.toString())
"""))

#GUI Left column
controls = [dropdown, spinner, toggle]
inputs = column(*controls, sizing_mode='fixed', height=250, width=350)
l1 = layout([[inputs, p1]], sizing_mode='fixed', height=600, width=150)
l2 = layout([[inputs, p2]], sizing_mode='fixed', height=600, width=150)
l3 = layout([[inputs, p3]], sizing_mode='fixed', height=600, width=150)
#Tab setup
tab1 = Panel(child=l1, title="Bar chart1")
tab2 = Panel(child=l2, title="Bar chart2")
tab3 = Panel(child=l3, title="Heat map")

tabs = Tabs(tabs=[tab1, tab2, tab3])

show(tabs)


