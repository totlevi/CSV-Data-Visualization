from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)


def generate_line_chart(data):
    plt.figure(figsize=(10, 6))
    for column in data.columns:
        plt.plot(data.index, data[column], marker='o', label=column)
    plt.title('Line Chart')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()
    plt.grid(True)
    # Save chart to bytes buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    # Encode bytes to base64 string
    image_png = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    return image_png


def generate_bar_chart(data):
    plt.figure(figsize=(10, 6))
    num_columns = len(data.columns)
    bar_width = 0.35
    index = data.index
    # make bars visible
    for i, column in enumerate(data.columns):
        plt.bar(index + i * bar_width, data[column], bar_width, label=column)
    plt.title('Bar Chart')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()
    plt.grid(True)
    # Save chart to bytes buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    # Encode bytes to base64 string
    image_png = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    return image_png


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/visualize', methods=['POST'])
def visualize():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            df = pd.read_csv(file)
            # display a part of the dataframe
            data_preview = df.head()

            # data analysis
            descriptive_stats = df.describe().to_html()

            # choose chart
            chart_type = request.form.get('chart_type')
            if chart_type == 'line':
                chart_image = generate_line_chart(data_preview)
            elif chart_type == 'bar':
                chart_image = generate_bar_chart(data_preview)
            else:
                chart_image = None

            return render_template('visualize.html', data_preview=data_preview.to_html(), chart_image=chart_image,
                                   descriptive_stats=descriptive_stats)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
