# Math 10 HW4
# Leo Cheung, ID 19421084

import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from streamlit.state.session_state import Value

#GitHub emojis
#https://raw.githubusercontent.com/omnidan/node-emoji/master/lib/emoji.json

st.set_page_config(page_title = "HW4 Leo Cheung", page_icon = ":ocean:")

#step 1: make a title
st.title("Math :keycap_ten: Homework 4")

#step 2: write name, ID, and GitHub link
st.markdown("Author: Leo Cheung, [GitHub link](https://github.com/ctZN4)")

u_input = st.text_input('Please input your name')

if u_input == "":
    st.stop()
else:
    st.success(f":heavy_check_mark: Hello and welcome, {u_input}!")


    #function that tests if a column in a DataFrame can be numeric
    def can_be_numeric(df,c):
        try:
            pd.to_numeric(df[c])
            return True
        except ValueError:
            return False

    try:
        #step 3: upload window for a CSV file
        filename = st.file_uploader(label = "Please upload a CSV file here", type = "csv")
        if "fn" not in st.session_state:
            st.session_state["fn"] = filename
        #else:
            #filename = st.session_state["fn"]

        #stops the rest from running if file is not uploaded
        if filename == None:
            raise FileNotFoundError()
        
        

        #step 4: read the CSV input
        df = pd.read_csv(filename)
        st.write(f"Here's the data from {filename.name}")
        st.dataframe(df)
        
        #step 5: change every single empty one-space string into NaN
        df1 = df.applymap(lambda x: np.nan if type(x) == str and x == " " else x)
        # same as df = df.replace(" ", np.nan)
        
        #st.write("Here's the modified DataFrame")
        #st.dataframe(df1)
        #st.write(f"Shapes of df: {df.shape}, df1: {df1.shape}")

        #step 6: lists the number columns in df1
        num_cols = [c for c in df1.columns if can_be_numeric(df1, c)]

        #step 7: changes the number columns from strings into actual numeric forms
        df1[num_cols] = df1[num_cols].apply(pd.to_numeric, axis = 0)

        #step 8: selection boxes for the x and y axes, defaults to "Index" (first column)
        choiceX = st.selectbox(label = "Choose the x-axis for the plot", options = num_cols)
        choiceY = st.selectbox(label = "Choose the y-axis for the plot", options = num_cols)

        #step 9: slider for choosing the range of x axis, defaults to 100
        choiceRange = st.slider(label = "Choose the range for the plot", min_value = 0, max_value = len(df1) - 1, value = (0, len(df1)))

        #step 10: prints out the user's choice
        st.write(f"You have chosen {choiceX} as the x-axis, {choiceY} as the y-axis, and {choiceRange} as the maximum row.")

        #step 11: chart out the plot, then display in streamlit
        charted = alt.Chart(df1[choiceRange[0]:choiceRange[1]]).mark_circle().encode(
            x = alt.X(choiceX, scale=alt.Scale(zero=False)),
            y = alt.Y(choiceY, scale=alt.Scale(zero=False)),
            color = alt.Color(choiceX, scale = alt.Scale(scheme = "greenblue")),
        ).properties(
            width = 800,
            height = 400
        )
        st.altair_chart(charted, use_container_width=True)

        #genre = st.radio("What's your favorite movie genre",('Comedy', 'Drama', 'Documentary'))
        #cursed, gives out all row indices from df1
        #df_choice = st.radio("Choose from df1", options = df1)

        #num = st.number_input("test num")
    except FileNotFoundError:
        st.write("The file is not found, please try uploading a CSV file.")
    except ValueError:
        st.write("There is a Value Error")
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:  \n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        st.write(message)
    finally:
        st.stop()



