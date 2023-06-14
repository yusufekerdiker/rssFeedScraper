import { HttpClient } from '@angular/common/http';
import { Injectable, Inject } from '@angular/core';
import { Observable, map } from 'rxjs';
import { News, Article } from '../models/news';

@Injectable({
  providedIn: 'root',
})
export class NewsService {
  // private readonly url = 'https://your-api-url.com';

  constructor(
    private http: HttpClient,
    @Inject('apiUrl') private apiUrl: string
  ) {}

  getNews(): Observable<News> {
    return this.http.get<News>(this.apiUrl);
  }

  getNewsByPublisher(publisher: string): Observable<Article[]> {
    // get publisher name and its content from api
    // the string represents name of the provider like cnet or wired
    return this.http.get<{ [key: string]: Article[] }>(this.apiUrl).pipe(
      // map is a way to process the data we received. It takes the data and changes it into what we need.
      map(newsData => newsData[publisher] || [])
      // api sends us an object where each key is a publisher name and its value is a list of articles.
      // find the list of articles that belong to the publisher we are interested in.
        
      // if the server doesn't have any articles for that publisher, we will get "undefined". 
      // to prevent this errors, we change it to an empty list when it returns undefined
    );
  }

}
