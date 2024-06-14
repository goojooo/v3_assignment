import pandas as pd
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import UploadedFile

from django.shortcuts import render, redirect


def home(request):
    return redirect('upload_file')


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            return redirect('analyze_file', pk=uploaded_file.pk)
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def analyze_file(request, pk):
    file_obj = UploadedFile.objects.get(pk=pk)
    df = pd.read_csv(file_obj.file.path)

    # Perform data analysis with pandas and numpy
    sample = df.head().to_html()
    summary = df.describe().to_html()
    # Create a simple visualization
    import matplotlib.pyplot as plt
    import seaborn as sns
    import io
    import base64

    sns_plot = sns.pairplot(df)
    img = io.BytesIO()
    sns_plot.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render(request, 'analyze.html', {
        'summary': summary,
        'sample': sample,
        'plot_url': plot_url
    })
