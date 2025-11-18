from ioutils.prompts import ask_months_to_run
from models.shop import FlowerShop


def main() -> None:
    # Initial greeting
    print("---------------------------------------------------------------")
    print("Welcome to the FlowerShop Simulator!")
    print("---------------------------------------------------------------")

    #  Ask how many months we should simulate (default: 6)
    months = ask_months_to_run(default_months=6)
    shop = FlowerShop()

    #  Run the simulation month by month
    for month in range(1, months + 1):
        alive = shop.run_month(month)
        if not alive:
            # The shop went bankrupt, so we stop
            break
    else:
        # This block runs only if the loop never hits the break above
        print("***********************************************************************")
        print("Congratulations! You have completed the simulation!")


if __name__ == "__main__":
    main()
