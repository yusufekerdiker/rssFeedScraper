import { HttpClient } from '@angular/common/http';
import { Injectable, Inject } from '@angular/core';
import { Observable } from 'rxjs';
import { News } from '../models/news';

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
}
