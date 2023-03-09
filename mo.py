import streamlit as st

def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
    return local_css()



def header(las_file):
    st.title('LAS File Header Info')
    if not las_file:
        st.warning('No file has been uploaded')
    else:
        for item in las_file.well:
            st.write(f"<b>{item.descr.capitalize()} ({item.mnemonic}):</b> {item.value}", unsafe_allow_html=True)





def home():
    #pweb = """<a href='http://andymcdonald.scot' target="_blank">http://andymcdonald.scot</a>"""
    #sm_li = """<a href='https://www.linkedin.com/in/andymcdonaldgeo/' target="_blank"><img src='https://cdn.exclaimer.com/Handbook%20Images/linkedin-icon_32x32.png'></a>"""
    #sm_tw = """<a href='https://twitter.com/geoandymcd' target="_blank"><img src='https://cdn.exclaimer.com/Handbook%20Images/twitter-icon_32x32.png'></a>"""
    #sm_med = """<a href='https://medium.com/@andymcdonaldgeo/' target="_blank"><img src='https://cdn.exclaimer.com/Handbook%20Images/Medium_32.png'></a>"""

    st.title('LAS Data Explorer ')
    st.write('## Welcome to the LAS Data Explorer')
    st.write('### Created by Mahmoud Ragab')
    st.write('''LAS Data Explorer is a tool designed using Python and Streamlit to help you view and gain an understanding of the contents of
    a LAS file.''')
    st.write('To begin using the app, load your LAS file using the file upload option on the sidebar. Once you have done this, you can navigate to the relevant tools using the Navigation menu.')
    st.write('\n')
    st.write('## Sections')
    st.write('**Header Info:** Information from the LAS file header.')
    st.write('**Data Information:** Information about the curves contained within the LAS file, including names, statisics and raw data values.')
    st.write('**Data Visualisation:** Visualisation tools to view las file data on a log plot, crossplot and histogram.')
    st.write('**Missing Data Visualisation:** Visualisation tools understand data extent and identify areas of missing values.')
    #st.write('## Get in Touch')
    #st.write(f'\nIf you want to get in touch, you can find me on Social Media at the links below or visit my website at: {pweb}.', unsafe_allow_html=True)
    
   # st.write(f'{sm_li}  {sm_med}  {sm_tw}', unsafe_allow_html=True)

    st.write('## Source Code, Bugs, Feature Requests')
    #githublink = """<a href='https://github.com/andymcdgeo/las_explorer' target="_blank">https://github.com/andymcdgeo/las_explorer</a>"""
    #st.write(f'\n\nCheck out the GitHub Repo at: {githublink}. If you find any bugs or have suggestions, please open a new issue and I will look into it.', unsafe_allow_html=True)
    
    
    
    
    
    
    
import streamlit as st
import pandas as pd

# Plotly imports
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px


def plot(las_file, well_data):
    st.title('LAS File Visualisation')
    
    if not las_file:
        st.warning('No file has been uploaded')
    
    else:
        columns = list(well_data.columns)
        st.write('Expand one of the following to visualise your well data.')
        st.write("""Each plot can be interacted with. To change the scales of a plot/track, click on the left hand or right hand side of the scale and change the value as required.""")
        with st.expander('Log Plot'):    
            curves = st.multiselect('Select Curves To Plot', columns)
            if len(curves) <= 1:
                st.warning('Please select at least 2 curves.')
            else:
                curve_index = 1
                fig = make_subplots(rows=1, cols= len(curves), subplot_titles=curves, shared_yaxes=True)

                for curve in curves:
                    fig.add_trace(go.Scatter(x=well_data[curve], y=well_data['DEPTH']), row=1, col=curve_index)
                    curve_index+=1
                
                fig.update_layout(height=1000, showlegend=False, yaxis={'title':'DEPTH','autorange':'reversed'})
                fig.layout.template='seaborn'
                st.plotly_chart(fig, use_container_width=True)

        with st.expander('Histograms'):
            col1_h, col2_h = st.beta_columns(2)
            col1_h.header('Options')

            hist_curve = col1_h.selectbox('Select a Curve', columns)
            log_option = col1_h.radio('Select Linear or Logarithmic Scale', ('Linear', 'Logarithmic'))
            hist_col = col1_h.color_picker('Select Histogram Colour')
            st.write('Color is'+hist_col)
            
            if log_option == 'Linear':
                log_bool = False
            elif log_option == 'Logarithmic':
                log_bool = True
        

            histogram = px.histogram(well_data, x=hist_curve, log_x=log_bool)
            histogram.update_traces(marker_color=hist_col)
            histogram.layout.template='seaborn'
            col2_h.plotly_chart(histogram, use_container_width=True)

        with st.expander('Crossplot'):
            col1, col2 = st.beta_columns(2)
            col1.write('Options')

            xplot_x = col1.selectbox('X-Axis', columns)
            xplot_y = col1.selectbox('Y-Axis', columns)
            xplot_col = col1.selectbox('Colour By', columns)
            xplot_x_log = col1.radio('X Axis - Linear or Logarithmic', ('Linear', 'Logarithmic'))
            xplot_y_log = col1.radio('Y Axis - Linear or Logarithmic', ('Linear', 'Logarithmic'))

            if xplot_x_log == 'Linear':
                xplot_x_bool = False
            elif xplot_x_log == 'Logarithmic':
                xplot_x_bool = True
            
            if xplot_y_log == 'Linear':
                xplot_y_bool = False
            elif xplot_y_log == 'Logarithmic':
                xplot_y_bool = True

            col2.write('Crossplot')
           
            xplot = px.scatter(well_data, x=xplot_x, y=xplot_y, color=xplot_col, log_x=xplot_x_bool, log_y=xplot_y_bool)
            xplot.layout.template='seaborn'
            col2.plotly_chart(xplot, use_container_width=True)
            
            
            
            
            
import streamlit as st
import pandas as pd

def raw_data(las_file, well_data):
    st.title('LAS File Data Info')
    if not las_file:
        st.warning('No file has been uploaded')
    else:
        st.write('**Curve Information**')
        for count, curve in enumerate(las_file.curves):
            # st.write(f"<b>Curve:</b> {curve.mnemonic}, <b>Units: </b>{curve.unit}, <b>Description:</b> {curve.descr}", unsafe_allow_html=True)
            st.write(f"   {curve.mnemonic} ({curve.unit}): {curve.descr}", unsafe_allow_html=True)
        st.write(f"<b>There are a total of: {count+1} curves present within this file</b>", unsafe_allow_html=True)
        
        st.write('<b>Curve Statistics</b>', unsafe_allow_html=True)
        st.write(well_data.describe())
        st.write('<b>Raw Data Values</b>', unsafe_allow_html=True)
        st.dataframe(data=well_data)         
            
            
            
import missingno as mno
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Plotly imports
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px


def missing(las_file, well_data):
    st.title('LAS File Missing Data')
    
    if not las_file:
        st.warning('No file has been uploaded')
    
    else:
        st.write("""The following plot can be used to identify the depth range of each of the logging curves.
         To zoom in, click and drag on one of the tracks with the left mouse button. 
         To zoom back out double click on the plot.""")

        data_nan = well_data.notnull().astype('int')
        # Need to setup an empty list for len check to work
        curves = []
        columns = list(well_data.columns)
        columns.pop(-1) #pop off depth

        col1_md, col2_md= st.beta_columns(2)

        selection = col1_md.radio('Select all data or custom selection', ('All Data', 'Custom Selection'))
        fill_color_md = col2_md.color_picker('Select Fill Colour', '#9D0000')
        # top_depth = col3_md.number_input('Top Depth', step=50.0, value=min_depth, min_value=min_depth, max_value=max_depth)
        # bottom_depth = col4_md.number_input('Bottom Depth', step=50.0, value=max_depth, min_value=min_depth, max_value=max_depth)

        if selection == 'All Data':
            curves = columns
        else:
            curves = st.multiselect('Select Curves To Plot', columns)

        if len(curves) <= 1:
            st.warning('Please select at least 2 curves.')
        else:
            curve_index = 1
            fig = make_subplots(rows=1, cols= len(curves), subplot_titles=curves, shared_yaxes=True, horizontal_spacing=0.02)

            for curve in curves:
                fig.add_trace(go.Scatter(x=data_nan[curve], y=well_data['DEPTH'], 
                    fill='tozerox',line=dict(width=0), fillcolor=fill_color_md), row=1, col=curve_index)
                fig.update_xaxes(range=[0, 1], visible=False)
                fig.update_xaxes(range=[0, 1], visible=False)
                curve_index+=1
            
            fig.update_layout(height=1000, showlegend=False, yaxis={'title':'DEPTH','autorange':'reversed'})
            # rotate all the subtitles of 90 degrees
            for annotation in fig['layout']['annotations']: 
                    annotation['textangle']=-90
            fig.layout.template='seaborn'
            st.plotly_chart(fig, use_container_width=True)
 #calculation
'''
import lasio
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import welly
import math           
            
def calculation(las_file, well_data):
    st.title('Data calculation')
    
    if not las_file:
        st.warning('No file has been uploaded') 
    else:
        def shale_volume(gamma_ray, gamma_ray_max, gamma_ray_min):
            
            vshale = (gamma_ray - gamma_ray_min) / (gamma_ray_max - gamma_ray_min)
            return vshale

        #Calculate Shale Volume
        df['VSHALE'] = shale_volume(df['GR'],df['GR'].max(),
                                    df['GR'].min())
        
        def density_porosity(input_density, matrix_density, fluid_density):
            
   
            denpor = (matrix_density - input_density) / (matrix_density - fluid_density)
            return denpor


       #Calculate density porosity
       #in case of sand matrix densiy=2.65 , and (formation almost slint) fluid density =1.1
        df['PHI_D'] = density_porosity(df['RHOB'], 2.65, 1.1)



# ## Total Porosity  Function


        def total_porosity(density_porosity,  Neutron_porosity):
   
            phit = (density_porosity + Neutron_porosity) / (2)
   
            return phit

#Calculate total porosity
        df['PHI_T'] = total_porosity(df['PHI_D'],df['NPHI'])
       

# ## Effective Porosity Function


        def effective_porosity(total_porosity, shale_volume):
    
            phieff = total_porosity * (1 - shale_volume)
            return phieff




#Calculate effective porosity
        df['PHI_EFF'] = effective_porosity(df['PHI_T'],df['VSHALE'])



# ## Sand Volume Function



        def sand_volume_correct(effective_porosity, shale_volume):
    
            vsand = 1-(effective_porosity-shale_volume)
            return vsand


#Calculate sand volume
        df['VSAND'] = sand_volume_correct(df['PHI_EFF'],df['VSHALE'])



# ## Formation Factor Function



        def formation_factor(arch_a, arch_m, effective_porosity):
    
            FF = (arch_a)/(effective_porosity**arch_m)
            return FF


#Calculate  Formation Factor
        df['FF'] = formation_factor(0.6, 2.15, df['PHI_EFF'])

# ## Irreducible Water saturation Function
# 


        def irrducible_saturation(formation_factor):
    #for n in formation_factor:
        
            Swirr = (formation_factor/2000)**0.5
        
            return Swirr


#Calculate Irreducible Water saturation

        df['Swirr'] = irrducible_saturation(df['FF'])



# ## Permeability (Timur equation) Function 


        def timur(effective_porosity, irrducible_saturation, A, B, C):
            # A, B , C are constent 
            # A = 0.136
            # B = 4.4
            # C = 2
            K = ((A *((effective_porosity)**B)) / (irrducible_saturation**C))
            #K = ((A*((effective_porosity)**B))/(irrducable_saturation**(C)))
            return K


 '''                       