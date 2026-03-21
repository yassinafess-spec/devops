from flask import Flask, jsonify, request, render_template
from datetime import datetime
import random
import uuid
import os
import socket
from functools import wraps

app = Flask(__name__)

# Base de données en mémoire
quizzes = {}
scores = {}

# Questions multi-catégories
questions_db = [
    # ============ INFORMATIQUE ============
    {
        "id": 1,
        "category": "Informatique",
        "subcategory": "Programmation",
        "question": "Quelle est la différence entre Git et GitHub ?",
        "options": [
            "Git est un outil, GitHub est une plateforme",
            "Git est de Microsoft, GitHub est de Google",
            "C'est la même chose",
            "Git est plus ancien"
        ],
        "correct": 0,
        "difficulty": "medium",
        "points": 20
    },
    {
        "id": 2,
        "category": "Informatique",
        "subcategory": "Systèmes",
        "question": "Que signifie 'RAM' ?",
        "options": [
            "Random Access Memory",
            "Readily Available Memory",
            "Rapid Action Module",
            "Random Allocation Memory"
        ],
        "correct": 0,
        "difficulty": "easy",
        "points": 10
    },
    
    # ============ HISTOIRE ============
    {
        "id": 3,
        "category": "Histoire",
        "subcategory": "Générale",
        "question": "En quelle année a débuté la Révolution Française ?",
        "options": ["1789", "1776", "1799", "1804"],
        "correct": 0,
        "difficulty": "easy",
        "points": 10
    },
    {
        "id": 4,
        "category": "Histoire",
        "subcategory": "Mondiale",
        "question": "Qui a peint la Joconde ?",
        "options": [
            "Léonard de Vinci",
            "Michel-Ange",
            "Raphaël",
            "Van Gogh"
        ],
        "correct": 0,
        "difficulty": "easy",
        "points": 10
    },
    {
        "id": 5,
        "category": "Histoire",
        "subcategory": "Antiquité",
        "question": "Quelle civilisation a construit le Machu Picchu ?",
        "options": [
            "Les Incas",
            "Les Mayas",
            "Les Aztèques",
            "Les Olmèques"
        ],
        "correct": 0,
        "difficulty": "medium",
        "points": 20
    },
    
    # ============ GÉOGRAPHIE ============
    {
        "id": 6,
        "category": "Géographie",
        "subcategory": "Capitales",
        "question": "Quelle est la capitale du Japon ?",
        "options": ["Tokyo", "Kyoto", "Osaka", "Nagoya"],
        "correct": 0,
        "difficulty": "easy",
        "points": 10
    },
    {
        "id": 7,
        "category": "Géographie",
        "subcategory": "Pays",
        "question": "Quel est le plus grand pays du monde ?",
        "options": [
            "Russie",
            "Canada",
            "Chine",
            "États-Unis"
        ],
        "correct": 0,
        "difficulty": "easy",
        "points": 10
    },
    {
        "id": 8,
        "category": "Géographie",
        "subcategory": "Océans",
        "question": "Quel est l'océan le plus profond ?",
        "options": [
            "Océan Pacifique",
            "Océan Atlantique",
            "Océan Indien",
            "Océan Arctique"
        ],
        "correct": 0,
        "difficulty": "medium",
        "points": 20
    },
    
    # ============ SCIENCE ============
    {
        "id": 9,
        "category": "Science",
        "subcategory": "Physique",
        "question": "Quelle est la formule de l'énergie cinétique ?",
        "options": [
            "E = 1/2 mv²",
            "E = mc²",
            "E = mgh",
            "E = F × d"
        ],
        "correct": 0,
        "difficulty": "hard",
        "points": 30
    },
    {
        "id": 10,
        "category": "Science",
        "subcategory": "Biologie",
        "question": "Quel organe est responsable de la pompe du sang ?",
        "options": ["Le cœur", "Les poumons", "Le cerveau", "Le foie"],
        "correct": 0,
        "difficulty": "easy",
        "points": 10
    },
    {
        "id": 11,
        "category": "Science",
        "subcategory": "Chimie",
        "question": "Quel est le symbole chimique de l'or ?",
        "options": ["Au", "Ag", "Fe", "Cu"],
        "correct": 0,
        "difficulty": "medium",
        "points": 20
    },
    
    # ============ SPORT ============
    {
        "id": 12,
        "category": "Sport",
        "subcategory": "Football",
        "question": "Qui a remporté la Coupe du Monde 2018 ?",
        "options": ["France", "Croatie", "Belgique", "Angleterre"],
        "correct": 0,
        "difficulty": "easy",
        "points": 10
    },
    {
        "id": 13,
        "category": "Sport",
        "subcategory": "Basketball",
        "question": "Combien de points vaut un panier à 3 points ?",
        "options": ["3", "2", "1", "4"],
        "correct": 0,
        "difficulty": "easy",
        "points": 10
    },
    {
        "id": 14,
        "category": "Sport",
        "subcategory": "Tennis",
        "question": "Quel joueur a le plus de Grand Chelems ?",
        "options": [
            "Novak Djokovic",
            "Roger Federer",
            "Rafael Nadal",
            "Pete Sampras"
        ],
        "correct": 0,
        "difficulty": "medium",
        "points": 20
    },
    
    # ============ ART ============
    {
        "id": 15,
        "category": "Art",
        "subcategory": "Peinture",
        "question": "Quel mouvement artistique est représenté par Picasso ?",
        "options": [
            "Cubisme",
            "Surréalisme",
            "Impressionnisme",
            "Renaissance"
        ],
        "correct": 0,
        "difficulty": "medium",
        "points": 20
    },
    {
        "id": 16,
        "category": "Art",
        "subcategory": "Musique",
        "question": "Qui a composé la 9ème symphonie ?",
        "options": [
            "Beethoven",
            "Mozart",
            "Bach",
            "Chopin"
        ],
        "correct": 0,
        "difficulty": "medium",
        "points": 20
    },
    
    # ============ CINÉMA ============
    {
        "id": 17,
        "category": "Cinéma",
        "subcategory": "Oscars",
        "question": "Quel film a remporté le plus d'Oscars ?",
        "options": [
            "Titanic",
            "Le Seigneur des Anneaux",
            "Ben Hur",
            "Avatar"
        ],
        "correct": 1,
        "difficulty": "hard",
        "points": 30
    },
    {
        "id": 18,
        "category": "Cinéma",
        "subcategory": "Acteurs",
        "question": "Qui incarne Iron Man dans le MCU ?",
        "options": [
            "Robert Downey Jr.",
            "Chris Evans",
            "Chris Hemsworth",
            "Mark Ruffalo"
        ],
        "correct": 0,
        "difficulty": "easy",
        "points": 10
    },
    
    # ============ LITTÉRATURE ============
    {
        "id": 19,
        "category": "Littérature",
        "subcategory": "Classiques",
        "question": "Qui a écrit 'Les Misérables' ?",
        "options": [
            "Victor Hugo",
            "Alexandre Dumas",
            "Émile Zola",
            "Gustave Flaubert"
        ],
        "correct": 0,
        "difficulty": "easy",
        "points": 10
    },
    {
        "id": 20,
        "category": "Littérature",
        "subcategory": "Contemporaine",
        "question": "Quelle est la maison d'édition de Harry Potter ?",
        "options": [
            "Bloomsbury",
            "Gallimard",
            "Penguin",
            "HarperCollins"
        ],
        "correct": 0,
        "difficulty": "medium",
        "points": 20
    },
    
    # ============ MUSIQUE ============
    {
        "id": 21,
        "category": "Musique",
        "subcategory": "Rock",
        "question": "Quel groupe a chanté 'Bohemian Rhapsody' ?",
        "options": ["Queen", "The Beatles", "Led Zeppelin", "Pink Floyd"],
        "correct": 0,
        "difficulty": "easy",
        "points": 10
    },
    {
        "id": 22,
        "category": "Musique",
        "subcategory": "Pop",
        "question": "Qui est la 'Reine de la Pop' ?",
        "options": [
            "Madonna",
            "Beyoncé",
            "Taylor Swift",
            "Lady Gaga"
        ],
        "correct": 0,
        "difficulty": "medium",
        "points": 20
    },
    
    # ============ CUISINE ============
    {
        "id": 23,
        "category": "Cuisine",
        "subcategory": "Française",
        "question": "Quel est le plat national français ?",
        "options": [
            "Pot-au-feu",
            "Ratatouille",
            "Boeuf Bourguignon",
            "Quiche Lorraine"
        ],
        "correct": 1,
        "difficulty": "medium",
        "points": 20
    },
    {
        "id": 24,
        "category": "Cuisine",
        "subcategory": "Italienne",
        "question": "Dans quelle ville est née la pizza Margherita ?",
        "options": ["Naples", "Rome", "Milan", "Florence"],
        "correct": 0,
        "difficulty": "easy",
        "points": 10
    },
    
    # ============ NATURE ============
    {
        "id": 25,
        "category": "Nature",
        "subcategory": "Animaux",
        "question": "Quel est l'animal le plus rapide sur terre ?",
        "options": [
            "Guépard",
            "Lion",
            "Antilope",
            "Léopard"
        ],
        "correct": 0,
        "difficulty": "easy",
        "points": 10
    },
    {
        "id": 26,
        "category": "Nature",
        "subcategory": "Plantes",
        "question": "Quelle plante est symbole de l'amour ?",
        "options": ["Rose", "Tulipe", "Lys", "Marguerite"],
        "correct": 0,
        "difficulty": "easy",
        "points": 10
    },
    
    # ============ TECHNOLOGIE ============
    {
        "id": 27,
        "category": "Technologie",
        "subcategory": "IA",
        "question": "Que signifie 'GPT' dans ChatGPT ?",
        "options": [
            "Generative Pre-trained Transformer",
            "Global Processing Technology",
            "General Purpose Tool",
            "Graphical Programming Terminal"
        ],
        "correct": 0,
        "difficulty": "hard",
        "points": 30
    },
    {
        "id": 28,
        "category": "Technologie",
        "subcategory": "Smartphones",
        "question": "Quelle entreprise a créé le premier iPhone ?",
        "options": ["Apple", "Samsung", "Google", "Nokia"],
        "correct": 0,
        "difficulty": "easy",
        "points": 10
    },
    
    # ============ ÉCONOMIE ============
    {
        "id": 29,
        "category": "Économie",
        "subcategory": "Finance",
        "question": "Qu'est-ce que le Bitcoin ?",
        "options": [
            "Une cryptomonnaie",
            "Une banque",
            "Une action",
            "Un ETF"
        ],
        "correct": 0,
        "difficulty": "medium",
        "points": 20
    },
    {
        "id": 30,
        "category": "Économie",
        "subcategory": "Entreprises",
        "question": "Qui est le fondateur d'Amazon ?",
        "options": [
            "Jeff Bezos",
            "Elon Musk",
            "Bill Gates",
            "Mark Zuckerberg"
        ],
        "correct": 0,
        "difficulty": "easy",
        "points": 10
    },
    
    # ============ POLITIQUE ============
    {
        "id": 31,
        "category": "Politique",
        "subcategory": "Mondiale",
        "question": "Qui est le secrétaire général de l'ONU ?",
        "options": [
            "António Guterres",
            "Ban Ki-moon",
            "Kofi Annan",
            "Boutros Boutros-Ghali"
        ],
        "correct": 0,
        "difficulty": "hard",
        "points": 30
    },
    
    # ============ PHILOSOPHIE ============
    {
        "id": 32,
        "category": "Philosophie",
        "subcategory": "Antique",
        "question": "Qui a dit 'Je sais que je ne sais rien' ?",
        "options": ["Socrate", "Platon", "Aristote", "Descartes"],
        "correct": 0,
        "difficulty": "medium",
        "points": 20
    },
    
    # ============ MYTHOLOGIE ============
    {
        "id": 33,
        "category": "Mythologie",
        "subcategory": "Grecque",
        "question": "Qui est le roi des dieux grecs ?",
        "options": ["Zeus", "Poséidon", "Hadès", "Apollon"],
        "correct": 0,
        "difficulty": "easy",
        "points": 10
    },
    
    # ============ JEUX VIDÉO ============
    {
        "id": 34,
        "category": "Jeux Vidéo",
        "subcategory": "Console",
        "question": "Quelle est la console la plus vendue ?",
        "options": [
            "PlayStation 2",
            "Nintendo Switch",
            "PS4",
            "Game Boy"
        ],
        "correct": 0,
        "difficulty": "hard",
        "points": 30
    },
    
    # ============ ANIMAUX ============
    {
        "id": 35,
        "category": "Animaux",
        "subcategory": "Mammifères",
        "question": "Quel est l'animal terrestre le plus grand ?",
        "options": [
            "Éléphant d'Afrique",
            "Girafe",
            "Rhinocéros",
            "Hippopotame"
        ],
        "correct": 0,
        "difficulty": "easy",
        "points": 10
    }
]

# Catégories disponibles
CATEGORIES = {
    "Informatique": {"count": 2, "icon": "💻", "color": "#3498db"},
    "Histoire": {"count": 3, "icon": "📜", "color": "#e74c3c"},
    "Géographie": {"count": 3, "icon": "🌍", "color": "#2ecc71"},
    "Science": {"count": 3, "icon": "🔬", "color": "#9b59b6"},
    "Sport": {"count": 3, "icon": "⚽", "color": "#f39c12"},
    "Art": {"count": 2, "icon": "🎨", "color": "#e84393"},
    "Cinéma": {"count": 2, "icon": "🎬", "color": "#7f8c8d"},
    "Littérature": {"count": 2, "icon": "📚", "color": "#16a085"},
    "Musique": {"count": 2, "icon": "🎵", "color": "#d35400"},
    "Cuisine": {"count": 2, "icon": "🍳", "color": "#e67e22"},
    "Nature": {"count": 2, "icon": "🌿", "color": "#27ae60"},
    "Technologie": {"count": 2, "icon": "🤖", "color": "#2980b9"},
    "Économie": {"count": 2, "icon": "💰", "color": "#f1c40f"},
    "Politique": {"count": 1, "icon": "🏛️", "color": "#95a5a6"},
    "Philosophie": {"count": 1, "icon": "🧠", "color": "#8e44ad"},
    "Mythologie": {"count": 1, "icon": "⚡", "color": "#c0392b"},
    "Jeux Vidéo": {"count": 1, "icon": "🎮", "color": "#2c3e50"},
    "Animaux": {"count": 1, "icon": "🦒", "color": "#d35400"}
}

@app.route('/')
def home():
    """Page d'accueil HTML"""
    return render_template('index.html', categories=CATEGORIES)

@app.route('/api/health')
def health():
    """Health check pour Kubernetes"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "hostname": socket.gethostname(),
        "version": "3.0.0",
        "total_categories": len(CATEGORIES),
        "total_questions": len(questions_db)
    }), 200

@app.route('/api/info')
def info():
    """Informations sur l'API"""
    return jsonify({
        "name": "Quiz Game Général",
        "version": "3.0.0",
        "description": "Jeu de quiz avec 18 catégories différentes",
        "categories": [
            {
                "name": cat,
                "icon": info["icon"],
                "color": info["color"],
                "questions_count": info["count"]
            }
            for cat, info in CATEGORIES.items()
        ],
        "total_questions": len(questions_db),
        "difficulty_distribution": {
            "easy": len([q for q in questions_db if q['difficulty'] == 'easy']),
            "medium": len([q for q in questions_db if q['difficulty'] == 'medium']),
            "hard": len([q for q in questions_db if q['difficulty'] == 'hard'])
        }
    })

@app.route('/api/categories')
def get_categories():
    """Récupérer toutes les catégories avec statistiques"""
    categories_data = []
    for cat_name, cat_info in CATEGORIES.items():
        questions_in_cat = [q for q in questions_db if q['category'] == cat_name]
        categories_data.append({
            "name": cat_name,
            "icon": cat_info["icon"],
            "color": cat_info["color"],
            "count": len(questions_in_cat),
            "difficulties": {
                "easy": len([q for q in questions_in_cat if q['difficulty'] == 'easy']),
                "medium": len([q for q in questions_in_cat if q['difficulty'] == 'medium']),
                "hard": len([q for q in questions_in_cat if q['difficulty'] == 'hard'])
            }
        })
    return jsonify(categories_data)

@app.route('/api/questions', methods=['GET'])
def get_questions():
    """Récupérer toutes les questions"""
    category = request.args.get('category')
    difficulty = request.args.get('difficulty')
    
    filtered = questions_db
    
    if category:
        filtered = [q for q in filtered if q['category'] == category]
    
    if difficulty:
        filtered = [q for q in filtered if q['difficulty'] == difficulty]
    
    # Ne pas envoyer les réponses correctes
    safe_questions = []
    for q in filtered:
        q_copy = q.copy()
        del q_copy['correct']
        safe_questions.append(q_copy)
    
    return jsonify({
        "total": len(filtered),
        "questions": safe_questions
    })

@app.route('/api/questions/random', methods=['GET'])
def get_random_question():
    """Récupérer une question aléatoire"""
    category = request.args.get('category')
    difficulty = request.args.get('difficulty')
    
    filtered_questions = questions_db
    
    if category:
        filtered_questions = [q for q in filtered_questions if q['category'] == category]
    
    if difficulty:
        filtered_questions = [q for q in filtered_questions if q['difficulty'] == difficulty]
    
    if not filtered_questions:
        return jsonify({"error": "No questions found"}), 404
    
    question = random.choice(filtered_questions)
    # Ne pas envoyer la réponse correcte
    question_copy = question.copy()
    del question_copy['correct']
    
    return jsonify(question_copy)

@app.route('/api/quiz/start', methods=['POST'])
def start_quiz():
    """Démarrer un nouveau quiz"""
    data = request.get_json() or {}
    player_name = data.get('player_name', f"Player_{random.randint(1000, 9999)}")
    num_questions = min(data.get('num_questions', 10), len(questions_db))
    selected_categories = data.get('categories', [])
    
    # Sélectionner les questions
    available_questions = questions_db
    if selected_categories:
        available_questions = [q for q in available_questions if q['category'] in selected_categories]
    
    if len(available_questions) < num_questions:
        num_questions = len(available_questions)
    
    selected_questions = random.sample(available_questions, num_questions)
    
    # Créer une session de quiz
    session_id = str(uuid.uuid4())[:8]
    quizzes[session_id] = {
        "player_name": player_name,
        "questions": selected_questions,
        "current_index": 0,
        "answers": [],
        "score": 0,
        "start_time": datetime.now().isoformat(),
        "total_questions": num_questions,
        "categories": selected_categories
    }
    
    # Préparer la première question (sans la réponse)
    first_question = selected_questions[0].copy()
    del first_question['correct']
    
    return jsonify({
        "session_id": session_id,
        "player_name": player_name,
        "question": first_question,
        "question_number": 1,
        "total_questions": num_questions,
        "progress": f"1/{num_questions}",
        "categories": selected_categories
    })

@app.route('/api/quiz/answer', methods=['POST'])
def submit_answer():
    """Soumettre une réponse"""
    data = request.get_json()
    session_id = data.get('session_id')
    answer_index = data.get('answer_index')
    
    if session_id not in quizzes:
        return jsonify({"error": "Session not found"}), 404
    
    quiz = quizzes[session_id]
    current_question = quiz['questions'][quiz['current_index']]
    is_correct = (answer_index == current_question['correct'])
    
    # Points selon la difficulté
    points_map = {"easy": 10, "medium": 20, "hard": 30}
    points_earned = points_map.get(current_question['difficulty'], 10) if is_correct else 0
    
    # Enregistrer la réponse
    quiz['answers'].append({
        "question_id": current_question['id'],
        "category": current_question['category'],
        "subcategory": current_question['subcategory'],
        "question": current_question['question'],
        "user_answer": answer_index,
        "correct_answer": current_question['correct'],
        "is_correct": is_correct,
        "correct_text": current_question['options'][current_question['correct']],
        "points_earned": points_earned
    })
    
    if is_correct:
        quiz['score'] += points_earned
    
    # Passer à la question suivante
    quiz['current_index'] += 1
    is_finished = quiz['current_index'] >= quiz['total_questions']
    
    if is_finished:
        # Quiz terminé, sauvegarder le score
        end_time = datetime.now().isoformat()
        quiz['end_time'] = end_time
        max_possible = sum(
            {"easy": 10, "medium": 20, "hard": 30}.get(q['difficulty'], 10)
            for q in quiz['questions']
        )
        quiz['percentage'] = (quiz['score'] / max_possible) * 100 if max_possible > 0 else 0
        
        # Sauvegarder pour le leaderboard
        leaderboard_entry = {
            "player_name": quiz['player_name'],
            "score": quiz['score'],
            "total_questions": quiz['total_questions'],
            "percentage": quiz['percentage'],
            "date": end_time,
            "categories": quiz.get('categories', [])
        }
        
        if 'leaderboard' not in scores:
            scores['leaderboard'] = []
        scores['leaderboard'].append(leaderboard_entry)
        # Trier le leaderboard
        scores['leaderboard'] = sorted(scores['leaderboard'], 
                                      key=lambda x: x['score'], 
                                      reverse=True)[:20]
        
        # Statistiques par catégorie
        category_stats = {}
        for answer in quiz['answers']:
            cat = answer['category']
            if cat not in category_stats:
                category_stats[cat] = {"correct": 0, "total": 0}
            category_stats[cat]["total"] += 1
            if answer['is_correct']:
                category_stats[cat]["correct"] += 1
        
        return jsonify({
            "finished": True,
            "score": quiz['score'],
            "total_possible": max_possible,
            "percentage": quiz['percentage'],
            "answers": quiz['answers'],
            "category_stats": category_stats,
            "message": f"🎉 Félicitations {quiz['player_name']}! Score final: {quiz['score']} points sur {max_possible}",
            "ranking": f"Top {min(len(scores['leaderboard']), 20)}"
        })
    
    # Préparer la question suivante
    next_question = quiz['questions'][quiz['current_index']].copy()
    del next_question['correct']
    
    return jsonify({
        "finished": False,
        "is_correct": is_correct,
        "correct_answer": current_question['options'][current_question['correct']],
        "points_earned": points_earned,
        "score": quiz['score'],
        "next_question": next_question,
        "question_number": quiz['current_index'] + 1,
        "total_questions": quiz['total_questions'],
        "progress": f"{quiz['current_index'] + 1}/{quiz['total_questions']}"
    })

@app.route('/api/quiz/result/<session_id>', methods=['GET'])
def get_quiz_result(session_id):
    """Obtenir les résultats d'un quiz"""
    if session_id not in quizzes:
        return jsonify({"error": "Session not found"}), 404
    
    quiz = quizzes[session_id]
    return jsonify({
        "player_name": quiz['player_name'],
        "score": quiz['score'],
        "total_questions": quiz['total_questions'],
        "answers": quiz['answers'],
        "percentage": quiz.get('percentage', 0),
        "start_time": quiz['start_time'],
        "end_time": quiz.get('end_time', datetime.now().isoformat())
    })

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """Obtenir le classement"""
    limit = int(request.args.get('limit', 10))
    category = request.args.get('category')
    
    leaderboard = scores.get('leaderboard', [])
    
    if category:
        leaderboard = [entry for entry in leaderboard if category in entry.get('categories', [])]
    
    return jsonify({
        "leaderboard": leaderboard[:limit],
        "total_players": len(leaderboard)
    })

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Métriques pour monitoring"""
    active_sessions = len(quizzes)
    total_games_played = len(scores.get('leaderboard', []))
    
    # Statistiques par catégorie
    category_stats = {}
    for question in questions_db:
        cat = question['category']
        if cat not in category_stats:
            category_stats[cat] = 0
        category_stats[cat] += 1
    
    return jsonify({
        "active_sessions": active_sessions,
        "total_games_played": total_games_played,
        "total_questions": len(questions_db),
        "total_categories": len(CATEGORIES),
        "categories": category_stats,
        "difficulty_distribution": {
            "easy": len([q for q in questions_db if q['difficulty'] == 'easy']),
            "medium": len([q for q in questions_db if q['difficulty'] == 'medium']),
            "hard": len([q for q in questions_db if q['difficulty'] == 'hard'])
        },
        "server_info": {
            "hostname": socket.gethostname(),
            "timestamp": datetime.now().isoformat()
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
