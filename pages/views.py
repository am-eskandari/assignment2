# pages/views.py

import pandas as pd
from django.http import HttpResponseRedirect
from pycaret.classification import load_model, predict_model
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages


def homePageView(request):
    return render(request, 'home.html')


def homePost(request):
    if request.method == 'POST':
        try:
            uniformity_of_cell_size = int(request.POST.get('uniformity_of_cell_size', -1))
            uniformity_of_cell_shape = int(request.POST.get('uniformity_of_cell_shape', -1))
            bare_nuclei = int(request.POST.get('bare_nuclei', -1))
            bland_chromatin = int(request.POST.get('bland_chromatin', -1))
            normal_nucleoli = int(request.POST.get('normal_nucleoli', -1))
            clump_thickness = int(request.POST.get('clump_thickness', -1))

            # Perform error checking
            if any(value < 0 for value in
                   [uniformity_of_cell_size, uniformity_of_cell_shape, bare_nuclei, bland_chromatin, normal_nucleoli,
                    clump_thickness]):
                raise ValueError("All values must be zero or positive.")

        except ValueError as e:
            messages.error(request, f"Invalid input: {e}")
            return render(request, 'home.html')

        return HttpResponseRedirect(reverse('results', kwargs={
            'uniformity_of_cell_size': uniformity_of_cell_size,
            'uniformity_of_cell_shape': uniformity_of_cell_shape,
            'bare_nuclei': bare_nuclei,
            'bland_chromatin': bland_chromatin,
            'normal_nucleoli': normal_nucleoli,
            'clump_thickness': clump_thickness
        }))

    return redirect('home')


def results(request, uniformity_of_cell_size, uniformity_of_cell_shape, bare_nuclei, bland_chromatin, normal_nucleoli,
            clump_thickness):
    print("*** Inside results()")

    # Load saved model using PyCaret's load_model
    try:
        loaded_model = load_model('C:/comp4949-pipeline-rf')
        print("Model loaded successfully.")
    except Exception as e:
        error_message = f"An error occurred while loading the model: {str(e)}"
        print(error_message)
        return render(request, 'results.html', {
            'uniformity_of_cell_size': uniformity_of_cell_size,
            'uniformity_of_cell_shape': uniformity_of_cell_shape,
            'bare_nuclei': bare_nuclei,
            'bland_chromatin': bland_chromatin,
            'normal_nucleoli': normal_nucleoli,
            'clump_thickness': clump_thickness,
            'prediction': error_message
        })

    # Create a DataFrame for the input data with the updated variables
    input_df = pd.DataFrame({
        'Uniformity of Cell Size': [uniformity_of_cell_size],
        'Uniformity of Cell Shape': [uniformity_of_cell_shape],
        'Bare Nuclei': [bare_nuclei],
        'Bland Chromatin': [bland_chromatin],
        'Normal Nucleoli': [normal_nucleoli],
        'Clump Thickness': [clump_thickness]
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
        'uniformity_of_cell_size': uniformity_of_cell_size,
        'uniformity_of_cell_shape': uniformity_of_cell_shape,
        'bare_nuclei': bare_nuclei,
        'bland_chromatin': bland_chromatin,
        'normal_nucleoli': normal_nucleoli,
        'clump_thickness': clump_thickness,
        'prediction': prediction_result
    })
