import streamlit as st
import validators
import numpy as np
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import findWordCount
import DataScraper

# Streamlit app layout
st.title("SEO Tracker and Analyzer Tool")

theme_color = '#03c6fc'

# Input box for URL
url = st.text_input("Enter the URL to analyze:", "https://www.mkbhd.com")

# Checkboxes for selecting algorithms
selected_algorithms = st.multiselect("Select the algorithms to run:", ["naiveStringMatching", "kmpAlgorithm", "rabinKarp", "suffixArray", "suffixTree"])


try:
    # Button to start analysis
    if st.button("Analyze"):

        if not validators.url(url):
            st.error("Please enter a valid URL!")
            
        scrapped_data = DataScraper.getWepageData(url)
        wordCount, process_time = findWordCount.getProcessTimeAndWordCount(scrapped_data, selected_algorithms)
        response = {"data" : wordCount, "process_time": process_time }

        # Check if the request was successful
        if response:
            # Display the results
            results = response
            word_freq = results["data"]


            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Words", "Word Cloud", "Top 10 Words", "Processing Times", "Scatter Plot", "Word Length Distribution"])

            with tab2:
                # Word Cloud
                def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
                    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
                    return np.random.choice(colors)

                wordcloud = WordCloud(width=800, height=500, background_color='black', color_func=color_func).generate_from_frequencies(word_freq)

                plt.figure(figsize=(10, 5))
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis('off')
                st.pyplot(plt)

            with tab3:
                # Bar Chart for Top 10 Words
                st.subheader("Top 10 Words")
                top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
                top_words_df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
                bar_chart = px.bar(top_words_df, x='Word', y='Frequency', color='Frequency')
                bar_chart.update_layout(
                                        xaxis=dict(gridcolor='white', linecolor='white', linewidth=2),
                                        yaxis=dict(gridcolor='white', linecolor='white', linewidth=2)
                                    )
                bar_chart.update_traces(marker_color=theme_color,  hovertemplate='<b>%{x}</b><br>Frequency: %{y}<extra></extra>')
                
                st.plotly_chart(bar_chart)

            with tab4:
                # Line Chart for Processing Times
                st.subheader("Processing Times")
                process_times = results["process_time"]
                process_times_df = pd.DataFrame(list(process_times.items()), columns=['Algorithm', 'Time'])
                line_chart = px.line(process_times_df, x='Algorithm', y='Time', markers=True)
                line_chart.update_layout(
                                                xaxis=dict(gridcolor='white', linecolor='white', linewidth=2),
                                                yaxis=dict(gridcolor='white', linecolor='white', linewidth=2)
                                            )
                line_chart.update_traces(line_color=theme_color, marker_color=theme_color)
                                                        
                st.plotly_chart(line_chart)

            with tab5:
                # Scatter Plot
                st.subheader("Word Frequency Scatter Plot")
                scatter_df = pd.DataFrame(list(word_freq.items()), columns=['Word', 'Frequency'])
                scatter_chart = px.scatter(scatter_df, x='Word', y='Frequency', size='Frequency', color='Frequency')
                scatter_chart.update_traces(marker=dict(color=theme_color, line=dict(color='white', width=1.5)), 
                                            hovertemplate='<b>%{x}</b><br>Frequency: %{y}<extra></extra>')
                scatter_chart.update_layout(xaxis=dict(gridcolor='white', linecolor='white', linewidth=2), yaxis=dict(gridcolor='white', linecolor='white', linewidth=2))
                st.plotly_chart(scatter_chart)
            
            with tab1:
                # Table of All Words
                st.subheader("All Words Table")
                all_words_df = pd.DataFrame(list(word_freq.items()), columns=['Word', 'Frequency']).sort_values(by='Frequency', ascending=False)
                all_words_df.reset_index(drop=True, inplace=True)
                st.dataframe(all_words_df, height=400)  # Set the height of the scrollable area
                # Custom CSS to set the width of the columns
                st.markdown("""
                    <style>
                        .dataframe th, .dataframe td {
                            width: 1000px !important;
                        }
                    </style>
                    """, unsafe_allow_html=True)
            
            with tab6:
                # Word Length Distribution (Line Chart)
                st.subheader("Word Length Distribution")
                word_lengths = [len(word) for word in word_freq.keys()]
                word_lengths_df = pd.DataFrame(word_lengths, columns=['Word Length'])
                word_length_counts = word_lengths_df['Word Length'].value_counts().sort_index()
                line_chart = px.line(x=word_length_counts.index, y=word_length_counts.values)
                line_chart.update_layout(
                    xaxis=dict(gridcolor='lightgray', linecolor='white', linewidth=2),
                    yaxis=dict(gridcolor='lightgray', linecolor='white', linewidth=2)
                )
                line_chart.update_traces(line_color=theme_color, marker_color=theme_color)
                st.plotly_chart(line_chart)

        else:
            # Display an error message
            st.error("Failed to analyze the URL. Please try again.")

except Exception as e:
    pass