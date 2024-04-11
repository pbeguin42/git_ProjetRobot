import RPi.GPIO as GPIO
import time
import socket

# Définition des broches GPIO
# Modifier les numéros de broches en fonction de votre configuration matérielle
ENA = 17  # PWM pour la vitesse du moteur A
IN1 = 27  # Contrôle de direction du moteur A
IN2 = 22  # Contrôle de direction du moteur A
ENB = 18  # PWM pour la vitesse du moteur B
IN3 = 23  # Contrôle de direction du moteur B
IN4 = 24  # Contrôle de direction du moteur B
ldr_pin = 5  # Modifier le numéro de la broche pour correspondre à votre configuration
trigger_pin = 6  # Modifier le numéro de la broche pour correspondre à votre configuration
echo_pin = 13  # Modifier le numéro de la broche pour correspondre à votre configuration
light_threshold = 700
sonar_threshold = 200

# Configuration des broches GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ldr_pin, GPIO.IN)
GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

# Initialisation des PWM pour le contrôle de vitesse
pwm_a = GPIO.PWM(ENA, 100)
pwm_b = GPIO.PWM(ENB, 100)

# Utilisation des fonctions
def drive_forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_a.start(100)
    pwm_b.start(100)

def stop():
    GPIO.output(ENA, GPIO.LOW)
    GPIO.output(ENB, GPIO.LOW)
    pwm_a.stop()
    pwm_b.stop()

def sonar_ping():
    GPIO.output(trigger_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trigger_pin, GPIO.LOW)
    start_time = time.time()
    stop_time = time.time()
    while GPIO.input(echo_pin) == 0:
        start_time = time.time()
    while GPIO.input(echo_pin) == 1:
        stop_time = time.time()
    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2  # vitesse du son en cm/s
    return distance

# Création d'un socket pour écouter les commandes
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind(('192.168.0.18', 12345))  # Remplacez l'adresse IP par celle de votre Raspberry Pi
serveur.listen(5)

print("En attente de connexions...")
client, adresse = serveur.accept()
print(f"Connexion établie avec {adresse}")

# Utilisation des fonctions
try:
    while True:

        commande = client.recv(1024).decode()
        print("Commande reçue:", commande)
        
        if commande == "avancer":
            drive_forward()
        else:
            print("Commande non reconnue")
            
        ldr_reading = GPIO.input(ldr_pin)
        sonar_distance = sonar_ping()

        print("LDR Reading:", ldr_reading)
        print("Distance Reading:", sonar_distance)

        # Vérifier si les lumières sont allumées
        if ldr_reading < light_threshold:
            stop()
            print("Lights are off")
            # Sortir de la boucle
            break

        # Vérifier la distance de ce qui est devant nous
        if sonar_distance < sonar_threshold:
            # Tourner autour
            stop()
            print("Obstacle detected!")
            # Code pour faire demi-tour
            # Mettez votre logique de mouvement ici

        # Avancer
        drive_forward()

        time.sleep(0.1)  # Attendre un court instant avant de lire à nouveau les capteurs

except KeyboardInterrupt:
    pass

# Nettoyage des broches GPIO
GPIO.cleanup()
