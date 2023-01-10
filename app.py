


from flask import Flask, render_template ,request ,redirect
import pickle
import requests




df = pickle.load(open('df.pkl','rb'))
Distance = pickle.load(open('distance.pkl','rb'))
app = Flask(__name__)

def get_posters(movie_id):
    responce = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=7099bf827554b98221e97cb365dd1613&language=en-US')
    # print(responce)
    data = responce.json()
    # print(data)
    return 'https://image.tmdb.org/t/p/original' + data['poster_path']

def Recommender(movie):
    recomm = []
    movie_poster = []

    movie_index =df[df['title'] == movie].index[0]
    distance = Distance[movie_index]
    movies_list =sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]
    for i in movies_list:
        recomm.append(df.iloc[i[0]].title)
        # print(i[0])
        movie_poster.append(get_posters(df.iloc[i[0]].movie_id))

    return recomm,movie_poster


     



@app.route('/', methods =['POST','GET'])
def movies():
    if request.method == 'POST':
        selected_movie = request.form['selected_movie']
        if selected_movie == 'none':
            return redirect('/')

        return render_template('movies.html',selected_movie=selected_movie,image = Recommender(selected_movie)[1], Recommen = Recommender(selected_movie)[0] , movies = df.title)
    else:
        return render_template('movies.html', movies = df.title)
    

if __name__ == '__main__':
   app.run(debug=True)