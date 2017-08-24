from numpy import random
from bokeh.plotting import figure, curdoc
from bokeh.layouts import row, widgetbox, layout
from bokeh.models.widgets import Button

def draw_plot(data):
    plot = figure(width = 550, height = 350)
    plot.circle(data, data)
    return plot

def add_to_axis(axis):
    if axis == 'y': layout.children.append(draw_plot(data))
    elif axis == 'x': layout.children.append(row(draw_plot(data)))

def add_below(): add_to_axis('x')

def add_across(): add_to_axis('y')

data = [random.random() for i in range(10)]

add_below_button = Button(label = 'add below', width = 150)
add_across_button = Button(label = 'add across', width = 150)

add_below_button.on_click(add_below)
add_across_button.on_click(add_across)

curdoc().add_root(widgetbox([add_below_button, add_across_button], width = 200))

layout = row(width = 10000, height = 10000)

curdoc().add_root(layout)
