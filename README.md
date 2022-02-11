# Mealwise
A web app to help a restaurant keep track of its inventory throughout the day. Capstone project for [Codecademy Django](https://www.codecademy.com/learn/paths/build-python-web-apps-with-django) course.

This app uses [Bootstrap 5](https://getbootstrap.com/), [htmx](https://htmx.org/), [_hyperscript](https://hyperscript.org/), [Bokeh](https://bokeh.org/) for the revenue chart, and [django-admin-interface](https://github.com/fabiocaccamo/django-admin-interface). The majority of that was added after completing the requirements for the assignment (v1.0)

## Try it Out

Visit [iamjameswalters.pythonanywhere.com](https://iamjameswalters.pythonanywhere.com/) to interact with a live demo of the app. The database should reset nightly. Feel free to create your own account, or use `user: testuser/pass: mealwise`. Without signing in, you can place and delete orders. All the other features require an account.

## Local Installation

Dependencies and virtual environments on this project are managed with [Poetry](https://python-poetry.org/). After cloning the project, enter the repository and run `poetry install`. This will install all the project's dependencies within a virtual environment. Once that's done, run `poetry shell` to enter that environment, and navigate to the `mealwise/` directory to run `manage.py runserver`. Have fun! 🙂️
___
### Image Credits

This project uses a handful of demo images. These were sourced from [Wikimedia Commons](https://commons.wikimedia.org/)/[Flickr](https://www.flickr.com/) under [Creative Commons](https://creativecommons.org/) licenses. In compliance with the terms of those licenses, here is attribution for the images I used:

[CC BY-NC 2.0](https://creativecommons.org/licenses/by-nc/2.0/)
  * [Fruit salad by Like_the_Grand_Canyon](https://www.flickr.com/photos/like_the_grand_canyon/47835781931)

[CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0/)
  * [Macaroni and Cheese from Noodles and Company by Bjorn Watland](https://www.flickr.com/photos/bjornwatland/6027750150)

[CC BY 2.0](https://creativecommons.org/licenses/by/2.0/)
  * [Orange and Chocolate Jaffa cake by Marco Verch](https://www.flickr.com/photos/30478819@N08/32670469447)

[CC BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/deed.en)
  * [CountryFriedSteak.jpg by Kimsey0](https://commons.wikimedia.org/wiki/File:CountryFriedSteak.jpg)

[CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/deed.en)
  * [Grilled cheese sandwich on white plate.jpg by Senator2029](https://commons.wikimedia.org/wiki/File:Grilled_cheese_sandwich_on_white_plate.jpg)

Public Domain
  * [Peanut-Butter-Jelly-Sandwich.jpg by Evan-Amos](https://commons.wikimedia.org/wiki/File:Peanut-Butter-Jelly-Sandwich.jpg)

None of the images were modified.
