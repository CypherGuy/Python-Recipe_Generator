#!/bin/bash
nginx -t &&
service nginx start &&
streamlit run project_contents/app/home.py