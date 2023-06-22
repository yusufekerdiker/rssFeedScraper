import { HttpClient } from '@angular/common/http';
import { Injectable, Inject } from '@angular/core';
import { Observable, map } from 'rxjs';
import { News, Article } from '../models/news';

@Injectable({
  providedIn: 'root',
})
export class NewsService {
  constructor(
    private http: HttpClient,
    @Inject('apiUrl') private apiUrl: string
  ) {
    //retrieve the favorites from localStorage, if the item does not exist returns null.
    const storedFavorites = localStorage.getItem('favorites');
    //check ternary to check if storedFavorites is not null if storedFavorites is not null means we have some favorited articles stored in the localStorage
    //so we parse them with JSON.parse and assign favorites with them (json.parse transforms a json back to a js object)
    //if storedFavorites is null taht means we dont have any favorited articles in localstorage so we set favorites with an empty array
    this.favorites = new Set(
      storedFavorites ? JSON.parse(storedFavorites) : []
    );
  }

  //this ensures that an article can only be added once because set method allows only unique items
  private favorites: Set<Article> = new Set();

  addToFavorites(article: Article) {
    // add article to favorites then add it to set
    this.favorites.add(article);
    //then update localstorage with the new list
    localStorage.setItem(
      'favorites',
      JSON.stringify(Array.from(this.favorites))
    );
  }

  removeFromFavorites(article: Article) {
    //to remove  article from favorites we create a new set without that article
    this.favorites = new Set(
      Array.from(this.favorites).filter(
        (a) => a.title !== article.title || a.link !== article.link
      )
    );
    //then we update local storage with the new list of favorited articles
    localStorage.setItem(
      'favorites',
      JSON.stringify(Array.from(this.favorites))
    );
  }

  isFavorite(article: Article): boolean {
    //check if an article is favorited we check if it exists in the set of favorited articles
    return Array.from(this.favorites).some(
      (a) => a.title === article.title && a.link === article.link
    );
  }

  getFavorites(): Article[] {
    return Array.from(this.favorites);
  }

  getNews(): Observable<News> {
    return this.http.get<News>(this.apiUrl);
  }

  getNewsByPublisher(publisher: string): Observable<Article[]> {
    // get publisher name and its content from api
    // the string represents name of the provider like cnet or wired
    return this.http.get<{ [key: string]: Article[] }>(this.apiUrl).pipe(
      // map is a way to process the data we received. It takes the data and changes it into what we need.
      map((newsData) => newsData[publisher] || [])
      // api sends us an object where each key is a publisher name and its value is a list of articles.
      // find the list of articles that belong to the publisher we are interested in.

      // if the server doesn't have any articles for that publisher, we will get "undefined".
      // to prevent this errors, we change it to an empty list when it returns undefined
    );
  }
}
