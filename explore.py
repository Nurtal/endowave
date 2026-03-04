import numpy as np
import pandas as pd
import random
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

from compute_scats import scattering_transform_dataframe

# -----------------------------
# FITNESS FUNCTION
# -----------------------------
def compute_fitness(df, order, scat_file):

    # Réordonner colonnes (sauf LABEL)
    reordered = df[list(order) + ["LABEL"]]

    # Scattering
    scat_df = scattering_transform_dataframe(reordered, scat_file, J=3, Q=8)    
    
    X = scat_df.iloc[:, :-1]
    y = scat_df["LABEL"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, stratify=y
    )
    
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=200))
    ])
    
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    return accuracy_score(y_test, y_pred)


# -----------------------------
# GENETIC ALGORITHM
# -----------------------------
def genetic_algorithm(df, population_size=20, generations=10, mutation_rate=0.2):
    
    genes = list(df.columns[:-1])
    
    # Initial population
    population = [
        random.sample(genes, len(genes))
        for _ in range(population_size)
    ]
    
    for gen in range(generations):
        print(f"\nGeneration {gen}")
        
        # Evaluate fitness
        fitness_scores = [
            compute_fitness(df, individual, "data/toy/scat_explored.csv")
            for individual in population
        ]
        
        # Sort population by fitness
        sorted_pop = [
            x for _, x in sorted(
                zip(fitness_scores, population),
                key=lambda pair: pair[0],
                reverse=True
            )
        ]
        
        population = sorted_pop[:population_size // 2]  # selection
        
        print("Best accuracy:", max(fitness_scores))
        
        # Reproduction
        new_population = population.copy()
        
        while len(new_population) < population_size:
            parent = random.choice(population).copy()
            
            # Mutation (swap two genes)
            if random.random() < mutation_rate:
                i, j = random.sample(range(len(parent)), 2)
                parent[i], parent[j] = parent[j], parent[i]
            
            new_population.append(parent)
        
        population = new_population
    
    return population[0]









if __name__ == "__main__":

    df = pd.read_csv("data/toy/test_shuffled.csv")

    best_order = genetic_algorithm(df)
    print("Best ordering:", best_order)
    
