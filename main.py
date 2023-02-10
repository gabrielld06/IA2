import numpy as np
import pandas as pd
import math

def correct_release_year(str):
    year = int(str)
    if year < 1980:
        return 'antigo'
    elif year < 1990:
        return '80s'
    elif year < 2000:
        return '90s'
    elif year < 2010:
        return '00s'
    elif year < 2020:
        return '10s'
    else:
        return '20s'

def correct_country(str):
    if 'United States' in str:
        return 'american'
    elif 'Brazil' in str:
        return 'nacional'
    else:
        return 'other'

def correct_genres(lst):
    return lst.split('-')

def correct_date(date):
    return date.split('-')[0]

def correct_runtime(time):
    time = float(time)
    if time < 90:
        return 'curto'
    elif time < 120:
        return 'medio'
    else:
        return 'longo'

def correct_votes(vote):
    vote = float(vote)
    return math.floor(vote)

def make_profile(movies):
    profile = {
        'genres' : {},
        'language' : {},
        'release_date' : {}, 
        'vote_average' : {},
        'runtime' : {}
    }

    for index, movie in movies.iterrows():
        # genre
        for genre in movie['genres']:
            if genre in profile['genres']:
                profile['genres'][genre] += 1
            else:
                profile['genres'][genre] = 1

        # language
        lang = movie['original_language']
        if lang in profile['language']:
            profile['language'][lang] += 1
        else:
             profile['language'][lang] = 1
        
        # release_date
        lanc = movie['release_date']
        if lanc in profile['release_date']:
            profile['release_date'][lanc] += 1
        else:
             profile['release_date'][lanc] = 1

        # vote_average
        votes = movie['vote_average']
        if votes in profile['vote_average']:
            profile['vote_average'][votes] += 1
        else:
             profile['vote_average'][votes] = 1
        
        # runtime
        time = movie['runtime']
        if time in profile['runtime']:
            profile['runtime'][time] += 1
        else:
             profile['runtime'][time] = 1
    print(profile)
    return profile

def evaluate_profile(profile):
    # genre utility
    totalGenreUtility = 0
    for key, value in profile['genres'].items():
        totalGenreUtility += value

    genreUtiliy = {}
    for key, value in profile['genres'].items():
        genreUtiliy[key] = value / totalGenreUtility

    # language utility
    languageUtiliy = {}
    for key, value in profile['language'].items():
        languageUtiliy[key] = value / 10
    
    # release date utility
    releaseDateUtiliy = {}
    for key, value in profile['release_date'].items():
        releaseDateUtiliy[key] = value / 10
    
    # vote average utility
    voteAverageUtiliy = {}
    for key, value in profile['vote_average'].items():
        voteAverageUtiliy[key] = value / 10
    
    # runtime utility
    runtimeUtiliy = {}
    for key, value in profile['runtime'].items():
        runtimeUtiliy[key] = value / 10
    
    profileUtility = {
        'genres': genreUtiliy,
        'language': languageUtiliy,
        'release_date': releaseDateUtiliy,
        'vote_average': voteAverageUtiliy,
        'runtime': runtimeUtiliy
    }
    print(profileUtility)

    return profileUtility

def evaluate(profile, movie):
    movie = movie.to_dict(orient='records')[0]
    utility = 0
    genreUtil = 2
    # genre utility
    for genre in movie['genres']:
        if genre in profile['genres']:
            utility += genreUtil * profile['genres'][genre]
            genreUtil -= 1.5/len(movie['genres'])
    # language utility
    lang = movie['original_language']
    if lang in profile['language']:
        utility += profile['language'][lang]
    
    # release date utility
    date = movie['release_date']
    if date in profile['release_date']:
        utility += profile['release_date'][date]
    
    # vote average utility
    vote = movie['vote_average']
    if vote in profile['vote_average']:
        utility += profile['vote_average'][vote]

    # runtime utility
    time = movie['runtime']
    if time in profile['runtime']:
        utility += profile['runtime'][time]

    return utility

'''
Variaveis

- genres - gêneros

- original_language (americano, nacional, outro)

- release_date (<80, 80s, 90s, 00s, 10s, 20s)

- vote_average

- runtime (longo, medio, curto)



- rating (G, PG, PG-13, R,  NC-17) ** esse nao tem
'''

def main():
    pd.set_option('mode.chained_assignment', None)
    df = pd.read_csv('movies.csv', low_memory=False,converters={"genres": lambda x: x.strip("[]").replace("'","").split(", ")})

    # pd.set_option('display.max_rows', len(df[idx]))

    df['vote_average'] = df['vote_average'].apply(correct_votes)
    df['runtime'] = df['runtime'].apply(correct_runtime)

    # profile = ['', '', '', '', '', '', '', '', '', '']
    # movies = df[df['title'].isin(profile)]

    familyProfileMovies = ['Grown Ups 2', 'Shrek 2', 'The Hangover', 'You Don\'t Mess with the Zohan', 'Sonic the Hedgehog', 'Just Go with It', 'Dumb and Dumber To', 'Blended', 'Monsters, Inc.', 'Spider-Man: Homecoming']
    familyMovies = df[df['title'].isin(familyProfileMovies)]
    familyProfile =evaluate_profile( make_profile(familyMovies))

    felipeProfileMovies = ['Life of Brian', 'Monty Python and the Holy Grail', 'Bee Movie', 'The Truman Show', 'Me, Myself & Irene', 'Citizen Kane', 'Uncut Gems', 'Eleven Samurai', 'Big Momma\'s House', 'Highlander']
    felipeMovies = df[df['title'].isin(felipeProfileMovies)]
    felipeProfile = evaluate_profile(make_profile(felipeMovies))

    zeProfileMovies = ['Back to the Future', 'White Chicks', 'Shrek', 'Rocky II', 'Rambo: First Blood Part II', 'Teenage Mutant Ninja Turtles', 'Creed II', 'Rango', 'Barnyard', 'Grown Ups 2']
    zeMovies = df[df['title'].isin(zeProfileMovies)]
    zeMovies = zeMovies.drop(2648)
    zeProfile = evaluate_profile(make_profile(zeMovies))

    # print(df[df['title'].str.contains('Rocky')])
    
    print(familyProfile, end='\n\n')
    print(felipeProfile, end='\n\n')
    print(zeProfile, end='\n\n')

    movie = df[df['title'] == 'Puss in Boots: The Last Wish']
    print(movie)
    print(f'Felipe: {evaluate(felipeProfile, movie)}')
    print(f'Ze: {evaluate(zeProfile, movie)}')

    print()

    movie = df[df['title'] == 'Zombieland']
    print(movie)
    print(f'Felipe: {evaluate(felipeProfile, movie)}')
    print(f'Ze: {evaluate(zeProfile, movie)}')

    print()

    movie = df[df['title'] == 'The Fault in Our Stars']
    print(movie)
    print(f'Felipe: {evaluate(felipeProfile, movie)}')
    print(f'Ze: {evaluate(zeProfile, movie)}')
    
    print()

    movie = df[df['title'] == 'Shrek 2']
    print(movie)
    print(f'Felipe: {evaluate(felipeProfile, movie)}')
    print(f'Ze: {evaluate(zeProfile, movie)}')

    print()

    movie = df[df['title'] == 'Shrek']
    print(movie)
    print(f'Felipe: {evaluate(felipeProfile, movie)}')
    print(f'Ze: {evaluate(zeProfile, movie)}')


if __name__ == "__main__":
    main()