from user_ui import UserUI


def main() -> None:
    user_ui = UserUI()
    user_ui.request_input()
    user_ui.print_words()
    user_ui.print_average_number()
    user_ui.print_median_number()
    user_ui.print_top_of_ngrams()


if __name__ == '__main__':
    main()
