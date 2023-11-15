import random

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix


def calcconfusion(predicted, reality):
    """
    TODO: BESCHRIJVING

    Creates a confusion matrix with given values.

    args:
    - predicted
    - reality

    result:
    """
    cm = confusion_matrix(reality, predicted)

    sns.heatmap(cm, annot=True, fmt='d', cmap='Reds', xticklabels=['Klasse 0', 'Klasse 1', 'Klasse 2'], yticklabels=['Klasse 0', 'Klasse 1', 'Klasse 2'])
    plt.xlabel('Voorspelde waarden'), plt.ylabel('Ware waarden')
    plt.show()


def calcregression():
    """
    TODO: BESCHRIJVING
    """
    pass


if __name__ == "__main__":
    calcconfusion(random.choices(range(0, 3), k=100000), random.choices(range(0, 3), k=100000))
