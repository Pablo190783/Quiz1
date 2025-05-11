import csv
from pathlib import Path

def generate_questions_a():
    # Preguntas sobre directores, actores principales, años de estreno
    questions = [
        ["¿Quién dirigió la película Parasite en 2019?", "Bong Joon-ho", "Alfonso Cuarón", "Quentin Tarantino", "Bong Joon-ho"],
        ["¿En qué año se estrenó la serie Stranger Things?", "2016", "2015", "2017", "2016"],
        ["¿Quién interpretó a Joker en Joker de 2019?", "Joaquin Phoenix", "Heath Ledger", "Jared Leto", "Joaquin Phoenix"],
        ["¿Quién dirigió la película The Grand Budapest Hotel en 2014?", "Wes Anderson", "Paul Thomas Anderson", "David Fincher", "Wes Anderson"],
        ["¿En qué año se estrenó la película Interstellar?", "2014", "2013", "2015", "2014"],
        ["¿Quién interpretó a Amy Dunne en Gone Girl de 2014?", "Rosamund Pike", "Ben Affleck", "Neil Patrick Harris", "Rosamund Pike"],
        ["¿Quién dirigió la película Birdman en 2014?", "Alejandro G. Iñárritu", "Damien Chazelle", "Richard Linklater", "Alejandro G. Iñárritu"],
        ["¿En qué año se estrenó la serie True Detective?", "2014", "2013", "2015", "2014"],
        ["¿Quién interpretó a Jordan Belfort en The Wolf of Wall Street de 2013?", "Leonardo DiCaprio", "Matthew McConaughey", "Jonah Hill", "Leonardo DiCaprio"],
        ["¿Quién dirigió la película Django Unchained en 2012?", "Quentin Tarantino", "Christopher Nolan", "Martin Scorsese", "Quentin Tarantino"],
        ["¿En qué año se estrenó la serie House of Cards?", "2013", "2012", "2014", "2013"],
        ["¿Quién interpretó a Katniss Everdeen en The Hunger Games de 2012?", "Jennifer Lawrence", "Shailene Woodley", "Emma Watson", "Jennifer Lawrence"],
        ["¿Quién dirigió la película The Social Network en 2010?", "David Fincher", "David O. Russell", "Aaron Sorkin", "David Fincher"],
        ["¿En qué año se estrenó la película Black Swan?", "2010", "2009", "2011", "2010"],
        ["¿Quién interpretó a Nina Sayers en Black Swan de 2010?", "Natalie Portman", "Mila Kunis", "Winona Ryder", "Natalie Portman"],
        ["¿Quién dirigió la película La La Land en 2016?", "Damien Chazelle", "Barry Jenkins", "Greta Gerwig", "Damien Chazelle"],
        ["¿En qué año se estrenó la serie Westworld?", "2016", "2015", "2017", "2016"],
        ["¿Quién interpretó a Mia Dolan en La La Land de 2016?", "Emma Stone", "Emily Blunt", "Amy Adams", "Emma Stone"],
        ["¿Quién dirigió la película Moonlight en 2016?", "Barry Jenkins", "Jordan Peele", "Steve McQueen", "Barry Jenkins"],
        ["¿En qué año se estrenó la película Arrival?", "2016", "2015", "2017", "2016"],
        ["¿Quién interpretó a Louise Banks en Arrival de 2016?", "Amy Adams", "Emily Blunt", "Scarlett Johansson", "Amy Adams"],
        ["¿Quién dirigió la película Get Out en 2017?", "Jordan Peele", "Spike Lee", "Guillermo del Toro", "Jordan Peele"],
        ["¿En qué año se estrenó la serie The Handmaid's Tale?", "2017", "2016", "2018", "2017"],
        ["¿Quién interpretó a June Osborne en The Handmaid's Tale?", "Elisabeth Moss", "Alexis Bledel", "Yvonne Strahovski", "Elisabeth Moss"],
        ["¿Quién dirigió la película Dunkirk en 2017?", "Christopher Nolan", "Hans Zimmer", "Denis Villeneuve", "Christopher Nolan"],
        ["¿En qué año se estrenó la película Blade Runner 2049?", "2017", "2016", "2018", "2017"],
        ["¿Quién interpretó a Rick Deckard en Blade Runner 2049?", "Harrison Ford", "Ryan Gosling", "Jared Leto", "Harrison Ford"],
        ["¿Quién dirigió la película Lady Bird en 2017?", "Greta Gerwig", "Sofia Coppola", "Dee Rees", "Greta Gerwig"],
        ["¿En qué año se estrenó la serie Big Little Lies?", "2017", "2016", "2018", "2017"],
        ["¿Quién interpretó a Celeste Wright en Big Little Lies?", "Nicole Kidman", "Reese Witherspoon", "Shailene Woodley", "Nicole Kidman"],
        ["¿Quién dirigió la película Knives Out en 2019?", "Rian Johnson", "Chris Evans", "Daniel Craig", "Rian Johnson"],
        ["¿En qué año se estrenó la película 1917?", "2019", "2018", "2020", "2019"],
        ["¿Quién interpretó a William Schofield en 1917?", "George MacKay", "Dean-Charles Chapman", "Colin Firth", "George MacKay"],
        ["¿Quién dirigió la película The Irishman en 2019?", "Martin Scorsese", "Quentin Tarantino", "Alfonso Cuarón", "Martin Scorsese"],
        ["¿En qué año se estrenó la serie Watchmen?", "2019", "2018", "2020", "2019"],
        ["¿Quién interpretó a Angela Abar en Watchmen?", "Regina King", "Yahya Abdul-Mateen II", "Jean Smart", "Regina King"],
        ["¿Quién dirigió la película Jojo Rabbit en 2019?", "Taika Waititi", "Roman Griffin Davis", "Scarlett Johansson", "Taika Waititi"],
        ["¿En qué año se estrenó la película Once Upon a Time in Hollywood?", "2019", "2018", "2020", "2019"],
        ["¿Quién interpretó a Rick Dalton en Once Upon a Time in Hollywood?", "Leonardo DiCaprio", "Brad Pitt", "Margot Robbie", "Leonardo DiCaprio"],
        ["¿Quién dirigió la película The Shape of Water en 2017?", "Guillermo del Toro", "Alfonso Cuarón", "Alejandro G. Iñárritu", "Guillermo del Toro"],
        ["¿En qué año se estrenó la serie Mindhunter?", "2017", "2016", "2018", "2017"],
        ["¿Quién interpretó a Holden Ford en Mindhunter?", "Jonathan Groff", "Holt McCallany", "Cameron Britton", "Jonathan Groff"],
        ["¿Quién dirigió la película A Quiet Place en 2018?", "John Krasinski", "Emily Blunt", "Michael Bay", "John Krasinski"],
        ["¿En qué año se estrenó la película Hereditary?", "2018", "2017", "2019", "2018"],
        ["¿Quién interpretó a Annie Graham en Hereditary?", "Toni Collette", "Alex Wolff", "Milly Shapiro", "Toni Collette"],
        ["¿Quién dirigió la película BlacKkKlansman en 2018?", "Spike Lee", "Jordan Peele", "Boots Riley", "Spike Lee"],
        ["¿En qué año se estrenó la película Roma?", "2018", "2017", "2019", "2018"],
        ["¿Quién interpretó a Cleo en Roma?", "Yalitza Aparicio", "Marina de Tavira", "Nancy García", "Yalitza Aparicio"],
        ["¿Quién dirigió la película The Favourite en 2018?", "Yorgos Lanthimos", "Alfonso Cuarón", "Pawel Pawlikowski", "Yorgos Lanthimos"],
        ["¿En qué año se estrenó la serie Succession?", "2018", "2017", "2019", "2018"],
    ]
    return questions

def generate_questions_b():
    # Preguntas sobre bandas sonoras, plataformas, ciudades
    questions = [
        ["¿Quién compuso la banda sonora de Inception en 2010?", "Hans Zimmer", "John Williams", "Alexandre Desplat", "Hans Zimmer"],
        ["¿En qué plataforma se estrenó la serie The Witcher?", "Netflix", "Amazon Prime", "HBO", "Netflix"],
        ["¿En qué ciudad se desarrolla la serie Friends?", "New York", "Los Angeles", "Chicago", "New York"],
        ["¿Quién compuso la banda sonora de The Shape of Water en 2017?", "Alexandre Desplat", "Hans Zimmer", "John Williams", "Alexandre Desplat"],
        ["¿En qué plataforma se estrenó la serie The Mandalorian?", "Disney+", "Netflix", "Hulu", "Disney+"],
        ["¿En qué ciudad se desarrolla la serie Breaking Bad?", "Albuquerque", "Denver", "Miami", "Albuquerque"],
        ["¿Quién compuso la banda sonora de Blade Runner 2049 en 2017?", "Hans Zimmer", "Clint Mansell", "Trent Reznor", "Hans Zimmer"],
        ["¿En qué plataforma se estrenó la serie Ozark?", "Netflix", "HBO", "Amazon Prime", "Netflix"],
        ["¿En qué ciudad se desarrolla la serie The Wire?", "Baltimore", "Philadelphia", "Boston", "Baltimore"],
        ["¿Quién compuso la banda sonora de Dunkirk en 2017?", "Hans Zimmer", "James Newton Howard", "Alan Silvestri", "Hans Zimmer"],
        ["¿En qué plataforma se estrenó la serie Chernobyl?", "HBO", "Netflix", "Sky Atlantic", "HBO"],
        ["¿En qué ciudad se desarrolla la serie Peaky Blinders?", "Birmingham", "London", "Manchester", "Birmingham"],
        ["¿Quién compuso la banda sonora de Interstellar en 2014?", "Hans Zimmer", "Michael Giacchino", "Max Richter", "Hans Zimmer"],
        ["¿En qué plataforma se estrenó la serie The Queen's Gambit?", "Netflix", "Hulu", "Disney+", "Netflix"],
        ["¿En qué ciudad se desarrolla la serie Stranger Things?", "Hawkins", "Indianapolis", "Columbus", "Hawkins"],
        ["¿Quién compuso la banda sonora de La La Land en 2016?", "Justin Hurwitz", "Hans Zimmer", "Alexandre Desplat", "Justin Hurwitz"],
        ["¿En qué plataforma se estrenó la serie Your Honor?", "Showtime", "Netflix", "Amazon Prime", "Showtime"],
        ["¿En qué ciudad se desarrolla la serie Succession?", "New York", "Los Angeles", "Chicago", "New York"],
        ["¿Quién compuso la banda sonora de The Social Network en 2010?", "Trent Reznor", "Hans Zimmer", "Clint Mansell", "Trent Reznor"],
        ["¿En qué plataforma se estrenó la serie The Undoing?", "HBO", "Netflix", "Hulu", "HBO"],
        ["¿En qué ciudad se desarrolla la serie The Sopranos?", "New Jersey", "New York", "Philadelphia", "New Jersey"],
        ["¿Quién compuso la banda sonora de Black Panther en 2018?", "Ludwig Göransson", "Kendrick Lamar", "Hans Zimmer", "Ludwig Göransson"],
        ["¿En qué plataforma se estrenó la serie Bridgerton?", "Netflix", "Amazon Prime", "Disney+", "Netflix"],
        ["¿En qué ciudad se desarrolla la serie Shameless?", "Chicago", "Detroit", "Cleveland", "Chicago"],
        ["¿Quién compuso la banda sonora de Roma en 2018?", "Leo Daniderff", "Steven Price", "Alfonso Cuarón", "Leo Daniderff"],
        ["¿En qué plataforma se estrenó la serie The Morning Show?", "Apple TV+", "Netflix", "HBO", "Apple TV+"],
        ["¿En qué ciudad se desarrolla la serie Atlanta?", "Atlanta", "Miami", "New Orleans", "Atlanta"],
        ["¿Quién compuso la banda sonora de Knives Out en 2019?", "Nathan Johnson", "Hans Zimmer", "Alexandre Desplat", "Nathan Johnson"],
        ["¿En qué plataforma se estrenó la serie Euphoria?", "HBO", "Netflix", "Amazon Prime", "HBO"],
        ["¿En qué ciudad se desarrolla la serie The Walking Dead?", "Atlanta", "Richmond", "Savannah", "Atlanta"],
        ["¿Quién compuso la banda sonora of A Quiet Place en 2018?", "Marco Beltrami", "Hans Zimmer", "John Carpenter", "Marco Beltrami"],
        ["¿En qué plataforma se estrenó la serie The Haunting of Hill House?", "Netflix", "HBO", "Amazon Prime", "Netflix"],
        ["¿En qué ciudad se desarrolla la serie True Detective?", "Louisiana", "Arkansas", "Texas", "Louisiana"],
        ["¿Quién compuso la banda sonora of The Grand Budapest Hotel en 2014?", "Alexandre Desplat", "Hans Zimmer", "Wes Anderson", "Alexandre Desplat"],
        ["¿En qué plataforma se estrenó la serie Ted Lasso?", "Apple TV+", "Netflix", "Hulu", "Apple TV+"],
        ["¿En qué ciudad se desarrolla la serie The Crown?", "London", "Edinburgh", "Bristol", "London"],
        ["¿Quién compuso la banda sonora of Birdman en 2014?", "Antonio Sánchez", "Hans Zimmer", "Alexandre Desplat", "Antonio Sánchez"],
        ["¿En qué plataforma se estrenó la serie Mare of Easttown?", "HBO", "Netflix", "Amazon Prime", "HBO"],
        ["¿En qué ciudad se desarrolla la serie The Handmaid's Tale?", "Boston", "Chicago", "Toronto", "Boston"],
        ["¿Quién compuso la banda sonora of Get Out en 2017?", "Michael Abels", "Hans Zimmer", "Daniel Lopatin", "Michael Abels"],
        ["¿En qué plataforma se estrenó la serie Loki?", "Disney+", "Netflix", "HBO", "Disney+"],
        ["¿En qué ciudad se desarrolla la serie Sex and the City?", "New York", "Los Angeles", "Miami", "New York"],
        ["¿Quién compuso la banda sonora of Moonlight en 2016?", "Nicholas Britell", "Hans Zimmer", "Max Richter", "Nicholas Britell"],
        ["¿En qué plataforma se estrenó la serie The White Lotus?", "HBO", "Netflix", "Amazon Prime", "HBO"],
        ["¿En qué ciudad se desarrolla la serie Boardwalk Empire?", "Atlantic City", "New York", "Chicago", "Atlantic City"],
        ["¿Quién compuso la banda sonora of Jojo Rabbit en 2019?", "Michael Giacchino", "Hans Zimmer", "Alexandre Desplat", "Michael Giacchino"],
        ["¿En qué plataforma se estrenó la serie WandaVision?", "Disney+", "Netflix", "HBO", "Disney+"],
        ["¿En qué ciudad se desarrolla la serie Mad Men?", "New York", "Los Angeles", "Chicago", "New York"],
        ["¿Quién compuso la banda sonora of The Irishman en 2019?", "Robbie Robertson", "Hans Zimmer", "Max Richter", "Robbie Robertson"],
        ["¿En qué plataforma se estrenó la serie Squid Game?", "Netflix", "HBO", "Amazon Prime", "Netflix"],
    ]
    return questions

def generate_questions_c():
    # Preguntas sobre premios, géneros, personajes secundarios
    questions = [
        ["¿Qué película ganó el Oscar a Mejor Película en 2019?", "Parasite", "1917", "Once Upon a Time in Hollywood", "Parasite"],
        ["¿De qué género es la serie Black Mirror?", "Ciencia ficción", "Comedia", "Drama", "Ciencia ficción"],
        ["¿Quién interpreta a Kendall Roy en Succession?", "Jeremy Strong", "Adam McKay", "Brian Cox", "Jeremy Strong"],
        ["¿Qué película ganó el Oscar a Mejor Película en 2017?", "Moonlight", "La La Land", "Manchester by the Sea", "Moonlight"],
        ["¿De qué género es la serie The Office?", "Comedia", "Drama", "Thriller", "Comedia"],
        ["¿Quién interpreta a Saul Goodman en Better Call Saul?", "Bob Odenkirk", "Jonathan Banks", "Michael McKean", "Bob Odenkirk"],
        ["¿Qué película ganó el Oscar a Mejor Película en 2018?", "The Shape of Water", "Three Billboards Outside Ebbing Missouri", "Get Out", "The Shape of Water"],
        ["¿De qué género es la serie Narcos?", "Crimen", "Comedia", "Romance", "Crimen"],
        ["¿Quién interpreta a Rue Bennett en Euphoria?", "Zendaya", "Hunter Schafer", "Sydney Sweeney", "Zendaya"],
        ["¿Qué película ganó el Oscar a Mejor Película en 2016?", "Spotlight", "The Revenant", "Bridge of Spies", "Spotlight"],
        ["¿De qué género es la serie The Crown?", "Drama", "Comedia", "Ciencia ficción", "Drama"],
        ["¿Quién interpreta a Oberyn Martell en Game of Thrones?", "Pedro Pascal", "Indira Varma", "Michiel Huisman", "Pedro Pascal"],
        ["¿Qué película ganó el Oscar a Mejor Película en 2015?", "Birdman", "The Grand Budapest Hotel", "Boyhood", "Birdman"],
        ["¿De qué género es la serie Fargo?", "Crimen", "Comedia", "Fantasía", "Crimen"],
        ["¿Quién interpreta a Beth Harmon en The Queen's Gambit?", "Anya Taylor-Joy", "Marielle Heller", "Thomas Brodie-Sangster", "Anya Taylor-Joy"],
        ["¿Qué película ganó el Oscar a Mejor Película en 2014?", "12 Years a Slave", "Gravity", "Dallas Buyers Club", "12 Years a Slave"],
        ["¿De qué género es la serie Westworld?", "Ciencia ficción", "Comedia", "Romance", "Ciencia ficción"],
        ["¿Quién interpreta a Maeve Millay en Westworld?", "Thandiwe Newton", "Angela Sarafyan", "Tessa Thompson", "Thandiwe Newton"],
        ["¿Qué película ganó el Oscar a Mejor Película en 2013?", "Argo", "Life of Pi", "Lincoln", "Argo"],
        ["¿De qué género es la serie True Detective?", "Crimen", "Comedia", "Fantasía", "Crimen"],
        ["¿Quién interpreta a Rust Cohle en True Detective?", "Matthew McConaughey", "Woody Harrelson", "Colin Farrell", "Matthew McConaughey"],
        ["¿Qué película ganó el Oscar a Mejor Película en 2012?", "The Artist", "The Descendants", "Hugo", "The Artist"],
        ["¿De qué género es la serie Stranger Things?", "Ciencia ficción", "Comedia", "Romance", "Ciencia ficción"],
        ["¿Quién interpreta a Eleven en Stranger Things?", "Millie Bobby Brown", "Finn Wolfhard", "Gaten Matarazzo", "Millie Bobby Brown"],
        ["¿Qué película ganó el Oscar a Mejor Película en 2011?", "The King's Speech", "The Social Network", "Black Swan", "The King's Speech"],
        ["¿De qué género es la serie Breaking Bad?", "Crimen", "Comedia", "Romance", "Crimen"],
        ["¿Quién interpreta a Jesse Pinkman en Breaking Bad?", "Aaron Paul", "Bryan Cranston", "Dean Norris", "Aaron Paul"],
        ["¿Qué película ganó el Oscar a Mejor Película en 2010?", "The Hurt Locker", "Avatar", "Inglourious Basterds", "The Hurt Locker"],
        ["¿De qué género es la serie The Sopranos?", "Crimen", "Comedia", "Fantasía", "Crimen"],
        ["¿Quién interpreta a Christopher Moltisanti en The Sopranos?", "Michael Imperioli", "James Gandolfini", "Steven Van Zandt", "Michael Imperioli"],
        ["¿Qué película ganó el Oscar a Mejor Película en 2020?", "Nomadland", "The Trial of the Chicago 7", "Promising Young Woman", "Nomadland"],
        ["¿De qué género es la serie The Mandalorian?", "Ciencia ficción", "Comedia", "Drama", "Ciencia ficción"],
        ["¿Quién interpreta a Din Djarin en The Mandalorian?", "Pedro Pascal", "Carl Weathers", "Temuera Morrison", "Pedro Pascal"],
        ["¿Qué película ganó el Oscar a Mejor Película en 2021?", "CODA", "The Power of the Dog", "Belfast", "CODA"],
        ["¿De qué género es la serie Ted Lasso?", "Comedia", "Drama", "Crimen", "Comedia"],
        ["¿Quién interpreta a Rebecca Welton en Ted Lasso?", "Hannah Waddingham", "Juno Temple", "Sarah Niles", "Hannah Waddingham"],
        ["¿Qué película ganó el Oscar a Mejor Película en 2022?", "Everything Everywhere All at Once", "The Banshees of Inisherin", "Top Gun Maverick", "Everything Everywhere All at Once"],
        ["¿De qué género es la serie Squid Game?", "Drama", "Comedia", "Ciencia ficción", "Drama"],
        ["¿Quién interpreta a Seong Gi-hun en Squid Game?", "Lee Jung-jae", "Park Hae-soo", "Jung Ho-yeon", "Lee Jung-jae"],
        ["¿Qué película ganó el Oscar a Mejor Película en 2009?", "Slumdog Millionaire", "The Curious Case of Benjamin Button", "Milk", "Slumdog Millionaire"],
        ["¿De qué género es la serie The Wire?", "Crimen", "Comedia", "Romance", "Crimen"],
        ["¿Quién interpreta a Omar Little en The Wire?", "Michael K. Williams", "Idris Elba", "Dominic West", "Michael K. Williams"],
        ["¿Qué película ganó el Oscar a Mejor Película en 2008?", "No Country for Old Men", "There Will Be Blood", "Atonement", "No Country for Old Men"],
        ["¿De qué género es la serie Mad Men?", "Drama", "Comedia", "Ciencia ficción", "Drama"],
        ["¿Quién interpreta a Peggy Olson en Mad Men?", "Elisabeth Moss", "January Jones", "Christina Hendricks", "Elisabeth Moss"],
        ["¿Qué película ganó el Oscar a Mejor Película en 2007?", "The Departed", "Babel", "The Queen", "The Departed"],
        ["¿De qué género es la serie House of Cards?", "Drama", "Comedia", "Crimen", "Drama"],
        ["¿Quién interpreta a Claire Underwood en House of Cards?", "Robin Wright", "Kate Mara", "Neve Campbell", "Robin Wright"],
        ["¿De qué género es la serie Peaky Blinders?", "Crimen", "Comedia", "Romance", "Crimen"],
        ["¿Quién interpreta a Arthur Shelby en Peaky Blinders?", "Paul Anderson", "Joe Cole", "Finn Cole", "Paul Anderson"],
    ]
    return questions

def write_csv(file_path, questions):
    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(['question', 'option_a', 'option_b', 'option_c', 'answer'])
        writer.writerows(questions)

def main():
    base_dir = Path('/Users/pablostiefel/Documents/QuizFutbolYouTube/movies')
    base_dir.mkdir(exist_ok=True)

    write_csv(base_dir / 'Questions_A.csv', generate_questions_a())
    write_csv(base_dir / 'Questions_B.csv', generate_questions_b())
    write_csv(base_dir / 'Questions_C.csv', generate_questions_c())
    print("Archivos generados: Questions_A.csv, Questions_B.csv, Questions_C.csv")

if __name__ == "__main__":
    main()
