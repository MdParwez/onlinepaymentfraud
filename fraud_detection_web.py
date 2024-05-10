# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 11:58:21 2024

@author: tejas
"""

import streamlit as st
import numpy as np
import pickle
import os
from PIL import Image
import sklearn




# Set page configuration
st.set_page_config(
    page_title="Fraud Prediction App",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
    
)



# Get the current directory of the Streamlit script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the file paths for the model files
rf_model_path = os.path.join(current_dir, "RF_model.sav")
knn_model_path = os.path.join(current_dir, "KNN_model.sav")

# Load models
loaded_rf_model = pickle.load(open(rf_model_path, 'rb'))
loaded_knn_model = pickle.load(open(knn_model_path, 'rb'))

st.sidebar.image(r"IMAGES/payment_fraud.jpg",use_column_width=True)

# Define introduction function
def intro():
    image = Image.open(r"IMAGES/image.jpg")
    st.image(image, use_column_width=True)
    st.title('Online Payments Fraud Detection')
    st.write('Welcome to the Online Payments Fraud Detection app! This app empowers you with real-time protection against credit card fraud. Our advanced algorithms analyze every transaction, identifying suspicious activity before it impacts your finances. Experience peace of mind knowing Fraud Fortress stands guard 24/7, safeguarding your hard-earned money.')
    st.markdown('The dataset used in this app contains the following columns:')
    st.markdown('* step: Represents a unit of time where 1 step equals 1 hour.')
    st.markdown('* type: Type of online transaction.')
    st.markdown('* amount: The amount of the transaction.')
    st.markdown('* nameOrig: Customer starting the transaction.')
    st.markdown('* oldbalanceOrg: Balance before the transaction.')
    st.markdown('* newbalanceOrig: Balance after the transaction.')
    st.markdown('* nameDest: Recipient of the transaction.')
    st.markdown('* oldbalanceDest: Initial balance of recipient before the transaction.')
    st.markdown('* newbalanceDest: The new balance of recipient after the transaction.')
    st.markdown('* isFlaggedFraud: Transaction has been marked potentially fraudulent by the system')
    st.markdown('* isFraud: Indicates whether the transaction is fraudulent (1) or not (0).')

# Prediction function
def predict(model, data):
    input_data_as_numpy_array = np.asarray(data).reshape(1, -1)
    prediction = model.predict(input_data_as_numpy_array)
    return prediction[0]

# Data Plots page
def data_plots():
    # Add a dropdown to select the plot
    plot_selection = st.selectbox('Select Plot', ['Correlation Matrix', 'Fraud vs. Flagged Fraud', 'Fraudulent Transactions by Type', 'Transaction Types'])

    # Display the selected plot
    if plot_selection == 'Correlation Matrix':
        st.image(r"IMAGES/confusion_matrix.png")
    elif plot_selection == 'Fraud vs. Flagged Fraud':
        st.image(r"IMAGES/fraud_flagged_counts.png")
    elif plot_selection == 'Fraudulent Transactions by Type':
        st.image(r"IMAGES/fraud_transactiontype.png")
    elif plot_selection == 'Transaction Types':
        st.image(r"IMAGES/transaction_types.png")

# Prediction page
def Prediction():
    # Feature input
   # Model selection
    model_choice = st.sidebar.radio("Select Model:", ("Random Forest", "KNN"))
    
    # Center feature input
    col1, col2, col3 = st.columns([1, 5, 1])
    
    with col2:
        st.header("Enter Transaction Details")
        step = st.number_input("Step (Hour of the day)", min_value=1, max_value=744)
        type = st.selectbox("Transaction Type", ["TRANSFER", "CASH_OUT"])
        amount = st.number_input("Amount ($)", min_value=0.0)
        oldbalanceOrg = st.number_input("Old Balance Origin", min_value=0.0)
        newbalanceOrig = st.number_input("New Balance After", min_value=0.0)
        oldbalanceDest = st.number_input("Old Balance Destination", min_value=0.0)
        newbalanceDest = st.number_input("New Balance Destination", min_value=0.0)
        isFlaggedFraud = st.selectbox("Is Flagged Fraud?", [0, 1])
        predict_button = st.button("Predict")
        
        if predict_button:
            # Binary encode transaction type
            type_encoded = 0 if type == "TRANSFER" else 1
            
            # Combine all features
            input_data = [step, type_encoded, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest, isFlaggedFraud]

            if model_choice == "Random Forest":
                prediction = predict(loaded_rf_model, input_data)  # Using RF model for prediction
            elif model_choice == "KNN":
                prediction = predict(loaded_knn_model, input_data)  # Using KNN model for prediction

            if prediction == 0:
                st.success("The transaction seems legitimate.")
                st.image(r"IMAGES/legit_tran.png", width=300,use_column_width=True, output_format='auto')
            else:
                st.error("The transaction is flagged as potentially fraudulent.")
                st.image(r"IMAGES/fraud_tran_icon.jpg", width=300,use_column_width=True, output_format='auto')
# Main app
def main():
    pages = {
        "Home": intro,
        "Models": Prediction,
        "Data Visualization": data_plots
    }

    st.sidebar.title('NAVIGATION BAR')
    selection = st.sidebar.radio(" ", list(pages.keys()))

    page = pages[selection]
    page()

if __name__ == "__main__":
    main()
