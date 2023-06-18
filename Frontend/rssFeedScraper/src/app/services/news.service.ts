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
    //retrieve the favorites from localStorage
    const storedFavorites = localStorage.getItem('favorites');
    if (storedFavorites) {
      this.favorites = new Set(JSON.parse(storedFavorites));
    }
  }

  private favorites = new Set<Article>();

  addToFavorites(article: Article) {
    this.favorites.add(article);

    localStorage.setItem('favorites', JSON.stringify(Array.from(this.favorites)));
  }

  removeFromFavorites(article: Article) {
    this.favorites.delete(article);

    localStorage.setItem('favorites', JSON.stringify(Array.from(this.favorites)));
  }

  isFavorite(article: Article): boolean {
    return this.favorites.has(article);
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

/* 
export class NewsService {
  private newsSubject = new BehaviorSubject<News>(null);
  news$ = this.newsSubject.asObservable();

  constructor(private http: HttpClient) {
    this.refreshNews();
  }

  refreshNews() {
    this.http.get<News>(this.apiUrl).subscribe(data => {
      let allArticles = [];
      for (const publisher in data) {
        allArticles = allArticles.concat(data[publisher]);
      }
      this.newsSubject.next(allArticles);
    });
  }
}

*/