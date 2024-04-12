# pages/views.py

import pandas as pd
from django.http import HttpResponseRedirect
from pycaret.classification import load_model, predict_model


def homePageView(request):
    # If no specific context is needed, you can simply render the template without a context dictionary
    return render(request, 'home.html')


from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages  # To handle error messages


def homePost(request):
    if request.method == 'POST':
        try:
            clump_thickness = int(request.POST.get('clump_thickness', -1))  # Default to -1 for error handling
            bland_chromatin = int(request.POST.get('bland_chromatin', -1))
            marginal_adhesion = int(request.POST.get('marginal_adhesion', -1))
            bare_nuclei = int(request.POST.get('bare_nuclei', -1))
            single_epithelial_cell_size = int(request.POST.get('single_epithelial_cell_size', -1))

            # Assume zeros are allowed except for 'Bare Nuclei'
            if bare_nuclei <= 0:
                raise ValueError("Bare Nuclei must be greater than zero. Zero or negative values are not allowed.")

            if any(value < 0 for value in [clump_thickness, bland_chromatin, marginal_adhesion, single_epithelial_cell_size]):
                raise ValueError("Negative values are not allowed. All values must be zero or positive.")

        except ValueError as e:
            messages.error(request, f"Invalid input: {e}")
            return render(request, 'home.html')

        return HttpResponseRedirect(reverse('results', kwargs={
            'clump_thickness': clump_thickness,
            'bland_chromatin': bland_chromatin,
            'marginal_adhesion': marginal_adhesion,
            'bare_nuclei': bare_nuclei,
            'single_epithelial_cell_size': single_epithelial_cell_size,
        }))

    return redirect('home')



def results(request, clump_thickness, bland_chromatin, marginal_adhesion, bare_nuclei, single_epithelial_cell_size):
    print("*** Inside results()")

    # Load saved model using PyCaret's load_model
    try:
        loaded_model = load_model('C:/comp4949-pipeline')
        print("Model loaded successfully.")
    except Exception as e:
        error_message = f"An error occurred while loading the model: {str(e)}"
        print(error_message)
        return render(request, 'results.html', {
            'clump_thickness': clump_thickness,
            'bland_chromatin': bland_chromatin,
            'marginal_adhesion': marginal_adhesion,
            'bare_nuclei': bare_nuclei,
            'single_epithelial_cell_size': single_epithelial_cell_size,
            'prediction': error_message
        })

    # Create a DataFrame for the input data
    input_df = pd.DataFrame({
        'Clump Thickness': [clump_thickness],
        'Bland Chromatin': [bland_chromatin],
        'Marginal Adhesion': [marginal_adhesion],
        'Bare Nuclei': [bare_nuclei],
        'Single Epithelial Cell Size': [single_epithelial_cell_size]
    })

    # Predict using the loaded model
    try:
        predictions = predict_model(loaded_model, data=input_df)
        # Retrieve the numerical prediction label
        numeric_prediction = predictions['prediction_label'][0]
        # Map the numerical prediction to a more readable form
        prediction_result = "Malignant" if numeric_prediction == 1 else "Benign"
        print("Prediction successful:", prediction_result)
    except Exception as e:
        error_message = f"An error occurred during prediction: {str(e)}"
        print(error_message)
        prediction_result = error_message

    # Return results to the user through the results.html template
    return render(request, 'results.html', {
        'clump_thickness': clump_thickness,
        'bland_chromatin': bland_chromatin,
        'marginal_adhesion': marginal_adhesion,
        'bare_nuclei': bare_nuclei,
        'single_epithelial_cell_size': single_epithelial_cell_size,
        'prediction': prediction_result
    })

