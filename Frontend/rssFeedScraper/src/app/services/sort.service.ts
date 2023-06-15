import { Injectable } from '@angular/core';
import { Article } from '../models/news'; // Update with your correct path

@Injectable({
  providedIn: 'root',
})
export class SortService {

  constructor() { }

  sortArticles(allArticles: Article[], changeSortingOrder: boolean): Article[] {
    return allArticles.sort((a, b) => {
      if (changeSortingOrder) {
        return new Date(b.publishDate).getTime() - new Date(a.publishDate).getTime();
      } else {
        return new Date(a.publishDate).getTime() - new Date(b.publishDate).getTime();
      }
    });
  }
}
