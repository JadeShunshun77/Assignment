from ioutils.prompts import ask_months_to_run
from models.shop import FlowerShop


def main() -> None:
    # Initial greeting
    print("---------------------------------------------------------------")
    print("Welcome to the FlowerShop Simulator!")
    print("---------------------------------------------------------------")

    # Months
    months = ask_months_to_run(default_months=6)
    shop = FlowerShop()

    #  Run the simulation
    for month in range(1, months + 1):
        alive = shop.run_month(month)
        if not alive:
            # The shop went bankrupt
            break
    else:
        print("***********************************************************************")
        print("Congratulations! You have completed the simulation!")


if __name__ == "__main__":
    main()
