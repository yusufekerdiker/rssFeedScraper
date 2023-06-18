// search.service.ts
import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SearchService {

  private searchSubject = new BehaviorSubject<string>('');

  getSearchTerm() {
    return this.searchSubject.asObservable();
  }

  setSearchTerm(term: string) {
    console.log("Setting search term to: ", term);
    this.searchSubject.next(term);
  }
  
}
