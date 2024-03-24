import RPi.GPIO as GPIO
import time

# Définition des broches GPIO
# Modifier les numéros de broches en fonction de votre configuration matérielle
ENA = 17  # PWM pour la vitesse du moteur A
IN1 = 27  # Contrôle de direction du moteur A
IN2 = 22  # Contrôle de direction du moteur A
ENB = 18  # PWM pour la vitesse du moteur B
IN3 = 23  # Contrôle de direction du moteur B
IN4 = 24  # Contrôle de direction du moteur B

# Configuration des broches GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Fonctions pour contrôler les moteurs
def avancer(vitesse):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    GPIO.output(ENA, GPIO.HIGH)
    GPIO.output(ENB, GPIO.HIGH)
    pwm_a.start(vitesse)
    pwm_b.start(vitesse)

def arreter():
    GPIO.output(ENA, GPIO.LOW)
    GPIO.output(ENB, GPIO.LOW)
    pwm_a.stop()
    pwm_b.stop()

# Initialisation des PWM pour le contrôle de vitesse
pwm_a = GPIO.PWM(ENA, 100)
pwm_b = GPIO.PWM(ENB, 100)

# Utilisation des fonctions
avancer(50)  # Avancer à 50% de la vitesse maximale
time.sleep(2)  # Attendre pendant 2 secondes
arreter()     # Arrêter les moteurs

# Nettoyage des broches GPIO
GPIO.cleanup()

