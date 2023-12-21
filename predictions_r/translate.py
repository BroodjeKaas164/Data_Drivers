def train_models():
    models = ['glm', 'parRF', 'rf']
    listModels = []
    for model in models:
        listModels.append(f'model_{model}')
    print(listModels)

train_models()