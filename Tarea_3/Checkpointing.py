import pickle
import os
import time

CHECKPOINT_FILE = "checkpoint.pkl"


# GUARDAR ESTADO 
def save_checkpoint(state):
    with open(CHECKPOINT_FILE, "wb") as f:
        pickle.dump(state, f)


# CARGAR ESTADO 
def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "rb") as f:
            return pickle.load(f)
    return None



def main():

    # Intentar restaurar estado
    state = load_checkpoint()
        
    if state is None:
        print("Iniciando desde cero")
        counter = 0
    else:
        print("Restaurando desde checkpoint")
        counter = state["counter"]

    for i in range(counter, 50):

        print("Procesando:", i)
        time.sleep(0.5)

        # Guardar progreso cada iteración
        save_checkpoint({
            "counter": i + 1
        })


if __name__ == "__main__":
    main()