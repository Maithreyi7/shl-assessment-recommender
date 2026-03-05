# shl-assessment-recommender
Hiring managers and recruiters often struggle to find the right assessments for the roles that they are hiring for. The current system relies on keyword searches and filters, making the process time-consuming and inefficient. This is an intelligent recommendation system that simplifies this process.

# SHL Assessment Recommendation Engine

## Overview
This project implements a keyword-based recommendation engine that suggests relevant SHL assessments based on:

- Job Role
- Job Level
- Language Preference

The system ranks results using a weighted scoring mechanism and displays the top matches in a professional UI built with Streamlit.

## Features

- Relevance scoring system
- Ranked recommendations (Top Match / Strong Match / Match)
- Clean corporate UI
- Explanation for each recommendation
- Fully deployable web application

## Scoring Logic

- Job Role Match → 2 points
- Job Level Match → 1 point
- Language Match → 1 point

Results are sorted by highest relevance score.

## Tech Stack

- Python
- Streamlit
- Pandas

## Deployment

Live App:  
https://your-app-url.streamlit.app

GitHub Repository:  
https://github.com/yourusername/shl-assessment-recommender

## Future Enhancements

- NLP-based semantic matching
- API-based recommendation endpoint
- Analytics dashboard
- Database integration

---

Developed as part of SHL Research Engineer Assessment.~Maithreyi Adluri
