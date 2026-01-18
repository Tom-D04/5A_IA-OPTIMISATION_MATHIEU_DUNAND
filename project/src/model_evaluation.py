import os
import sys
import warnings
warnings.filterwarnings("ignore")

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import seaborn as sns
from analyze_music import analyze_music, GENRES
from eval_dataset import DATASET, SAMPLES_DIR

def evaluate(dataset=DATASET, samples_dir=SAMPLES_DIR):
    """Évalue le modèle sur le dataset de test"""
    
    y_true = []
    y_pred = []
    
    subgenre_correct = 0
    subgenre_total = 0
    
    instrument_correct = 0
    instrument_total = 0
    
    global_correct = 0  # Genre OU sous-genre correct
   
    for item in dataset:
        filepath = os.path.join(samples_dir, item["file"])
        
        if not os.path.exists(filepath):
            print(f"\n!MANQUANT! {item['file']}")
            continue
        results = analyze_music(filepath)
        
        # Genre prédit
        if results['genres_detected']:
            sorted_genres = sorted(results['genres_detected'].items(), key=lambda x: x[1], reverse=True)
            predicted_genre = sorted_genres[0][0]
        else:
            predicted_genre = "unknown"
            
        y_true.append(item["genre"])
        y_pred.append(predicted_genre)
        
        # Sous-genres
        detected_subgenres = results['sous_genres']
        subgenre_match = any(sg in detected_subgenres for sg in item["subgenres"])
        subgenre_correct += 1 if subgenre_match else 0
        subgenre_total += 1

        # Instruments
        detected_instruments = results['instruments']
        instrument_match = any(inst in detected_instruments for inst in item["instruments"])
        instrument_correct += 1 if instrument_match else 0
        instrument_total += 1
        
        # Global: genre correct OU au moins 1 sous-genre correct
        genre_match = (predicted_genre == item["genre"])
        if genre_match or subgenre_match:
            global_correct += 1

    if len(y_true) == 0:
        print("\nAucun fichier analysé.")
        return None
    
    total = len(y_true)
    
    # Accuracy genre principal
    correct_count = sum(1 for t, p in zip(y_true, y_pred) if t == p)
    genre_accuracy = correct_count / total
    
    # Global Accuracy (genre OU sous-genre correct)
    global_accuracy = global_correct / total

    # Précision et Recall en moyenne pour les différents genres
    labels = list(set(y_true))
    precision_list = []
    recall_list = []
    
    for genre in labels:
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == genre and p == genre)
        fp = sum(1 for t, p in zip(y_true, y_pred) if t != genre and p == genre)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t == genre and p != genre)
        
        precision_list.append(tp / (tp + fp) if (tp + fp) > 0 else 0)
        recall_list.append(tp / (tp + fn) if (tp + fn) > 0 else 0)
    
    avg_precision = sum(precision_list) / len(precision_list)
    avg_recall = sum(recall_list) / len(recall_list)

    print(f"\nGenre")
    print(f"\tAccuracy: {genre_accuracy:.1%} ({correct_count}/{total})")
    print(f"\tPrécision: {avg_precision:.1%}")
    print(f"\tRecall: {avg_recall:.1%}")

    # Sous-genres
    subgenre_accuracy = subgenre_correct / subgenre_total
    print(f"\nAccuracy détection sous-genres (au moins 1 détecté) : {subgenre_accuracy:.1%} ({subgenre_correct}/{subgenre_total})")

    # Instruments
    instrument_accuracy = instrument_correct / instrument_total
    print(f"\nAccuracy détection instruments (au moins 1 détecté) : {instrument_accuracy:.1%} ({instrument_correct}/{instrument_total})")

    # Global Accuracy
    print(f"\nGlobal Accuracy (genre OU sous-genre correct): {global_accuracy:.1%} ({global_correct}/{total})")

    # Matrice de confusion avec seaborn
    plot_confusion_matrix(y_true, y_pred, labels)
    
    return {
        'genre_accuracy': genre_accuracy,
        'global_accuracy': global_accuracy,
        'subgenre_accuracy': subgenre_accuracy,
        'instrument_accuracy': instrument_accuracy
    }


def plot_confusion_matrix(y_true, y_pred, labels):
    """Affiche la matrice de confusion avec seaborn"""
    
    # Construction de la matrice
    n = len(labels)
    matrix = [[0] * n for _ in range(n)]
    
    for t, p in zip(y_true, y_pred):
        if t in labels and p in labels:
            i = labels.index(t)
            j = labels.index(p)
            matrix[i][j] += 1
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(matrix, annot=True, fmt='d', cmap='Blues',
                xticklabels=labels, yticklabels=labels)
    plt.xlabel('Prédit')
    plt.ylabel('Réel')
    plt.title('Matrice de Confusion de Classification de Genre')
    plt.tight_layout()
    plt.savefig('project/evaluation_results/confusion_matrix.png', dpi=150)
    plt.show()


if __name__ == "__main__":
    if not os.path.exists(SAMPLES_DIR):
        os.makedirs(SAMPLES_DIR)
        print(f"Dossier créé: {SAMPLES_DIR}")
        print(f"\nPlacer les fichiers audio dans ce dossier")
    else:
        results = evaluate()
        
        if results:
            print(f"\nRésultats :")
            print(f"\tAccuracy Genre Principal: {results['genre_accuracy']:.1%}")
            print(f"\tAccuracy Sous-genres: {results['subgenre_accuracy']:.1%}")
            print(f"\tGlobal Accuracy (genre OU un des sous-genres correct): {results['global_accuracy']:.1%}")
            print(f"\tAccuracy Instruments: {results['instrument_accuracy']:.1%}")